Movie recommender system and sentiment analysis

For the movie recommender system, I have used the IMDB movie dataset which is a collection of over 5000 movies 
I have used the Cosine function & K-Nearest Neighbor algorithm to determine the similarities between the movie and then recommend it accordingly

For Movie Review sentiment analysis,i have trained the model with the IMDB review sentiment dataset which has 50000 reviews along with their sentiment here I have considered 
only two sentiments (positive sentiment and negative sentiment) for classification I have used a naive Bayes classifier, Forgetting the user review I have to scrape the IMDb public reviews web page using the beautiful soup python library


These were the accuracy of the classifier (using Tfidf Vectorizer)

Gaussian classifier  = 78%
multinomial classifier = 83%
bernaulli classifier = 90%

here I have used Bernoulli classifier to build the model





