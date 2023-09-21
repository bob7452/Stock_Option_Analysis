import parsing
from bs4 import BeautifulSoup
url = 'https://www.marketwatch.com/investing/Stock/JPM/options'


soup = parsing.requestCMD(url)

# 找到包含"Expires Sep 22, 2023"文本的<th>元素
expires_th = soup.find('th', colspan="3", text="Expires Sep 22, 2023")

# 找到<td>元素包含"115.00"文本的元素
strike_td = soup.find('td', text="115.00")

# 如果找到<th>和<td>元素，找到<td>元素后的四个兄弟元素
if expires_th and strike_td:
    siblings = strike_td.find_next_siblings('td', limit=6)
    for sibling in siblings:
        print(sibling)
else:
     print("未找到相关元素")

