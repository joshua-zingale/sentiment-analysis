from bs4 import BeautifulSoup
import requests
import yelp

# url is set to page where you search for business
# initial scrape helps us narrow down our scope
key_search_url = requests.get('https://www.yelp.com/search?find_desc=photo+developing&find_loc=San+Diego%2C+CA&ns=1').text
soup = BeautifulSoup(key_search_url, 'lxml')
scrape = soup.find_all("div", {"class": "businessName__09f24__3Wql2 display--inline-block__09f24__3L1EB border-color--default__09f24__1eOdn"})

# raw_link is a dictionary of each listed business' name and its webpage
raw_link = {}
for i in range(0, len(scrape)):
    business_name = scrape[i].find("a")['name']
    business_yelp_page = "https://www.yelp.com/" +scrape[i].find("a")['href']
    raw_link[business_name] = business_yelp_page

# create file to dump reviews
f = open('dumped_reviews.txt', 'w+')

# for each business, this iteration dumps all of their reviews into a text file
# includes header for each business, includes numbered reviews, and the star rating after each review
i = 0
for each in raw_link:
    tester = yelp.get_reviews(raw_link.get(each), -1, -1)

    f.write('Review for ' + each + ':\n')

    for j in range(0, len(tester) - 1):
        review_text = tester[j]['comment']['text']
        star_rating = tester[j]['rating']
        f.write('Review ' + str(j + 1) + ': ' + review_text + '\n' + str(star_rating) + '\n\n')

    i = i + 1
f.close()