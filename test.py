import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


putpath = '/media/ponder/ADATA HM900/OptionData/2023-09-13/AAPL/2023-09-15/PUT/OptionData.csv'
callpath = '/media/ponder/ADATA HM900/OptionData/2023-09-13/AAPL/2023-09-15/CALL/OptionData.csv'
debug = 1


def replace_nan_with_zero(row):
    if np.isnan(row['TotalPain_x']) or np.isnan(row['TotalPain_y']):
        row['TotalPain_x'] = 0
        row['TotalPain_y'] = 0
    return row

def bePositive(value,x,isCall):
    
    if isCall:
        result = x-value
    else:
        result = value-x
    
    if result < 0:
        return 0
    else:
        return result

def CalculateSum(strike,df,isCall):
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
        df = CalculateSum(strike,mainList,isMainCall)
        totalMainDF = pd.concat([totalMainDF,df])

        df = CalculateSum(strike,subList,not isMainCall)
        totalSubDF  = pd.concat([totalSubDF,df])
#        Product = mainList['Strike'].apply(bePositive,args=(strike,isCall,)) * DataList['OI']
#        Sum = Product.sum()
#        data = {'Strike' : [strike] ,'TotalPain' : [Sum] }
#        df = pd.DataFrame(data)
#        allDF = pd.concat([allDF,df])
    
    return totalMainDF,totalSubDF


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

if debug :
    callPain = maindf if isCall else subdf
    putPain  = subdf  if isCall else maindf
    callPain.to_csv('callpain.csv')
    putPain.to_csv('putpain.csv')
    print(callPain)
    print(putPain)

merged_df = pd.merge(maindf, subdf, on='Strike', how='outer')

merged_df=  merged_df.dropna()

merged_df['TotalPain'] = merged_df['TotalPain_x'] + merged_df['TotalPain_y']

result_df = merged_df[['Strike', 'TotalPain']]

print(result_df)


result_df.to_csv('result.csv')

min_index = result_df['TotalPain'].idxmin()

# 使用最小值的索引获取对应的 'name' 值
min_name = result_df.loc[min_index, 'Strike']

# 打印最小值和对应的 'name' 值
print(" Min Loss : ", result_df['TotalPain'].min())
print(" Max Pain : ", min_name)
