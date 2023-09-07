import yfinance as yf
import pandas as pd
from bsm import BSM
from datetime import datetime

def ExDays(date):
    year,mom,day = date.split("-")
    day = int(day)
    mom = int(mom)
    year = int(year)
            
    # 指定日期（2024年6月21日）
    specified_date = datetime(year, mom, day)

    # 当前日期
    current_date = datetime.now()

    # 计算时间间隔
    time_interval = specified_date - current_date

    # 获取时间间隔的年数
    years = time_interval.days / 365.0

    return years

calc = BSM()



if __name__ == "__main__":

    # 創建yfinance的Ticker對象
    ticker = yf.Ticker("TSLA")

    # 獲取QQQ的期權數據
    options = ticker.options

    # 打印可用的期權到期日期
    print("可用的期權到期日期：")
    for exp_date in options:
        print(exp_date)

    # 選擇一個到期日期
    selected_exp_date = options[3]

    # 獲取選定到期日期的期權鏈
    option_chain = ticker.option_chain(selected_exp_date)

    print(selected_exp_date)

    # 打印買權合約
    print("買權合約：")
    print(option_chain.calls)

    # 打印賣權合約
    print("賣權合約：")
    print(option_chain.puts)

    selected_call_option = option_chain.calls[option_chain.calls['strike'] == 240]

    # 打印行使價為300的買權合約
    print("行使價為240的買權合約：")
    print(selected_call_option)


        
    # 获取QQQ的实时数据
    tsladata = ticker.history(period="1d")

    # 获取当前股价
    current_stock_price = tsladata['Close'].iloc[0]

    # 設定期權相關參數

    S = current_stock_price
    K = selected_call_option['strike'].iloc[0]     # 行使價格
    V = selected_call_option['impliedVolatility'].iloc[0] # 波動率
    T = ExDays(selected_exp_date) #Expiration date (days from now / 365)
    dT = "C" #Call / Put

    print('Theo: ', round(calc.theo(S, K, V, T, dT), 2))
    print('Delta: ', round(calc.delta(S, K, V, T, dT), 2))
    print('Theta: ', round(calc.theta(S, K, V, T), 2))
    print('Vega: ', round(calc.vega(S, K, V, T), 2))
    print('Gamma: ', round(calc.gamma(S, K, V, T), 2))

