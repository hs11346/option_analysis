from urllib.request import urlopen

# import json
import json
from pandas import json_normalize

# store the URL in url as
# parameter for urlopen
url = "https://cdn.cboe.com/api/global/delayed_quotes/options/SPY.json"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
dict = json.loads(response.read())

df = json_normalize(dict['data']['options'])

