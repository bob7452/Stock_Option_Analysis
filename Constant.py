from datetime import datetime
from datetime import timedelta
import os
import pandas as pd

Stock = ["QQQ","SPY","DIA","IWM",     \
         "AAPL","MSFT","GOOG","META", \
         "AMZN","TSLA","NVDA","TLT",  \
         "^Vix","SMH","NFLX","ARKK",  \
         "AMD","JPM", "U","XLB",      \
         "BITO","XLE","XHB","XLP",    \
         "XLV","XLU","XLI","XBI",     \
         "XLK","UVXY","SOXL","XLF",   \
         "KWEB"]

Type   = ["C","P"]
OptionType = ["CALL","PUT"]

disk_path = "/media/ponder/ADATA HM900/"

op_path   = 'OptionData'

stock_path = 'StockPriceData'

db_path   = 'DailyReport'

backup_path = 'BackUp'

DailyReprotPath = '/home/ponder/migoogledrive/Stock/Daily/'

daliy_picture   = "/home/ponder/migoogledrive/Stock/Daily/picture/"

Debug     = True

offset_time = 28

def getToday(offset = 0): 
    #today = datetime.date.today()
    #day_of_week = today.weekday()

    current = datetime.now()
    day_of_week = current.weekday()
    current_hour = current.hour

    print(f'today is week {day_of_week+1}')
    if day_of_week == 0:
        offset = 76

    print(f'time is {current_hour}:00')
    if current_hour < 12 :
        print('operation save data mission')
        offset = 16

    current = current - timedelta(hours=offset)
    return current

def find_third_friday(input_date,name):
    # 轉換輸入日期為datetime物件
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    print(f'input date {input_date}')

    # 找出這個月的第一天
    first_day_of_month = datetime(input_date.year, input_date.month, 1)
    
    # 找出這個月的第一個星期五
    first_friday = first_day_of_month + timedelta(days=(4 - first_day_of_month.weekday() + 7) % 7)
    
    # 找出這個月的第三週的星期五
    third_friday = first_friday + timedelta(days=14)
    print(f'third_friday {third_friday}')
    
    if name == "^Vix":
        third_friday = third_friday - timedelta(days=2)
        print(f'^Vix {third_friday}')
    
    # 比較輸入日期是否超過第三週的星期五，如果超過則加一個月
    if input_date > third_friday:
        next_month = input_date.replace(day=1) + timedelta(days=32)  # 加一個月
        first_day_of_next_month = datetime(next_month.year, next_month.month, 1)
        first_friday = first_day_of_next_month + timedelta(days=(4 - first_day_of_next_month.weekday() + 7) % 7)
        third_friday = first_friday + timedelta(days=14)
        print(f'Go On Next Month {third_friday}')
    
    if name == "^Vix":
        ans_day = third_friday - timedelta(days=2)
        print(f'^Vix {ans_day}')
    else:
        ans_day = third_friday
        print(f'others {ans_day}')

    return ans_day.strftime('%Y-%m-%d')

class IOTool:
    def __init__(self) -> None:
        pass

    def list_subdirectories(self,path):
        subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return subdirectories    

    def savefile(instance : pd.DataFrame,FilePath):

        directory = os.path.dirname(FilePath)

        if not os.path.exists(directory):
            os.makedirs(directory)

        instance.to_csv(FilePath)
