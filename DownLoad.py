import pandas as pd
import os 
from datetime import datetime
import yfinance as yf
from bsm import RiskBSM
from RIskRate import Rate
import numpy as np

def savefile(df,dT,name,date):

    if dT == "C":
        dT = "CALL"
    else:
        dT = "PUT"

    today_date = datetime.today().strftime('%Y-%m-%d')
    Path = "/media/ponder/ADATA HM900/OptionData/"
    Path = Path+"/"+dT+"/"+name+"/"+today_date+"/"+date+"/"
    directory = os.path.dirname(Path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    Path = Path + "OptionData.csv"
    df.to_csv(Path, index=False)

def ExDays(date):
    year,mom,day = date.split("-")
    day = int(day)
    mom = int(mom)
    year = int(year)
            
    specified_date = datetime(year, mom, day)
    current_date = datetime.now()
    time_interval = specified_date - current_date
    years = time_interval.days / 365.0

    return years

def DownLoad_Data(name,dT):
    print("Stock Name : " + name + " " + dT)

    # Model Select
    calc = RiskBSM()

    ## Initialize Ticket Param
    ticker = yf.Ticker(name)
    options = ticker.options
    ticker_data = ticker.history(period="1d")
    current_stock_price = ticker_data['Close'].iloc[0]

    ## Option Value 
    S = current_stock_price 
    r = Rate.riskfree() / 100
    

    for index,exp_date in enumerate(options):
        option_chain = ticker.option_chain(options[index])
        allDF = pd.DataFrame()

        T = ExDays(exp_date) #Expiration date (days from now / 365)
        
        print("========= "+ name +" - "+ exp_date +" =========")
        total = len(option_chain.calls['strike'])

        for index, price in enumerate(option_chain.calls['strike']):

            selected_call_option = option_chain.calls[option_chain.calls['strike'] == price] 

            K = selected_call_option['strike'].iloc[0]
            V = selected_call_option['impliedVolatility'].iloc[0] if not np.isnan(selected_call_option['impliedVolatility'].iloc[0]) else 0
            oi = selected_call_option['openInterest'].iloc[0] if not np.isnan(selected_call_option['openInterest'].iloc[0]) else 0
            volume = selected_call_option['volume'].iloc[0] if not np.isnan(selected_call_option['volume'].iloc[0]) else 0
            lastPrice = selected_call_option['lastPrice'].iloc[0] if not np.isnan(selected_call_option['lastPrice'].iloc[0]) else 0
            bid = selected_call_option['bid'].iloc[0] if not np.isnan(selected_call_option['bid'].iloc[0]) else 0
            ask = selected_call_option['ask'].iloc[0] if not np.isnan(selected_call_option['ask'].iloc[0]) else 0
                
            Theo = round(calc.theo(S, K, V, T, dT,r), 4)
            Delta  = round(calc.delta(S, K, V, T, dT,r), 4)
            Theta  = round(calc.theta(S, K, V, T,r), 4)
            Vega   = round(calc.vega(S, K, V, T,r), 4)
            Gamma  = round(calc.gamma(S, K, V, T,r), 4)

            data = { 'Date'  : [exp_date],
                    'CurrentPrice' : [S],
                    'Strike' : [price],
                    'OI' : [oi],
                    'volume': [volume],
                    'lastPrice' : [lastPrice],
                    'bid'   : [bid],
                    'ask'   : [ask],
                    'Theo Price' : [Theo],
                    'Delta' : [Delta],
                    'Gamma' : [Gamma],
                    'Theta' : [Theta],
                    'Vega'  : [Vega],
                    'IV' : [V],
                    'Rate(1Y)' : [r],
                    }
            df = pd.DataFrame(data)
            allDF = pd.concat([allDF,df])


            print(f"==== Process {index+1}/{total} ====")

        print(allDF.to_string(index=False))
        savefile(allDF,dT,name,exp_date)
        print("")
        print("========================================")
