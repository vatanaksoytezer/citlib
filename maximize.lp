% cardinal(T) :- T = #count{1,A,B: entity_covered(A,B)}.

#maximize{1@1,A,B: entity_covered(A,B)}.
% #show entity_listed/2.
