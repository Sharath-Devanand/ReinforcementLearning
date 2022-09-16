import itertools
import operator
import numpy as np
import random

def allStates(r,n):
   size = n + r - 1
   for indices in itertools.combinations(range(size), n-1):
       starts = [0] + [index+1 for index in indices]
       stops = indices + (size,)
       yield tuple(map(operator.sub, stops, starts))

def everyState(N,r):
    everyStateList = []
    for i in range(0,r+1):
        for j in range(1,N+1):
            stateForOne  = list(allStates(i,j))
            everyStateList = everyStateList + stateForOne
    return everyStateList

def everyAction(N,r):
    everyActionList = []
    for i in range(1,r+1):
        stateForOne  = list(allStates(N,i))
        everyActionList = everyActionList + stateForOne
    return everyActionList

def reward(state,action):
    N = len(state)
    drem = []
    for i in range(0,N):
        drem.append((state[i]-action[i]))
    drem_max = max(drem)
    SIR = []
    for i in range(0,N):
        SIR.append((drem_max-drem[i])*action[i])
    rewardValue = sum(SIR)
    return rewardValue

def checkIfOneNegative(someList):
    L = len(someList)
    indices = []
    for i in range(0,L):
        if someList[i]<=0:
            indices.append(i)
    if len(indices)>0:
        binary = True
    else:
        binary = False
    return [binary, indices]

def checkIfAllNegative(someList):
    L = len(someList)
    count = 0
    for i in range(0,L):
        if someList[i]<=0:
            count = count+1
    if count==L:
        binary = False
    else:
        binary = True
    return binary

"""
def temperoaryName2(qTable,p_exp, allPossibleStates, actions,i):
    check3 = np.count_nonzero(qTable)/(np.shape(qTable[0])*np.shape(qTable[1]))
    
    if check3<=1-p_exp[i]:
        currentActionIndex = random.randint(0,len(actions)-1)
    else:
        #print(p_exp[i])
        indexCurrentState = allPossibleStates.index(tuple(currentState))
        maxValue = max(qTable[indexCurrentState][:])
        currentACtionIndex = np.where(qTable==maxValue)[1][0]
        #print(currentACtionIndex)

    rewardAction = np.array(actions[currentActionIndex])
    nextState = np.array(currentState) - rewardAction

    temperoryName1()

    currentState = nextState
    
    
    check = checkIfAllNegative(currentState)

    time = time+1


def temperoryName1(nextState, queue, time, rewardAction, allPossibleStates, currentActionIndex, qTable, beta, N,B):
    check2 = checkIfOneNegative(nextState)
    if check2[0]:
        listCurrentState = list(nextState)
        enum = enumerate(listCurrentState)
        for j in list(reversed(check2[1])):
            del listCurrentState[j]
            if queue[j,1]<time:
                queue[j,3]=1

        nextState = tuple(listCurrentState)

        currentState = nextState

        check = checkIfAllNegative(nextState)
        if check:
            update = reward(nextState, rewardAction)
            xCoord = allPossibleStates.index(tuple(nextState))
            qTable[xCoord, currentActionIndex] += beta*update
        
        M = N - len(check2[1])
        if M==0:
            return
        actions = list(allStates(B,M))
"""
    