import pandas as pd
import os 
from datetime import datetime
from datetime import timedelta
import yfinance as yf
from bsm import RiskBSM
from RIskRate import Rate
import numpy as np
import fear_and_greed
import parsing
import Constant as myarg

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
            
    specified_date = datetime(year, mom, day) + timedelta(hours = 16)
  
    if myarg.Debug:
        print("ExDays",specified_date)

    time_interval = specified_date - myarg.getToday(myarg.offset_time)
    years = time_interval.days / 365.0

    return years if years > 0 else 0  

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

def GreenIndex():
    data = fear_and_greed.get()
    return data

def MarketBreath():
    data = parsing.main()
    return data

def DownLoad_Index():

    # Time < 12
    current_hour = datetime.now().hour
    if current_hour > 12:
        print('only save option oi , index data skip save')
        return 0

    greendata = GreenIndex()
    marketdata = MarketBreath()
    
    today = myarg.getToday(myarg.offset_time)
    today_date = today.strftime('%Y-%m-%d')

    
    ticker = yf.Ticker("SPY")
    ticker_data = ticker.history(period="1d")
    current_stock_price = ticker_data['Close'].iloc[0]


    data = pd.DataFrame({'Date' : [today_date],
            'SPY'  : [current_stock_price],
            'Fear' : [greendata.value],
            'MMTW' : [marketdata[0]],
            'MMFI' : [marketdata[1]],
            'MMOH' : [marketdata[2]],
            'MMTH' : [marketdata[3]]
    })

    filepath = os.path.join(myarg.disk_path,myarg.stock_path,"Index","Index.csv")
   
    if os.path.exists(filepath):
        alldf = pd.read_csv(filepath)
        alldf = pd.concat([alldf,data])
        alldf.to_csv(filepath,index=False)
    else:
        data.to_csv(filepath,index=False)

#def DownLoad_GreenIndex():
#    result = GreenIndex() 
#    today = myarg.getToday(myarg.offset_time)
#    today_date = today.strftime('%Y-%m-%d')
#    data = {'Date' : [today_date],
#       	    'Value':[result.value],
#            'Type' : [result.description]}
#    df = pd.DataFrame(data)
#
#    #Path = os.path.join(myarg.disk_path,myarg.stock_path,"Index",today_date,"CNNGreenIndex.csv")
#    #savefile(df,Path)


#def DownLoad_MarketBreath():
#    mbtype = ['MMTW','MMFI','MMTH']
#    alldf = pd.DataFrame()
#    result = MarketBreath()
#           
#    today = myarg.getToday(myarg.offset_time)
#    today_date = today.strftime('%Y-%m-%d')
#
#    for index,Name in enumerate(mbtype):
#        data = { 'Date' : [today_date],
#                 'Type' : [Name],
#                 'Value': result[index]
#               }  
#        df = pd.DataFrame(data)
#        alldf = pd.concat([alldf,df])
#
#    #Path = os.path.join(myarg.disk_path,myarg.stock_path,"Index",today_date,"MarketBreath.csv")
#    #savefile(alldf,Path)

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
     
    today = myarg.getToday(myarg.offset_time)
    today_date = today.strftime('%Y-%m-%d')   
    Path = os.path.join(myarg.disk_path,myarg.stock_path,name,today_date,"Data.csv")
    kBar = yf.download(tickers = name, period="1d", interval=Interval)
    savefile(kBar,Path)

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
   
    # Time < 12
    current_hour = datetime.now().hour
    if current_hour < 12:
        updateDataOnly = True
    else:
        updateDataOnly = False

    for index,exp_date in enumerate(options):
        option_chain = ticker.option_chain(options[index])
        allDF = pd.DataFrame()

        T = ExDays(exp_date) #Expiration date (days from now / 365)
        
        print("========= "+ name +" - "+ exp_date +" =========")

        if(dT == "C"):
            StrikeList = option_chain.calls['strike']
            total = len(option_chain.calls['strike'])
        else:
            StrikeList = option_chain.puts['strike']
            total = len(option_chain.puts['strike'])
        
        if(total == 0):
            print("StrikeList is empty , skip")
            continue

        for index, price in enumerate(StrikeList):
            if(dT == "C"):
                selected_option = option_chain.calls[StrikeList == price] 
            else:
                selected_option = option_chain.puts[StrikeList == price]

            K = selected_option['strike'].iloc[0]
            V = selected_option['impliedVolatility'].iloc[0] if not np.isnan(selected_option['impliedVolatility'].iloc[0]) else 0
            oi = selected_option['openInterest'].iloc[0] if not np.isnan(selected_option['openInterest'].iloc[0]) else 0
            volume = selected_option['volume'].iloc[0] if not np.isnan(selected_option['volume'].iloc[0]) else 0
            lastPrice = selected_option['lastPrice'].iloc[0] if not np.isnan(selected_option['lastPrice'].iloc[0]) else 0
            bid = selected_option['bid'].iloc[0] if not np.isnan(selected_option['bid'].iloc[0]) else 0
            ask = selected_option['ask'].iloc[0] if not np.isnan(selected_option['ask'].iloc[0]) else 0
            
            if myarg.Debug:
                print("S",S)
                print("K",K)
                print("V",V)
                print("T",T)
                print("dT",dT)
                print("r",r)
            
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

            print(f"==== Process {index+1}/{total} ====")

        print(allDF.to_string(index=False))

        Type = "calldata.csv" if dT == "C" else "putdata.csv"
        today = myarg.getToday(myarg.offset_time)
        today_date = today.strftime('%Y-%m-%d')
        Path = os.path.join(myarg.disk_path,myarg.op_path,name,exp_date,today_date,Type)
       
        if not os.path.exists(Path):
            bNewContract = True
            print('Catch New Contract')
        else:
            bNewContract = False
            print('Contract already exists')
        
        if updateDataOnly or bNewContract:
            print('Update Data')
            savefile(allDF,Path)
        else:
            print('Update OI and Calulate Greeks')
        
            allDF.reset_index(drop=True, inplace=True)
            
            originData = pd.read_csv(Path)
            originData.reset_index(drop=True, inplace=True)

            originData['OI'] = allDF['OI']
            savefile(originData,Path)
        print("")

        print("========================================")
