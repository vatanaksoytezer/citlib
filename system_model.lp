% #const n=6.
% % Define vertices
% vertex(0..n).
% % Define edges
% edge(0,1).
% edge(1,2).
% edge(1,3).
% edge(1,4).
% edge(1,5).
% edge(2,4).
% edge(3,4).
% edge(4,5).
% edge(5,6).

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


% Define vertices
vertex(0..78).
% Define edges
edge(ss,s0).
edge(ss,s0_2).
edge(ss,s0_3).
edge(s0_2,s1).
edge(s7_3,s9).
edge(s7_3,s8).
edge(s8,s9).
edge(s8,s8_2).
edge(s9,s10).
edge(s10,s11).
edge(s11,s12).
edge(s11,s12_2).
edge(s12,s13).
edge(s12_2,s11_2).
edge(s11_2,s12).
edge(s13,s14).
edge(s13,s15).
edge(s13,s15_2).
edge(s13,s15_3).
edge(s13,s14_2).
edge(s13,s14_3).
edge(s13,s14_4).
edge(s13,s15_4).
edge(s14_2,s14_5).
edge(s14_2,s15_2).
edge(s0,s1_2).
edge(s14_3,s14_6).
edge(s14_3,s15_4).
edge(s14_4,s15_3).
edge(s14_4,s14_7).
edge(s14,s14_8).
edge(s14,s15).
edge(s15_2,s16).
edge(s15_4,s12_3).
edge(s15_3,s12_4).
edge(s15,s12_5).
edge(s12_5,s11_3).
edge(s11_3,s12_6).
edge(s11_3,s12_4).
edge(s12_4,s13_2).
edge(s0_3,s1_3).
edge(s12_6,s11_4).
edge(s13_2,s14_3).
edge(s13_2,s14_2).
edge(s13_2,s15_2).
edge(s13_2,s15_4).
edge(s12_3,s11_5).
edge(s11_5,s16).
edge(s11_5,s12_7).
edge(s12_7,s11_6).
edge(s16,s17).
edge(s17,s18).
edge(s18,s19).
edge(s19,s20).
edge(s20,s21).
edge(s1_3,s2).
edge(s21,s22).
edge(s22,s23).
edge(s23,s24).
edge(s24,s25).
edge(s25,s26).
edge(s26,s27).
edge(s14_8,s15).
edge(s14_7,s15_3).
edge(s14_6,s15_4).
edge(s2,s3).
edge(s14_5,s15_2).
edge(s8_2,s9).
edge(s1_2,s2_2).
edge(s2_2,s3_2).
edge(s3_2,s4).
edge(s4,s5).
edge(s5,s6).
edge(s6,s7).
edge(s7,s9_2).
edge(s7,s8_3).
edge(s8_3,s9_2).
edge(s8_3,s8_4).
edge(s3,s4_2).
edge(s9_2,s10_2).
edge(s8_4,s9_2).
edge(s1,s2_3).
edge(s2_3,s3_3).
edge(s3_3,s4_3).
edge(s4_3,s5_2).
edge(s5_2,s6_2).
edge(s6_2,s7_2).
edge(s7_2,s9_3).
edge(s7_2,s8_5).
edge(s8_5,s9_3).
edge(s8_5,s8_6).
edge(s4_2,s5_3).
edge(s9_3,s10_3).
edge(s8_6,s9_3).
edge(s11_6,s16).
edge(s10_2,s13).
edge(s10_3,s11_5).
edge(s11_4,s12_4).
edge(s5_3,s6_3).
edge(s6_3,s7_3).
edge(s27,se_2).
edge(se_2,se).