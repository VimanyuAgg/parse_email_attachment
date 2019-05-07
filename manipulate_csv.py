from csv import reader, writer
import datetime
import os
import re
import get_attachment
import logging
import sys
import traceback

today_date = str(datetime.datetime.now()).split(" ")[0]
current_path = os.path.dirname(os.path.realpath(__file__))



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-info.log'))
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-error.log'))
error_handler.setLevel(logging.ERROR)

debug_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-debug.log'))
debug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(debug_handler)


def format_date(dt):
    try:
        date_obj = datetime.datetime.strptime(dt, '%m/%d/%y')
        return datetime.datetime.strftime(date_obj, '%Y-%m-%d')
    except ValueError as e:
        try:
            date_obj = datetime.datetime.strptime(dt, '%m/%d/%Y')
            return datetime.datetime.strftime(date_obj, '%Y-%m-%d')
        except ValueError as e:
            return dt


def getQuarterStartDate():
    '''Returns the date of starting of current quarter'''
    current_year, current_month, current_dt = today_date.split("-")
    current_month = int(current_month)

    if current_month <=3:
        comp_date = datetime.datetime.strptime(str(current_year)+"-01-01",'%Y-%m-%d')
        return comp_date
    elif current_month <=6:
        # Map to Q4 of previous year & compare dt with Q3 begin date
        comp_date = datetime.datetime.strptime(str(current_year)+"-04-01", '%Y-%m-%d')
        return comp_date

    elif current_month <=9:
        # Map to Jan 1 of current year and compare with dt
        comp_date = datetime.datetime.strptime(str(current_year)+"-07-01", '%Y-%m-%d')
        return comp_date

    elif current_month <=12:
        # Map to Apr 1 of current year and compare with dt
        comp_date = datetime.datetime.strptime(str(current_year)+"-10-01", '%Y-%m-%d')
        return comp_date


def manipulate_csv():
    out = writer(open(os.path.join(current_path,get_attachment.FINAL_CSV), "w"), delimiter="|")

    for line in reader(open(os.path.join(current_path, get_attachment.BASEFILE), "r"), delimiter=","):
        try:
            if int(line[0]) > 3 and line[0].find(",") != -1:

                for i in range(len(line)):
                    if isinstance(line[i],str) and ("|" in line[i]):
                        line[i] = line[i].replace("|", "")

                new_line = [datetime.date.today().strftime('%b-%d-%Y')] + line
                out.writerow(new_line)
        except ValueError as e:
            logger.info(f"Expected error: {e} in line: {line}")
            logger.info(traceback.format_exc())


if __name__ == "__main__":
    manipulate_csv()


