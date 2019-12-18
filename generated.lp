#const n=6.
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

% testcase :- start(0), stop(n).% ##import(citlib.flow)
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


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/ordernew2.lp %%%%%%%%%%%%

1{order(A,B)}1 :- reaches(A,B).
% Set timeout for clingo

% Make this generic, key value dictionary for any variable

% #show flow/3.


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/citlib/flow.lp %%%%%%%%%%%%

% start(0).
% stop(n).

{flow(A,B,1) : edge(A, B), reached(A)}1 :- vertex(A).

reached(A) :- start(A).
% :- not reached(A), stop(A).
:- stop(A), reached(B), flow(A,B,E).

reached(B) :- reached(A), flow(A,B,1).
:- flow(A,B,1), not reached(B).

:- flow(A,B,1), flow(C,B,1), A!=C.

:- T = #sum{E,A: flow(A,B,E), start(A), edge(A,B)}, T!=1.
:- T = #sum{E,B: flow(A,B,E), stop(B), edge(A,B)}, T!=1.

#show flow/3.

% TODO: Do this python

start(0).
stop(6).
% cardinal(T):- T = #count{1,A,B: entity(A,B), flow(A,_,_), flow(_,B,_), start(A),stop(B)}.
cardinal(T) :- T = #count{1,A,B: entity(A,B), flow(A,_,_), flow(_,B,_)}.
:~ entity(A,B), cardinal(T).[-T@1]
entity_covered(A,B) :- entity(A,B), flow(A,_,_), flow(_,B,_).
% #show cardinal/1.
% #show order/2.
#show entity_covered/2.
testcase. % :- start(_), stop(_).
% :- not testcase.

% #show flow/3.
% #show testcase.

% TODO: Do this python
