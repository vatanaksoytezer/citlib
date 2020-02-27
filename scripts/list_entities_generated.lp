% Put these to coverage criterion


%%%%%%%%%% Auto Generated from /home/tezer/citlib/citlib/reachability.lp %%%%%%%%%%%%

reaches(A,B) :- edge(A,B), A!=B.
reaches(A,B) :- edge(A,C), reaches(C,B).
% #show reaches/2.


%%%%%%%%%% Auto Generated from /home/tezer/citlib/generated/ordernew2.lp %%%%%%%%%%%%

1{order(A,B)}1 :- reaches(A,B).
% Set timeout for clingo

% Make this generic, key value dictionary for any variable

% TODO: change this
entity(A,B) :- order(A,B).
% entity(A,B) :- consec(A,B).
% entity(A,B,C) :- order(A,B,C).
% entity_covered(A,B) :-

#show entity/2.
#show entity_covered/2.
% TODO: change this
% entity(A,B) :- consec(A,B).
% entity(A,B,C) :- order(A,B,C).
% entity_covered(A,B) :-
entity_covered(A,B) :- entity(A,B) , order(A,B).


#show entity_covered/2.#const n=6.
% Define vertices
vertex(0..n).
% Define edges
edge(0,1).
edge(1,2).
edge(1,3).
edge(1,4).
edge(1,5).
edge(2,4).
edge(3,4).
edge(4,5).
edge(5,6).

% bool_expr(d1t, a).
% bool_expr(d1f, ~a).

% edge_guard(1,2) :- d1f.
% edge_guard(1,3) :- d1t.

% states
% state(global).
% state(s1).
% state(s2).
% state(s3).
% state(s4).
% state(s5).
% state(s6).
% state(s7).
% state(s8).
% state(s9).

% % edges
% edge(s1,s2).
% edge(s1,s3).
% edge(s2,s4).
% edge(s3,s4).
% edge(s5,s6).
% edge(s5,s9).
% edge(s6,s7).
% edge(s6,s8).
% edge(s7,s9).
% edge(s8,s9).

% % edge guards, which need to be satisfied
% % before the edges can be taken
% edge_guard(s1,s2):-d1t.
% edge_guard(s1,s3):-d1f.
% edge_guard(s5,s6):-d2t.
% edge_guard(s5,s9):-d2f.
% edge_guard(s6,s7):-d3t.
% edge_guard(s6,s8):-d3f.
% edge_guard(s3,s4).
% edge_guard(s8,s9).
% edge_guard(s7,s9).
% edge_guard(s2,s4).

% bool_expr(d1t, a).
% bool_expr(d1f, ~a).

% bool_expr(d2t, (a & ~b) | c).
% bool_expr(d2f, ~((a & ~b) | c)).

% bool_expr(d3t, (k & l) | m).
% bool_expr(d3f, ~((k & l) | m)).
% boolean variables

