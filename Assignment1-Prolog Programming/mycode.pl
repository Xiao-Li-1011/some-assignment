% Xiao LI
% z5139219
% COMP9414 Artificial Intelligence
% Assignment 1 :Prolog Programming


% Q1: weird_sum function,
% use three functions to judge the number
% use recursion to get each element in the input list

change_number(Number, Result):-
	Number >= 6,
	Result is Number * Number.

change_number(Number, Result):-
	Number =< 2,
	Result is 0 - abs(Number).
change_number(Number, Reasult):-
	Number > 2,
	Number < 6,
	Reasult is 0.

% these three change_number functions are used to judge the number
% if number >= 6 then number ** 2
% if number =< 2 then -|number|
% if number > 2 and number< 6 then 0

weird_sum([], 0).
weird_sum([Head|Tail], Result):-
	weird_sum(Tail, NotFinish),
	change_number(Head,Number),
	Result is Number + NotFinish.

% use recursion to get the number from the input list

% Q2:same name in family.pl
% who have the same name is:
% A is B's father or male ancestors also B is A's
% A and B have the same male ancestors

descendant(Person, Descendant):-
	parent(Person, Descendant).
descendant(Person, Descendant):-
	parent(Person, Child), descendant(Child, Descendant).

% to confirm whether the Person is the ancestor of the Descendant

same_name(Person1, Person2):-
	male(Person1),
	parent(Person1, Person2).

% the Person1 is the Person2's father so they have the same name

same_name(Person1, Person2):-
	parent(Person1, Child),
	male(Person1),
	same_name(Child, Person2).

% the Person1 is the Person2's male ancestor so they have the same name

same_name(Person1, Person2):-
	male(Person2),
	parent(Person2, Person1).
same_name(Person1,Person2):-
	parent(Person2, Parent),
	male(Parent),
	same_name(Person1,Parent).

% be the same as the two functions above Person2 is the Person1's
% ancestor so they have the same name

same_name(Person1, Person2):-
	descendant(Ancestor,Person1),
	male(Ancestor),
	descendant(Ancestor,Person2).

% Person1 and Person2 have the same male ancestors so they have the same
% name

% Q3:put log of each number in numberlist to loglist
% use recusion to get each element in the input list and get their log
% when input negtive number or zero the system will raise error

log_table([],[]).
log_table([H|T],[[H,Result]|R]):-
	Result is log(H),
	log_table(T,R).

% use recursion to get each element's log

% Q4: divide the list by the even and odd number
% start from the last element in the input list
% the get the second last element and compare with the last element
% if is both evens or odds put them togther
% if not same type append a new element into the result list
% then ...
% while the first element in the input list

both_even_or_odd(Number1,Number2):-
	Remainder1 is Number1 mod 2,
	Remainder2 is Number2 mod 2,
	Remainder1 = Remainder2.

% check the Number1 and Number2 are both even or both odd

paruns([H|T],Result):-
	paruns(T,NotFinish),
	NotFinish = [[H1|T1]|OtherT],
	both_even_or_odd(H,H1),
	append([H],[H1|T1],NotFinish1),
	append([NotFinish1],OtherT,Result).

% judge the first element in the result and input list, they are both
% evens or odds then put them  togther in one element in the result

paruns([H|T],Result):-
	paruns(T,NotFinish),
	NotFinish = [[H1|_T1]|_OtherT],
	not(both_even_or_odd(H,H1)),
	append([[H]],NotFinish,Result).

% judge the first element in the result and input list, they are one is
% even and one is odd then the result get a new element contain the
% input number

paruns([H],[[H]]).

% this function is for control the finish reason, if only one element in
% the input list, then put this element into the result list

% Q5 heap binary tree

% use the recursion to find the binary tree's empty branch for the end
% then to confirm if the number 'parents' number is greater than
% 'children' number

is_heap(empty).
is_heap(tree(L,Num,R)):-
	is_heap(L),is_heap(R),
	(L = tree(__,LNum,__) *-> K @=< LNum;true),
	(R = tree(__,RNum,__) *-> K @=< RNum;true).








