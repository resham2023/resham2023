"""
    Web crawler
"""
import re
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import queue



visited_urls = []
products = []
product = {}

response = requests.get("https://scrapeme.live/shop/")
# response = requests.get("https://www.amazon.com/shop/")
soup = BeautifulSoup(response.content, "html.parser")
link_elements = soup.select("a[href]")

#SEED URL
urls = ["https://scrapeme.live/shop/"]
# urls = ["https://www.amazon.com/"]

# get the page to visit from the list
current_url = urls.pop()
print("current_url is ", current_url)
# crawling logic
response = requests.get(current_url)
soup = BeautifulSoup(response.content, "html.parser")

link_elements = soup.select("a[href]")

# mark the current URL as visited
visited_urls.append(current_url)

#Loop thru all links.
for link_element in link_elements:
    url = link_element['href']

    if "https://scrapeme.live/shop/" in url and url not in urls and url not in visited_urls:
        if url not in urls and url not in visited_urls:
            urls.append(url)
            print("urls are", urls)

            response1 = requests.get(url)
            soup1 = BeautifulSoup(response1.content, "html.parser")

            product = {"url": url,  "price": soup1.select_one(".price"),
                       "image": soup1.select_one(".wp-post-image")["src"]}
#            product["image"] = soup.select_one(".wp-post-image")["src"]
# product["name"] = soup.select_one(".product_title").text()
# product["price"] = soup.select_one(".price")
#        product = {"url": url, "image": soup.select_one(".wp-post-image")["src"],
#                   "title": soup.select_one(".product_title").text()}
#        print("product ", product)
            products.append(product)
            print("products are", products)

# write to CSV
with open('products.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
# , fieldnames=["url", "image"])
    writer.writerow(["url", "price",  "image"])
    # populating the CSV
    for product in products:
        writer.writerow(product.values())

# pause the script for random delay
time.sleep(random.uniform(1, 3))

print("3. URL",  url)
