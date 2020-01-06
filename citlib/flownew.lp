% each edge is either flow or not flow
{flow(A, B, N+1)} :- edge(A, B), edge_guard(A, B), visited(A, N).

% only one edge origination from a state can be flow
:- flow(A, B, _), flow(A, C, _), B != C.

% only one edge comming to  a state can be flow
:- flow(A, B, _), flow(C, B, _), A != C.

% a state is visited if one of the incoming edges is flow
visited(A, N) :- flow(_, A, N).

% reachability
reached(A, B):- flow(A, B, _).
reached(A, B):- flow(A, C, _), reached(C, B).

% gloabal state is always visited
visited(global, -1).

% importing required rules.
% None

% user specific definitions
% user defined visited
visited(s1,0).

% ASP directives
% None
