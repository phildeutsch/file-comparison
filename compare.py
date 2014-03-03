#	Usage:
#	Compares the files with given extension in two folders
#	python compareCPB.py <extension> <folder1> <folder2> <outputFile>

import csv
import glob
import sys, os
import datetime

def loadFiles(folder, extension):
        fileList = glob.glob(folder + '/*.' + extension)
        for i in range(len(fileList)):
                fileList[i] = fileList[i].split('/')[-1]
        return fileList

def loadFileData(pathToFile):
	fileData = []
        with open(pathToFile, 'r') as csvfile:
		rowreader = csv.reader(csvfile, delimiter=';')
		for row in rowreader:
			fileData.append(row)
	return fileData

extension   = str(sys.argv[1])
folder1     = str(sys.argv[2])
folder2     = str(sys.argv[3])
outFileName = str(sys.argv[4])

sys.stdout.write('Comparing .ext files:\n')
fileList1 = loadFiles(folder1)
fileList2 = loadFiles(folder2)
filesToCompare = list(set.intersection(set(fileList1), set(fileList2)))
filesNotIn1 = list(set(fileList2)-set(fileList1))
filesNotIn2 = list(set(fileList1)-set(fileList2))

for i in range(len(filesToCompare)/100):
        sys.stdout.write('|')
        sys.stdout.flush()
print('')

with open(outFileName, 'w') as outFile:
        outFile.write(','.join(['Folder 1:', folder1, '\n']))
        outFile.write(','.join(['Folder 2:', folder2, '\n']))
        outFile.write(','.join(['Time of comparison:', str(datetime.datetime.now()), '\n']))
        outFile.write('File,Trade,Column,Value1,Value2\n')

        for i in range(len(filesNotIn1)):
                writeList = [filesNotIn1[i], "NA", "NA", "Missing", "NA", '\n']
                outFile.write(','.join(writeList))
        for i in range(len(filesNotIn2)):
                writeList = [filesNotIn2[i], "NA", "NA", "NA", "Missing", '\n']
                outFile.write(','.join(writeList))
        filesError  = []
        fileCounter = 0
        for fileName in filesToCompare:
#		print fileName
		fileCounter = fileCounter + 1
		if fileCounter % 100 == 0:
			sys.stdout.write('|')
			sys.stdout.flush()
		path1 = folder1 + '/' + fileName
		path2 = folder2 + '/' + fileName
		data1 = loadFileData(path1)
		data2 = loadFileData(path2)
		
		if len(data1) is not len(data2):
			writeList = [fileName, 'NA', '# of Trades', str(len(data1)), str(len(data2)), 'NA', 'NA', '\n']
			outFile.write(','.join(writeList))

		for i in range(len(data1)):
			ID1 = data1[i][0].split('+')[0]
			for j in range(len(data2)):
				if len(data2[j]) == 0:
					ID2 = None
				else:
					ID2 = data2[j][0].split('+')[0]
				if ID1 == ID2:
					break
			if ID2 != ID1:
				writeList = [fileName, ID1, 'NA', 'NA', 'not found', 'NA', 'NA', '\n']
				outFile.write(','.join(writeList))
			else:
#					print(data1[i], data2[j])
				if len(data1[i]) is not len(data2[j]):
					writeList = [fileName, data1[i][0], 'Line length', str(len(data1)), str(len(data2)),'\n']
					outFile.write(','.join(writeList))

				for col in range(1,min(len(data1[i]), len(data2[j]))):
					val1 = data1[i][col].strip()
					val2 = data2[j][col].strip()
					check = val1 == val2
					if check is False:
						writeList = [fileName, data1[i][0], str(col+1), str(val1), str(val2),'\n']
						outFile.write(','.join(writeList))
#						print(val1, val2, check, val1==val2) 
if len(filesError) > 0:
	print('Errors comparing the following files:')
	print(filesError)
print('')

