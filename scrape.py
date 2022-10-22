import os
import requests as r
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from google_search import GoogleSearch

load_dotenv()

terms = "how to chop"
vegetable = "potato"

search = GoogleSearch(terms, vegetable)

results = search.query()

print(results)

api_url = os.environ.get("API_URL")


# veg = {
#     "description": "",
#     "name": "",
#     "procedure": "",
#     "resource": ""
#     }
#
#
# response = r.put(f"{api_url}/veggies/{veg['name']}", json=veg)
#
# print(response.status_code)
