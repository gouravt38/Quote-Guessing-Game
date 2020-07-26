import requests
from bs4 import BeautifulSoup
# from time import sleep
from random import choice
from csv import DictReader

base_url = "http://quotes.toscrape.com"

def read_quotes(filename):
	with open(filename, "r") as file :
		csv_reader = DictReader(file)
		return list(csv_reader)

def start_game(q):
	single_qoute = choice(q)
	remaining_guesses = 4
	print("Here's a qoute: ")
	print(single_qoute["text"])
	# print(single_qoute["author"])
	guess = ' '

	while guess.lower() != single_qoute["author"].lower() and remaining_guesses > 0:
		guess = input(f"Who said this Quote? Guesses remaing are: {remaining_guesses} \n")
		if guess.lower() == single_qoute["author"].lower():
			print("YOU GOT IT RIGHT BUDDY!!!!!")
			break
		remaining_guesses -= 1
		if remaining_guesses == 3: 
			res = requests.get(f"{base_url}{single_qoute['bio-link']}")
			soup = BeautifulSoup(res.text, "html.parser")
			birth_date = soup.find(class_ = "author-born-date").get_text()
			birth_place = soup.find(class_ = "author-born-location").get_text()
			print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
		elif remaining_guesses == 2:
			print(f"Hers's a Hint: The author's first name starts whith {single_qoute['author'][0]}")
		elif remaining_guesses == 1:
			last_initial = single_qoute["author"].split(" ")[1][0]
			print(f"Hers's a Hint: The author's last name starts whith {last_initial}")
		else:
			print(f"Sorry ran out of Guesses. \n The answer was {single_qoute['author']}") 

	again = ''
	while again not in ('y', 'n', 'yes', 'no'):
		again = input("Would you like to play again? y/n: ")
	if again.lower() in ('yes', 'y'):
		return start_game(q)
	else :
		print("OK GOODBYE!!")

p_quotes = read_quotes("quotes.csv")
start_game(p_quotes)