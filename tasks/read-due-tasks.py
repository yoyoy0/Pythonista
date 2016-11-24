# https://gist.github.com/Moving-Electrons/7762481

# This script reads an Abstractspoon ToDoList file, searches for tasks overdue, due today and due within the next 7 days and puts the results in a text file in Markdown format. It includes Due Dates, Categories and Priorities per task. More information in www.movingelectrons.net

import sys
import csv
import operator
import time
from datetime import date
'''Summary:
 This script reads the .csv file generated by TodoList (from abstractspoon) using csvreader (csv library) and puts the contents in a list of lists that is later iterated over to separate tasks in 4 buckets (lists of lists): Overdue, Today, Tomorrow and Next 7 days. Each of these lists has the priority column converted to integer so that they can be sorted by the column. The results are then written to a .txt file'''

# Contants definition
file = sys.argv[1] # .csv file from Abstractspoon TodoList
output = sys.argv[2] # Output .txt file
#Columns in the csv file. 1st column is "0":
ddtCol=3
priCol=1
catCol=4
desCol=0
completionCol=2

def append_ListInFile(list,workingFile):
	for row in list:
		size = len(row) #finding out size of the list (some of them include the Due Date field and some don't
		if size == 4:
			rowStr = '**'+str(row[0])+"** **"+row[1]+"** "+row[2]+" "+row[3]
			workingFile.write("%s  \r\n" % rowStr)
		elif size == 3:
			rowStr = '**'+str(row[0])+"** **"+row[1]+"** "+row[2]
			workingFile.write("%s  \r\n" % rowStr)
			
			
			
			
# ----------------------------
data_initial = open(file, 'rb')
data = csv.reader((line.replace('\0','') for line in data_initial), delimiter=",")#replaces the NULL bytes in the file so that csv.reader parser doesn't give an error. This is an unresolved issue related to the way ToDoList encodes the CSV file.

header = data.next()
td = date.today() #gets today's date
print 'Today\'s date: %s' % str(td)

sortedList = sorted(data, key=operator.itemgetter(ddtCol)) #Sorts by DueDate (however, since data is a string type, the sort is almost meaningless. This is use to dump contents of file in a list of lists). SortedList is created after the header was taken, the header is not included in sortedList

overdueLst = []
todayLst = []
tomorrowLst = []
futureLst = []

print 'Iterating inside task list...'
for row in range(len(sortedList)):
	if sortedList[row][ddtCol] == '': # if Due Date is blank, continue
		continue
	elif sortedList[row][completionCol] == '100': # if task has been completed, continue
		continue
	else:
		dtStr = sortedList[row][ddtCol].split('/')
		xDate = date(int(dtStr[2]),int(dtStr[0]),int(dtStr[1])) # transforms date string coming from .csv file into Date format for later comparison
		dtDif = xDate-td
		if dtDif.days<0:
			'''In the following line a temporary list is created with the data to be used in the txt file. It has the following fields: Priority (as integer!), Category, Description and Due Date. I'm also adding "[]" to categories and "due: " to Due Dates'''
			tempLst=[int(sortedList[row][priCol]),'['+sortedList[row][catCol]+']',sortedList[row][desCol],'due: '+sortedList[row][ddtCol]]
			overdueLst.append(tempLst)
		elif dtDif.days==0:
			tempLst=[int(sortedList[row][priCol]),'['+sortedList[row][catCol]+']',sortedList[row][desCol]]
			todayLst.append(tempLst)
		elif dtDif.days==1:
			tempLst=[int(sortedList[row][priCol]),'['+sortedList[row][catCol]+']',sortedList[row][desCol]]
			tomorrowLst.append(tempLst)
		elif dtDif.days>=2 and dtDif.days<=7:
			tempLst=[int(sortedList[row][priCol]),'['+sortedList[row][catCol]+']',sortedList[row][desCol],'due: '+sortedList[row][ddtCol]]
			futureLst.append(tempLst)
print 'Done.'
data_initial.close()

# sorting lists
print 'Sorting lists...'
overdueLst2 = sorted(overdueLst, key=operator.itemgetter(0), reverse=True)
todayLst2 = sorted(todayLst, key=operator.itemgetter(0), reverse=True)
tomorrowLst2 = sorted(tomorrowLst, key=operator.itemgetter(0), reverse=True)
futureLst2 = sorted(futureLst, key=operator.itemgetter(0), reverse=True)
print 'Done.'

# Writing to the file
print 'Writing tasks to file...'
txtFile= open(output, 'w')
txtFile.write("## TodoList - Work\r\n")
txtFile.write("## Overdue Tasks:\r\n")
append_ListInFile(overdueLst2,txtFile)
txtFile.write("\n## Today's Tasks (%s):\r\n" % str(td))
append_ListInFile(todayLst2,txtFile)
txtFile.write("\n## Tomorrow's Tasks:\r\n")
append_ListInFile(tomorrowLst2,txtFile)
txtFile.write("\n## Next 7 days:\r\n")
append_ListInFile(futureLst2,txtFile)
txtFile.close()
print 'Done.'
