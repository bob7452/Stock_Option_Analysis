import sys
import DownLoad 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run Auto Mode")

        Stock = ["QQQ","SPY","AAPL","MSFT","GOOG","META","AMZN","TSLA","NVDA","TLT","^Vix","SOXX"]
        Type   = ["C","P"]
        
        for Name in Stock:
            for dT in Type:
                DownLoad.DownLoad_Data(Name,dT)

    else:
        name = sys.argv[1]
        dT   = sys.argv[2]
        print(name +" / "+dT)
        DownLoad.DownLoad_Data(name,dT)
