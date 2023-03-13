from sortedcontainers import SortedSet, SortedList


P = SortedSet(key=lambda x: x[1][0])

P.add([0, [1, 1]])
P.add([0, [5, 1]])
P.add([0, [2, 1]])
P.add([0, [0, 1]])
P.add([0, [10, 1]])

print(P.pop(0))
print(P.pop(0))
print(P.pop(0))
print(P.pop(0))
