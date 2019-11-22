#const n = 3.

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



display
occurs.
