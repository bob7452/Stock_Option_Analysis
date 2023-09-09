import requests
import xml.etree.ElementTree as ET
FALLBACK_RISK_FREE_RATE = 0.02
TREASURY_URL = "https://home.treasury.gov/sites/default/files/interest-rates/yield.xml"

class Rate:
    def riskfree():
        try:
            r = requests.get(TREASURY_URL)

            root = ET.fromstring(r.text)
            days = root.findall('.//G_BC_CAT')
            last = days[-1]

            def parse(node):
                return float(node.text)

            m1 = parse(last.find('BC_1MONTH'))
            m2 = parse(last.find('BC_2MONTH'))
            m3 = parse(last.find('BC_3MONTH'))
            m6 = parse(last.find('BC_6MONTH'))
            y1 = parse(last.find('BC_1YEAR'))
            y2 = parse(last.find('BC_2YEAR'))
            y3 = parse(last.find('BC_3YEAR'))
            y5 = parse(last.find('BC_5YEAR'))
            y7 = parse(last.find('BC_7YEAR'))
            y10 = parse(last.find('BC_10YEAR'))
            y20 = parse(last.find('BC_20YEAR'))
            y30 = parse(last.find('BC_30YEAR'))

            return y1
        except Exception:
            return lambda x: FALLBACK_RISK_FREE_RATE