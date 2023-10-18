import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from Constant import *
import yfinance as yf

class DATAPLOT:
    __Key = [
            'DEX',
            'GEX',
            'P-C IV'
    ]
    __Color = [
        '#ADD8E6' , #lightpurple
        '#FFB6C1', #lightblue
    ]

    def __init__(self,subSize,data_y_list,date,title,path):
        self.__subSize = subSize
        self.__data_y_list = data_y_list
        self.__date = date
        self.__gs = 0
        self.__title = title
        self.__path = path

    def __createPlot(self):
        fig = plt.figure(figsize=(12,8))
        height_ratios = [1] * self.__subSize  # Equal height for each subplot
        self.__gs = gridspec.GridSpec(self.__subSize, 1, \
                                      height_ratios=height_ratios, \
                                      hspace=0.1, wspace=0.1, top=0.9, \
                                      bottom=0.1, left=0.1, right=0.9)
    
    def _Plot(self):
        self.__createPlot()

        dataMax = [max(data) for data in self.__data_y_list]
        dataMin = [min(data) for data in self.__data_y_list]

        for index in range(self.__subSize):
            ax = plt.subplot(self.__gs[index])
            data = self.__data_y_list[index]
            maxBoundary = dataMax[index]
            minBoundary = dataMin[index]
            name = self.__Key[index]
            color = self.__Color[index%2]
            # 繪製 data1 柱狀圖（上面的子圖）
    
            ax.bar(self.__date,data,color=color,label = name)
            ax.axhline(y=maxBoundary, color='#ff0000', linestyle='--', label=f'{name} Upper Bound {round(maxBoundary,2)}')
            ax.axhline(y=minBoundary, color='g', linestyle='--', label=f'{name} Lower Bound {round(minBoundary,2)}') 
            ax.set_ylabel(f'Value ({name})')
            ax.legend(loc='upper left')
            ax.grid(True)

            if index != self.__subSize - 1:  # Hide x-axis labels for all subplots except the last one
                ax.set_xticks([])


        # 調整日期標籤的顯示角度
        plt.xticks(rotation=45, ha='right')

        # 加上大標題
        plt.suptitle(str(self.__title), fontsize=16)

        # 顯示圖表
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(str(self.__path)+'.png',dpi = 300)
        #plt.show()

def historical_volatility(stock_name, window_size=30):
    tickets = yf.download(stock_name, period='3y')
    price = tickets['Adj Close'].pct_change()
    price = price.dropna()
    
    historical_volatilities = []
    for i in range(len(price) - window_size + 1):
        price_window = price[i:i + window_size]
        price_changes = price_window.diff().dropna()
        historical_volatility = price_changes.std()*np.sqrt(252)
        historical_volatilities.append(historical_volatility)
    
    return historical_volatilities

def genpicture(name,exday,path):

    try:
        data = pd.read_csv(path)
    except:
        print(f'{path} plot figure fail\n')

    # 取得資料筆數
    num_records = data.shape[0]

    # 如果資料筆數超過30筆，只保留最近的30筆
    if num_records > 30:
        recent_data = data.tail(30)
    else:
        recent_data = data  # 如果不足30筆，則使用所有資料

    ydata = [recent_data['Dex'], recent_data['Gex'], recent_data['putIV'] - recent_data['CallIV']]
    date = recent_data['Date']
    title = name + ' ' + exday
    plot = DATAPLOT(3,ydata,date,title,path)

    plot._Plot()
    



# if __name__ == "__main__":
#     genpicture(name,exday,path)

