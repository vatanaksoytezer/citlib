% start(0).
% stop(n).

{flow(A,B,1) : edge(A, B), reached(A)}1 :- vertex(A).

reached(A) :- start(A).
% :- not reached(A), stop(A).
:- stop(A), reached(B), flow(A,B,E).

reached(B) :- reached(A), flow(A,B,1).
:- flow(A,B,1), not reached(B).

:- flow(A,B,1), flow(C,B,1), A!=C.
flow_num(A,B,1) :- start(A), edge(A,B), flow(A,B,_).
flow_num(B,C,N) :- flow_num(A,B,N-1), flow(B,C,_).   
:- T = #sum{E,A: flow(A,B,E), start(A), edge(A,B)}, T!=1.
:- T = #sum{E,B: flow(A,B,E), stop(B), edge(A,B)}, T!=1.

#show flow_num/3.