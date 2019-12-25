##import(citlib.reachability)
##import(citlib.flow)
##define timeout=2

start(1).
stop(5).

% {order(A,B): flow(A,_,_), flow(_,B,_)}.
{order(A,B,C): flow(A,_,_), flow(_,B,_), flow(B,_,_), flow(_,C,_)}.

% #maximize{1@1,A,B: entity_covered(A,B)}.
#maximize{1@1,A,B,C: entity_covered(A,B,C)}.

% entity_covered(A,B) :- entity(A,B), order(A,B).

% #show entity_covered/2.
testcase.