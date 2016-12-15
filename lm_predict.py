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

# 95% TRAIN | 05% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.830201   0.370034  15.756  < 2e-16 ***
# heartrate     0.144626   0.004437  32.598  < 2e-16 ***
# bloodpressure 0.011313   0.003305   3.423 0.000628 ***
# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.392385   0.884775   3.834 0.000129 ***
# heartrate       0.145465   0.004441  32.759  < 2e-16 ***
# bloodpressure   0.010847   0.003304   3.283 0.001042 ** 
# age             0.031139   0.011126   2.799 0.005170 ** 
# factor(gender)M 0.469527   0.315705   1.487 0.137079 

if __name__=='__main__':
	joined_files = ['induced_dead_ace_joined_test_05_0.1.csv','induced_dead_ace_joined_test_05_0.3.csv','induced_dead_ace_joined_test_05_0.5.csv']
	files = ['induced_dead_ace_test_05_0.1.csv','induced_dead_ace_test_05_0.3.csv','induced_dead_ace_test_05_0.5.csv']
	print 'No Join'
	for f in files: 
		# resprate ~heartrate + bloodpressure
		(name,leastsquared) = lm_predict(0.144626,0.011313,5.830201,f)
		print (name,leastsquared)
		#print rr_values
	print '###########################################'
	print 'Joined'
	for jf in joined_files: 
		(name,leastsquared) = lm_predict_joined(0.145465, 0.010847, 0.031139 , 0.469527, 3.3923854,jf)
		print (name,leastsquared)



# Dead Patient Ace Joined Table -> 2643

# Create the data for the chart.
# not_joined <- c(4932.343740123179,2905.2458388668874,1342.5335549972406,264.63339070904397)
# distributions <- c(70,80,90,95)
# plot(not_joined, distributions, type="l", lwd=2, col="blue", ylim=c(0, 12), xaxs="i", yaxs="i")
# joined <- c(5149.982721025402,3105.213382732825,1086.4348315361267,318.32722098806966)

# # Give the chart file a name.
# png(file = "Least_Squared_Varying_Train_Test_Distributions.jpg")

# # Plot the bar chart.
# plot(v,type = "o",col = "red", xlab = "Train", ylab = "Rain fall", 
#    main = "Rain fall chart")

# lines(t, type = "o", col = "blue")

# # Save the file.
# dev.off()

######## Different train/test distributions, least squared 

# 2644 Rows 
# 1850 
# 2115
# 2379 
# 2511




# train 70%, test 30% 

# No Join 
# ('0.1.csv', 4932.343740123179)
# ('0.3.csv', 14672.663873677118)
# ('0.5.csv', 23214.70125550916)
# Joined
# ('0.1.csv', 5149.982721025402)
# ('0.3.csv', 12015.438090824508)
# ('0.5.csv', 23446.298130530235)

# train 80%, test 20% 
# No Join
# ('0.1.csv', 2905.2458388668874)
# ('0.3.csv', 7859.365402605208)
# ('0.5.csv', 17159.443412678604)
# Joined
# ('0.1.csv', 3105.213382732825)
# ('0.3.csv', 8720.008280001373)
# ('0.5.csv', 15475.274385173194)

# train 90%, test 10%
# No Join
# ('0.1.csv', 1342.5335549972406)
# ('0.3.csv', 4365.742528772348)
# ('0.1.csv', 1342.5335549972406)
# Joined
# ('0.1.csv', 1086.4348315361267)
# ('0.3.csv', 4528.863447116168)
# ('0.5.csv', 7970.889865116953)

# train 95%, test 05% 
# No Join
# ('0.1.csv', 264.63339070904397)
# ('0.3.csv', 2662.3915099226106)
# ('0.5.csv', 3529.902271957436)
# Joined
# ('0.1.csv', 318.32722098806966)
# ('0.3.csv', 2271.2817881885603)
# ('0.5.csv', 3643.205256700546)





# Linear Regression Equations 

# 70% TRAIN | 30% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.602958   0.434759  12.888  < 2e-16 ***
# heartrate     0.145658   0.005201  28.005  < 2e-16 ***
# bloodpressure 0.011643   0.003778   3.082  0.00209 *
# Residual standard error: 7.83 on 1847 degrees of freedom
# Multiple R-squared:  0.3294,	Adjusted R-squared:  0.3287 
# F-statistic: 453.6 on 2 and 1847 DF,  p-value: < 2.2e-16

# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.242482   1.017738   3.186  0.00147 ** 
# heartrate       0.146254   0.005204  28.102  < 2e-16 ***
# bloodpressure   0.011184   0.003779   2.960  0.00312 ** 
# age             0.029881   0.012798   2.335  0.01966 *  
# factor(gender)M 0.516674   0.369022   1.400  0.16165  
# Residual standard error: 7.819 on 1845 degrees of freedom
# Multiple R-squared:  0.332,	Adjusted R-squared:  0.3305 
# F-statistic: 229.2 on 4 and 1845 DF,  p-value: < 2.2e-16 

# 80% TRAIN | 30% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.895305   0.407430  14.469  < 2e-16 ***
# heartrate     0.141619   0.004890  28.962  < 2e-16 ***
# bloodpressure 0.012837   0.003598   3.568 0.000367 ***
# Residual standard error: 7.864 on 2111 degrees of freedom
# Multiple R-squared:  0.3188,	Adjusted R-squared:  0.3181 
# F-statistic: 493.9 on 2 and 2111 DF,  p-value: < 2.2e-16

# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.967024   0.960521   4.130 3.77e-05 ***
# heartrate       0.142039   0.004894  29.026  < 2e-16 ***
# bloodpressure   0.012514   0.003600   3.476 0.000519 ***
# age             0.023831   0.012124   1.966 0.049463 *  
# factor(gender)M 0.496224   0.347086   1.430 0.152955 
# Residual standard error: 7.858 on 2109 degrees of freedom
# Multiple R-squared:  0.3206,	Adjusted R-squared:  0.3193 
# F-statistic: 248.8 on 4 and 2109 DF,  p-value: < 2.2e-16 

# 90% TRAIN | 10% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.825879   0.378400  15.396  < 2e-16 ***
# heartrate     0.143485   0.004542  31.592  < 2e-16 ***
# bloodpressure 0.011735   0.003366   3.486 0.000499 ***
# Residual standard error: 7.825 on 2375 degrees of freedom
# Multiple R-squared:  0.3298,	Adjusted R-squared:  0.3292 
# F-statistic: 584.4 on 2 and 2375 DF,  p-value: < 2.2e-16

# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.967024   0.960521   4.130 3.77e-05 ***
# heartrate       0.142039   0.004894  29.026  < 2e-16 ***
# bloodpressure   0.012514   0.003600   3.476 0.000519 ***
# age             0.023831   0.012124   1.966 0.049463 *  
# factor(gender)M 0.496224   0.347086   1.430 0.152955 
# Residual standard error: 7.815 on 2373 degrees of freedom
# Multiple R-squared:  0.332,	Adjusted R-squared:  0.3309 
# F-statistic: 294.9 on 4 and 2373 DF,  p-value: < 2.2e-16


# 95% TRAIN | 05% TEST 
# NOT JOINED 
# p-value: < 2.2e-16
# Coefficients:
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.830201   0.370034  15.756  < 2e-16 ***
# heartrate     0.144626   0.004437  32.598  < 2e-16 ***
# bloodpressure 0.011313   0.003305   3.423 0.000628 ***
# Residual standard error: 7.812 on 2507 degrees of freedom
# Multiple R-squared:  0.3312,	Adjusted R-squared:  0.3307 
# F-statistic: 620.9 on 2 and 2507 DF,  p-value: < 2.2e-16

# JOINED 
# p-value: < 2.2e-16
# Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
# (Intercept)     3.392385   0.884775   3.834 0.000129 ***
# heartrate       0.145465   0.004441  32.759  < 2e-16 ***
# bloodpressure   0.010847   0.003304   3.283 0.001042 ** 
# age             0.031139   0.011126   2.799 0.005170 ** 
# factor(gender)M 0.469527   0.315705   1.487 0.137079  
# Residual standard error: 7.8 on 2505 degrees of freedom
# Multiple R-squared:  0.3338,	Adjusted R-squared:  0.3328 
# F-statistic: 313.8 on 4 and 2505 DF,  p-value: < 2.2e-16































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





