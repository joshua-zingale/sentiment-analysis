from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

pageNum = 1
while pageNum <= 15:
	urlPage = 'https://www.ebay.com/urw/Sony-PS5-Blu-Ray-Edition-Console-White/product-reviews/19040936896?_itm=224287204129&pgn=' + str(pageNum)
	#open up connection, grab the page
	uClient = uReq(urlPage)
	page_html = uClient.read()
	uClient.close()
	#html parsing
	page_soup = soup(page_html, "html.parser")
	#grabs each review body
	reviewText = page_soup.findAll("p",{"itemprop":"reviewBody"})
	#view sample reviewText
	reviewText[0]

	for review in reviewText:
		description = review.text 
		print("description: " + description)
	pageNum = pageNum + 1

