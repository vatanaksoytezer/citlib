cardinal(T) :- T = #count{1,A,B: entity(A,B), flow(A,_,_), flow(_,B,_)}.
:~ entity(A,B), cardinal(T).[-T@1]
entity_covered(A,B) :- entity(A,B), flow(A,_,_), flow(_,B,_).
#show cardinal/1.
% #show order/2.
#show entity_covered/2.
