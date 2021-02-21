import datefinder
from datetime import datetime

def extract_date_diff(logger,string_with_dates,current_time):
    logger.info("Extracting date and time from log message")
    matches = datefinder.find_dates(string_with_dates)
    for log_time in matches:
        print(log_time)
    logger.info("Logging time is {}".format(log_time))
    difference = current_time - log_time
    total = difference.total_seconds()
    logger.info("Difference in both times in sec is {}".format(total))
    return total