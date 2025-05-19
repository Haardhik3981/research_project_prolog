# simpsons_datalog.py

from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('parent, male, female, mother, father, son, daughter, grandparent, X, Y, Z')

# Facts
+ parent('homer', 'bart')
+ parent('homer', 'lisa')
+ parent('homer', 'maggie')
+ parent('marge', 'bart')
+ parent('marge', 'lisa')
+ parent('marge', 'maggie')
+ parent('abe', 'homer')
+ parent('mona', 'homer')

+ male('homer')
+ male('bart')
+ male('abe')

+ female('marge')
+ female('lisa')
+ female('maggie')
+ female('mona')

# Rules
mother(X, Y) <= parent(X, Y) & female(X)
father(X, Y) <= parent(X, Y) & male(X)
son(X, Y)    <= parent(Y, X) & male(X)
daughter(X, Y) <= parent(Y, X) & female(X)
grandparent(X, Y) <= parent(X, Z) & parent(Z, Y)

# Example queries
print("Who are Bart's grandparents?")
print(grandparent(X, 'bart'))

print("Who is Lisa's mother?")
print(mother(X, 'lisa'))

print("Who are Maggie's siblings?")
print(parent(X, 'maggie') & parent(X, Y))

print("All sons of Marge:")
print(son(X, 'marge'))

print("All daughters of Homer:")
print(daughter(X, 'homer'))