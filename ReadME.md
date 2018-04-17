# **Tweet Trend**

There are 3 python files and 1 Html file

-lambda3 (sqs): Extract data such as tweets and co-ordinates using tweepy.

-Lambda1: Triggers sqs, Get data from sqs, compare with keyword provided from front-end, do sentimental analysis and pass to sns.

-Lambda2: Is triggered by sns and stores data into elasticsearch.

-index.html: Used to send key-word to lambda1 using API gateway and retrieves data from elasticsearch and plot it on google maps.


link: https://s3.us-east-2.amazonaws.com/tweetplot/index.html

