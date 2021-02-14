import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import numpy as np
import pickle
print('-------------------START--------------------')


def auto(width, iterate):

    dims = (iterate, width) #Array of rows is created, each row is an array.
    array = np.zeros(dims, dtype=int) #creates matrix of integer zeros x,y ; width, iterate
    array[0][len(array[0]) // 2] = 1  #Places the starting 'activated' cell in the center of first row

    for row, new_row in zip(array, array[1:]):    #cycles through each row, and the row below it
        for column_index, column in enumerate(new_row):  #cycles through each entry horizantally for array[i]
            # print('array[new_row], column_index \n', new_row, column_index)
            new_row[column_index] = enforce(row, column_index)

    return array

def left_shift(matrix_in): #takes completed automaton result matrix and shifts it the the left side
                           #rather than being centered
    matrix = matrix_in
    for row_index, row in enumerate(matrix):
        leftmost = 0
        limit = len(row); counter = 0
        while(row[leftmost] == 0 and counter < limit):
            row = np.append(row[1:], 0)
            counter += 1
        matrix[row_index] = row
    return matrix

def right_shift(matrix_in): #takes completed automaton result matrix and shifts it the the right side
                            #rather than being centered
    matrix = matrix_in
    for row_index, row in enumerate(matrix):
        rightmost = len(row) - 1
        limit = len(row); counter = 0
        while(row[rightmost] == 0 and counter < limit):
            row = np.append(0, row[:-1])
            counter += 1
        matrix[row_index] = row
    return matrix

def up_shift_dep(matrix_in):
    matrix = matrix_in
    center = np.where(matrix[0] == 1)[0]; center = int(center)
    #finds index of initial activated cell in first row
    for row_index, row in enumerate(matrix[1:]):
        print('*****row index*****: ', row_index)
        max_shift = row_index
        current_shift = 0
        while(current_shift <= max_shift):
            print('current_shift: ', current_shift)
            print('row_index:     ', row_index)
            print('center:        ', center)
            matrix[row_index - current_shift][center + row_index] = row[center + current_shift]
            matrix[row_index - current_shift][center - row_index] = row[center - current_shift]
            current_shift += 1
    return matrix

def up_shift(matrix_in): #very slow, see if np has builtins for handling column shifting

    matrix = matrix_in
    row_length = len(matrix[0])
    column_length = len(matrix)

    for row_index in range(row_length):

        topmost = 0
        limit = column_length; counter = 0

        while (matrix[topmost][row_index] == 0 and counter < limit):

            for column_index in range(1, column_length):

                matrix[column_index - 1][row_index] = matrix[column_index][row_index]
                matrix[column_index][row_index] = 0

            counter += 1

    return matrix

def enforce(current, ind): #'ind'ex
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
    wbb = [0,1,1] ; r5 = 1
    bww = [1,0,0] ; r2 = 1
    bwb = [1,0,1] ; r7 = 0
    bbw = [1,1,0] ; r1 = 0
    bbb = [1,1,1] ; r0 = 0

    array = [bbb,bbw,bww,www,wwb,wbb,wbw,bwb]
    ruleArray = [r0, r1, r2, r3, r4, r5, r6, r7]
    # print('n is', n)
    if (n == 0):
        p = "".join(map(str, ruleArray))
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
def plot(width, iterate, filename):

    plt.matshow(auto(width, iterate))
    plt.title(rules(0))
    #fig = plt.matshow(auto(237, 500))
    plt.xlabel('Iterations')
    plt.savefig(filename, dpi=1400)
    # plt.show()

def plot_left(width, iterate, filename):
    auto_center = auto(width, iterate)
    auto_left = left_shift(auto_center)
    plt.matshow(auto_left)
    plt.title(rules(0))
    #fig = plt.matshow(auto(237, 500))
    plt.xlabel('Iterations')
    plt.savefig(filename, dpi=1400)

def plot_right(width, iterate, filename):
    auto_center = auto(width, iterate)
    auto_right = right_shift(auto_center)
    plt.matshow(auto_right)
    plt.title(rules(0))
    #fig = plt.matshow(auto(237, 500))
    plt.xlabel('Iterations')
    plt.savefig(filename, dpi=1400)

def plot_matrix(matrix_in, filename, dpi):
    plt.matshow(matrix_in)
    plt.title(rules(0))
    plt.xlabel('Iterations')
    plt.savefig(filename, dpi=dpi)

#plt.matshow(auto(237, 500))
#plt.show()

def pattern_in_sequence(sequence):
    established_pattern = []
    est_pattern_repeats = 0
    candidate_pattern   = []
    for element in sequence:
        if element

def left_pattern_count(array): #takes 2x2 array
    column_count = len(array[0])
    for column_index in range(column_count):
        column = array[:,column_index]
        for column_element in reversed(column):



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


i = 10
w = 2 + (i*2)
# plot(w, i, str(i) + ' auto.png');      print('plot')
# plot_left(w, i, str(i) + ' left_shift_auto.png'); print('plot_left')
# plot_right(w, i, str(i) + ' right_shift_auto.png'); print('plot_right')

auto_center = auto(w, i)
left_shift_auto = left_shift(auto_center)
left_pattern_count(left_shift_auto)

# auto_upshift = up_shift(auto_center)
# plot_matrix(auto_upshift, str(i) + ' up_shift.png', 1400)


# left_auto = left_shift(auto(w, i))

# with open('left_rule30_save', 'wb') as file:
#     pickle.dump(left_auto, file)

# left_auto = None
# with open('left_rule30_save', 'rb') as file:
#     left_auto = pickle.load(file)

# def leftshift_patter(left_auto): #finds repetitive sequences in columns of left_shifted automaton
    


print('🦀🦀🦀🦀-------------over-------------🦀🦀🦀🦀'); quit()

# def samplemat(dims):
#     """Make a matrix with all zeroes and increasing elements on the diagonal"""
#     aa = np.zeros(dims)
#     for i in range(min(dims)):
#         aa[i, i] = 1
#     return aa

# Display matrix
# plt.matshow(samplemat((15,15)))

# plt.show()
