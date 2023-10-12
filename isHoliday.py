import sys
from pandas_market_calendars import get_calendar
import Constant as myarg

today = myarg.getToday(myarg.offset_time)
today = today.strftime('%Y-%m-%d')
nyse = get_calendar('NYSE')


is_holidays = nyse.valid_days(start_date=today, end_date=today)

if is_holidays.empty:
    sys.exit(1)
else:
    sys.exit(0)

