import imdb
ia = imdb.IMDb()
import requests
from bs4 import BeautifulSoup

def reviews(title):
    search = ia.search_movie(title)
    imdb_id = search[0].movieID
    #url = "https://www.imdb.com/title/tt" + imdb_id + "/reviews?ref_=tt_urv"
    url = "https://www.imdb.com/title/tt" + imdb_id + "/reviews?ref_=tt_urv&paginationKey={}"
    print("url generated is", url)
    reviews = []
    key = 'g4xolermtiqhejcxxxgs753i36t52q343qkt37xmaxb6qp4iq4vmyen5d2wqj72k6bmmazd6'
    count=0
    while count<10:
        r = requests.get(url.format(key))
        page_html = r.content
        soup = BeautifulSoup(page_html, 'html.parser')
        key = soup.find("div", class_="load-more-data")
        if not key:
            break
        reviews.extend(soup.find_all("div", class_="text"))
        count+=1
    #print(reviews)
    #print(type(reviews))
    result=[]
    #print(reviews[0])
    for i in range(len(reviews)-1):
        result.append(reviews[i].text)
        print("review no",i+1)
        print(reviews[i].text)
        print("****************")
    return result
