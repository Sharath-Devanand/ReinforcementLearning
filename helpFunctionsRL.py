import itertools
import operator
import random
import numpy as np

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

def reward2(queue,action,time):
    N = queue.shape[0]
    drem = []
    for i in range(0,N):
        drem.append(queue[i][1]-time)
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

def actionByAgent(qTable,p_exp,currentState,allPossibleStates,allPossibleActions,actions):
    fillPercentage = np.count_nonzero(qTable)/(np.shape(qTable)[0]*np.shape(qTable)[1])
            
    if fillPercentage<=1-p_exp:
        currentActionIndex = random.randint(0,len(actions)-1)
    else:
        L = len(currentState)
        indexCurrentState = allPossibleStates.index(tuple(currentState))
        listOfActionIndices = [i for i in range(len(allPossibleActions)) if len(allPossibleActions[i])==L]
        currentActionIndex = np.argmax(qTable[indexCurrentState][listOfActionIndices],axis=0)
    return currentActionIndex

## Deleting Nodes with negative rates from the index values given from checkIfOneNegative function
## Check deadline of completed nodes with time and update value

def deleteElement(queue,nextState,indices,time):
    listNextState = list(nextState)
    for j in list(reversed(indices)):
        del listNextState[j]
        if queue[j,1]<time:
            queue[j,3]=1
    nextState = tuple(listNextState)
    return [nextState,queue]

def randomPolicy(allPossibleStates,allPossibleActions):
    L1 = len(allPossibleStates)
    L2 = len(allPossibleActions)
    policyTable = np.zeros([L1,L2])
    for i in range(L1):
        matchIndices = []
        for j in range(L2):
            if len(allPossibleStates[i])==len(allPossibleActions[j]):
                matchIndices.append(j)
        L = len(matchIndices)
        for k in matchIndices:
            policyTable[i,k] = round(1/L,2)
    return policyTable