
% part 1 ok!!!!!

trigger(Percepts, goals(Goals_rest, Goals_truff)) :-
	split(Percepts, Goals_rest, Goals_truff).
split([], [], []).
split([restaurant(X, Y, S)|Tail], [goal(X, Y, S)|Goals_rest], Goals_truff) :-
	split(Tail, Goals_rest, Goals_truff).
split([truffle(X, Y, S)|Tail], Goals_rest, [goal(X, Y, S)|Goals_truff]) :-
	split(Tail, Goals_rest, Goals_truff).

% part 2 ok!!!!!!

is_in(Goal, [Head|_]) :-
	member(Goal, Head).
is_in(Goal, [Head|Tail]) :-
	not(member(Goal, Head)),
	is_in(Goal,Tail).

insert_goal(Goal, [Intention|Intentions], Belief, [Intention|Intentions1]) :-
	not(greater_than_plan(Goal, Intention, Belief)), !,
	insert_goal(Goal, Intentions, Belief, Intentions1).
insert_goal(Goal, Intentions, _, [[Goal, []]|Intentions]).

greater_than_plan(goal(_, _, S1), [goal(_, _, S2)|_], _) :-
	S1 > S2.
greater_than_plan(goal(X1, Y1, S1), [goal(X2, Y2, S2)|_], beliefs(at(X, Y), _)) :- 
	S1 = S2,
	distance((X, Y), (X1, Y1), Df),
	distance((X, Y), (X2, Y2), Ds),
	Df < Ds.

incorporate_goals(goals(Goals1, Goals2), Belief, intents(Intentions_rest, Intentions_truff), intents(Intentions_rest1, Intentions_truff1)) :-
	compute_intentions(Goals1, Belief, Intentions_rest, Intentions_rest1),
	compute_intentions(Goals2, Belief, Intentions_truff, Intentions_truff1).

compute_intentions([], _, Intentions, Intentions).
compute_intentions([Goal|Tail], Belief, Intentions, Intentions1) :-
	is_in(Goal, Intentions),
	compute_intentions(Tail, Belief, Intentions, Intentions1).
compute_intentions([Goal|Tail], Belief, Intentions, Intentions1) :-
	not(is_in(Goal, Intentions)),
	insert_goal(Goal, Intentions, Belief, UpdatedIntentions),
	compute_intentions(Tail, Belief, UpdatedIntentions, Intentions1).

% part3

% 0 is restaurant 1 is truffle

get_action(beliefs(at(X, Y), stock(T)), intents([[goal(Xg, Yg, S), []]|Tail], Goals_truff), intents([[goal(Xg, Yg, S), Plan]|Tail], Goals_truff), Action) :-
    T >= S,
    get_plan(X, Y, Xg, Yg, _, [Action|Plan], 0).

get_action(beliefs(_, stock(T)), intents([[goal(Xg, Yg, S), [Action|Plan]]|Tail], Goals_truff), intents([[goal(Xg, Yg, S), Plan]|Tail], Goals_truff), Action) :- 
    T >= S,
    applicable(Action).

get_action(beliefs(at(X, Y), stock(T)), intents([[goal(Xg, Yg, S), [Action|_]]|Tail], Goals_truff), intents([[goal(Xg, Yg, S), NewPlan]|Tail],Goals_truff), Action1) :-
    T >= S,
    not(applicable(Action)),
    get_plan(X, Y, Xg, Yg, _, [Action1|NewPlan], 0).

get_action(beliefs(at(X, Y), _), intents(Goals_rest, [[goal(Xg, Yg, S), []]|Tail]), intents(Goals_rest, [[goal(Xg, Yg, S), Plan]|Tail]), Action):-
    get_plan(X, Y, Xg, Yg, _, [Action|Plan], 1).

get_action(_, intents(Goals_rest, [[goal(Xg, Yg, S), [Action|Plan]]|Tail]), intents(Goals_rest, [[goal(Xg, Yg, S), Plan]|Tail]), Action):-
    applicable(Action).

get_action(beliefs(at(X, Y), _), intents(Goals_rest, [[goal(Xg, Yg, S), [Action|_]]|Tail]), intents(Goals_rest, [[goal(Xg, Yg, S), NewPlan]|Tail]), Action1):-
    not(applicable(Action)),
    get_plan(X, Y, Xg, Yg, _, [Action1|NewPlan], 1).

get_action(beliefs(at(X, Y), stock(_)), intents(Intentions_rest, []), intents(Intentions_rest, []), move(X, Y)).

get_plan(X, Y, X, Y, PartialPlan, NewPlan, Sign) :-
    Sign = 0,
    reverse([sell(X, Y)|PartialPlan], NewPlan);
    Sign = 1,
    reverse([pick(X, Y)|PartialPlan], NewPlan).

get_plan(X, Y, Xg, Yg, PartialPlan, NewPlan, Sign) :-
    get_move(X, Y, Xg, Yg,  move(Xn, Yn)),
    get_plan(Xn, Yn, Xg, Yg, [move(Xn, Yn)|PartialPlan], NewPlan, Sign).

get_move(X, Y, Xg, Yg, Action) :-
    Dx is X + 1,
    distance((Dx, Y), (Xg, Yg), D1),
    distance((X, Y), (Xg, Yg), D2),
    D1 < D2,
    Action = move(Dx, Y);
    Dx is X - 1,
    distance((Dx, Y), (Xg, Yg), D1),
    distance((X, Y), (Xg, Yg), D2),
    D1 < D2,
    Action = move(Dx, Y);
    Dy is Y + 1,
    distance((X, Dy), (Xg, Yg), D1),
    distance((X, Y), (Xg, Yg), D2),
    D1 < D2,
    Action = move(X, Dy);
    Dy is Y - 1,
    distance((X, Dy), (Xg, Yg), D1),
    distance((X, Y), (Xg, Yg), D2),
    D1 < D2,
    Action = move(X, Dy).

reverse(L, R) :-
    reverse(L, [], R).
reverse([], R, R).
reverse([H|T], PR, R) :-
    reverse(T, [H|PR], R).
    
% part4 ok!!!

update_beliefs(at(Xn, Yn), beliefs(at(_, _), stock(T)), beliefs(at(Xn, Yn), stock(T))).
update_beliefs(sold(Xn, Yn, Sn), beliefs(at(_, _), stock(T)), beliefs(at(Xn, Yn), stock(Tn))) :-
	Tn is T - Sn.
update_beliefs(picked(Xn, Yn, Sn), beliefs(at(_, _), stock(T)), beliefs(at(Xn, Yn), stock(Tn))) :-
	Tn is T + Sn.

% part5 ok!!!!

update_intentions(at(_, _), Intentions, Intentions).
update_intentions(sold(Xn, Yn, _), intents([[goal(Xn, Yn, _), _]|Intentions], Goals_truff), intents(Intentions, Goals_truff)).
update_intentions(picked(Xn, Yn, _), intents(Goals_rest, [[goal(Xn, Yn, _), _]|Intentions]), intents(Goals_rest, Intentions)).
