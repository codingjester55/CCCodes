import csv
import re


#inputFilename = 'ICD9_Xwlk_COPD_Rdmsn_FY17.csv'
inputFilename = 'ICD_Xwlk_Stroke_Rdmsns_FY17.csv'
condition = 'STROKE'
#outputFilename = 'X_ICD9_CC_COPD.csv'
#outputFilenameError = 'X_ICD9_CC_COPD_ERRORS.csv'
outputFilename = 'X_ICD9_CC_' + condition + '.csv'
outputFilenameError = 'X_ICD9_CC_' + condition + '_ERRORS.csv'


# Retrieve input csv and create output files 
#with open("ICD9_Xwlk_COPD_Rdmsn_FY17.csv", "r") as inputFile:
with open(inputFilename, 'r') as inputFile:
#with open('COPD.csv', 'r') as inputFile:
	lines = csv.reader(inputFile, delimiter=',')
	outputFile = open(outputFilename, 'w')
	outputFileErrors = open(outputFilenameError, 'w')

	# For each row in CSV, parse the CC value
	for line, row in enumerate(lines):
		# line 0 - file header; line 1 - column headers
		if line == 1: # keep column headers
			outputFile.write(row[0] + "," + row[1] + "," + row[2] + "," + row[3] + '\n')
		if line > 1:
			# strip invalid characters (commas, colons, quotes) from the labels
			cleanICDLabel = row[1].translate({ord(c): None for c in ',:"'})
			cleanCCLabel = row[3].translate({ord(c): None for c in ',:"'})
			
			CCValue = re.match(r'(CC )(.*)',row[2])  # Strip 'CC' prefix on CC value
			if CCValue:
				Codes = CCValue.group(2).split(', ')  # sometimes we have multiple ranges or codes separated by ','
				for code in Codes:
					# single code - nothing but numbers
					singleCode = re.match(r'(\d*)',code)  
					if singleCode:
						#print("ROW ADDED: " + row[0] + "," + cleanICDLabel + "," + singleCode.group(1) + "," + cleanCCLabel)
						outputFile.write(row[0] + "," + cleanICDLabel + "," + singleCode.group(1) + "," + cleanCCLabel + '\n')

					# range of codes
					codeRange = re.match(r'(\d*)-(.\d*)',code)  
					if codeRange:
						start = int(codeRange.group(1))
						end = int(codeRange.group(2))
						if start < end:
							for x in range(start,end+1):
								#print("ROW ADDED: " + row[0] + "," + cleanICDLabel + "," + str(x) + "," + cleanCCLabel)
								outputFile.write(row[0] + "," + cleanICDLabel + "," + str(x) + "," + cleanCCLabel + '\n')
								
			else:
				print("ERROR - offending row: ",row)
				outputFileErrors.write(str(row) + '\n')

	outputFile.close()
	outputFileErrors.close()

inputFile.close()
