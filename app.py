import streamlit as st
import pandas as pd
import pickle
import requests
import time
import string
import re
import nltk
from nltk.corpus import stopwords
stop_words=set(stopwords.words('english'))
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import temp
tfidf = pickle.load(open("tfidf_vectorizer.pkl","rb"))
bnb = pickle.load(open("bnb_classifier.pkl","rb"))
st.set_page_config(layout="wide")
st.title("Movie Recommender System and Movie Review Sentiment Analysis")
movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies_new = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

selected_movie = st.selectbox(
     'Enter Movie Name?',
     movies_new["title"].values )


def fetch_poster(movie_id):
     #url = "https://api.themoviedb.org/3/movie/" + movie_id + "api_key=6cfbcd2d040a833b478ca4b06eb36ae9&language=en-US"
     response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6cfbcd2d040a833b478ca4b06eb36ae9&language=en-US".format(movie_id))
     #response = requests.get(url)
     data = response.json()
     #time.sleep(3)
     #print(data["poster_path"])
     return "http://image.tmdb.org/t/p/w500//" + data["poster_path"]

def cleaning(text):
    pattern = "<.*>"
    text = re.sub(pattern, "", text)
    res = ""
    for i in text:
        if i.isalnum() == True or i == " ":
            res = res + i
        elif i.isalnum() == False:
            res = res + ''
    text = res
    text = text.lower()
    new_text = []
    words = word_tokenize(text)
    for word in words:
        if word not in stop_words:
            new_text.append(word)
    result = " ".join(new_text)
    text = result
    result = ""
    ss = SnowballStemmer('english')
    x = [ss.stem(w) for w in text.split(" ")]
    result = " ".join(x)
    text = result
    return text



def movie_recommended(movie):
     movie_namelist = []
     movie_poster_urls=[]
     distances = []
     movie_list = []
     movie_index = movies_new[movies_new["title"] == movie].index[0]
     distances = similarity[movie_index]
     distances = list(enumerate(distances))
     movie_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]  # selecting top 5
     for i in movie_list:
          movie_namelist.append((movies_new.iloc[i[0]].title, round(i[1] * 100, 2)))
          movie_id=movies_new.iloc[i[0]].movie_id
          movie_poster_urls.append(fetch_poster(movie_id))
     # print(movie_poster_urls)
     return movie_namelist,movie_poster_urls


def start_recommendation():
    results, result_imgs = movie_recommended(selected_movie)
    with st.spinner('Wait for it...'):
        time.sleep(3)
    st.success('Here Are The Recommended Movies!')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(result_imgs[0])
        st.subheader(results[0][0])
    with col2:
        st.image(result_imgs[1])
        st.subheader(results[1][0])
    with col3:
        st.image(result_imgs[2])
        st.subheader(results[2][0])
    with col4:
        st.image(result_imgs[3])
        st.subheader(results[3][0])
    with col5:
        st.image(result_imgs[4])
        st.subheader(results[4][0])


def start_semantic_analysis():
    # with st.spinner('Wait for it...'):
    #     time.sleep(20)

    selected_movie_id = movies_new[movies_new["title"] == selected_movie].movie_id
    # reviews = fetch_review(selected_movie_id, selected_movie)
    reviews = temp.reviews(selected_movie)
    print("reviews",reviews)
    for i in range(len(reviews) - 1):
        reviews[i] = cleaning(reviews[i])
    vector_inp = tfidf.transform(reviews)
    output = bnb.predict(vector_inp)
    st.success('Here Are The Result of sentiment analysis!')
    print("output is ", output)
    output = output.tolist()
    positive_reviews = output.count(1)
    negative_reviews = len(reviews) - positive_reviews
    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Positive review %")
        st.subheader(round((positive_reviews * 100) / len(reviews), 2))
    with col2:
        st.subheader("Negative review %")
        st.subheader(round((negative_reviews * 100) / len(reviews), 2))
    # st.write("positive review % is ", round((positive_reviews * 100) / len(reviews), 2))
    # st.write("negative review % is ", round((negative_reviews * 100) / len(reviews), 2))

def display_cast(movie_id):
    summary_url = "https://api.themoviedb.org/3/movie/{}?api_key=6cfbcd2d040a833b478ca4b06eb36ae9&language=en-US".format(movie_id)
    res = requests.get(summary_url)
    data_sum = res.json()
    if data_sum["overview"]:
        movie_summary = data_sum["overview"]
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=6cfbcd2d040a833b478ca4b06eb36ae9&language=en-US".format(movie_id)
    response  = requests.get(url)
    data = response.json()
    array_cast=[]
    array_originalname=[]
    array_character_name=[]
    array_director_name=[]
    img_links_array=[]
    director_list=[]
    for element in data["cast"]:
        if element["known_for_department"]=="Acting":
            array_cast.append(element)
        if element["known_for_department"]=="Directing":
            array_director_name.append(element)
    print("array_director_name",array_director_name)
    for element in array_director_name:
        if element["profile_path"]:
            temp={}
            imglink = "http://image.tmdb.org/t/p/w500//" + element["profile_path"]
            temp["d_name"] = element["original_name"]
            temp["d_img"] = imglink
            director_list.append(temp)

    for element in array_cast:
        if element["profile_path"]:
            array_originalname.append(element["original_name"])
            array_character_name.append(element["character"])
            imglink = "http://image.tmdb.org/t/p/w500//" + element["profile_path"]
            img_links_array.append(imglink)
    return img_links_array,movie_summary,array_originalname,array_character_name,director_list






# st.image()

movie_index = movies_new[movies_new["title"] == selected_movie].index[0]
selected_movie_id = movies_new.loc[movie_index].at["movie_id"]
if st.button("Submit"):
    imglink = fetch_poster(selected_movie_id)
    img_links_array,movie_summary,array_originalname,array_character_name,director_list=display_cast(selected_movie_id)
    col1,col2 = st.columns([2,5])
    with col1:

        st.image(imglink,width=250)

    with col2:
        st.text(" ")
        st.header(selected_movie)
        st.subheader(movie_summary)
        st.text(" ")


    st.header("Cast of the movie")
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    with col1:

        st.image(img_links_array[0])
        st.text(array_originalname[0])
        st.text(array_character_name[0])
    with col2:
        st.image(img_links_array[1])
        st.text(array_originalname[1])
        st.text(array_character_name[1])
    with col3:
        st.image(img_links_array[2])
        st.text(array_originalname[2])
        st.text(array_character_name[3])
    with col4:
        st.image(img_links_array[4])
        st.text(array_originalname[4])
        st.text(array_character_name[4])
    with col5:
        st.image(img_links_array[5])
        st.text(array_originalname[5])
        st.text(array_character_name[5])
    with col6:
        st.image(img_links_array[6])
        st.text(array_originalname[6])
        st.text(array_character_name[6])

    start_recommendation()
    start_semantic_analysis()










