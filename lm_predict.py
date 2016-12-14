import csv

def count(fileName):
  numRows = 0
  with open(fileName, 'r') as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
  return row_count

def lm_predict(a,b,intercept,fileName):
	acceptedPredictions = 0
	total = count(fileName) 
	with open(fileName,'r') as f: 
		reader = csv.DictReader(f,delimiter = ',')
		for line in reader: 
			if line['resprate'] == "": 
				#predict value and fill in 
				hr = float(line['heartrate'])
				bp = float(line['bloodpressure'])
				actual = float(line['removed'])
				upRange = actual*1.2  #1.20#*1.05
				lwRange = actual*.8   #.8 #.95
				observed = a * hr + b * bp + intercept 
				line['resprate'] = observed

				# If in acceptable range 
				if lwRange <= observed and observed <= upRange: 
					acceptedPredictions += 1 


	return fileName[-7:],acceptedPredictions, acceptedPredictions/float(total*float(fileName[-7:-4]))


def lm_predict_joined(a,b,c,d,intercept,fileName):
	acceptedPredictions = 0
	total = count(fileName) 
	with open(fileName,'r') as f: 
		reader = csv.DictReader(f,delimiter = ',')
		for line in reader: 
			if line['resprate'] == "": 
				#predict value and fill in 
				hr = float(line['heartrate'])
				bp = float(line['bloodpressure'])
				age = float(line['age'])
				gender = (line['gender'])
				if gender == "F": 
					gender = 1 
				else: 
					gender = 0 
				actual = float(line['removed'])

				upRange = actual*1.2o  #1.20#*1.05
				lwRange = actual*.8   #.8 #.95

				observed = a * hr + b * bp + c * age + gender + intercept 
				line['resprate'] = observed

				# If in acceptable range 
				if lwRange <= observed and observed <= upRange: 
					acceptedPredictions += 1 


	return fileName[-7:],acceptedPredictions, acceptedPredictions/float(total*float(fileName[-7:-4]))



if __name__=='__main__':
	joined_files = ['induced_dead_ace_joined_test_0.1.csv','induced_dead_ace_joined_test_0.3.csv','induced_dead_ace_joined_test_0.5.csv']
	files = ['induced_dead_ace_test_0.1.csv','induced_dead_ace_test_0.3.csv','induced_dead_ace_test_0.5.csv']
	print 'No Join'
	for f in files: 
		# resprate ~heartrate + bloodpressure
		a,x,y = lm_predict(0.08599, -0.02001,13.93718,f)
		print (a,x,y)
	print '###########################################'
	print 'Joined'
	for jf in joined_files: 
		a,x,y = lm_predict_joined(0.09174, -0.01727,0.02514,0.55427,11.36239,jf)
		print (a,x,y)


# ('0.1.csv', 5, 0.8771929824561403)
# ('0.3.csv', 14, 0.8187134502923977)
# ('0.5.csv', 22, 0.7719298245614035)




