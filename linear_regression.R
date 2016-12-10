dat = read.csv("Documents/ace.csv", header = TRUE)

fit <- lm(heartrate ~ bloodpressure + resprate, data=dat)
summary(fit)

plot(dat$bloodpressure, dat$heartrate, col = 'blue', main="Scatter Plot of 'altered_chartevents' Table",
     xlab="Measurements", ylab="Heartrate (bpm)")
legend("topright", c("Blood Pressure (mmHg)", "Respiratory Rate (insp/min)"), fill=c("blue", "red"), cex=c(.9,.9), text.width=70)
points(dat$resprate, dat$heartrate, col = 'red')





install.packages("rgl")
library("rgl")

# open3d()
# plot3d(hr,bp,rr, col=c('blue','red','forestgreen'), 
#        main="Scatter Plot of 'altered_chartevents' Table",
#        xlab="Heartrate (bpm)", ylab="Blood Pressure (mmHg)", zlab="Respiratory Rate (insp/min)")



plot3d(rr,hr,bp,col=c('blue','red','forestgreen'), xlab="RR (insp/min)",ylab="HR (bpm)",zlab="BP (mmHg)")
fit <- lm(bp ~ rr + hr)
coefs <- coef(fit)
planes3d(coefs["rr"], coefs["hr"], -1, coefs["(Intercept)"], alpha=0.5)






