import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#array created to store reviews as an appended dictionary
posts = []

pageNum = 1
productReviewPage = input("Enter Ebay Product Review Page:")

inputPageNum = input("Enter the number of pages to scrape")
while pageNum <= int(inputPageNum)
    pageEquals = productReviewPage.index('=')
    # Ebay specific sorting tags: '?sort=-rating' --> sort highest ratings first / '&sort=%2Brating' --> sort lowest ratings first
    urlPage = productReviewPage[0:pageEquals+1] + str(pageNum) + '&sort=%2Brating'
    #open up connection, grab the page
    uClient = uReq(urlPage)
    page_html = uClient.read()
    uClient.close()
    #html parsing
    page_soup = soup(page_html, "html.parser")
    #grab review section contents
    genReview = page_soup.findAll("div",{"class":"ebay-review-section"})
    for review in genReview:
        description = review.p.text
        starRating = review.meta["content"]
        post = {'text' : description, 'rating' : starRating}
        if int(starRating) > 3:
            posts.append(post)
    pageNum = pageNum + 1

#saving reviews into text file
with open('parsed_data.txt', 'w') as file:
    json.dump(posts, file)

