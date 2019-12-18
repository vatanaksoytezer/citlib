 
import sys
import re
import copy
import os
import subprocess
from pyeda.inter import *
from shutil import copyfile
import random

# RULE: coverage_criterion.pl must define at least rule named 'entity'

# TODO: May be we can have a rezerved rule for things that can only assume one value
# TODO: Currently all the rules must be defined in a single line
# TODO: We are not currently enforcing that variables can only be used if they are defined
#       previously.

def clingo_output_indicates_satisfiability(out_file):
    # check to see if an output is produced
    if not os.path.isfile(out_file):
        print("FATAL: clingo output file '%s' does not exist! Exiting..." % out_file)
        sys.exit(-1)

    # read the output
    output = None
    with open(out_file, 'r') as in_file:
        output = in_file.read()
     
    # First, check to see if an error has occured
    if re.compile('\:\s*error\s*\:').search(output):
        print("WARNING: Output file '%s' indicates malformed ASP program" % out_file)
        return None
    
    # check to see if the problem is satisfiable
    if 'UNSATISFIABLE' not in output and 'SATISFIABLE' in output:
        return True # satisfiable

    # unsatisfiable
    return False

# the lp cmd is assumed to use clingo
def is_asp_satisfiable(lp_cmd, out_file='lp.out'):
    # remove the output file it exists
    if os.path.isfile(out_file):
        os.remove(out_file)
            
    # run the cmd
    cmd = "%s >& %s" % (lp_cmd, out_file)
    os.system(cmd)

    # parse the output for satisfiability
    verdict = clingo_output_indicates_satisfiability(out_file) 

    # Hopefully, there will be no need for debugging, do delete the output file
    if verdict is not None:
        os.remove(out_file)

    return verdict

def bool_exprs_to_clingo(exprs):
    asp = ''
    all_vars = set([])
    
    for expr_info in exprs:

        expr_str = expr_info['expr']        
        rule_head = expr_info['name']
        
        # convert it ot expression
        e = expr(expr_str)

        # get the variables in the expression
        vars = e.inputs

        # update all vars
        all_vars = all_vars.union(set(vars))

        
        dnf = e.to_dnf()
        dnf = str(dnf)

        asp += '% ' + rule_head + ' : orig = ' + expr_str + '\n'
        asp += '% ' + rule_head + ' : dnf  = ' + dnf + '\n'
    
        # dnf may be just one end, in this case
        #  to make the processing easier we intorduced a dummy or
        if 'Or(' not in dnf:
            dnf = 'Or(' + dnf + ')'
 
        ands = None
        if 'And(' not in dnf:
            # there is not an And in the expression
            # which means that there is a single Or, so:
            # NEW
            #ands = re.compile("Or\(([^\(]+)\)").search(dnf).group(1)
            ands = re.compile("Or\s*\(([^\(]+)\)").search(dnf).group(1)
            ands = re.sub('\s+','', ands)
            ands = ands.split(',')
            for i in range(len(ands)):
                ands[i] = '(' + ands[i] + ')'
        else:
            # we have Ands...
            ands = re.findall(r'And\([^\)]+\)', dnf)

        for bool_and in ands:
            terms = re.compile("\(([^\(]+)\)").search(bool_and).group(1)
            terms = re.sub('\s+','', terms)
            terms = terms.split(',') 

            my_terms = []
            for term in terms:            
                my_term  = ''
                if term.startswith('~'):
                    # I need a negatition
                    my_terms.append("parameter(global, %s, false)" % term[1:])
                    #my_terms.append("false(%s)" % term[1:])
                else:
                    my_terms.append("parameter(global, %s, true)" % term)
                    #my_terms.append("true(%s)" % term)

            rule_body = ", ".join(my_terms)

            rule = "%s :- %s." % (rule_head, rule_body)

            asp += "%s\n" % rule
        
        asp += '\n'

    # now, declare the variables
    var_decs = '% boolean variables\n'
    for var in all_vars:
        var_decs += "1 {parameter(global, %s, true); parameter(global, %s, false)} 1.\n" % (var, var)
        #var_decs += "1 {true(%s);false(%s)} 1.\n" % (var, var)
    var_decs += '\n'

    asp = var_decs + asp

    return asp


def compile_bool_exprs(bool_exprs):
    exprs_info = []

    for bool_expr in bool_exprs:
        print(bool_expr)
        # NEW
        # args = re.compile("^bool_expr\((.+)\)\.$").search(bool_expr).group(1).split(',')
        args = re.compile("^bool_expr\s*\((.+)\)\s*\.$").search(bool_expr).group(1)
        args = re.sub('\s+', '', args)
        args = arg.split(',')

        if len(args) != 2:
            print("FATAL: bool_expr should have two args: bool_expr(name, expr).")
            print("Violation: %s", bool_expr)
            sys.exit(1)
    
        exprs_info.append({'name' : args[0], 'expr' : args[1]})
        
    asp = bool_exprs_to_clingo(exprs_info)

    return asp


def get_arity(rule):

    arity = None
    
    # get the head
    head = re.sub('\s*:-.+$', '', rule)

    if '(' not in head:
        arity = 0
    else:
        args = re.compile("\(([^\(\)]+)\)").search(head).group(1)
        arity = len(args.split(','))
                
    return arity

def get_arities(rules):
    arities = []

    for rule in rules:
        arities.append(get_arity(rule))

    return arities

def get_entity_signatures(entities):

    signatures = {}
    
    # NOTE we assume that in an entity rule the first
    #      argument is always the type
    for entity in entities:
        arity = get_arity(entity)

        # get rid of the body, if exists
        entity = re.sub('\s*:-.+$', '', entity).strip()
        
        # get rid of the '.' at the end, if exists
        entity = re.sub('\s*\.$', '', entity).strip()

        # Now, put a '.' at the end
        entity += '.'

        # get the entity key so that we can store the same thing over and over again.
        # replace all the variable names in the head with a new variable name,
        # but do not touch the atoms
        # TODO assumes that entity has at least one argument, which makes sense indeed

        # NEW
        #args = re.compile("^entity\((.+)\)\.$").search(entity).group(1)
        args = re.compile("^entity\s*\((.+)\)\s*\.$").search(entity).group(1)
        args = re.sub('\s+', '', args)
        args = args.split(',')
        new_args = []
        var_idx = 1
        for arg in args:
            if arg[0].isupper():
                # we have a variable, rename it
                new_args.append('S' + str(var_idx))
                var_idx += 1
            else:
                # we have an atom keep that as it is
                new_args.append(arg)
        entity_key = "entity(%s)." % ','.join(new_args)

        if entity_key in signatures:
            continue
        
        # replace the first parameter with 'Type', e.g., 
        entity = re.sub('entity\s*\(', 'entity_signature(', entity)
        signatures[entity_key] = entity
        
    return list(signatures.values())

# NOTE: cmd must be a list 
def run_cmd(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT):
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

    if stdout is None:
        stdout = ''
    else:
        stdout = stdout.decode('UTF-8')

    if stderr is None:
        stderr = ''
    else:
        stderr = stderr.decode('UTF-8')

    return stdout, stderr

# FIXME: We assume that each rule is given in a single line in all the
# inoput files

def library_any_order(arg):
    if 't' not in arg:
        print("FATAL: any_order requires strength 't'. Exiting...")
        sys.exit(1)
 
    t = int(arg['t'])

    model = ''
    
    if t == 2:
        model += '% any 2-orders\n'
        model += 'any_order(S1, S2) :- reaches(S1, S2).\n'
        model += '\n'
    elif t == 3:
        model += '% any 3-orders\n'
        model += 'any_order(S1, S2, S3) :- reaches(S1, S2), reaches(S2, S3).\n'
        model += '\n'
    else:
        print("FATAL: any_order Not yet supported strength t=%s" % t)
        sys.exit(1)

    return model


def library_consecutive_order(arg):
    
    if 't' not in arg:
        print("FATAL: consecutive_order requires strength 't'. Exiting...")
        sys.exit(1)

    t = int(arg['t'])

    model = ''
    
    if t == 2:
        model += '% consecutive 2-orders\n'
        model += 'consecutive_order(S1, S2) :- edge(S1, S2).\n'
        model += '\n'
    elif t == 3:
        model += '% consecutive 3-orders\n'
        model += 'consecutive_order(S1, S2, S3) :- edge(S1, S2), edge(S2, S3).\n'
        model += '\n'
    else:
        print("FATAL: consecutive_order: Not yet supported strength t=%s" % t)
        sys.exit(1)                

    return model

def library_nonconsecutive_order(arg):
    
    if 't' not in arg:
        print("FATAL: nonconsecutive_order requires strength 't'. Exiting...")
        sys.exit(1)

    t = int(arg['t'])

    model = ''
    
    if t == 2:
        model += '% nonconsecutive 2-orders\n'
        model += 'nonconsecutive_order(S1, S2) :- reaches(S1, S3), reaches(S3, S2), S2 != S3.\n'
        model += '\n'
    elif t == 3:
        model += '% nonconsecutive 3-orders\n'
        model += 'nonconsecutive_order(S1, S2, S3) :- reaches(S1, S4), reaches(S4, S2), reaches(S2, S3), S2 != S4.\n'
        model += 'nonconsecutive_order(S1, S2, S3) :- reaches(S1, S2), reaches(S2, S4), reaches(S4, S3), S3 != S4.\n'    
        model += '\n'
    else:
        print("FATAL: nonconsecutive_order: Not yet supported strength t=%s" % t)
        sys.exit(1)

    return model


def library_consecutivenonconsecutive_order(arg):

    if 't' not in arg:
        print("FATAL: consecutivenonconsecutive_order requires strength 't'. Exiting...")
        sys.exit(1)

    t = int(arg['t'])

    model = ''

    if t == 2:
        model += '% consecutivenonconsecutive 2-orders\n'
        model += 'consecutivenonconsecutive_order(A, B):- consecutive_order(A, B).\n'
        model += 'consecutivenonconsecutive_order(A, B):- nonconsecutive_order(A, B).\n'
        model += '\n'
    elif t == 3:
        model += '% consecutivenonconsecutive 3-orders\n'
        model += 'consecutivenonconsecutive_order(A, B, C):- consecutive_order(A, B, C).\n'
        model += 'consecutivenonconsecutive_order(A, B, C):- nonconsecutive_order(A, B, C).\n'
        model += '\n'
    else:
        print("FATAL: consecutivenonconsecutive_order: Not yet supported strength t=%s" % t)
        sys.exit(1)

    return model


def library_parameters_on_same_path(arg):

    if 't' not in arg:
        print("FATAL: parameters_on_same_path requires strength 't'. Exiting...")
        sys.exit(1)

    t = int(arg['t'])

    model = ''
     
    if t == 2:
        model += '% parameter_on_same_path t=2\n'
        model += '''parameter_on_same_path(S1, V1, Val1, S2, V2, Val2) :- reaches(S1, S2), 
	            parameter(S1, V1, Val1),
	            parameter(S2, V2, Val2).'''
        model += '\n'
    elif t == 3:
        model += '% parameter_on_same_path t=3\n'
        model += '''parameter_on_same_path(S1, V1, Val1, S2, V2, Val2, S3, V3, Val3) :- reaches(S1, S2),
                     reaches(S2, S3),
	             parameter(S1, V1, Val1),
	             parameter(S2, V2, Val2),
	             parameter(S3, V3, Val3).'''
        model += '\n'
    else:
        print("FATAL: parameters_on_same_path: Not yet supported strength t=%s" % t)
        sys.exit(1)

    return model
                    

def library_def_use_pair(arg):                    
    model = ''
     
    model += '% def-use pairs\n'
    model += 'def_clear_path(S1, S2, O):- object(O), edge(S1, S2), not def(S2, O).\n'
    model += 'def_clear_path(S1, S2, O):- object(O), edge(S1, S3), not def(S3, O), def_clear_path(S3, S2, O).\n'
    

    model += 'def_use_pair(S1, S2, O) :- object(O), def(S1, O), use(S2, O), edge(S1, S2).\n'
    model += 'def_use_pair(S1, S2, O) :- object(O), def(S1, O), use(S2, O), def_clear_path(S1, S3, O), edge(S3, S2).\n'

    model += '\n'

    return model

            

# possible constructor_algos: one-test-case-at-a-time-constructor, cover-and-generate-constructor, 
def parse(mode, input_file, facts, constructor_algo=None):

    imports = {}

    # NOTE: testcase should not be here as it could also be used
    # in the coverage_criterion file, in which case it will totally be ignore
    # by this script generation code
    keywords = ['state', 'edge', 'parameter', 'edge_guard', 'object',
                'def', 'puse', 'cuse', 'entity_signature', 'entity',
                'entity_covered', '__global_constraint__',
                '__directive__', 'bool_expr', 'single_path_needed', '__edges_found__']
    
    
    if not (mode == 'coverage_criterion' or mode == 'ucit_generation' or mode == 'system_model'):
        print ("FATAL: Unknown mode of generation '%s'. Exiting..." % mode)
        sys.exit(1)

    facts_to_maintain = {}
    
    #facts = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            # remove the white spaces from the front and back
            line = line.strip()

            # skip empty lines
            if line == '':
                continue

            # skip comments
            if line.startswith('%'):
                continue
 
            # found a constraint
            type = None
            if line.startswith(':-'):
                type = '__global_constraint__'
            elif line.startswith('##'):
                # we have a U-CIT directive
                match = re.compile("^##\s*import\s+([^\s]+)\s*(.*)$").search(line)
                importing = match.group(1)

                if importing not in imports:
                    imports[importing] = []
                
                    
                argStr = match.group(2)
                
                # parse the arguments
                args = argStr.split(',')
                myargs = {}
                for arg in args:                        
                    tokens = arg.split('=')
                    # there must be two tokens
                    if len(tokens) != 2:
                        continue

                    left_side = tokens[0].strip()
                    right_side = tokens[1].strip()

                    myargs[left_side] = right_side

                imports[importing].append(myargs)
                
                continue
            elif line.startswith('#'):
                # now we have ASP directive
                type = '__directive__'
                
            else: 
                # TODO: remove all the white space characters
                # This may not be the right way to do it. But for the time being
                # NEW
                #line = re.sub('\s', '', line)
                #type = re.compile("^([^\(\:\.]+).*\.$").search(line).group(1).strip()
                type = re.compile("^([^\(\:\.\s]+).*\.$").search(line).group(1).strip()
                
            
            if (type == None):
                print("FATAL: Not know how to parse '%s'" % line)
                sys.exit(1)

            if type not in facts:
                facts[type] = []

            facts[type].append(line)


        # I found some edges so the other stages, e.g., enumeration
        # and generation, need to be notified
        if 'edge' in facts:
            facts['__edges_found__'] = ''

        if '__edges_found__' in facts:
            facts_to_maintain['__edges_found__'] = ''
            
        # parse the edges
        edges = {}
        if 'edge' in facts:
            for edge in facts['edge']:
                # get the state from the parameter            
                # NEW
                #match = re.compile("^edge\(([^\,]+)\,([^\,\)]+)").search(edge)
                match = re.compile("^edge\s*\(([^\,]+)\,([^\,\)]+)").search(edge)
                state1 = match.group(1).strip()
                state2 = match.group(2).strip()
                edges[state1 + ' ' + state2] = ''
            

        # start creating the model
        model = ''

        if 'state' in facts:
            # create the state facts
            model += '% states\n'
            # add the global state
            model += 'state(global).\n'
            model += '\n'.join(facts['state'])
            model += '\n\n'

        if 'edge' in facts:
            # create the edge facts
            model += '% edges\n'
            for e in facts['edge']:
                e = re.sub(r'\s*\.\s*$', '', e)
                model += "min_edge_cnt {%s} max_edge_cnt.\n" % e
            model += '\n\n'

        if 'parameter' in facts:                    
            # create the parameter facts
            global_parameters = ''
            local_parameters  = ''
            for parameter in facts['parameter']:
                # remove the . at the end 
                parameter = re.sub('\s*\.\s*$', '', parameter)

                # FIXME what we did for the edges with min_edge_cnt and max_edge_cnt
                # should also be done with the parameters. That is the user should be able
                # to determine how many settings for parameters are valid
                # get the state from the parameter            
                # NEW
                # state = re.compile("^parameter\(([^\,]+)").search(parameter).group(1)
                state = re.compile("^parameter\s*\(\s*([^\,\s]+)").search(parameter).group(1) 
                if state == 'global':                
                    global_parameters += "1 {%s} 1.\n" % parameter
                else:
                    local_parameters += "1 {%s} 1 :- visited(%s).\n" % (parameter, state)
                                
            model += '% global parameters\n'
            model += '% each global parameter should assume only one value\n'        
            if global_parameters == '':
                model += '% None\n'
            else:
                model += global_parameters
            model += '\n'

            model += '% local parameters\n'
            model += '% each local parameter should assume only one value,\n'
            model += '% given that the respective state is visited\n'        
            if local_parameters == '':
                model += '% None\n'
            else:
                model += local_parameters
            model += '\n'

        edges_with_guards = {}
        if 'edge_guard' in facts:
            model += '% edge guards, which need to be satisfied\n'
            model += '% before the edges can be taken\n'
            model += '\n'.join(facts['edge_guard'])
            model += '\n'
            
            # find the edges with no guard conditions
            # and add 'true' as the guard

            for edge in facts['edge_guard']:
                # get the state from the parameter            
                # NEW
                #match = re.compile("^edge_guard\(([^\,]+)\,([^\,\)]+)").search(edge)
                match = re.compile("^edge_guard\s*\(([^\,]+)\,([^\,\)]+)").search(edge)
                state1 = match.group(1).strip()
                state2 = match.group(2).strip()
                edges_with_guards[state1 + ' ' + state2] = ''

        if 'edge' in facts:
            # find the difference
            for edge in set(edges.keys()) - set(edges_with_guards.keys()):
                model += "edge_guard(" + ",".join(edge.split()) + ").\n"
            model += '\n'
        
        # constraints that are enforced globally

        if '__global_constraint__' in facts:
            model += '% global constraints\n'
            if '__global_constraint__' not in facts:
                model += '% None\n'
            else:
                model += '\n'.join(facts['__global_constraint__'])
                model += '\n'
            model += '\n'

        # objects
        if 'object' in facts:
            model += '% objects to be shared\n'
            if 'object' not in facts:
                model += '% None\n'
            else:
                model += '\n'.join(facts['object'])
                model += '\n'
            model += '\n'

        # definitions
        if 'def' in facts:
            model += '% defs, i.e., things that update the shared objects\n'
            model += '\n'.join(facts['def'])
            model += '\n'

        # puses
        if 'puse' in facts:
            model += '% p-uses, i.e., uses where shared objects are used in predicates\n'
            model += '\n'.join(facts['puse'])
            model += '\n'

        # cuses
        if 'cuse' in facts:
            model += '% c-uses, i.e., uses where shared objects are used in computations \n'
            model += '\n'.join(facts['cuse'])
            model += '\n'
            
        # uses
        if mode == 'system_model' and ('cuse' in facts or 'puse' in facts):
            model += '% a p-use or a c-use is considered as a use\n'
            model += 'use(S, O) :- puse(S, O).\n'
            model += 'use(S, O) :- cuse(S, O).\n'
            model += '\n'
  
        if '__edges_found__' in facts:
            if 'single_path_needed' in facts:
                # define the constants
                model += '% We need a single path,\n'
                model += '%  which means that a path is either taken or not taken.\n' 
                model += '#const min_edge_cnt=0.\n'
                model += '#const max_edge_cnt=1.\n'
                model += '\n'
            
                # which means that we need a single path
 
                model += '% without visiting a state one cannot take an edge originating from it\n'
                model += ':- not visited(S), edge(S, _).\n'
                model += '\n'
                
                model += '% only one edge origination from a state can be taken\n'
                model += ':- edge(S1, S2), edge(S1, S3), S2 != S3.\n'
                model += '\n'                    
                
                model += '% only one edge comming to  a state can be taken\n'
                model += ':- edge(S1, S2), edge(S3, S2), S1 != S3.\n'
                model += '\n'
                
                model += '% a state is visited if one of the incoming edges is taken\n'
                model += 'visited(S) :- edge(_, S).\n'
                model += '\n' 
            else:
                # Because otherwise the mode will force the other stages
                # to have mutiple paths
                if mode != 'system_model':
                    # So we are not really looking for a single path
                    # that is lets have all the edges in place
                    model += '% We are not looking for a single path,\n'
                    model += '%  thus lets have all the edged in place.\n' 
                    model += '#const min_edge_cnt=1.\n'
                    model += '#const max_edge_cnt=2.\n'
                    model += '\n'            
            
            if mode == 'system_model':        
                model += '% reachability\n'
                model += 'reaches(S1, S2):- edge(S1, S2).\n'
                model += 'reaches(S1, S2):- edge(S1, S3), reaches(S3, S2).\n'
                model += '\n'

                

            if 'state' in facts:
                model += '% gloabal state is always visited\n'
                model += 'visited(global).\n'
                model += '\n'
        

            if 'bool_expr' in facts:
                facts_to_maintain['bool_expr'] = facts['bool_expr']
            
        # We are creating the model for entity generation
        # That is, enumerating all possible entites to be covered
        if mode == 'coverage_criterion':            
            if 'entity' not in facts:
                print("FATAL: No entity is defined for coverage. Exiting...")
                sys.exit(1)
                
            # coverage criterion
            model += '% coverage criterion\n'
            model += '\n'.join(facts['entity'])
            model += '\n'
            model += '\n'
 
            # Now, add the #show directives so that all the entites is reported
            arities = set(get_arities(facts['entity']))
            for arity in arities:
                model += "#show entity/%d.\n" % arity
            model += '\n'

            # Now, get the entity signatures so that we can pass that information to
            #      the ucit generation part
            entity_signatures = get_entity_signatures(facts['entity'])
                        
            # FIXME: This could be a memory problem if there are too
            # many facts
            #facts_to_maintain['entity'] = copy.deepcopy(facts['entity'])
            facts_to_maintain['entity'] = facts['entity']
            facts_to_maintain['entity_signature'] = entity_signatures

            # Now, convert the boolean expressions
            if 'bool_expr' in facts:
                model += compile_bool_exprs(facts['bool_expr'])
                facts_to_maintain['bool_expr'] = facts['bool_expr']
            
        elif mode == 'ucit_generation':
            model += '% condition under which an entity is considered covered\n'
            for entity in facts['entity']:
                covered = ''
                if ':-' not in entity:
                    # entity to be covered is just a fact
                    covered = re.sub('\s*\.\s*$','', entity)
                    covered = re.sub('^entity', 'entity_covered', covered)
                    covered += ":-%s\n" % entity + '\n'
                    model += covered
                else:
                    # the entity is a rule
                    covered = re.sub('\s*:-.+$', '', entity)
                    covered = re.sub('^entity', 'entity_covered', covered)
                    covered = covered + ':-' + re.sub('\s*:-\s*', ',', entity) + '\n'
                    model += covered
            model += '\n'

            if('testcase' not in facts):
                print(facts)
                print("FATAL: in file '%s', 'testcase' rule must be defined!" % input_file)
                sys.exit(1)

            if constructor_algo == 'one-test-case-at-a-time-constructor':
                # This constrcutor will generate a test case at a time such that
                # each test case covers the most number of previosuly uncovered
                # entities.
                model += '% at least one the entites needs to be covered\n'
                for signature in facts['entity_signature']:
                    model += "entity_covered :- %s\n" % re.sub('^entity_signature', 'entity_covered', signature) 
                model += ':- not entity_covered.\n'
                model += '\n'

                model += '% number of entities to be covered should be maximized\n'
 
                maximize = '#maximize{'
                for signature in facts['entity_signature']:
                    signature = re.sub('\s*\.\s*$', '', signature)
                    signature = re.sub('^entity_signature', 'entity_covered', signature)
                    # NEW
                    #maximize += "1,%s:%s;\n" % (re.compile("^entity_covered\((.+)\)").search(signature).group(1), signature)
                    maximize += "1,%s:%s;\n" % (re.compile("^entity_covered\s*\((.+)\)").search(signature).group(1), signature) 
                
                # remove the last ;
                maximize = re.sub('\;\n$', '', maximize)
                maximize += '}.\n'
                model += maximize
                model += '\n'

            elif constructor_algo == 'cover-and-generate-constructor':                
                # This is the cluster based construction approach
                # At this poin we don't need to add anything
                None
            else:
                print("FATAL: Unknown constrcutor approach '%s'. Exiting..." % constructor_algo)
                sys.exit(1)

            model += '% test case\n'
            model += '\n'.join(facts['testcase'])
            model += '\n'
            model += '\n'
                             
            # TODO: We assume that for the test cases that can be generated
            #       thereis testcase :- tescase(....) rule
            model += '% we need to compute a test case\n'
            model += ':- not testcase.\n'
            model += '\n'

            # Now, convert the boolean expressions
            if 'bool_expr' in facts:
                model += compile_bool_exprs(facts['bool_expr'])
                
        # perform the imports
        model += '% importing required rules.\n'
        if (len(imports) == 0):
            model += '% None\n'
        else:
            for importing in imports:
                for arg in imports[importing]:
                    model += eval("library_%s(arg)" % importing)
        model += '\n'
        
        # dump everything which is not a keyword
        model += '% user specific definitions\n'
        found = False
        for keyword in facts:
            if keyword not in keywords:
                found = True
                model += '% user defined ' + keyword + '\n'
                model += '\n'.join(facts[keyword])
                model += '\n\n'
        if not found:
            model += '% None\n\n'

        # print the directives
        model += '% ASP directives\n'
        if '__directive__' not in facts:
            model += '% None\n'
        else:
            model += '\n'.join(facts['__directive__'])
            model += '\n'
        model += '\n'
        
        return model, facts_to_maintain

def create_model(indir,
                 system_model_file,
                 coverage_criterion_file,
                 ucit_generation_file):

    system_model_script = indir + '/system_model.lp'
    if os.path.isfile(system_model_script):
        os.remove(system_model_script)
        
    enumeration_script = indir + '/enumerate_entities.lp'
    if os.path.isfile(enumeration_script):
        os.remove(enumeration_script)

    one_test_case_at_a_time_constructor_script = indir + '/one_test_case_at_a_time_constructor.lp'
    if os.path.isfile(one_test_case_at_a_time_constructor_script):
        os.remove(one_test_case_at_a_time_constructor_script)
 
    cover_and_generate_constructor_script = indir + '/cover_and_generate_constructor.lp'
    if os.path.isfile(cover_and_generate_constructor_script):
        os.remove(cover_and_generate_constructor_script)
          
    print('\n######## PROCESSING INPUT #########')
    facts_to_maintain = {}

    print("Generating the system model: '%s'" % system_model_script)
    system_model, facts_to_mantain = parse('system_model', system_model_file, facts_to_maintain)
    with open(system_model_script, "w") as f:
        f.write(system_model)

    print("Generating the entity enumeration script: '%s'" % enumeration_script)
    coverage_criterion, facts_to_mantain = parse('coverage_criterion', coverage_criterion_file, facts_to_mantain)
    with open(enumeration_script, "w") as enum_file:
        enum_file.write(coverage_criterion)

    facts_to_mantain_copy = copy.deepcopy(facts_to_mantain)                
    print("Generating one-test-case-at-a-time-constructor: '%s'" % one_test_case_at_a_time_constructor_script)
    ucit_generation, some_more_facts_to_mantain = parse('ucit_generation',
                                                        ucit_generation_file,
                                                        facts_to_mantain_copy,
                                                        constructor_algo='one-test-case-at-a-time-constructor')    
    with open(one_test_case_at_a_time_constructor_script, "w") as gen_file:
        gen_file.write(ucit_generation)
    ucit_generation = None # reset the constructor

    facts_to_mantain_copy = copy.deepcopy(facts_to_mantain)                
    print("Generating cover-and-generate-constructor: '%s'" % cover_and_generate_constructor_script)
    ucit_generation, some_more_facts_to_mantain = parse('ucit_generation',
                                                        ucit_generation_file,
                                                        facts_to_mantain_copy,
                                                        constructor_algo='cover-and-generate-constructor')    
    with open(cover_and_generate_constructor_script, "w") as gen_file:
        gen_file.write(ucit_generation)
    ucit_generation = None # reset the constructor

    print('######################################')          
 
def parse_clingo_output_for_entities_to_be_covered(output_file, workdir):
    # check to see if the output file indicates satisfiable constraints
    satisfiable = clingo_output_indicates_satisfiability(output_file)

    if satisfiable is None:
        # something went wrong with the asp
        print("Fatal: The clingo output '%s' indicates an error. Exiting..." % output_file)
        sys.exit(-1)
        
    # read the solution and dump it to a file
    tmp_file = workdir + '/clingo.output'
    if os.path.isfile(tmp_file):
        os.remove(tmp_file)
        
    os.system("grep 'entity' %s > %s" % (output_file, tmp_file))

    # process the entity rules
    tmp_processed_file = tmp_file + '.processed'
    if os.path.isfile(tmp_processed_file):
        os.remove(tmp_processed_file)
        
    with open(tmp_file, "r") as inf, open(tmp_processed_file, "w") as outf:
        for line in inf:
            # TODO: Performance issue . Can we read these one by one
            entities = re.findall('entity\([^\)]+\)', line)
            for entity in entities:
                outf.write(entity + '.\n')

    entities_lst_file = workdir + '/entities.lst'
    if os.path.isfile(entities_lst_file):
        os.remove(entities_lst_file)

    print("Generating: '%s'" % entities_lst_file)   
    os.system("sort %s | uniq > %s" % (tmp_processed_file, entities_lst_file))

    # FIXME you need top shuffle the list of entities

    # Remove the temp files
    if os.path.isfile(tmp_file):
        os.remove(tmp_file)
        
    if os.path.isfile(tmp_processed_file):
        os.remove(tmp_processed_file)
         
    return True, entities_lst_file
      
def one_test_case_at_a_time_constructor(dir):
    constructor_name = 'one_test_case_at_a_time_constructor'

    print("\n######## ENUMERATING ENTITES using %s #########" % constructor_name)
    # create the work dir
    workdir = dir + '/' + constructor_name
    if not os.path.exists(workdir):
        os.makedirs(workdir)
         
    system_model_file = dir + '/system_model.lp'
    one_test_case_at_a_time_constructor_file = dir + '/one_test_case_at_a_time_constructor.lp'

    all_entities_file = dir + '/entities.lst'

    # find out where we were left
    steps = [s for s in os.listdir(workdir) if re.match(r'step.[0-9]+$', s)]

    # find the last step idx
    idxs = []
    for s in steps:
        idxs.append(int(re.compile("\.([0-9]+)$").search(s).group(1)))

    # we are going to rerun the last step as we don't know where it stopped
    step = 1
    if len(idxs) > 0:
        step = max(idxs)

    # this means that we have just started
    # so copy all the entities to be coverd
    if step == 1: 
        copyfile(all_entities_file, workdir + '/step.1')

    entities_file = "%s/step.%d" % (workdir, step)
        
    remaining_entities_to_cover = True
    # repeat until all the entities are covered
    while(remaining_entities_to_cover):
        stdout, stderr = run_cmd(['wc', '-l', entities_file])
        entity_cnt = None
        if stdout != '':
            entity_cnt = int(stdout.split()[0])

        if entity_cnt is None:
            print("FATAL: Entity count in '%s' cannot be determined. Exiting..." % entities_file)
            sys.exit(-1)

        if entity_cnt == 0:
            print('Everything is already covered...')
            return

        clingo_raw_output = entities_file + '.testcase'
        if os.path.isfile(clingo_raw_output):
            os.remove(clingo_raw_output)

        clingo_cmd = "clingo %s %s %s >& %s" % (system_model_file,
                                                one_test_case_at_a_time_constructor_file,
                                                entities_file, clingo_raw_output)
 
        print("############")
        print("Step: %s" % str(step))
        print("Entites to cover: %s" % entity_cnt)
        print("  This may not be reliable as we are simply counting the number of lines.")
        print("Running cmd: '%s'" %  clingo_cmd)
        print("Generating: '%s'" %  clingo_raw_output)
        
        os.system(clingo_cmd)

        # TODO We are parsing just the entites_covered
        # we also need to parse the test case
    
        #find all the entities covered
        tmp_file = clingo_raw_output + '.parsed'
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        # TODO: This is really a trick. Could generate wrong results find a better way
        #    of parsing the optimal solution out of the output
        os.system("grep 'entity_covered' %s > %s" % (clingo_raw_output, tmp_file))

        # process the entity rules
        tmp_processed_file = clingo_raw_output + '.covers'
        if os.path.isfile(tmp_processed_file):
            os.remove(tmp_processed_file)

        print("Generating: '%s'" %  tmp_processed_file)

        # TODO you need to get the last line, because when you need to optimize the solution
        #    ,ultiple solution can be generated and the last one is the optimum one

        with open(tmp_file, "r") as inf, open(tmp_processed_file, "w") as outf:
            optimum_solution = None
            # FIXME The following code assumes that the last solution reported is the best found
            # so far. I am not sure if this is really the case if the time-out mechanism is used
            for line in inf:
                optimum_solution = line

                
            entities = re.findall('entity_covered\([^\)]+\)', optimum_solution)
            for entity in entities:
                entity = re.sub('entity_covered\s*\(', 'entity(', entity)
                outf.write(entity + '.\n')

        os.remove(tmp_file)

        tmp_file = tmp_processed_file + '.tmp'
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)
        os.system("sort %s | uniq > %s" % (tmp_processed_file, tmp_file))

        os.system("cp -f %s %s" % (tmp_file, tmp_processed_file))
        os.remove(tmp_file)

        # remove the list of covered entities from the list of
        # yet to be covered entities

        # remove the step number and add the next number
        next_entities_file = re.sub('\.[0-9]+$', '', entities_file)
        step += 1
        next_entities_file += '.' + str(step)

        # take the set difference between the two files
        print("Generating: '%s'" % next_entities_file)
        os.system("comm -23 %s %s > %s" % (entities_file, tmp_processed_file, next_entities_file) )

        # check to see if there are still entites to be covered
        stdout, stderr = run_cmd(['grep', '-m', '1', "entity(", next_entities_file])
        if 'entity(' not in stdout:
            remaining_entities_to_cover = False

        # FIXME you need top shuffle the list of entities
        
        entities_file = next_entities_file

        print("############")

    print("\n###############################################")

def enumerate_entities(dir, system_model_lp, enumerate_entities_lp):

    print('\n######## ENUMERATING ENTITES #########')
 
    # enumerate the entities to be covered
    clingo_raw_output = dir + '/enumerate_entities.raw.output'
    # generate all solutions
    clingo_cmd = "clingo 0 %s %s >& %s" % (system_model_lp, enumerate_entities_lp, clingo_raw_output)    
    print("Running: '%s'" % clingo_cmd)
    print("Generating: '%s'" % clingo_raw_output)   
    os.system(clingo_cmd)
    print("Parsing: '%s'" % clingo_raw_output)
    computed_some_entities, entities_to_cover_file = parse_clingo_output_for_entities_to_be_covered(clingo_raw_output, dir)
    
    if not computed_some_entities:
        print("FATAL: There is no entity to cover. Exiting...")
        sys.exit(1)

    print("Generated: '%s'" % entities_to_cover_file)
    
    print('######################################')
    
        
def compute_ucit(dir):

    # input files
    system_model_file = dir + '/system.model'
    coverage_criterion_file = dir + '/coverage.criterion'
    ucit_generation_file = dir + '/ucit.testcase'

    # create the scripts
    create_model(dir,
                 system_model_file,
                 coverage_criterion_file,
                 ucit_generation_file)

    # output files generated by create_model
    system_model_lp = dir + '/system_model.lp'
    enumerate_entities_lp = dir + '/enumerate_entities.lp'
     
    # enumerate the entities to be covered
    enumerate_entities(dir, system_model_lp, enumerate_entities_lp)
 
    # run the one_test_case_at_a_time_constructor
    one_test_case_at_a_time_constructor(dir)

    # run the cover_and_generate constructor
    cover_and_generate_constructor(dir)
    

def cover_and_generate_constructor(dir):
    constructor_name = 'cover_and_generate_constructor'

    print("\n######## ENUMERATING ENTITES using %s #########" % constructor_name)
    
    # create the workdir
    workdir = dir + '/' + constructor_name
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    # create the dir underwhich the clusters will be stored
    clusters_dir = workdir + '/clusters'
    if not os.path.exists(clusters_dir):
        os.makedirs(clusters_dir)
        
    system_model_file = dir + '/system_model.lp'
    cluster_based_constructor_file = dir + '/cover_and_generate_constructor.lp'
    all_entities_file = dir + '/entities.lst'
    covered_entities_file = "%s/covered_entities.lst" % workdir
    remaining_entities_file = "%s/remaining_entities.lst" % workdir
    current_entity_lp = "%s/current_entity.lp" % workdir
    cluster_check_output = "%s/cluster_check.output" % workdir
    
    # Find all the clusters that have been created so far
    clusters = [c for c in os.listdir(clusters_dir) if re.match(r'cluster.[0-9]+$', c)]

    # find the next index to be used
    idxs = []
    for cluster in clusters:
        idxs.append(int(re.compile("\.([0-9]+)$").search(cluster).group(1)))

    next_cluster_idx = 1
    if len(idxs) > 0:
        next_cluster_idx = max(idxs) + 1

    # if some clusters have already existed then figure
    # out the entities yet to be covered
    if len(idxs) > 0:
        # Figure out all the entities already covered
        with open(covered_entities_file, 'w') as out_file:
            for cluster in clusters:
                with open(clusters_dir + '/' + cluster, 'r') as in_file:
                    for line in in_file:
                        if re.match(r'^\s*entity\s*\(', line):
                            out_file.write(line)
                            
        # Now find the ones that are remaining to be covered
        # take the set difference between the two files
        os.system("comm -23 %s %s > %s" % (all_entities_file, covered_entities_file, remaining_entities_file) )
    else:
        # There is no cluster out there
        # therefore the ramining entities to be covered is the same as all entites to be covered
        copyfile(all_entities_file, remaining_entities_file)

    # Now, the remaining entities file contain all the entities yet to be covered
    # Iterate over them and find a cluster for each entity
    with open(remaining_entities_file, 'r') as entities_file:
        for entity in entities_file:

            if os.path.isfile(current_entity_lp):
                os.remove(current_entity_lp)
        
            if entity.strip() == '':
                continue
            
            if not re.match(r'^\s*entity\s*\(', entity):
                print("FATAL: Malformed entity '%s' in file '%s'" % (entity, remaining_entities_file))
                sys.exit(-1)

            # here is the constraint for covering the entity
            # It should have the entity together with the not entity_covered constaint to
            # make sure that the entity is indeed covered
            entity_lp = entity        
            entity_lp += re.sub('^\s*entity\s*\(', ':- not entity_covered(', entity)
            with open(current_entity_lp, 'w') as curr_entity_file:
                curr_entity_file.write(entity_lp)

            # try to find a cluster that can accomodate this entity
            # shuffle the clusters
            random.shuffle(clusters)

            found_cluster = None
            for cluster in clusters:
                # solve system_model.lp + cluster_based_constructor.lp + cluster + current_entity together
                cluster_lp = clusters_dir + '/' + cluster + '.lp'
                clingo_cmd = "clingo %s %s %s %s" % (system_model_file, cluster_based_constructor_file, cluster_lp, current_entity_lp)

                # check to see if this is satisfiable
                satisfiable = is_asp_satisfiable(clingo_cmd, cluster_check_output)

                if satisfiable is None:
                    print("Fatal: Something is wrong with the ASP program: '%s'" % clingo_cmd)
                    print("       Check the output: '%s'" % cluster_check_output)                    
                    sys.exit(-1)
                    
                if satisfiable:
                    found_cluster = cluster
                    break

            if found_cluster is None:
                # none of the existing clusters can accomodate this entity then create
                # a new cluster
                new_cluster = 'cluster.' + str(next_cluster_idx)
                clusters.append(new_cluster)
                next_cluster_idx += 1
                found_cluster = new_cluster

            # udate the entity list in the cluster 
            with open(clusters_dir + '/' + found_cluster, "a") as f:
                f.write(entity)

            # update the asp program for the cluster
            with open(clusters_dir + '/' + found_cluster +'.lp', "a") as f:
                f.write(entity_lp)
    
    print('######################################')          


#compute_ucit('./scenarios/cost_aware')

compute_ucit('./scenarios/standard_ca')

#compute_ucit('./scenarios/test_case_aware_ca')

#compute_ucit('./scenarios/decision_coverage')

#compute_ucit('./scenarios/order_based')

#compute_ucit('./scenarios/def_use_pair')


