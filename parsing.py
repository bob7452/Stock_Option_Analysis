import requests
from bs4 import BeautifulSoup

urls = [ 'https://www.barchart.com/stocks/quotes/$MMTW',
	'https://www.barchart.com/stocks/quotes/$MMFI',
	'https://www.barchart.com/stocks/quotes/$MMTH'
	]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0'
}

def requestCMD(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("request fail , error code:", response.status_code)
        return 'NAN'

def Parsing(soup,target,offset):
    search_text = target
    if search_text in soup.text:
        index = soup.text.index(search_text)
        start_index = index + len(search_text)
        end_index = soup.text.find("\n", start_index)
        
        if end_index != -1:
            result = soup.text[start_index:start_index+offset].strip()
            print("Result :",result)
            return result
        else:
            print("Not Find")
    else:
        print("Not Find")
    
def main(url="",find="",offset=0):
    if url == "" :
        for url  in urls:
            text = requestCMD(url) 
            target = 'Last Price'
            result = Parsing(text,target,6)
            print('ans : ',result)
    else:
        test = requestCMD(url)
        target = find
        Parsing(text,find,offset)
