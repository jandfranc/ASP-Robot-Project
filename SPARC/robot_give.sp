#const n = 8.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sorts
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#robot = [r].

#person = [p][0..6].

#actor = #robot + #person.

#object = [o][0..5].

#hold_I_fluent = has(#actor(X),#object(Y)).

#inertial_fluent = #hold_I_fluent.

#fluent = #inertial_fluent.

#take_action = take(#robot(Z), #person(X), #object(Y)).

#give_action = give(#robot(Z), #person(X), #object(Y)).

#action = #take_action + #give_action.

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


%%Defines rules for actions:
%%if robot takes object from person at time I, robot has it at time I+1
%%if robot gives object at time I to person, person has it at time I+1
holds(has(R,O),I+1) :-  occurs(take(R,P,O),I),
                       holds(has(P,O),I),
                       -holds(has(R,O1),I),
                       O != O1.

-holds(has(P,O),I+1) :- occurs(take(R,P,O),I),
                       holds(has(P,O),I),
                       -holds(has(R,O1),I),
                       O != O1.

holds(has(P,O),I+1) :-  occurs(give(R,P,O),I),
                       holds(has(R,O),I),
                       -holds(has(P,O1),I),
                       P != R,
                       O != O1.

-holds(has(R,O),I+1) :- occurs(give(R,P,O),I),
                       holds(has(R,O),I),
                       -holds(has(P,O1),I),
                       P != R,
                       O != O1.

%%give cant happen if object not available

-occurs(give(R,P,O),I) :- -holds(has(R,O),I),
                           holds(has(P,O1),I).


-occurs(take(R,P,O),I) :- -holds(has(P,O),I),
                          holds(has(R,O1),I).

%%two actors can't have the same object
-holds(has(A,O),I) :- holds(has(B,O),I),
                      A != B.

%%An actor can't have two objects
-holds(has(A,O1),I+1) :- holds(has(A,O2),I),
                       O1 != O2.


%%Only one action occurs at a time.
:- occurs(A1,I),
   occurs(A2,I),
   A1 != A2.


%%Goal must be achieved
:- not success.


%%Success occurs if goal true at time I
success :- goal(I).


%%If goal not achieved, an action may happen
occurs(A,I) | -occurs(A,I) :- not goal(I).


%%if an action occured, something_happened
something_happened(I) :- occurs(A,I).


%%Something must happen at each time step, if goal isnt achieved
:- goal(I), goal(I-1),
   J < I,
   not something_happened(J).


%% CWA for Inertial Fluents

holds(F,I+1) :- #inertial_fluent(F),
                holds(F,I),
                not -holds(F,I+1).

-holds(F,I+1) :- #inertial_fluent(F),
                 -holds(F,I),
                 not holds(F,I+1).

%% CWA for Actions
-occurs(A,I) :- not occurs(A,I).

%%%%%%%%%%%%%%%%%%
%%Initial setup
%%%%%%%%%%%%%%%%%%
holds(has(p0, o0),0).
holds(has(p1, o1),0).
holds(has(p2, o2),0).
holds(has(p3, o3),0).
holds(has(p4, o4),0).
holds(has(p5, o5),0).


%%%%%%%%%%%%%%%%%%
%%Goal
%%%%%%%%%%%%%%%%%%
goal(I) :- holds(has(p1,o1),I),
           holds(has(p2,o3),I),
           holds(has(p3,o5),I),
           holds(has(p4,o2),I),
           holds(has(p6,o4),I).
goal(I+1) :- goal(I).

%%%%%%%%%%%%%%%%%%
display
%%%%%%%%%%%%%%%%%%
occurs.
