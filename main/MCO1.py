"""
References
https://www.geeksforgeeks.org/python-program-for-quicksort/
https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
https://www.geeksforgeeks.org/how-to-check-the-execution-time-of-python-script/
https://www.geeksforgeeks.org/python-program-for-insertion-sort/
https://pandas.pydata.org/docs/reference/index.html
"""
import random
import pandas as pd
from pandas import DataFrame
from datetime import datetime

"""
Description
A function that implements the insertion sort algorithm

Parameter:
arr - array to sort
n - size of arr
"""

def insertionSort(arr, n):
    for i in range(1, n):
        pivot = arr[i]
        j = i-1
        while(j >= 0) and (pivot < arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = pivot

"""
Description
A function that implements the quick sort algoritm

Parameter:
a - array to sort
p - lower bound
r - upper bound
"""
    
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            (arr[j], arr[i]) = (arr[i], arr[j])
    (arr[high], arr[i + 1]) = (arr[i + 1], arr[high])
    return i + 1

def quickSort(arr, low, high):
    if low < high:
        pti = partition(arr, low, high)
        quickSort(arr, low, pti - 1)
        quickSort(arr, pti + 1, high)

"""
Description
A function used to create a random string from the letters acgt

Parameter:
n - size of the result string

Return Value:
The string generated
"""

def generateRandomString(n):
    sbstring = "acgt"
    result = ''.join(random.choice(sbstring) for i in range(n))
    return result

if __name__ == "__main__":
    
    # number of algorithms
    ALGORITHMS = 2
    # number of test cases
    TESTS = [50,100,150,200,250]
    # values for length of string allows multiple sizes in 1 run
    STR_LENGTH = [128,256,512,1024,2048]
    # store name of sorting algorithms
    sortingAlgos = { 0:"Insertion Sort", 1 :"Quick Sort"}
    # Array to store times
    insertionSortTests = []
    quickSortTests = []
    insertionAverageTime = []
    quickAverageTime = []
    # Dataframes
    dataframes = []
    
    for sortAlgo in range(ALGORITHMS):
        # loop through all lengths available
        for i in range(len(STR_LENGTH)):
            #temp array to store time
            temp = []
            # reset mean for every size
            mean = 0
            for j in range(TESTS[i]):

                # stat recording time
                start = datetime.now()

                # generate test case and record size
                sampleTest = generateRandomString(STR_LENGTH[i])
                n = len(sampleTest)

                # list comprehension to make suffixes
                arr = [sampleTest[index:n] for index in range(n)]

                # dic comprehenstion to store suffix position
                suffix = {arr[index]:index for index in range(n)}
                
                # calls which sorting function will be used
                insertionSort(arr,n) if sortAlgo == 0 else quickSort(arr,0,n-1)

                # suffix array built using array items a key and starting positions as values
                suffixArr = [suffix[arr[index]] for index in range(n)]

                # end recording time and Print suffix array
                print("\nThe suffix array of Test #" + str(j+1) + " is: ")
                end = datetime.now()
                print(suffixArr)

                # add time to mean, and display
                testTime = (end - start).total_seconds() * 1000
                mean += testTime
                print("The time for Test #" + str(j+1) + " is: " + str(testTime))

                # add testime to temporary recorder
                temp.append(testTime)
                
            mean /= TESTS[i]
            # print details about the test
            print("\nThe average time for " + sortingAlgos[sortAlgo]+ " with " + str(STR_LENGTH[i]) + " elements is: " + str(mean) + "\n")
            
            # store times depending on which algorithm
            if sortAlgo == 0:
                insertionSortTests.append(temp)
                insertionAverageTime.append(mean)
            else:
                quickSortTests.append(temp)
                quickAverageTime.append(mean)
            
    # construct dataframes
    for i in range(len(TESTS)):
        dataframes.append(DataFrame({"Insertion Sort": insertionSortTests[i], "Quick Sort": quickSortTests[i]}))
    AverageTimeDf = DataFrame({"Elements": STR_LENGTH, "Insertion Sort": insertionAverageTime , "Quick Sort" : quickAverageTime})
    
    # move to excel file
    filename = "Result.xlsx"
    with pd.ExcelWriter(filename) as writer:
        for i in range(len(dataframes)):
            sheetname = str(STR_LENGTH[i]) + " Elements"
            dataframes[i].to_excel(writer, sheet_name= sheetname ,index = False)
        AverageTimeDf.to_excel(writer, sheet_name = "Average Time", index = False)
