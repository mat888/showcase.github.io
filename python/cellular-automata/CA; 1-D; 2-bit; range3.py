import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import numpy as np 
print('-------------------START--------------------')


def auto(width, iterate):

    dims = (iterate, width) #Array of rows is created, each row is an array.
    array = np.zeros(dims, dtype=int) #creates matrix of integer zeros x,y ; width, iterate
    array[0][len(array[0]) // 2] = 1  #Places the starting 'on' cell in the center of first row
    #print(array)
    for i in range(1, iterate):    #cycles through each vertical array
        for j in range(0, width):  #cycles through each entry horizantally for array[i]
            array[i][j] = enforce(array[i-1], array[i], j)
    #print(array)
    return array

def enforce(current, next, ind): #'ind'ex
    cLen = len(current)
    above = [current[((ind-1)%(cLen))], current[ind], current[((ind+1)%(cLen))]]
    return rules(above)

def rules(n):
    
    #The naming patterns indicate visually how a cell will determine its state.
    #The cell will look at the cell directly above it and the two cells to each side.
    #From left to right, the cell will match the layout above to one of the eight possible keys.
    # 'bwb' for example will tell the cell its state if it sees 'black white black' above it.

    www = [0,0,0] ; r3 = 0
    wwb = [0,0,1] ; r4 = 1
    wbw = [0,1,0] ; r6 = 1
    wbb = [0,1,1] ; r5 = 0
    bww = [1,0,0] ; r2 = 1
    bwb = [1,0,1] ; r7 = 0
    bbw = [1,1,0] ; r1 = 1
    bbb = [1,1,1] ; r0 = 0

    array = [bbb,bbw,bww,www,wwb,wbb,wbw,bwb]
    ruleArray = [r0, r1, r2, r3, r4, r5, r6, r7]
    if (n == 0):
        p = "".join(map(str, ruleArray))
        #print('//////////////////////////')
        #print(str(p))
        return str(p)
    for i in range (0, 8):
        if (n == array[i]):
            return ruleArray[i]
    return("Error: The state above the cell was not listed")

# print(n[(m-1)%9])
# print(n[m%9])
# print(n[(m+1)%9])
#Display matrix
#auto(width, iterations)
def plot(width, iterate):
    #print(pattern(auto(width, iterate))[0])
    print("Number of unique lines")
    print(pattern(auto(width, iterate))[1])
    plt.style.use('dark_background')
    plt.matshow(auto(width, iterate))
    plt.title(rules(0))
    #fig = plt.matshow(auto(237, 500))
    plt.xlabel('Iterations')
    plt.show()

#plt.matshow(auto(237, 500))
#plt.show()

def pattern(x):
    switch = 0 #***
    arr = x
    match = []

    for i in range(0, len(x)):
        switch = 0

        for j in range(0, len(match)):

            if (np.array_equal(arr[i], arr[match[j][0]])):
                match[j].append(i)
                switch = 1 #***Keeps match from appending i twice
                break

        if (switch == 0): #***
            match.append([i])

    results = [match, len(match)]
    #print('Pattern-------------------------')
    #print(match)
    #print('Unique lines:')
    #print(len(match))
    return results

def patternCheck(width, iterate):
    arr = []
    for i in range(1, width):
        arr.append([i,pattern(auto(i, iterate))[1]])
    print(arr)
    return arr

def patternCheckIterate(width, firstIterate, lastIterate): #first/last iterate to check
    arr = []
    for i in range(firstIterate, lastIterate):
        entry = pattern(auto(width, i))[1]
        if (entry != i):
            arr.append([i, pattern(auto(width, i))[1]])
        
    print(arr)
    return arr

def listSum(width, iterate):
    arr = auto(width, iterate)
    results = [None] * iterate
    for i in range(0, len(arr)):
        results[i] = [i+1,(sum(arr[i]))]
    print(results)

def listBinary(width, iterate): #converts each iteration into a binary number
    arr = auto(width, iterate)
    bins = [None] * iterate
    for i in range (0, iterate):
        num = 0
        for j in range(0, width):
            num += (arr[i][j] * 2) ** (j)
        bins[i] = num
    print(bins)
    return(bins)

def listDiff(x):
    arr = [None] * (len(x) - 1)
    for i in range(0, len(x) - 1):
        arr[i] = x[i+1] / x[i]
    print(arr)

#patternCheckIterate(14, 1100, 1300)
#patternCheck(14, 1000)
listSum(128, 64)
listBinary(16, 8)
#listDiff(listBinary(50,25))
plot(42, 350)


print('completed')
# def samplemat(dims):
#     """Make a matrix with all zeroes and increasing elements on the diagonal"""
#     aa = np.zeros(dims)
#     for i in range(min(dims)):
#         aa[i, i] = 1
#     return aa

# Display matrix
# plt.matshow(samplemat((15,15)))

# plt.show()
