### using alphavantage.co
import requests

mm_api = 'BTH0SI5DKVWBY6KB'

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=mm_api'
r = requests.get(url)
data = r.json()
print(data)


