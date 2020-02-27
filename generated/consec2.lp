consec(A,B) :- edge(A,B).
:- not flow(A,B,1), order(A,B).