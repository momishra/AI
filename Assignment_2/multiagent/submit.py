import time
#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation

keyVal = dict()

def BT(L, M): # iterative backtracking
    pairs = dict()
    origL = L
    start_time = 0
    while(L > 0):
        start_time = time.time()
        golombArray = []
        i =0
        if (L == 0):
            golombArray.append(0)
        else:
            while(i <= L and len(golombArray) < M):
                golombArray.append(i)
                if len(golombArray) != 1:
                    currDiffList = []
                    flag = False
                    # find the difference between all the possible pairs and check if that difference is repeating
                    for j in range(len(golombArray) -1):
                        currVal = golombArray[len(golombArray)-1]
                        k = j+1
                        while(k < len(golombArray)):
                            diff = abs(golombArray[j] - golombArray[k])
                            if diff not in currDiffList and diff != 0:
                                currDiffList.append(diff)
                            else:
                                flag = True
                                break
                            if (flag == True) : # to exit the outer loop too
                                break
                            k += 1
                    if(flag == True):
                        if(i == L):
                            golombArray.remove(currVal)
                            i = golombArray[-1] + 1
                            golombArray[-1] = i
                        else:
                            i = golombArray[-1]
                            golombArray.remove(currVal)
                if(i == L and len(golombArray) < M):
                    golombArray = golombArray[:-1]
                    i = golombArray[-1]+1
                    golombArray[-1] = i

                i += 1

        if (len(golombArray) < M):
            break
        else:
            pairs[L] = golombArray
        L -= 1

    if len(pairs) > 0:
        # now for finding optimal solution check for the golombArray having min last element
        min = origL
        marks = pairs[min]
        for key,val in pairs.items():
            if val[-1] < min:
                min = val[-1]
                marks = val
        print "BT:: Optimal Solution for given ruler for min L ",min,marks
        #print "BT:: Time taken is %s seconds" % (time.time() - start_time)
        return min, marks
    else:
        print "BT:: Solution does not exist for given ruler"
        return -1,[]

#Your backtracking+Forward checking function implementation
def FC(L, M):
    origL = L
    pairs = dict()
    start_time = 0
    while(L > 0):
        start_time = time.time()
        golombArray = []
        diffList = []
        remValidVals = []
        i=0
        while (i <= L):
            if (len(golombArray) == 0):
                golombArray.append(i)
                diffList.append(i)
            else:
                remValidVals,diffList = doForwardCheck(golombArray,i,diffList,L,M)
                if len(remValidVals) != 0: # add a check of M and length
                    golombArray.append(i)

                if(i==L and len(golombArray)<M):
                    i = golombArray[-1]
                    golombArray.remove(i)
                    # get the difference list of last valid value or calculate differrnce again
                    try:
                        for v in keyVal[i]:
                            if v in diffList:
                                diffList.remove(v)
                    except KeyError:
                        print
            i += 1

        if (len(golombArray) < M):
            break
        else:
            pairs[L] = golombArray
        L -= 1

    if len(pairs) > 0:
        min = origL
        marks = pairs[min]
        for key, val in pairs.items():
            if val[-1] < min:
                min = val[-1]
                marks = val
        print "FC:: Optimal Solution for given ruler for min L ", min, marks
        #print "FC:: Time taken is %s seconds" % (time.time() - start_time)
        return min, marks
    else:
        print "FC:: Solution does not exist for given ruler"
        return -1, []


def doForwardCheck(golombArray,i,difference,L,M):
    # add a condition for i==L and diffList is greater than 0 then .. return i as validVal
    remVals = []
    remVals = range(i,L+1)
    marks = list(golombArray)
    marks.append(i) # extending the partial solution
    diffList = diffConstraint(marks,difference) # like for 3 new differences are there but it will not satisfy forward check thing
    if(len(diffList) > 0):
        newList = list(diffList)
        newList.extend(difference) # instead of extending it here
        for k in newList:
            for j in marks:
                val = k+j
                if val in remVals:
                    remVals.remove(val)

        if(i == L and len(golombArray) == (M - 1)):
            remVals.append(i)

        if(len(remVals) > 0):
            return remVals,newList
        else:
            return [],difference
    else:
        return [],difference

def diffConstraint(marks,difference):
    global keyVal
    diffList = []
    flag = False
    currVal = marks[-1]
    for j in range(len(marks) - 1):
        diff = abs(currVal - marks[j])
        if diff not in difference:
            diffList.append(diff)
        else:
            flag = True
            break

    if(flag == True):
        return []
    else:
        keyVal[currVal] = diffList
        return diffList

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]


#Testcases for BT and FC
BT(1,1)
FC(1,1)
#BT(6,4)
#FC(6,4)
BT(15,5)
FC(15,5)
#BT(17,6)
#FC(17,6)
#BT(25,7)
#FC(25,7)
BT(40,8)
FC(40,8)
#BT(44,9)
#FC(44,9)
#BT(55,10)
#FC(55,10)