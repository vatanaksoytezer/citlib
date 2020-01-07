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
