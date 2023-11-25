import sys
from pandas_market_calendars import get_calendar
import Constant as myarg

def isholidays():
    today = myarg.getToday(myarg.offset_time)
    today = today.strftime('%Y-%m-%d')
    nyse = get_calendar('NYSE')
    
    
    is_holidays = nyse.valid_days(start_date=today, end_date=today)

    if is_holidays.empty:
        print('plz enjoy ur holidays')
        return 1
    else:
        print('Fighting')
        return 0

if __name__ == "__main__":
    ans = isholidays()

    if ans:
        sys.exit(1)
    else:
        sys.exit(0)
