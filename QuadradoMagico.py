#algoritmo ainda não otimizado para quadrados de ordem maior que 3

import random

fitnessValue = 0
order = 3
answerOrder = order + 2
popSize = 50
indSize = order
mutRate = 0.1 
bestFit = 0

## Quadrado Magico ##

def is_valid_move(square, row, col, num):
    # Verifica se o número já existe
    while col < order:
        if num in square[row] or num in [square[i][col] for i in range(len(square))]:
            print(f"movimento invalido, numero ja inserido")
            return False 
        col +=1 

    return True

def print_magic_square(square):
    for row in square:
        print('\t'.join(map(str, row)))

def fill_magic_square(ind):
    square = [[0] * answerOrder for _ in range(answerOrder)]
    row, col = 1, 1
    i=0
    while row < order+1:
        col = 1
        while col < order+1:            
            if is_valid_move(square, row, col, ind[i]):
                square[row][col] = ind[i]
                col += 1
                i += 1
        row += 1
    return square

def sumCol(square, order):
    col, row = 1, 1
    for col in range(order):
        total_sum = 0
        for row in range(order):
            total_sum += square[row+1][col+1]
        square[order+1][col+1] = total_sum
        square[0][col+1] = total_sum
    return square

def sumRow(square, order):
    for row in range(order):
        total_sum = 0
        for col in range(order):
            total_sum += square[row+1][col+1]
        square[row+1][order+1] = total_sum
        square[row+1][0] = total_sum
    return square

def sumDia(square, order):
    total_sum1 = 0
    total_sum2 = 0
    for i in range(order):
        total_sum1 += square[i+1][i+1]
        total_sum2 += square[i+1][order-i]
    square[0][0]= total_sum1
    square[order+1][order+1]= total_sum1
    square[0][order+1]= total_sum2
    square[order+1][0]= total_sum2
    return square

## Algoritmo Genetico ##

def evalFit(square, answerOrder, numInput):
    array = [int(num) for num in numInput]
    goal = int(sum(array)/(answerOrder-2))
    
    achievedGoal = 0

    for i in range(answerOrder):
        if(square[0][i] == goal):
            achievedGoal += 1
    for i in range(answerOrder-2):
        if(square[i+1][0] == goal):
            achievedGoal += 1
            
    return achievedGoal/((answerOrder-2)*2+2)

def createInd(order):
    avaliableNum = list(range(1, ((order*order)+1)))
    ind = random.sample(avaliableNum, order*order)
    return ind

def createPop(popSize, indSize):
    return [createInd(indSize) for _ in range(popSize)]

def selection(duplinhas):
    return [list(vetor) for vetor, _ in sorted(duplinhas.items(), key=lambda item: item[1], reverse=True)]

def crossover(ind1, ind2):
    cutPoint = random.randint(1, len(ind1) - 1)
    son1 = ind1[:cutPoint] + ind2[cutPoint:]
    son2 = ind2[:cutPoint] + ind1[cutPoint:]
    checkComb(son1)
    checkComb(son2)
    return son1, son2

def checkComb(ind):
    checkNum = set()
    for i in range(len(ind)):
        if ind[i] in checkNum:
            newNum = ind[i]
            while newNum in checkNum:
                newNum = (newNum % (order*order)) + 1
            ind[i] = newNum
        checkNum.add(ind[i])
    return ind

def mutation(desc, popSize):
    for i in range(popSize):
         if random.random() < mutRate:
            pos1, pos2, pos3, pos4 = random.sample(range(order*order), 4)
            desc[i][pos1], desc[i][pos2] = desc[i][pos2], desc[i][pos1]
            ## desc[i][pos3], desc[i][pos4] = desc[i][pos4], desc[i][pos3]

def sumAll(ind):
    magic_square = fill_magic_square(ind)
    sumCol(magic_square, order)
    sumRow(magic_square, order)
    sumDia(magic_square, order)
    return evalFit(magic_square, answerOrder, ind)

## Main Algoritmo Genetico ##

pop = createPop(popSize, indSize)

while bestFit < 1:

    duplinhas = {}
    for x in pop:
        if(len(x) == order*order):
            duplinhas[tuple(x)] = sumAll(x)
    pop = selection(duplinhas)
    bestFit = sumAll(pop[0])
    bestestind = pop[0]
    bestInd = pop[:popSize // 2]

    desc = []
    while len(desc) < popSize:
        dad = random.choice(bestInd)
        mom = random.choice(bestInd)
        son1, son2 = crossover(dad, mom)
        desc.append(son1)
        desc.append(son2)
    mutation(desc, popSize)
    pop = desc

print("Melhor Indivíduo:", bestestind)
print("Melhor Aptidão:", bestFit)

magic_square = fill_magic_square(bestestind)
sumCol(magic_square, order)
sumRow(magic_square, order)
sumDia(magic_square, order)
print_magic_square(magic_square)