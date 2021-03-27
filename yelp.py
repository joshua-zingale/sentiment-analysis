import requests
import json
from bs4 import BeautifulSoup as bs

def get_request_headers() -> dict:
	'''
	Gets the minimal acceptable header for Yelp to respond to get requests.
	:return: The headers.
	'''
	headers = {"X-Requested-With": "XMLHttpRequest", "Cookie": "hl=en_US; wdi=1|5BA68BDCB0C2D05E|0x1.812c42cdfee7cp+30|fe2be12b7818c73d; _ga=GA1.2.5BA68BDCB0C2D05E; g_state={\"i_p\":1615539423511,\"i_l\":1}; qntcst=D; __qca=P0-200804351-1615532292601; G_ENABLED_IDPS=google; bse=01175a525a614cb98ba61366622d1688; _gid=GA1.2.2001938892.1616548068; recentlocations=; location=%7B%22max_longitude%22%3A+-117.1492017129409%2C+%22address3%22%3A+%22%22%2C+%22min_longitude%22%3A+-117.1756008856576%2C+%22neighborhood%22%3A+%22Downtown%22%2C+%22address1%22%3A+%22%22%2C+%22place_id%22%3A+%2238317%22%2C+%22min_latitude%22%3A+32.7103776769484%2C+%22county%22%3A+%22San+Diego+County%22%2C+%22unformatted%22%3A+%22Downtown%2C+San+Diego%2C+CA%22%2C+%22display%22%3A+%22Downtown%2C+San+Diego%2C+CA%22%2C+%22borough%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22max_latitude%22%3A+32.7243129998341%2C+%22city%22%3A+%22San+Diego%22%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22zip%22%3A+%2292101%22%2C+%22parent_id%22%3A+1234%2C+%22place_key%22%3A+%22CA%3ASan_Diego%3A%3ADowntown%22%2C+%22country%22%3A+%22US%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22longitude%22%3A+-117.16240740006764%2C+%22location_type%22%3A+%22neighborhood%22%2C+%22confident%22%3A+null%2C+%22state%22%3A+%22CA%22%2C+%22latitude%22%3A+32.71767492028563%2C+%22usingDefaultZip%22%3A+false%2C+%22address2%22%3A+%22%22%2C+%22accuracy%22%3A+5%7D; adc=NNEUtrDZCDkt5Fu1idgoag%3AmZ9z2WAIrJvS7DgiAFczAw%3A1616548081; sc=beec9fb48a; _gat_global=1; OptanonConsent=isIABGlobal=false&datestamp=Tue+Mar+23+2021+18%3A23%3A05+GMT-0700+(Pacific+Daylight+Time)&version=6.10.0&hosts=&consentId=f54519c5-a2b6-4e35-abf3-61b9b74c6b50&interactionCount=1&landingPath=NotLandingPage&groups=BG10%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&AwaitingReconsent=false; xcj=1|oy3WiRV8Q4dD5hyMJiYNgND0cL8TlpgT1Ay3ZKbG-0Q; _gat_www=1"}
	return headers


def get_reviews(url: str, max_reviews: int = -1) -> dict:
	'''
	Gets all of the reviews along with their respective star ratings for a supplied Yelp listing.
	:param url: The base url of a Yelp page. e.g. "https://www.yelp.com/biz/chuck-e-cheese-national-city"
	:param max_reviews: The maximum number of reviews the function will grab. If set to a negative number, there will be no maximum.
	:return: An array of dictionaries, each representing a single review. There is a buch of data for each review; useful keys are ['comment']['text'] for the review text and ['rating'] for its associated star rating.
	'''

	business_id = get_id_from_bussiness_page(url)
	headers = get_request_headers()

	reviews = []

	i = 0

	# Loop will end if 1) the max number of reviews has been reached
	# after scraping one set of reviews or 2) if there are no more reviews.
	while i < max_reviews or max_reviews < 0:

		starting_i = i

		response = requests.get("https://www.yelp.com/biz/" + business_id + "/review_feed?rl=en&sort_by=date_desc&q=&start=" + str(i), headers)

		new_reviews = json.loads(response.text)["reviews"]


		for review in new_reviews:

			# Stop collecting reviews if maximum has been reached.
			if i == max_reviews:
				break
			text = review['comment']['text']

			# Fixing bug where all apostrophes are replaced by their html code &#39;
			text = text.replace("&#39;", "'")
			review['comment']['text'] = text

			reviews.append(review)

			i += 1

		# If the index has not advanced within this while iteration,
		# then no new reviews were added and no more remain.
		if starting_i == i:
			break

	return reviews



def get_id_from_bussiness_page(url: str) -> str:
	'''
	Gets the internal Yelp id of a business given its Yelp page URL.
	:param url: The url of the webpage.
	:return: The business id.
	'''
	response = requests.get(url, get_request_headers())

	soup = bs(response.text, "html.parser")

	# The script containing the business id
	script = str(soup.find_all("script")[5])

	# The business id is located 21 characters after "business_id"
	id_index = script.find("business_id") +21

	# Build id until it reaches the end quotation
	business_id = ""
	i = 0
	while script[id_index + i] !=  "\"":
    	
		business_id += script[id_index + i]

		i += 1

	return business_id
