% ##import(citlib.flow)
% ##import(citlib.graphs.c)
% ##import(citlib.any,t=2)


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/citlib/reachability.lp %%%%%%%%%%%%

reaches(A,B) :- edge(A,B), A!=B.
reaches(A,B) :- edge(A,C), reaches(C,B).
% #show reaches/2.
% ##import(citlib.order,t=2)
% TODO: We may want nonconsec to call any as a dependency
% ##import(citlib.nonconsec,t=2)
% ##import(citlib.all-entity)


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/ordernew3.lp %%%%%%%%%%%%

1{order(A,B,C)}1 :- reaches(A,B),reaches(B,C).
% ##import(citlib.ordernew,t=2)

% Set timeout for clingo

% Make this generic, key value dictionary for any variable

% #show flow/3.

% edge_guard(1,3) :- d2f.

% TODO: change this
% entity(A,B) :- order(A,B).
entity(A,B,C) :- order(A,B,C).
% entity_covered(A,B) :- 

#show entity/3.
#show entity_covered/3.
% TODO: change this
% entity(A,B) :- order(A,B).
% entity_covered(A,B) :- 
entity_covered(A,B,C) :- entity(A,B,C) , order(A,B,C).


#show entity_covered/3.#const n=6.
% Define vertices
vertex(0..n).
% Define edges
edge(0,1).
edge(1,2).
edge(1,3).
edge(1,4).
edge(1,5).
edge(2,4).
edge(3,4).
edge(4,5).
edge(5,6).

% Define start and stop
% start(0).
% stop(n).

% testcase :- start(0), stop(n).% boolean variables
1{parameter(global, a, true); parameter(global, a, false)}1.
1{parameter(global, b, true); parameter(global, b, false)}1.
1{parameter(global, c, true); parameter(global, c, false)}1.

% d2t : orig = (a&~b)|c
% d2t : dnf  = Or(c, And(a, ~b))
d2t :- parameter(global, a, true), parameter(global, b, false).

% d2f : orig = ~((a&~b)|c)
% d2f : dnf  = Or(And(~a, ~c), And(b, ~c))
d2f :- parameter(global, a, false), parameter(global, c, false).
d2f :- parameter(global, b, true), parameter(global, c, false).

