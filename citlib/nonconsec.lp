% Non-consecuive comment
% nonconsec(A,B,C) :- reaches(A,X), reaches(X,B), reaches(B,C), X!=B.
% nonconsec(A,B,C) :- reaches(A,B), reaches(B,X), reaches(X,C), X!=C.

:- T1 = #sum{E1 :flow(A,B,E1), flow(B,C,E2), order(A,B,C)}, T2 = #sum{E2 :flow(A,B,E1), flow(B,C,E2), order(A,B,C)}, T1+T2>=2.
