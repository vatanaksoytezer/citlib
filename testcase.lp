##import(citlib.reachability)
##import(citlib.flow)
##import(citlib.maximize)
##import(citlib.path_dependent_order)
##define timeout=1800

start(1).
stop(5).

% {order(A,B): flow(A,_,_), flow(_,B,_)}.

% TODO: Add this to library, auto generate
% {order(A,B,C): flow(A,_,_), flow(_,B,_), flow(B,_,_), flow(_,C,_)}.
% {order(A,B,C,D): flow(A,_,_), flow(_,B,_), flow(B,_,_), flow(_,C,_), flow(C,_,_), flow(_,D,_)}.


% TODO: This one as well, autogenerate
% #maximize{1@1,A,B: entity_covered(A,B)}.
% #maximize{1@1,A,B,C: entity_covered(A,B,C)}.

% entity_covered(A,B) :- entity(A,B), order(A,B).

% #show entity_covered/2.
testcase.
