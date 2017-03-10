from expression.utils import *

fin = open("proof1.in", "r")
fout = open("proof1.out", "w")

line = fin.readline().rstrip()
print(line, file=fout)
list = line.split("|-")
assumptions = {}
if len(list) == 2:
    line = list[0].split(",")
    for i in range(len(line)):
        if line[i] != "":
            assumptions[parseExp(line[i])] = i + 1
else:
    line = list

expressions = {}
list = []
line_number = 1
while True:
    line = fin.readline().rstrip()
    if not line:
        break

    temp = parseExp(line)

    state = 0
    num = -1

    # предположение ? 
    if temp in assumptions:
        state = 1
        num = assumptions[temp]

    # аксиома ?
    if state == 0:
        for i in range(len(axiomsExp)):
            if is_axiom(temp, axiomsExp[i]):
                state = 2
                num = i + 1
                break

    # Modus Ponens ?
    if state == 0:
        for i in range(len(list) - 1, -1, -1):
            tmp = Implication(list[i], temp)
            if tmp in expressions:
                state = 3
                num = expressions[list[i]], expressions[tmp]
                break

    print("(", line_number, ") ", line, " ", end="", file=fout)
    if state == 0:
        #не доказано
        print("(Not proven)", sep="", file=fout)
    elif state == 1:
        #предположение
        print("(Guess ", num, ")", sep="", file=fout)
    elif state == 2:
        print("(Sch. ax. ", num, ")", sep="", file=fout)
    else:
        first, second = num
        print("(M.P. ", first, ", ", second, ")", sep="", file=fout)

    if state != 0:
        expressions[temp] = line_number
        list.append(temp)
    line_number += 1


fin.close()
fout.close()
