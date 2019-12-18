consec(A,B,C) :- edge(A,B), edge(B,C).
:- not flow(A,B,1), order(A,B,C).
:- not flow(B,C,1), order(A,B,C).

% #show order/3.