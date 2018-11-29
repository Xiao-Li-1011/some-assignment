% Program:  family.pl
% Source:   Prolog
%
% Purpose:  This is the sample program for the Prolog Lab in COMP9414/9814/3411.
%           It is a simple Prolog program to demonstrate how prolog works.
%           See lab.html for a full description.
%
% History:  Original code by Barry Drake


% parent(Parent, Child)
%
parent(albert, jim).
parent(albert, peter).
parent(jim, brian).
parent(john, darren).
parent(peter, lee).
parent(peter, sandra).
parent(peter, james).
parent(peter, kate).
parent(peter, kyle).
parent(brian, jenny).
parent(irene, jim).
parent(irene, peter).
parent(pat, brian).
parent(pat, darren).
parent(amanda, jenny).


% female(Person)
%
female(irene).
female(pat).
female(lee).
female(sandra).
female(jenny).
female(amanda).
female(kate).

% male(Person)
%
male(albert).
male(jim).
male(peter).
male(brian).
male(john).
male(darren).
male(james).
male(kyle).


% yearOfBirth(Person, Year).
%
yearOfBirth(irene, 1923).
yearOfBirth(pat, 1954).
yearOfBirth(lee, 1970).
yearOfBirth(sandra, 1973).
yearOfBirth(jenny, 2004).
yearOfBirth(amanda, 1979).
yearOfBirth(albert, 1926).
yearOfBirth(jim, 1949).
yearOfBirth(peter, 1945).
yearOfBirth(brian, 1974).
yearOfBirth(john, 1955).
yearOfBirth(darren, 1976).
yearOfBirth(james, 1969).
yearOfBirth(kate, 1975).
yearOfBirth(kyle, 1976).

%def grandparent
%
grandparent(Grandparent, Grandchild):-
parent(Grandparent, Child), parent(Child, Grandchild).

%older(Person1, Person2):- Person1 is older than Person2
%
older(Person1, Person2):-
yearOfBirth(Person1, Year1), yearOfBirth(Person2, Year2), Year2 > Year1.

%Child1 and Child2 are brothers or sisters
%
siblings(Child1, Child2):-
parent(Parent1, Child1), parent(Parent2, Child2), Parent1 == Parent2, Child1 \= Child2.

%older brothers
olderBrother(Brother,Person):-
siblings(Brother,Person), male(Brother), yearOfBirth(Brother, Year1), yearOfBirth(Person, Year2), Year1 < Year2.

%descendant
descendant(Person, Descendant):-
parent(Person, Descendant).
descendant(Person, Descendant):-
parent(Person, Child), descendant(Child, Descendant).

%ancestor
ancestor(Person, Ancestor):-
parent(Ancestor, Person).
ancestor(Person, Ancestor):-
parent(Ancestor, Parent), ancestor(Person, Parent).

%same_family name
same_name(Person1, Person2):-
male(Person1),
parent(Person1, Person2).
same_name(Person1, Person2):-
parent(Person1, Child),
male(Person1),
same_name(Child, Person2).

same_name(Person1, Person2):-
male(Person2),
parent(Person2, Person1).
same_name(Person1,Person2):-
parent(Person2, Parent),
male(Parent),
same_name(Person1,Parent).


same_name(Person1, Person2):-
descendant(Ancestor,Person1),
male(Ancestor),
descendant(Ancestor,Person2).



