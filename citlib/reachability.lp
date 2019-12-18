reaches(A,B) :- edge(A,B), A!=B.
reaches(A,B) :- edge(A,C), reaches(C,B).
% #show reaches/2.