import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

KEYS = ['Delta','Gamma','Theta','Vega','IV','OI','volume']

def sumPain(maindf,subdf,debug):

    merged_df = pd.merge(maindf, subdf, on='Strike', how='outer') 
    merged_df=  merged_df.dropna()
    
    merged_df['TotalPain'] = merged_df['TotalPain_x'] + merged_df['TotalPain_y']
    result_df = merged_df[['Strike', 'TotalPain']]

    min_index = result_df['TotalPain'].idxmin()
    strike      = result_df.loc[min_index, 'Strike']
    min_loss    = result_df['TotalPain'].min()

    print(" Min Loss : ", result_df['TotalPain'].min())
    print(" Max Pain : ", strike)

    if debug :
        result_df.to_csv('result.csv')
        print(result_df)

    return strike,min_loss 

def bePositive(value,x,isCall):
    
    if isCall:
        result = x-value
    else:
        result = value-x
    
    if result < 0:
        return 0
    else:
        return result

def calPainSum(strike,df,isCall):
    temp = pd.DataFrame()
    Product = df['Strike'].apply(bePositive,args=(strike,isCall,)) * df['OI']
    Sum = Product.sum()
    data = {'Strike' : [strike] ,'TotalPain' : [Sum] }
    temp = pd.DataFrame(data)
    return temp 

def CalPain(mainList,subList,isMainCall):
    StrikeList = mainList['Strike']
    totalMainDF = pd.DataFrame()
    totalSubDF  = pd.DataFrame()
    

    for strike in StrikeList:
        df = pd.DataFrame()
        df = calPainSum(strike,mainList,isMainCall)
        totalMainDF = pd.concat([totalMainDF,df])

        df = calPainSum(strike,subList,not isMainCall)
        totalSubDF  = pd.concat([totalSubDF,df])
    
    return totalMainDF,totalSubDF

def CalGex(calldata,putdata):
    callGEX = calldata['OI'] * calldata['Gamma']
    putGEX  = putdata['OI']  * putdata['Gamma']

    totalGEX = callGEX.sum() - putGEX.sum()
    return totalGEX

def sumKeyData(data,key=""):
    if key != "":
        return data[key].sum()

    ans = []
    for keys in KEYS:
        ans.append(data[keys].sum())
    return ans

def main(callpath,putpath,debug=0):
    putdata  = pd.read_csv(putpath)
    calldata = pd.read_csv(callpath)
    
    callLen = len(calldata['Strike'])
    putLen  = len(putdata['Strike'])
    
    if callLen > putLen:
        mainList = putdata
        subList  = calldata
        isCall   = False
    else: 
        mainList = calldata
        subList  = putdata
        isCall   = True
    
    maindf , subdf = CalPain(mainList,subList,isCall)
    strikePrice , min_loss  = sumPain(maindf,subdf,debug)

    callKeySum = sumKeyData(calldata)
    putKeySum  = sumKeyData(putdata)
    Gex        = CalGex(calldata,putdata)
    
    #KEYS = ['Delta','Gamma','Theta','Vega','IV','OI','volume']
    data = { 'MaxPainStrike' : [strikePrice], 
             'MinLoss'    : [min_loss],
             'Gex'        : [Gex],
             'CallDelta'  : [callKeySum[0]],
             'CallGamma'  : [callKeySum[1]],
             'CallTheta'  : [callKeySum[2]],
             'CallVega'   : [callKeySum[3]],
             'CallIV'     : [callKeySum[4]],
             'CallOI'     : [callKeySum[5]],
             'Callvolume' : [callKeySum[6]],
             'putDelta'   : [putKeySum[0]],
             'putGamma'   : [putKeySum[1]],
             'putTheta'   : [putKeySum[2]],
             'putVega'    : [putKeySum[3]],
             'putIV'      : [putKeySum[4]],
             'putOI'      : [putKeySum[5]],
             'putvolume'  : [putKeySum[6]]
            }
    
    df = pd.DataFrame(data)
    return df    

#if __name__ == "__main__":
#    putpath  = '/media/ponder/ADATA HM900/OptionData/2023-09-11/AAPL/2023-09-15/PUT/OptionData.csv'
#    callpath = '/media/ponder/ADATA HM900/OptionData/2023-09-11/AAPL/2023-09-15/CALL/OptionData.csv'
#    data = main(callpath,putpath,1)   
#    print(data)

