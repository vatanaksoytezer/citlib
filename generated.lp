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

% bool_expr(d1t, a).
% bool_expr(d1f, ~a).

% edge_guard(1,2) :- d1f.
% edge_guard(1,3) :- d1t.

% states
% state(global).
% state(s1).
% state(s2).
% state(s3).
% state(s4).
% state(s5).
% state(s6).
% state(s7).
% state(s8).
% state(s9).

% % edges
% edge(s1,s2).
% edge(s1,s3).
% edge(s2,s4).
% edge(s3,s4).
% edge(s5,s6).
% edge(s5,s9).
% edge(s6,s7).
% edge(s6,s8).
% edge(s7,s9).
% edge(s8,s9).

% % edge guards, which need to be satisfied
% % before the edges can be taken
% edge_guard(s1,s2):-d1t.
% edge_guard(s1,s3):-d1f.
% edge_guard(s5,s6):-d2t.
% edge_guard(s5,s9):-d2f.
% edge_guard(s6,s7):-d3t.
% edge_guard(s6,s8):-d3f.
% edge_guard(s3,s4).
% edge_guard(s8,s9).
% edge_guard(s7,s9).
% edge_guard(s2,s4).

% bool_expr(d1t, a).
% bool_expr(d1f, ~a).

% bool_expr(d2t, (a & ~b) | c).
% bool_expr(d2f, ~((a & ~b) | c)).

% bool_expr(d3t, (k & l) | m).
% bool_expr(d3f, ~((k & l) | m)).
% ##import(citlib.reachability)
% ##import(citlib.flow)


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/citlib/flow.lp %%%%%%%%%%%%

% start(0).
% stop(n).

% Add edge guard here
{flow(A,B,1) : edge(A, B), reached(A)}1 :- vertex(A).
% {flow(A,B,1) : edge_guard(A,B), edge(A, B), reached(A)}1 :- vertex(A).
% {flow(A,B,1)}1 :- edge(A, B), edge_guard(A,B), reached(A), vertex(A;B).

reached(A) :- start(A).
% :- not reached(A), stop(A).
:- stop(A), reached(B), flow(A,B,E).

reached(B) :- reached(A), flow(A,B,1).
reached(global).

%:- flow(A,B,1), not reached(B).
:- flow(A,B,1), flow(A,C,1), B!= C.
:- flow(A,B,1), flow(C,B,1), A!=C.
flow_num(A,B,1) :- start(A), edge(A,B), flow(A,B,_).
flow_num(B,C,N) :- flow_num(A,B,N-1), flow(B,C,_).
% :- T = #sum{E,A: flow(A,B,E), start(A), edge(A,B)}, T!=1.
% :- T = #sum{E,B: flow(A,B,E), stop(B), edge(A,B)}, T!=1.

#show flow_num/3.



%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/maximize2.lp %%%%%%%%%%%%

#maximize{1@1,A,B: entity_covered(A,B)}.


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/path_dependent_order2.lp %%%%%%%%%%%%

{order(A,B):flow(A,_,_), flow(_,B,_)}.


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/any2.lp %%%%%%%%%%%%

:- T = #sum{E,A,B: flow(_,A,E),flow(_,B,E),order(A,B)}, T!=1.


%%%%%%%%%% Auto Generated from /home/tezer/su_courses/CS560/Project/generated/nonconsec2.lp %%%%%%%%%%%%

:- T1 = #sum{E1: flow(A,B,E1), order(A,B)},T1>=1.


start(1).
stop(5).

testcase.

% TODO: change this
% entity_covered(A,B) :-

#show entity/2.
#show entity_covered/2.
% TODO: change this
% entity_covered(A,B) :-
entity_covered(A,B) :- entity(A,B) , order(A,B).


#show entity_covered/2.entity(0,1).
entity(1,2).
entity(1,3).
entity(2,4).
entity(3,4).
entity(4,5).
entity(5,6).
entity(1,6).
entity(4,6).
entity(0,5).
entity(0,4).
entity(0,3).
entity(0,2).
entity(2,6).
entity(3,6).
entity(0,6).
% boolean variables

