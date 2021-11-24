import json

dic = {}
dic["recipient_emails"] = "eugenebrod@gmail.com"
dic["urls"] = "https://sfbay.craigslist.org/search/cta?query=nissan+truck&purveyor-input=all&max_auto_year=2005"

print(json.dumps(dic))