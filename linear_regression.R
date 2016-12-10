dat = read.csv("Documents/ace.csv", header = TRUE)

fit <- lm(heartrate ~ bloodpressure + resprate, data=dat)
summary(fit)

plot(dat$bloodpressure, dat$heartrate, col = 'blue', main="Scatter Plot of 'altered_chartevents' Table",
     xlab="Measurements", ylab="Heartrate (bpm)")
legend("topright", c("Blood Pressure (mmHg)", "Respiratory Rate (insp/min)"), fill=c("blue", "red"), cex=c(.9,.9), text.width=70)
points(dat$resprate, dat$heartrate, col = 'red')