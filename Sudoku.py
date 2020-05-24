# Importing libraries
import collections
from collections import Counter
import ast
import numpy as np
import pandas as pd
from random import randint
import time
import warnings


# ##### Kaggle dataset:
# https://www.kaggle.com/bryanpark/sudoku


quizzes = np.zeros((1000000, 81), np.int32)
solutions = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))

k = randint(1,1000000) 
df = pd.DataFrame(quizzes[k])
sol_df = solutions[k]



# making all zeros to the array
df = df.applymap(lambda x: [1,2,3,4,5,6,7,8,9] if x == 0 else x)


# solving Sudoku via eliminating numbers
def convert_single(value):
    if isinstance(value, list) and len(value) == 1:
        value = int(''.join([str(x) for x in value]))
        
    return value

## eliminating numbers row-wise
def row_check(df, row):

    filled_row_numbers = [x for x in df.loc[row] if not isinstance(x, list)]
    # del_numbers_from_array - elimination -1
    for i,j in enumerate(df.loc[row]):
        if isinstance(j, list):
            abc = [k for k in j if k not in filled_row_numbers]
            df.set_value(row, i, abc)


    comm_ele = [(item, count) for item, count in Counter([str(a) for a in list(df.loc[row])]).items() if count > 1]
    to_store = []
    to_store_to_append =[]
    for i in comm_ele:
        if len(ast.literal_eval(i[0])) == i[1]:
            to_store.append(ast.literal_eval(i[0]))
            to_store_to_append = list([item for sublist in to_store for item in sublist])

    # del_numbers_from_array - elimination -2
    filled_row_numbers = [x for x in df.loc[row] if not isinstance(x, list)]
    filled_row_numbers.extend(to_store_to_append)
    for i,j in enumerate(df.loc[row]):
        
        if isinstance(j, list) and j not in to_store:
            
            abc = [k for k in j if k not in filled_row_numbers]
            df.set_value(row, i, abc)
        
    lst = list(df.loc[row])
    arr = [a for a in lst if isinstance(a, list)]
    m = [item for item, count in Counter([str(a) for a in list([item for sublist in arr for item in sublist])]).items() if count == 1]
    if len(m) ==1:
        val = int(m[0])
        for s, t in enumerate(lst):
            if isinstance(t, list) and val in t:
                df.loc[row][s] = val
  
## eliminating numbers column-wise
def column_check(df, column):
    
    filled_column_numbers = [x for x in df.loc[:, column] if not isinstance(x, list)]
    for i,j in enumerate(df.loc[:, column]):
        if isinstance(j, list):
            qrs = [k for k in j if k not in filled_column_numbers]
            df.set_value(i, column, qrs)
            
            
    comm_ele = [(item, count) for item, count in Counter([str(a) for a in list(df.loc[:, column])]).items() if count > 1]
    to_store = []
    to_store_to_append = []
    for i in comm_ele:
        if len(ast.literal_eval(i[0])) == i[1]:
            to_store.append(ast.literal_eval(i[0]))
            to_store_to_append = list([item for sublist in to_store for item in sublist])
            
    filled_column_numbers = [x for x in df.loc[:, column] if not isinstance(x, list)]
    filled_column_numbers.extend(to_store_to_append)
    for i,j in enumerate(df.loc[:, column]):
        if isinstance(j, list) and j not in to_store:
            qrs = [k for k in j if k not in filled_column_numbers]
            df.set_value(i, column, qrs)
            
            
    lst = list(df.loc[:, column])
    arr = [a for a in lst if isinstance(a, list)]
    m = [item for item, count in Counter([str(a) for a in list([item for sublist in arr for item in sublist])]).items() if count == 1]
    if len(m) ==1:
        val = int(m[0])
        for s, t in enumerate(lst):
            if isinstance(t, list) and val in t:
                df.loc[:, column][s] = val
            
    
## eliminating numbers block-wise        
def remove_elem(value, filled_numbers):
    if isinstance(value, list):
        value = [k for k in value if k not in filled_numbers]
        
    return value

def remove_elem1(value, filled_numbers, to_store):
    if isinstance(value, list) and value not in to_store :
        value = [k for k in value if k not in filled_numbers]
        
    return value

boundaries = [[(0, 0), (2, 2)], [(3, 0), (5, 2)], [(6, 0), (8, 2)],
              [(0, 3), (2, 5)], [(3, 3), (5, 5)], [(6, 3), (8, 5)],
              [(0, 6), (2, 8)], [(3, 6), (5, 8)], [(6, 6), (8, 8)]]

def block_check(dframe):
    for j, i in enumerate(boundaries):
        filled_numbers = [a for a in np.reshape((dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]]).values, 9) if not isinstance(a, list)]
        dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]] = dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]].applymap(lambda x: remove_elem(x, filled_numbers))
        
        comm_ele = [a for a in np.reshape((dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]]).values, 9) if isinstance(a, list)]
        comm_ele = [(item, count) for item, count in Counter([str(a) for a in list(comm_ele)]).items() if count > 1]
        to_store = []
        to_store_to_append = []
        for y in comm_ele:
            if len(ast.literal_eval(y[0])) == y[1]:
                to_store.append(ast.literal_eval(y[0]))
                to_store_to_append = list([item for sublist in to_store for item in sublist])
                
        
        filled_numbers = [a for a in np.reshape((dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]]).values, 9) if not isinstance(a, list)]
        filled_numbers.extend(to_store_to_append)
        dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]] = dframe.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]].applymap(lambda x: remove_elem1(x, filled_numbers, to_store))
        
        
        lst = list(np.reshape((df.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]]).values, 9))
        arr = [a for a in lst if isinstance(a, list)]
        m = [item for item, count in Counter([str(a) for a in list([item for sublist in arr for item in sublist])]).items() if count == 1]
        if len(m) ==1:
            val = int(m[0])
            for s, t in enumerate(lst):
                if isinstance(t, list) and val in t:
                    lst[s] = val
                    lst = np.reshape(lst, (3, 3))
                    df.loc[i[0][0]:i[1][0], i[0][1]: i[1][1]] = lst

start_time = time.time()
while np.sum(df.sum()) < 405:
    for i in np.arange(9):
        row_check(df, i)
        df = df.applymap(convert_single)
        column_check(df, i)
        df = df.applymap(convert_single)
        block_check(df)
        df = df.applymap(convert_single)
print("--- %s seconds ---" % (time.time() - start_time))

result = np.array(df)

# check if the answer is correct
array_equal = np.allclose(result, sol_df)
array_equal
