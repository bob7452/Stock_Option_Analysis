import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


putpath = '/media/ponder/ADATA HM900/OptionData/2023-09-13/AAPL/2023-09-15/PUT/OptionData.csv'
callpath = '/media/ponder/ADATA HM900/OptionData/2023-09-13/AAPL/2023-09-15/CALL/OptionData.csv'

def replace_nan_with_zero(row):
    if np.isnan(row['TotalPain_x']) or np.isnan(row['TotalPain_y']):
        row['TotalPain_x'] = 0
        row['TotalPain_y'] = 0
    return row

def bePositive(value,x,isCall):
    
    index = 1 if isCall else -1
    result = (value - x) * index
    
    if result < 0:
        return 0
    else:
        return result

def CalPain(DataList,isCall):
    StrikeList = DataList['Strike']
    allDF = pd.DataFrame()

    for strike in StrikeList:
        Product = DataList['Strike'].apply(bePositive,args=(strike,isCall,)) * DataList['OI']
        Sum = Product.sum()
        data = {'Strike' : [strike] ,'TotalPain' : [Sum] }
        df = pd.DataFrame(data)
        allDF = pd.concat([allDF,df])
    
    return allDF


putdata  = pd.read_csv(putpath)
calldata = pd.read_csv(callpath)

callLen = len(calldata['Strike'])
putLen  = len(putdata['Strike'])


callPain = CalPain(calldata,1)
print(callPain)

putPain = CalPain(putdata,0)
print(putPain)

if len(callPain['Strike']) > len(putPain['Strike']):
    mainList = callPain
    subList  = putPain
else: 
    mainList = putPain
    subList  = callPain

# 使用 merge 方法将两个 DataFrame 合并，使用 'strike' 列作为连接键，并使用外连接方式（outer）确保保留所有 'strike' 值
merged_df = pd.merge(callPain, putPain, on='Strike', how='outer')

#merged_df = merged_df.apply(replace_nan_with_zero, axis=1)
merged_df=  merged_df.dropna()


print(merged_df)

# 计算 'value' 列的和，将结果存储在新的 'value' 列中
merged_df['TotalPain'] = merged_df['TotalPain_x'] + merged_df['TotalPain_y']

# 选择需要保留的列
result_df = merged_df[['Strike', 'TotalPain']]

# 打印合并后的结果
print(result_df)


result_df.to_csv('result.csv')
callPain.to_csv('callpain.csv')
putPain.to_csv('putpain.csv')

min_index = result_df['TotalPain'].idxmin()

# 使用最小值的索引获取对应的 'name' 值
min_name = result_df.loc[min_index, 'Strike']

# 打印最小值和对应的 'name' 值
print(" Min Loss : ", result_df['TotalPain'].min())
print(" Max Pain : ", min_name)
