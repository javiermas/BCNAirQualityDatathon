auto_arima_mean <- function(x) {
      auto_fun <- auto.arima(x)
      forecast_aux <- forecast(auto_fun, 1)
      result <- as.numeric(forecast_aux$mean)
      return(result)
}

auto_arima_up_80 <- function(x) {
      auto_fun <- auto.arima(x)
      forecast_aux <- forecast(auto_fun, 1)
      result <- as.numeric(forecast_aux$upper)[1]
      return(result)
}

auto_arima_up_95 <- function(x) {
      auto_fun <- auto.arima(x)
      forecast_aux <- forecast(auto_fun, 1)
      result <- as.numeric(forecast_aux$upper)[2]
      return(result)
}

p10 <- function(x) {
      return(quantile(x, 0.1))
}

p25 <- function(x) {
      return(quantile(x, 0.25))
}

p75 <- function(x) {
      return(quantile(x, 0.75))
}

p90 <- function(x) {
      return(quantile(x, 0.9))
}

dist_log_gamma <- function(x) {
      dist <- fitdist(as.numeric(as.matrix(x)), "gamma")
      dist <- summary(dist)
      result <- as.numeric(dist$loglik)
      return(result)
}

dist_log_norm <- function(x) {
      dist <- fitdist(as.numeric(as.matrix(x)), "norm")
      dist <- summary(dist)
      result <- as.numeric(dist$loglik)
      return(result)
}

dist_log_weibull <- function(x) {
      dist <- fitdist(as.numeric(as.matrix(x)), "weibull")
      dist <- summary(dist)
      result <- as.numeric(dist$loglik)
      return(result)
}

