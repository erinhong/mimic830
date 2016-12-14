import csv

def count(fileName):
  numRows = 0
  with open(fileName, 'r') as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
  return row_count

def lm_predict(a,b,intercept,fileName):
	rr_values = [] 
	leastSquared = 0
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
				upRange = actual*1.1  #1.20#*1.05
				lwRange = actual*.90   #.8 #.95
				observed = a * hr + b * bp + intercept 
				line['resprate'] = observed
				rr_values.append(observed)

				leastSquared += (actual-observed)**2 

				# # If in acceptable range 
				# if lwRange <= observed and observed <= upRange: 
				# 	acceptedPredictions += 1 
			else: 
				rr_values.append(float(line['resprate']))


	return fileName[-7:], leastSquared


def lm_predict_joined(a,b,c,d,intercept,fileName):
	acceptedPredictions = 0
	total = count(fileName) 
	leastSquared = 0
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

				upRange = actual*1.1  #1.20#*1.05
				lwRange = actual*.90   #.8 #.95

				observed = a * hr + b * bp + c * age + gender + intercept 
				line['resprate'] = observed

				leastSquared += (actual-observed)**2

				# # If in acceptable range 
				# if lwRange <= observed and observed <= upRange: 
				# 	acceptedPredictions += 1 


	return fileName[-7:],leastSquared



if __name__=='__main__':
	joined_files = ['induced_dead_ace_joined_test_10_0.1.csv','induced_dead_ace_joined_test_10_0.3.csv','induced_dead_ace_joined_test_10_0.5.csv']
	files = ['induced_dead_ace_test_10_0.1.csv','induced_dead_ace_test_10_0.3.csv','induced_dead_ace_test_10_0.1.csv']
	print 'No Join'
	for f in files: 
		# resprate ~heartrate + bloodpressure
		(name,leastsquared) = lm_predict(0.143485,0.011735,5.825879,f)
		print (name,leastsquared)
		#print rr_values
	print '###########################################'
	print 'Joined'
	for jf in joined_files: 
		(name,leastsquared) = lm_predict_joined(0.144150, 0.011310, 0.027668, 0.511245, 3.611799,jf)
		print (name,leastsquared)



# Dead Patient Ace Joined Table -> 2643



######## Different train/test distributions, least squared 

# train 90%, test 10%
# No Join
# ('0.1.csv', 1342.5335549972406)
# ('0.3.csv', 4365.742528772348)
# ('0.1.csv', 1342.5335549972406)
# Joined
# ('0.1.csv', 1086.4348315361267)
# ('0.3.csv', 4528.863447116168)
# ('0.5.csv', 7970.889865116953)

# Linear Regression Equations 

# 70% TRAIN | 30% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.602958   0.434759  12.888  < 2e-16 ***
# heartrate     0.145658   0.005201  28.005  < 2e-16 ***
# bloodpressure 0.011643   0.003778   3.082  0.00209 *
# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.242482   1.017738   3.186  0.00147 ** 
# heartrate       0.146254   0.005204  28.102  < 2e-16 ***
# bloodpressure   0.011184   0.003779   2.960  0.00312 ** 
# age             0.029881   0.012798   2.335  0.01966 *  
# factor(gender)M 0.516674   0.369022   1.400  0.16165   


# 80% TRAIN | 30% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.895305   0.407430  14.469  < 2e-16 ***
# heartrate     0.141619   0.004890  28.962  < 2e-16 ***
# bloodpressure 0.012837   0.003598   3.568 0.000367 ***
# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.967024   0.960521   4.130 3.77e-05 ***
# heartrate       0.142039   0.004894  29.026  < 2e-16 ***
# bloodpressure   0.012514   0.003600   3.476 0.000519 ***
# age             0.023831   0.012124   1.966 0.049463 *  
# factor(gender)M 0.496224   0.347086   1.430 0.152955  

# 90% TRAIN | 10% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.825879   0.378400  15.396  < 2e-16 ***
# heartrate     0.143485   0.004542  31.592  < 2e-16 ***
# bloodpressure 0.011735   0.003366   3.486 0.000499 ***
# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.967024   0.960521   4.130 3.77e-05 ***
# heartrate       0.142039   0.004894  29.026  < 2e-16 ***
# bloodpressure   0.012514   0.003600   3.476 0.000519 ***
# age             0.023831   0.012124   1.966 0.049463 *  
# factor(gender)M 0.496224   0.347086   1.430 0.152955 


































######## SCRAP, WRONG SCORE METRIC 

#(1.05,.95) we see fewer differences between joined and unjoined performance 
# No Join
# ('0.1.csv', 11, 0.1387137452711223)
# ('0.3.csv', 38, 0.15973097940311057)
# ('0.5.csv', 51, 0.12862547288776796)
# ###########################################
# Joined
# ('0.1.csv', 11, 0.1387137452711223)
# ('0.3.csv', 22, 0.09247583018074822)
# ('0.5.csv', 50, 0.12610340479192939)

# (1.03,.97) shows at least that joined performs as expected
# No Join
# ('0.1.csv', 7, 0.08827238335435056)
# ('0.3.csv', 26, 0.10928961748633881)
# ('0.5.csv', 33, 0.0832282471626734)
# ###########################################
# Joined
# ('0.1.csv', 9, 0.11349306431273642)
# ('0.3.csv', 13, 0.054644808743169404)
# ('0.5.csv', 26, 0.06557377049180328)

# The fact that these values don't show the gradient we expected, 
# may suggest overfitting as we expected poorer performance 

# No Join vs Join for 0.1 (fewest missing values), the joined approach 
# does at least as well as unjoined if not a little better 
# The more values that are missing, it just does worse possibly due ill-fit 
# in the model and random correlation between our chosen variables. 





