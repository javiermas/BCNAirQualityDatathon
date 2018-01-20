library(pacman)
p_load(tidyverse, stringr, lubridate, reshape, tidyquant, forecast, progress)

data_obs_read <- read_csv(file = "data/all_obs.csv")

data_obs <- data_obs_read %>% 
      dplyr::select(-one_of("X1")) %>% 
      dplyr::select(one_of(c("AirQualityStationEoICode", "Concentration", "DatetimeBegin"))) %>% 
      dplyr::rename(station = AirQualityStationEoICode, conc_obs = Concentration, timeb = DatetimeBegin) %>%
      dplyr::mutate(date = as.Date(timeb), day = day(timeb), month = month(timeb), year = year(timeb), 
                    week = week(timeb), hour = hour(timeb)) %>%
      dplyr::group_by(station, date) %>%
      dplyr::mutate(max_conc_obs_per_day = max(conc_obs)) %>% 
      dplyr::mutate(target = ifelse(max_conc_obs_per_day > 100, 1, 0))

data_model_read <- read_csv(file = "data/all_models.csv")

data_model <- data_model_read %>% 
      dplyr::select(-one_of("X1", "year", "AirPollutant")) %>%
      dplyr::rename(conc_model = Concentration, date = day) %>% 
      dplyr::mutate(hour = hour(hour), date = as.Date(date)) %>% 
      dplyr::group_by(station, date) %>% 
      dplyr::summarise(conc_models_mean = mean(conc_model))
      

data_tot <- data_obs %>% dplyr::left_join(data_model)

width_vector <- seq(2, 90)
functions_vector <- c("mean", "median", "sd", "min", "max", "p10", "p25", "p75", "p90", 
                      "kurtosis", "skewness")

data_roll_day <- data_tot %>% 
      dplyr::group_by(station, date) %>%
      dplyr::summarise(max_conc_obs = max(conc_obs), max_conc_models_mean = max(conc_models_mean))

colnames_aux <- c("max_conc_obs", "max_conc_models_mean")

total_var <- length(functions_vector) * length(width_vector) * length(colnames_aux)
pb <- progress_bar$new(total = total_var)
for(i in 1:length(functions_vector)) {
      for(j in 1:length(width_vector)) {
            for(h in 1:length(colnames_aux)) {
                  data_roll_day <- data_roll_day %>% 
                        tq_mutate_(select     = colnames_aux[h], 
                                   mutate_fun = "rollapply",
                                   width      = width_vector[j],
                                   FUN        = functions_vector[i],
                                   col_rename = paste0(colnames_aux[h],
                                                       "_", functions_vector[i], "_", 
                                                       width_vector[j]))
                  pb$tick()
                  Sys.sleep(1 / total_var)
            }
      }
}

write_csv(data_roll_day, "data/data_roll_day.csv")
