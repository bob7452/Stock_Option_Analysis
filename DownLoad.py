import pandas as pd
import os 
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import yahooquery as yfq
from bsm import RiskBSM
from RIskRate import Rate
import numpy as np

def savefile(df,FilePath,findex = False):

    directory = os.path.dirname(FilePath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(FilePath, index=findex)

def ExDays(date):
    year,mom,day = date.split("-")
    day = int(day)
    mom = int(mom)
    year = int(year)
            
    specified_date = datetime(year, mom, day)
    current_date = datetime.now()
    newyork_date = current_date - timedelta(hours=12)
    time_interval = specified_date - newyork_date
    years = time_interval.days / 365.0

    return years    

def specialName(name):
    if name == "^Vix":
        return "VIXW"
    else:
        return str(name)

def CombineOptionName(name,price,optionType,ExDate):
    
    fNumber = int(price * 1000)
    fNumber = f'{fNumber:08d}'
    name    = specialName(name)
    date_string = ExDate
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_object.strftime("%y%m%d")

    contractName = name+formatted_date+optionType+fNumber
    print(f"contractName = {contractName}")
    return contractName

def DownLoad_Data(name,DLType,OptionType,Iterval="1m"):

    if DLType == 0:
        print("Start Download Option Data")
        DownLoad_Option(name,OptionType)
    elif DLType == 1:
        print(f"Start Download Stock Data , Iterval ={Iterval}")
        DownLoad_StockBar(name,Iterval)
    else:
        print(f"Start Download Stock & Option Data , Iterval = {Iterval}")
        DownLoad_Option(name,OptionType)
        DownLoad_StockBar(name,Iterval)

def DownLoad_StockBar(name,Interval="1m"):
    Path = "/media/ponder/ADATA HM900/StockPriceData/"
    today_date = datetime.today().strftime('%Y-%m-%d')
    Path = Path+"/"+today_date+"/"+name+"/"+"Data.csv"
    kBar = yf.download(tickers = name, period="1d", interval=Interval)
    savefile(kBar,Path,True)

def DownLoad_OptionBar(name,price,dT,exp_date,Interval="1m"):
    Path = "/media/ponder/ADATA HM900/StockPriceData/"
    today_date = datetime.today().strftime('%Y-%m-%d')
    Name = CombineOptionName(name,price,dT,exp_date)
    Path = Path+"/"+today_date+"/"+name+"/"+dT+"/"+exp_date+"/"+Name+".csv"
    kBar = yf.download(tickers=Name, period="3d", interval=Interval)
    savefile(kBar,Path,True)

def DownLoad_Option(name,dT):
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

        if T < 0 :
            continue
        
        print("========= "+ name +" - "+ exp_date +" =========")
        total = len(option_chain.calls['strike'])

        if(dT == "C"):
            StrikeList = option_chain.calls['strike']
        else:
            StrikeList = option_chain.puts['strike']

        for index, price in enumerate(StrikeList):
            if(dT == "C"):
                selected_call_option = option_chain.calls[option_chain.calls['strike'] == price] 
            else:
                selected_call_option = option_chain.puts[option_chain.puts['strike'] == price]

            K = selected_call_option['strike'].iloc[0]
            V = selected_call_option['impliedVolatility'].iloc[0] if not np.isnan(selected_call_option['impliedVolatility'].iloc[0]) else 0
            oi = selected_call_option['openInterest'].iloc[0] if not np.isnan(selected_call_option['openInterest'].iloc[0]) else 0
            volume = selected_call_option['volume'].iloc[0] if not np.isnan(selected_call_option['volume'].iloc[0]) else 0
            lastPrice = selected_call_option['lastPrice'].iloc[0] if not np.isnan(selected_call_option['lastPrice'].iloc[0]) else 0
            bid = selected_call_option['bid'].iloc[0] if not np.isnan(selected_call_option['bid'].iloc[0]) else 0
            ask = selected_call_option['ask'].iloc[0] if not np.isnan(selected_call_option['ask'].iloc[0]) else 0
                
            Theo   = round(calc.theo(S, K, V, T, dT,r), 4)
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

            # if volume != 0:
            #     DownLoad_OptionBar(name,price,dT,exp_date) 
            print(f"==== Process {index+1}/{total} ====")

        print(allDF.to_string(index=False))

        today_date = datetime.today().strftime('%Y-%m-%d')
        Path = "/media/ponder/ADATA HM900/OptionData/"
        Type = "CALL" if dT == "C" else "PUT"
        Path = Path+"/"+today_date+"/"+name+"/"+exp_date+"/"+Type+"/"+"OptionData.csv"
        savefile(allDF,Path)
        print("")

        print("========================================")
