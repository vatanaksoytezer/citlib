% cardinal(T) :- T = #count{1,A,B: entity_covered(A,B)}.

% #maximize{1@1,A,B: entity_listed(A,B)}.
% entity_covered(A,B) :- entity(A,B), 
% #show entity_listed/2.