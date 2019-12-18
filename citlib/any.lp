
:- T = #sum{E,A,B,C :flow(_,A,E), flow(_,B,E), flow(_,C,E), order(A,B,C)}, T!=1.
