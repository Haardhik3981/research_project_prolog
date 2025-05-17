from pyswip import Prolog

prolog = Prolog()
prolog.consult("simpsons_kb.pl")

print("1. Is Marge Bart’s mother?")
print(list(prolog.query("mother(marge, bart)")))

print("2. Is Homer Maggie’s father?")
print(list(prolog.query("father(homer, maggie)")))

print("3. Is Abe Bart’s grandparent?")
print(list(prolog.query("grandparent(abe, bart)")))

print("4. Is Bart Marge’s son?")
print(list(prolog.query("son(bart, marge)")))

print("5. Is Lisa Homer’s daughter?")
print(list(prolog.query("daughter(lisa, homer)")))

print("6. Who are Bart’s grandparents?")
print(list(prolog.query("grandparent(X, bart)")))

print("7. Who are Lisa’s parents?")
print(list(prolog.query("parent(X, lisa)")))

print("8. Who are the males?")
print(list(prolog.query("male(X)")))

print("9. Who are the females?")
print(list(prolog.query("female(X)")))