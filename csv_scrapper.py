import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

base_url = "http://quotes.toscrape.com"
def scrape_quotes():
	all_qoutes = []
	url = "/page/1"
	while url:
		res = requests.get(f"{base_url}{url}")
		# print(f"Now Scrapping {base_url}{url}`")
		soup = BeautifulSoup(res.text, "html.parser")
		quotes = soup.find_all(class_="quote")

		for qoute in quotes:
			all_qoutes.append({
				"text" : qoute.find(class_ = "text").get_text(),
				"author" : qoute.find(class_ = "author").get_text(),
				"bio-link" : qoute.find("a")["href"]
				})
		 
			next_page = soup.find(class_= "next")
			url = next_page.find("a")["href"] if next_page else None 
			# sleep(1)
	return all_qoutes

def write_quotes(quotes):
	with open("quotes.csv", "w") as file:
		headers = ["text", "author", "bio-link"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for quote in quotes:
			csv_writer.writerow(quote)

quotes = scrape_quotes()
write_quotes(quotes )
