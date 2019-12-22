#const n = 3.
sorts
#location = [x][0..24].
#robot = [r].
#inertial_fluent = at(#robot,#location).
#defined_fluent = adjacent(#location(X),#location(Y)):X!=Y.
#fluent = #inertial_fluent + #defined_fluent.
#action = move(#robot,#location(X)).
#step = 0..n.
predicates
holds(#fluent,#step).
occurs(#action,#step).
success().
goal(#step).
something_happened(#step).
rules
-holds(F,I) :- #defined_fluent(F),
               not holds(F,I).
-holds(at(R,L2),I) :- holds(at(R,L1),I),
                      L1 != L2.
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
holds(adjacent(x0, x1),0).
holds(adjacent(x0, x2),0).
holds(adjacent(x1, x0),0).
holds(adjacent(x1, x4),0).
holds(adjacent(x2, x0),0).
holds(adjacent(x2, x3),0).
holds(adjacent(x3, x2),0).
holds(adjacent(x3, x4),0).
holds(adjacent(x4, x1),0).
holds(adjacent(x4, x3),0).
holds(adjacent(x4, x5),0).
holds(adjacent(x5, x4),0).
holds(at(r,x0),0).
goal(I) :- holds(at(r,x5),I).
display
occurs.
