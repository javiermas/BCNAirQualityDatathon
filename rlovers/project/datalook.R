library(pacman)
p_load(tidyverse, stringr, lubridate, reshape, tidyquant, forecast, progress)

data_obs_read <- read_csv(file = "data/all_obs.csv")
data_model_read <- read_csv(file = "data/all_models.csv")

target_dates <- read_csv("data/targets.csv") %>% 
      dplyr::select(date) %>% unique()

data_obs_date_fix <- data_obs_read %>% 
      dplyr::group_by(DatetimeBegin, AirQualityStationEoICode, Concentration) %>% 
      dplyr::mutate(row_number_aux = 1:n()) %>% 
      dplyr::filter(row_number(row_number_aux) == 1) %>% 
      dplyr::select(-one_of("X1")) %>% 
      dplyr::group_by(DatetimeBegin, AirQualityStationEoICode) %>% 
      dplyr::select(one_of("DatetimeBegin", "AirQualityStationEoICode"))

data_model_date_fix <- data_model_read %>% 
      tidyr::drop_na() %>% 
      dplyr::mutate(DatetimeBegin = ymd_hms(paste(day, hour))) %>% 
      dplyr::select(-one_of("X1", "year", "AirPollutant", "day", "hour")) %>% 
      dplyr::select(one_of("DatetimeBegin", "station")) %>% 
      dplyr::rename(AirQualityStationEoICode = station)

dates_data_tot <- data_obs_date_fix %>% 
      dplyr::full_join(data_model_date_fix) %>% 
      dplyr::group_by(DatetimeBegin, AirQualityStationEoICode) %>% 
      dplyr::mutate(row_number_aux = 1:n()) %>% 
      dplyr::filter(row_number(row_number_aux) == 1) %>% 
      dplyr::select(-one_of("row_number_aux"))
      
data_obs <- data_obs_read %>%
      dplyr::group_by(DatetimeBegin, AirQualityStationEoICode, Concentration) %>% 
      dplyr::mutate(row_number_aux = 1:n()) %>% 
      dplyr::filter(row_number(row_number_aux) == 1) %>% 
      dplyr::select(-one_of("X1")) %>% 
      dplyr::select(one_of(c("AirQualityStationEoICode", "Concentration", "DatetimeBegin"))) %>% 
      dplyr::rename(conc_obs = Concentration)

data_model_aux <- data_model_read %>% 
      tidyr::drop_na() %>% 
      dplyr::mutate(DatetimeBegin = ymd_hms(paste(day, hour))) %>% 
      dplyr::select(-one_of("X1", "year", "AirPollutant", "day", "hour")) %>% 
      dplyr::select(one_of("DatetimeBegin", "station", "Concentration")) %>% 
      dplyr::rename(AirQualityStationEoICode = station, conc_model = Concentration) %>% 
      dplyr::group_by(AirQualityStationEoICode, DatetimeBegin) %>% 
      dplyr::mutate(model = 1:n())

data_model_1 <- data_model_aux %>% 
      dplyr::filter(model == 1) %>% 
      dplyr::rename(conc_model_1 = conc_model) %>% 
      dplyr::select(-one_of("model"))
data_model_2 <- data_model_aux %>% 
      dplyr::filter(model == 2) %>% 
      dplyr::rename(conc_model_2 = conc_model) %>% 
      dplyr::select(-one_of("model"))
data_model <- data_model_1 %>% 
      dplyr::left_join(data_model_2) %>% 
      tidyr::drop_na()

data_tot_ini <- dates_data_tot %>% 
      dplyr::left_join(data_obs) %>% 
      dplyr::left_join(data_model) %>%
      dplyr::rename(station = AirQualityStationEoICode, timeb = DatetimeBegin,
                    conc_obs = Concentration) %>%
      dplyr::mutate(date = as.Date(timeb), day = day(timeb), month = month(timeb), year = year(timeb), 
                    week = week(timeb)) %>% 
      dplyr::filter(year < 2016)

data_tot <- data_tot_ini %>%
      dplyr::group_by(timeb) %>% 
      dplyr::mutate(conc_obs = ifelse(is.na(conc_obs), mean(conc_obs, na.rm = TRUE), conc_obs),
                    conc_model_1 = ifelse(is.na(conc_model_1), mean(conc_model_1, na.rm = TRUE), 
                                          conc_model_1),
                    conc_model_2 = ifelse(is.na(conc_model_2), mean(conc_model_2, na.rm = TRUE), 
                                          conc_model_2)) %>% 
      dplyr::group_by(station, date) %>% 
      summarise(conc_obs = max(conc_obs, na.rm = TRUE), 
                conc_model_1 = max(conc_model_1, na.rm = TRUE),
                conc_model_2 = max(conc_model_2, na.rm = TRUE),
                day = max(day),
                month = max(month),
                year = max(year),
                week = max(week)) %>% 
      dplyr::group_by(station) %>% 
      dplyr::mutate(conc_obs_lag1 = lag(conc_obs)) %>% 
      dplyr::group_by(station) %>% 
      dplyr::mutate(conc_obs_lag2 = lag(conc_obs_lag1)) %>% 
      dplyr::filter(date >= "2013-01-03")

data_lm <- data_tot %>% 
      dplyr::filter(year < 2015)
      
reg_coef <- lm(conc_obs~., data = data_lm)

data_tot_lm <- data_tot %>% 
      dplyr::mutate(conc_obs = ifelse(conc_obs == -Inf, predict(reg_coef), conc_obs)) %>% 
      dplyr::mutate(target = ifelse(conc_obs > 100, 1, 0)) %>% 
      dplyr::group_by(station) %>% 
      dplyr::mutate(conc_obs_lag1 = lag(conc_obs)) %>% 
      dplyr::group_by(station) %>% 
      dplyr::mutate(conc_obs_lag2 = lag(conc_obs_lag1)) %>% 
      dplyr::mutate(target_lag1 = lag(target)) %>%
      dplyr::mutate(target_lag2 = target_lag1) %>%      
      dplyr::filter(date >= "2013-01-05") %>% 
      dplyr::ungroup() %>% 
      dplyr::mutate(row_ind = NA) %>%
      dplyr::mutate(conc_model_lm = ifelse(is.na(row_ind), predict(reg_coef))) %>% 
      dplyr::select(-one_of("row_ind"))

width_vector <- seq(2, 90)
functions_vector <- c("mean", "median", "sd", "min", "max", "p10", "p25", "p75", "p90", 
                      "kurtosis", "skewness")

data_roll_day <- data_tot_lm %>% 
      dplyr::group_by(station)

colnames_aux <- c("conc_obs", "conc_model_1", "conc_model_2")

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
