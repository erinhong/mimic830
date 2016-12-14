dat = read.csv("Documents/ERIN\ HONG/IHTFP4/6_830/mimic830/dead_ace_train.csv", header = TRUE)
dat_gaps = read.csv("Documents/ERIN\ HONG/IHTFP4/6_830/mimic830/induced_ace_test_0.1.csv", header = TRUE)

# Calculating Mean, Variance and CoVariance 
mean <- mean(dat$resprate)
variance <- var(dat$resprate)

# Generate the Linear Regression Model 
fit <- lm(formula = resprate ~heartrate + bloodpressure, data = dat)
intercept <- fit$coefficients[1]
hr <- fit$coefficients[2]
bp <- fit$coefficients[3]

# Make Initial Guesses where there exist gaps 
guesses <- vector() 

bpList <- dat_gaps$bloodpressure
hrList <- dat_gaps$heartrate
rrList <- dat_gaps$resprate
for (i in 1:length(rrList)){
  if (is.na(rrList[i])){
    guessVal = hr*hrList[i] + bp*bpList[i] + intercept 
    print (guessVal)
    guesses <- c(guesses,guessVal)
  }else{
    guesses <- c(guesses,rrList[i])
  }
}
print (guesses)









