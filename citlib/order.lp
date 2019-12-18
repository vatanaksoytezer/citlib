{order(A,B,C) : reaches(A,B), reaches(B,C)} :- vertex(A).
:-order(_,_,C), order(_,_,C1), C!=C1.
:-order(_,B,_), order(_,B1,_), B!=B1.
:-order(A,_,_), order(A1,_,_), A!=A1.
:- not order(_,_,_).

#show order/3.

% 1{order(A,B) : reaches(A,B)}1.

% #show order/2.