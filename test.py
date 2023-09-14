import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


putpath = '/media/ponder/ADATA HM900/OptionData/2023-09-11/AAPL/2023-09-15/PUT/OptionData.csv'
callpath = '/media/ponder/ADATA HM900/OptionData/2023-09-11/AAPL/2023-09-15/CALL/OptionData.csv'

def dataFilting(df):
    x = df['Strike'].values
    y = df['TotalPain'].values
    f = interp1d(x, y, kind='quadratic', fill_value='extrapolate')

    df['TotalPain'] = df.apply(lambda row: f(row['Strike']) if np.isnan(row['TotalPain']) else row['TotalPain'], axis=1)

    return df

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

merged_df = merged_df.apply(replace_nan_with_zero, axis=1)

print(merged_df)

# 计算 'value' 列的和，将结果存储在新的 'value' 列中
merged_df['TotalPain'] = merged_df['TotalPain_x'] + merged_df['TotalPain_y']

# 选择需要保留的列
result_df = merged_df[['Strike', 'TotalPain']]

# 打印合并后的结果
print(result_df)

result_df = dataFilting(result_df)

print(result_df)

result_df.to_csv('result.csv')

#merged_df = mainList.merge(subList, on='Strike', how='outer').fillna(0)

#merged_df['TotalPain'] = merged_df['TotalPain_x'] + merged_df['TotalPain_y']
#
#merged_df = merged_df.drop(['TotalPain_x', 'TotalPain_y'], axis=1)
#


#for strike,index in enumerate(mainList['Strike']):
#    has_value = strike in subList['Strike'].values
#    
#    if has_value:
#        subindex  = subList[subList['Strike']==strike].index.tolist()
#        totalPain = mainList['TotalPain'].iloc[index]+subList['TotalPain'].iloc[subindex]
#    else:
#        totalPain = mainList['TotalPain'].iloc[index]
#
#    data = {'Strike' : [strike] , 'TotalPain' : [totalPain]}
#    df = pd.DataFrame(data)
#    resDF = pd.concat([resDF,df])
#
#
#print(merged_df)

# 找到 'value' 列的最小值的索引
#min_index = merged_df['TotalPain'].idxmin()

# 使用最小值的索引获取对应的 'name' 值
#min_name = merged_df.loc[min_index, 'Strike']

#print("Max Pain Strike : ", min_name)
#print("Total Loss : ",merged_df['TotalPain'].min())


#callPain.to_csv("callpain.csv")
#putPain.to_csv("putpain.csv")
#merged_df.to_csv("output.csv")






