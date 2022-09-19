"""
This python file is used to assist the main jupyter file of simulating the paper - A Reinforcement Learning Based Network Scheduler For Deadline-Driven Data Transfers.
The paper compares different heurestics algorithms for scheduling with the Reinforcement Learning algorithm. This python file consists functions which are used for the
different heurestic algorithms, which are - Random Scheduling, Equal Scheduling and Earliest Deadline First Scheduling. Below is the list of functions in this file with
an overview of what the function does. Above each function, the specific explanation is provided for better understanding and readability of code.

1. equal_number_partition - Divide a number N into m equal partitions.
2. partition_number - Divide a number N into m random partitions.
3. generate_queue - Generate 2D array of rates, deadlines, values and file size of N sources.
4. edf_rate_scheduler - Assign complete bandwidth to the source with least deadline.
5. equal_rate_scheduler - Assign equal bandwidth to all sources.
6. random_rate_scheduler - Assign random bandwidth to all sources.
"""

import random
import math
import numpy as np

"""
equal_number_parition
1. Input - B,N
2. Function - Divides B equally in N parts.
            - Compute and store remainder of B and N
            - Assign rate equally by assigning B-reminder/N (remainder of B-remainder =0) to all elements in a list
            - For the remminder amount of values, randomly select indices and add 1 to the value of the element with remainder number of times.
3. Output - Returns list of equal parts

"""


def equal_number_partition(B,N):
    rem = B%N
    rate = [int((B-rem)/N) for i in range(0,N)]
    for i in range(0,rem):
        idx = random.randrange(0,N)
        rate[idx] = rate[idx]+1
    return rate

"""
random_number_partition
1. Input - N,m
2. Function - Divide N randomly into m integers
            - Create an empty list and assign a duplicate of number N
            - Run a for loop for m-1 times to assign valye
            - Generate a random number between the initial_value argument and N
            - Append the random number in the list and subtract it from the number N to ensure the range in which the sum of random numbers generated is within N.
            - Append the last element as the difference of N and the sum of the list.
3. Output - List of size m with randomly partitioned N
"""

def random_number_partition(N,m):
    parted = []
    L = N
    for i in range(0,m-1):
        k = random.randint(0,L)
        parted.append(k)
        L = L-k
    parted.append(N - sum(parted))
    return parted

"""
generate_queue
1. Input - Sum_Rmin, N
2. Function - Generate a 2D list of parameters of all sources.
            - The first parameter, filesize is generated with a uniform random distribution for all the sources.In this case, the range is between 10 and 50.
            - The second parameter which is the minimum rates required for the sources is computed by partitioning an argument to the function, Sum_Rmin to N sources.
            - The random_number_partition function is used in order to generate the list of paritions.
            - The third paramter is the deadline. It is calculated by dividing the generated filesize and the minimum rate for each source.
            - The deadlines are also rounded off to one decimal for efficient computations.
            - The fourth and the final parameter is the value, which is assigned 0 for all the sources as none of the sources have undergone processing.
3. Output - 2-D queue array of size (N,4)
"""

def generate_queue(Sum_Rmin,N):
    minRange = 10
    maxRange = 50
    F = [math.floor(random.uniform(minRange,maxRange)) for i in range(0,N)]
    Rmin = random_number_partition(Sum_Rmin,N)
    while any(elem==0 for elem in Rmin):
        Rmin = random_number_partition(Sum_Rmin,N)
    
    
    print(len(Rmin),len(F),N)
    d = [round(F[i]/Rmin[i],1) for i in range(0,N)]
    queue = np.zeros([N,4])
    v = [0 for i in range(0,N)]
    queue[:,0] = Rmin
    queue[:,1] = d
    queue[:,2] = F
    queue[:,3] = v
    return queue

"""
edf_rate_scheduler
1. Input - queue, N, B
2. Function - Assigning complete bandwidth to the source with the least deadline at every time slot. Accordingly updating the value of each source (1- before deadline;
            - 0 - after deadline)
            - 
3. Ouptut - queue
"""

def edf_rate_scheduler(queue,N,B):
    time = 0
    temp = queue[:,1]

    while sum(queue[:,2])!=0:
        for i in range(0,N):
            if queue[i,2]<0:
                queue[i,2] = 0
                temp[np.argmin(temp)] = temp[np.argmax(temp)]+1
                if queue[i,1]>time:
                    queue[i,3]=1
        
        pace = [B*int(elem==min(temp)) for elem in temp]
        if sum(queue[:,2])==0:
            break

        queue[:,2] = queue[:,2] - pace
        temp = temp-1

        time = time+1
    return queue

"""
equal_rate_scheduler
1. Input - queue, N, B
2. Function - 
2. Output - Updated queue
"""

def equal_rate_scheduler(queue,N,B):
    N_active = N
    time = 0
    while sum(queue[:,2])!=0:
        count = 0
        idx = []
        for i in range(0,N):
            if queue[i,2]<=0:
                queue[i,2] = 0
                count = count+1
                if queue[i,1]>time:
                    queue[i,3]=1
            else:
                idx.append(i)
        N_active = N-count
        if N_active==0:
            break
        pace = equal_number_partition(B,N_active)
        
        pace_upd = [0 for i in range(0,N)]
        
        for i in range(0,N_active):
            pace_upd[idx[i]] = pace[i]
        
        queue[:,2] = queue[:,2] - pace_upd
        time = time+1
    return queue

"""
random_rate_scheduler
1. Input - queue, N, B
2. Function - 
3. Output - Updated queue
"""

def random_rate_scheduler(queue, N, B):
    N_active = N
    time = 0
    while sum(queue[:,2])!=0:
        count = 0
        idx = []
        
        for i in range(0,N):
            if queue[i,2]<=0:
                queue[i,2] = 0
                count = count+1
                if queue[i,1]>time:
                    queue[i,3]=1
            else:
                idx.append(i)
        
        N_active = N-count
        if N_active==0:
            break
        pace = random_number_partition(B,N_active)
        
        
        pace_upd = [0 for i in range(0,N)]
        for i in range(0,N_active):
            pace_upd[idx[i]] = pace[i]
            
        queue[:,2] = queue[:,2] - pace_upd
        

        time = time+1
    return queue