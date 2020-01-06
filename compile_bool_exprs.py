import re
import sys
from pyeda.inter import *

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
        var_decs += "1{parameter(global, %s, true); parameter(global, %s, false)}1.\n" % (var, var)
        #var_decs += "1 {true(%s);false(%s)} 1.\n" % (var, var)
    var_decs += '\n'

    asp = var_decs + asp

    return asp



def compile_bool_exprs(bool_exprs):
    exprs_info = []

    for bool_expr in bool_exprs:
        args = re.compile("^bool_expr\s*\((.+)\)\s*\.$").search(bool_expr).group(1)
        args = re.sub('\s+', '', args)
        args = args.split(',')

        if len(args) != 2:
            print("FATAL: bool_expr should have two args: bool_expr(name, expr).")
            print("Violation: %s", bool_expr)
            sys.exit(1)
    
        exprs_info.append({'name' : args[0], 'expr' : args[1]})
        
    # print(exprs_info)
    asp = bool_exprs_to_clingo(exprs_info)

    return asp


# in bool_expr the first argument is the name of the expression
# the second one is the expression itself
exprs = ["bool_expr(d2t, (k & l) | m).",
         "bool_expr(d2f, ~((k & l) | m))."]
 
# exprs1 = ["bool_expr(d1t, a).", "bool_expr(d1f, ~a)."]

asp = compile_bool_exprs(exprs)
# print(asp)
 
