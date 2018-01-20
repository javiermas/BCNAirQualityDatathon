
setwd("~/Desktop/data")

target.raw = read.csv("targets.csv")
headers_obs_raw = read.csv("headers_obs.csv")
# headers_mod_raw = read.csv2("headers_mod.csv")
stations.raw = read.csv("stations.csv")

setwd("~/Desktop/data/processed")
all_obs_raw = read.csv("all_obs.csv")
str(all_obs_raw)

# omit useless variable
all_obs = all_obs_raw
all_obs[1:4] = NULL
all_obs[6:8] = NULL
all_obs[7] = NULL
all_obs[9:10] = NULL
str(all_obs)
summary(all_obs)

# treat times
library(lubridate)
all_obs$DatetimeBegin = ymd_hms(all_obs$DatetimeBegin)
all_obs$DatetimeEnd = ymd_hms(all_obs$DatetimeEnd)
str(all_obs$DatetimeBegin)
summary(all_obs$DatetimeBegin)

# check for outliers
install.packages("outliers")
library(outliers)

prop.table(table(all_obs$AirQualityStation))
prop.table(table(all_obs$AirQualityStationEoICode))
prop.table(table(all_obs$SamplingPoint))
prop.table(table(all_obs$SamplingProcess))
prop.table(table(all_obs$Sample))
prop.table(table(all_obs$Concentration))

str(all_obs$AirQualityStation)
plot(all_obs$AirQualityStation)
plot(all_obs$AirQualityStationEoICode)
plot(all_obs$SamplingPoint)
plot(all_obs$SamplingProcess)
plot(all_obs$Sample)
plot(all_obs$Concentration)
barplot(all_obs$Concentration)
outlier(all_obs$Concentration, opposite = FALSE, logical = FALSE)

all_obs$DateBegin = as.Date(all_obs$DatetimeBegin)
all_obs$DateEnd = as.Date(all_obs$DatetimeEnd)

# all_obs$TimeBegin = as.(all_obs$DatetimeBegin)
# all_obs$TimeEnd = as.Date(all_obs$DatetimeEnd)

install.packages("forecast")
library(forecast)

myts <- ts(all_obs$Concentration, start=c(2013, 1), end=c(2015, 12), frequency=12) 
# plot series
plot(myts)

time = all_obs$DateBegin
obs = all_obs$Concentration

x = ggplot(all_obs, aes(x=DateBegin, y=Concentration)) + # draw points
  geom_smooth(method="loess", se=F)
x

x = ggplot(all_obs, aes(x=DateBegin, y=Concentration) + 
  geom_bar(stat="identity", width=.5, fill="tomato3")
  

con = all_obs$Concentration
hist(con)
pop_sd <- sd(con)*sqrt((length(con)-1)/(length(con)))
pop_mean <- mean(con)
Python

z <- (40 - pop_mean) / pop_sd
z
p <- pnorm(z) 
(50 - pop_mean) / pop_sd

outlierKD <- function(dt, var) {
  var_name <- eval(substitute(var),eval(dt))
  na1 <- sum(is.na(var_name))
  m1 <- mean(var_name, na.rm = T)
  par(mfrow=c(2, 2), oma=c(0,0,3,0))
  boxplot(var_name, main="With outliers")
  hist(var_name, main="With outliers", xlab=NA, ylab=NA)
  outlier <- boxplot.stats(var_name)$out
  mo <- mean(outlier)
  var_name <- ifelse(var_name %in% outlier, NA, var_name)
  boxplot(var_name, main="Without outliers")
  hist(var_name, main="Without outliers", xlab=NA, ylab=NA)
  title("Outlier Check", outer=TRUE)
  na2 <- sum(is.na(var_name))
  cat("Outliers identified:", na2 - na1, "n")
  cat("Propotion (%) of outliers:", round((na2 - na1) / sum(!is.na(var_name))*100, 1), "n")
  cat("Mean of the outliers:", round(mo, 2), "n")
  m2 <- mean(var_name, na.rm = T)
  cat("Mean without removing outliers:", round(m1, 2), "n")
  cat("Mean if we remove outliers:", round(m2, 2), "n")
  response <- readline(prompt="Do you want to remove outliers and to replace with NA? [yes/no]: ")
  if(response == "y" | response == "yes"){
    dt[as.character(substitute(var))] <- invisible(var_name)
    assign(as.character(as.list(match.call())$dt), dt, envir = .GlobalEnv)
    cat("Outliers successfully removed", "n")
    return(invisible(dt))
  } else{
    cat("Nothing changed", "n")
    return(invisible(var_name))
  }
}
outlierKD(all_obs, all_obs$Concentration)

install.packages("fitdistrplus")
library("fitdistrplus")

stats = descdist(all_obs$Concentration)
fw <- fitdist(all_obs$Concentration, "weibull")

head(all_obs)

sta1 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES0691A")
sta2 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1396A")
sta3 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1438A")
sta4 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1480A")
sta5 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1679A")
sta6 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1856A")
sta7 = all_obs %>%
  filter(all_obs$AirQualityStationEoICode == "ES1992A")

unique(all_obs$AirQualityStationEoICode)
freq = table(all_obs$Concentration)

# station 1 - Weibull
sta1.dist = outlierKD(sta1, sta1$Concentration)  #41 - 40 mean outlier
stat.sta1 = descdist(sta1$Concentration)
plotdist(sta1$Concentration, histo = TRUE, demp = TRUE)

sta1.gam <- fitdist(sta1$Concentration, "gamma")
sta1.norm <- fitdist(sta1$Concentration, "norm")
sta1.pois <- fitdist(sta1$Concentration, "pois")
sta1.wei <- fitdist(sta1$Concentration, "weibull")

par(mfrow = c(2, 2))
plot.legend <- c("Gamma", "Normal", "Poisson", "Weibull")
denscomp(list(sta1.gam, sta1.norm, sta1.pois, sta1.wei), legendtext = plot.legend)
qqcomp(list(sta1.gam, sta1.norm, sta1.pois, sta1.wei), legendtext = plot.legend)

summary(sta1.gam)


# station 2 = Gamma 
plotdist(sta2$Concentration, histo = TRUE, demp = TRUE)
sta2.dist = outlierKD(sta2, sta2$Concentration) # 31 - 31
stat.sta2 = descdist(sta2$Concentration)
sta2.gam <- fitdist(sta2$Concentration, "gamma")
sta2.norm <- fitdist(sta2$Concentration, "norm")
sta2.pois <- fitdist(sta2$Concentration, "pois")
sta2.wei <- fitdist(sta2$Concentration, "weibull")

denscomp(list(sta2.gam, sta2.norm, sta2.pois, sta2.wei), legendtext = plot.legend)
qqcomp(list(sta2.gam, sta2.norm, sta2.pois, sta2.wei), legendtext = plot.legend)

# station 3 = Gamma (outlier to remove)
plotdist(sta3$Concentration, histo = TRUE, demp = TRUE)
sta3.dist = outlierKD(sta3, sta3$Concentration) # 55 - 54
stat.sta3 = descdist(sta3$Concentration)

sta3.gam <- fitdist(sta3$Concentration, "gamma")
sta3.norm <- fitdist(sta3$Concentration, "norm")
sta3.pois <- fitdist(sta3$Concentration, "pois")
sta3.wei <- fitdist(sta3$Concentration, "weibull")

denscomp(list(sta3.gam, sta3.norm, sta3.pois, sta3.wei), legendtext = plot.legend)
qqcomp(list(sta3.gam, sta3.norm, sta3.pois, sta3.wei), legendtext = plot.legend)

# station 4 = Gamma (outlier to remove)
plotdist(sta4$Concentration, histo = TRUE, demp = TRUE)
sta4.dist = outlierKD(sta4, sta4$Concentration) # 53 - 52
stat.sta4 = descdist(sta4$Concentration)

sta4.gam <- fitdist(sta4$Concentration, "gamma")
sta4.norm <- fitdist(sta4$Concentration, "norm")
sta4.pois <- fitdist(sta4$Concentration, "pois")
sta4.wei <- fitdist(sta4$Concentration, "weibull")
denscomp(list(sta4.gam, sta4.norm, sta4.pois, sta4.wei), legendtext = plot.legend)
qqcomp(list(sta4.gam, sta4.norm, sta4.pois, sta4.wei), legendtext = plot.legend)

# station 5 = Weibull - little skew 
plotdist(sta5$Concentration, histo = TRUE, demp = TRUE)
sta5.dist = outlierKD(sta5, sta5$Concentration) # 37 - 37
stat.sta5 = descdist(sta5$Concentration)

sta5.gam <- fitdist(sta5$Concentration, "gamma")
sta5.norm <- fitdist(sta5$Concentration, "norm")
sta5.pois <- fitdist(sta5$Concentration, "pois")
sta5.wei <- fitdist(sta5$Concentration, "weibull")
denscomp(list(sta5.gam, sta5.norm, sta5.pois, sta5.wei), legendtext = plot.legend)
qqcomp(list(sta5.gam, sta5.norm, sta5.pois, sta5.wei), legendtext = plot.legend)

# station 6 = Gamma - much more skewness
plotdist(sta6$Concentration, histo = TRUE, demp = TRUE)
sta6.dist = outlierKD(sta6, sta6$Concentration) # 29  - 25
stat.sta6 = descdist(sta6$Concentration)

sta6.gam <- fitdist(sta6$Concentration, "gamma")
sta6.norm <- fitdist(sta6$Concentration, "norm")
sta6.pois <- fitdist(sta6$Concentration, "pois")
sta6.wei <- fitdist(sta6$Concentration, "weibull")


denscomp(list(sta6.gam, sta6.norm, sta6.pois, sta6.wei), legendtext = plot.legend)
qqcomp(list(sta6.gam, sta6.norm, sta6.pois, sta6.wei), legendtext = plot.legend)

# station 7 = Weibull - much more skewness
plotdist(sta7$Concentration, histo = TRUE, demp = TRUE)
descdist(sta7$Concentration, boot = 1000)

sta7.dist = outlierKD(sta7, sta7$Concentration) # 32  - 29
stat.sta7 = descdist(sta7$Concentration)

sta7.gam <- fitdist(sta7$Concentration, "gamma")
sta7.norm <- fitdist(sta7$Concentration, "norm")
sta7.pois <- fitdist(sta7$Concentration, "pois")
sta7.wei <- fitdist(sta7$Concentration, "weibull")

denscomp(list(sta7.gam, sta7.norm, sta7.pois, sta7.wei), legendtext = plot.legend)
qqcomp(list(sta7.gam, sta7.norm, sta7.pois, sta7.wei), legendtext = plot.legend)

dev.off()
















x.norm <- rnorm(n=22919,m=38,sd=23.27878)
sta1.norm = hist(x.norm,main="Histogram of observed data")
plot(ecdf(x.norm),main="Empirical cumulative distribution function")
plot(density(x.norm),main="Density estimate of data")
z.norm<-(x.norm-mean(x.norm))/sd(x.norm) ## standardized data
qqnorm(z.norm) ## drawing the QQplot
abline(0,1) ## drawing a 45-degree reference line

sta2.dist = outlierKD(sta2, sta2$Concentration)
stat.sta2 = descdist(sta2$Concentration)
stat.sta2
x.norm2 <- rnorm(n=22599,m=33.74762,sd=21.84783)
sta2.norm = hist(x.norm2,main="Histogram of observed data")
plot(ecdf(x.norm2),main="Empirical cumulative distribution function")
plot(density(x.norm2),main="Density estimate of data")
z.norm2<-(x.norm2-mean(x.norm2))/sd(x.norm2) ## standardized data
qqnorm(z.norm2) ## drawing the QQplot
abline(0,1) ## drawing a 45-degree reference line





sta3.dist = outlierKD(sta3, sta3$Concentration)
sta4.dist = outlierKD(sta4, sta4$Concentration)
sta5.dist = outlierKD(sta5, sta5$Concentration)
stat.sta5 = descdist(sta5$Concentration)
stat.sta5
x.norm5 <- rnorm(n=23030,m=37.82353,sd=23.73178)
sta5.norm = hist(x.norm5,main="Histogram of observed data")
plot(ecdf(x.norm5),main="Empirical cumulative distribution function")
plot(density(x.norm5),main="Density estimate of data")
z.norm5<-(x.norm5-mean(x.norm5))/sd(x.norm5) ## standardized data
qqnorm(z.norm5) ## drawing the QQplot
abline(0,1) ## drawing a 45-degree reference line


x.wei<-rweibull(n=200,shape=2.1,scale=1.1) ## sampling from a Weibull
# distribution with parameters shape=2.1 and scale=1.1
x.teo<-rweibull(n=200,shape=2, scale=1) ## theorical quantiles from a
# Weibull population with known paramters shape=2 e scale=1
qqplot(x.teo,x.wei,main="QQ-plot distr. Weibull") ## QQ-plot
abline(0,1) ## a 45-degree reference line is plotted


sta6.dist = outlierKD(sta6, sta6$Concentration)
sta7.dist = outlierKD(sta7, sta7$Concentration)

install.packages("fBasics")
library(fBasics) 




