% states
state(global).
state(s1).
state(s2).
state(s3).
state(s4).
state(s10).
% state(s5).
% state(s6).
% state(s7).
% state(s8).
% state(s9).

% edges
edge(s1,s2).
edge(s1,s3).
edge(s2,s4).
edge(s3,s4).
edge(s2,s10).
% edge(s5,s6).
% edge(s5,s9).
% edge(s6,s7).
% edge(s6,s8).
% edge(s7,s9).
% edge(s8,s9).

% edge guards, which need to be satisfied
% before the edges can be taken
edge_guard(s1,s2):-d1t.
edge_guard(s1,s3):-d1f.
% edge_guard(s5,s6):-d2t.
% edge_guard(s5,s9):-d2f.
% edge_guard(s6,s7):-d3t.
% edge_guard(s6,s8):-d3f.
% edge_guard(s8,s9).
% edge_guard(s7,s9).
edge_guard(s2,s4)  :- d2t.
edge_guard(s2,s10) :- d2f.
edge_guard(s3,s4).

% each edge is either taken or not taken
{taken(A, B, N+1)}1 :- edge(A, B), edge_guard(A, B), visited(A, N).

% only one edge origination from a state can be taken
:- taken(A, B, _), taken(A, C, _), B != C.

% only one edge comming to  a state can be taken
:- taken(A, B, _), taken(C, B, _), A != C.

% a state is visited if one of the incoming edges is taken
visited(A, N) :- taken(_, A, N).

% reachability
reaches(A, B):- taken(A, B, _).
reaches(A, B):- taken(A, C, _), reaches(C, B).

% gloabal state is always visited
visited(global, -1).

% importing required rules.
% None

% user specific definitions
% user defined visited
visited(s1,0).
% visited(s5,0).

% ASP directives
% None
% boolean variables
1{parameter(global, a, true); parameter(global, a, false)}1.

% d1t : orig = a
% d1t : dnf  = a
d1t :- parameter(global, a, true).

% d1f : orig = ~a
% d1f : dnf  = ~a
d1f :- parameter(global, a, false).

1{parameter(global, l, true); parameter(global, l, false)}1.
1{parameter(global, k, true); parameter(global, k, false)}1.
1{parameter(global, m, true); parameter(global, m, false)}1.

% d2t : orig = (k&l)|m
% d2t : dnf  = Or(m, And(k, l))
d2t :- parameter(global, k, true), parameter(global, l, true).

% d2f : orig = ~((k&l)|m)
% d2f : dnf  = Or(And(~k, ~m), And(~l, ~m))
d2f :- parameter(global, k, false), parameter(global, m, false).
d2f :- parameter(global, l, false), parameter(global, m, false).