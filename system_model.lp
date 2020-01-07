#const n=6.
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

bool_expr(d1t, a).
bool_expr(d1f, ~a).

edge_guard(1,2) :- d1f.
edge_guard(1,3) :- d1t.
