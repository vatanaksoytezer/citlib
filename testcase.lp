##import(citlib.flow)
start(0).
stop(6).
% cardinal(T):- T = #count{1,A,B: entity(A,B), flow(A,_,_), flow(_,B,_), start(A),stop(B)}.
cardinal(T) :- T = #count{1,A,B: entity(A,B), flow(A,_,_), flow(_,B,_)}.
:~ entity(A,B), cardinal(T).[-T@1]
entity_covered(A,B) :- entity(A,B), flow(A,_,_), flow(_,B,_).
% #show cardinal/1.
% #show order/2.
#show entity_covered/2.
testcase. % :- start(_), stop(_).
% :- not testcase.

% #show flow/3.
% #show testcase.

% TODO: Do this python
