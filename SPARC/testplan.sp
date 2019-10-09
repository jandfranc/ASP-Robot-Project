#const n = 8.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sorts
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#location = [x][0..24].

#robot = [r].

#inertial_fluent = at(#robot,#location).

#defined_fluent = adjacent(#location(X),#location(Y)):X!=Y.

#fluent = #inertial_fluent + #defined_fluent.

#action = move(#robot,#location(X)).

#step = 0..n.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
predicates
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

holds(#fluent,#step).

occurs(#action,#step).

success().

goal(#step).

something_happened(#step).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-holds(F,I) :- #defined_fluent(F),
               not holds(F,I).

%%Can't be in two places
-holds(at(R,L2),I) :- holds(at(R,L1),I),
                      L1 != L2.

%%Only move to adjacent places
holds(at(R,L),I+1) :- occurs(move(R,L),I),
                      holds(at(R,LP),I),
                      holds(adjacent(L,LP),0),
                      LP != L.

holds(F,I+1) :- #inertial_fluent(F),
                holds(F,I),
                not -holds(F,I+1).

-holds(F,I+1) :- #inertial_fluent(F),
                 -holds(F,I),
                 not holds(F,I+1).

-occurs(A,I) :- not occurs(A,I).

:- occurs(A1,I),
   occurs(A2,I),
   A1 != A2.

success :- goal(I).
:- not success.

occurs(A,I) | -occurs(A,I) :- not goal(I).

something_happened(I) :- occurs(A,I).

:- goal(I), goal(I-1),
   J < I,
   not something_happened(J).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(adjacent(x0, x5),0).
holds(adjacent(x0, x1),0).
holds(adjacent(x1, x6),0).
holds(adjacent(x1, x2),0).
holds(adjacent(x1, x0),0).
holds(adjacent(x2, x7),0).
holds(adjacent(x2, x3),0).
holds(adjacent(x2, x1),0).
holds(adjacent(x3, x8),0).
holds(adjacent(x3, x4),0).
holds(adjacent(x3, x2),0).
holds(adjacent(x4, x9),0).
holds(adjacent(x4, x3),0).
holds(adjacent(x5, x10),0).
holds(adjacent(x5, x6),0).
holds(adjacent(x5, x0),0).
holds(adjacent(x6, x11),0).
holds(adjacent(x6, x7),0).
holds(adjacent(x6, x5),0).
holds(adjacent(x6, x1),0).
holds(adjacent(x7, x12),0).
holds(adjacent(x7, x8),0).
holds(adjacent(x7, x6),0).
holds(adjacent(x7, x2),0).
holds(adjacent(x8, x13),0).
holds(adjacent(x8, x9),0).
holds(adjacent(x8, x7),0).
holds(adjacent(x8, x3),0).
holds(adjacent(x9, x14),0).
holds(adjacent(x9, x8),0).
holds(adjacent(x9, x4),0).
holds(adjacent(x10, x15),0).
holds(adjacent(x10, x11),0).
holds(adjacent(x10, x5),0).
holds(adjacent(x11, x16),0).
holds(adjacent(x11, x12),0).
holds(adjacent(x11, x10),0).
holds(adjacent(x11, x6),0).
holds(adjacent(x12, x17),0).
holds(adjacent(x12, x13),0).
holds(adjacent(x12, x11),0).
holds(adjacent(x12, x7),0).
holds(adjacent(x13, x18),0).
holds(adjacent(x13, x14),0).
holds(adjacent(x13, x12),0).
holds(adjacent(x13, x8),0).
holds(adjacent(x14, x19),0).
holds(adjacent(x14, x13),0).
holds(adjacent(x14, x9),0).
holds(adjacent(x15, x20),0).
holds(adjacent(x15, x16),0).
holds(adjacent(x15, x10),0).
holds(adjacent(x16, x21),0).
holds(adjacent(x16, x17),0).
holds(adjacent(x16, x15),0).
holds(adjacent(x16, x11),0).
holds(adjacent(x17, x22),0).
holds(adjacent(x17, x18),0).
holds(adjacent(x17, x16),0).
holds(adjacent(x17, x12),0).
holds(adjacent(x18, x23),0).
holds(adjacent(x18, x19),0).
holds(adjacent(x18, x17),0).
holds(adjacent(x18, x13),0).
holds(adjacent(x19, x24),0).
holds(adjacent(x19, x18),0).
holds(adjacent(x19, x14),0).
holds(adjacent(x20, x15),0).
holds(adjacent(x20, x21),0).
holds(adjacent(x21, x16),0).
holds(adjacent(x21, x22),0).
holds(adjacent(x21, x20),0).
holds(adjacent(x22, x17),0).
holds(adjacent(x22, x23),0).
holds(adjacent(x22, x21),0).
holds(adjacent(x23, x18),0).
holds(adjacent(x23, x24),0).
holds(adjacent(x23, x22),0).
holds(adjacent(x24, x19),0).
holds(adjacent(x24, x23),0).

holds(at(r,x1),0).
goal(I) :- holds(at(r,x8),I).
