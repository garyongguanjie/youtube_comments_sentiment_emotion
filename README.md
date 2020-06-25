# Youtube sentiment emotion analysis using distilBERT
Predicts emotions from 13 categories

anger,boredom,empty,enthusiasm,fun,happiness,hate,love,neutral,relief,sadness,surprise,worry

Predicts sentiments from 3 categories

neutral, positive, negative

[See blog post here](https://garyongguanjie.github.io/youtube_comments_sentiment_emotion/)

# Training data
Training data on tweets as I could not find any labelled dataset of youtube comments.

https://www.kaggle.com/maxjon/complete-tweet-sentiment-extraction-data

# Training code
https://www.kaggle.com/garyongguanjie/comments-analysis \
You can download the model here under **output**

# Inference
Download the model from above. Mount it onto your google drive and run the notebook below. Youtube comments scraper is included in this notebook all you need to do is to put in the video id.\
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/garyongguanjie/youtube_comments_sentiment_emotion/blob/master/sentiment.ipynb)

# Results
On the validation set, my sentiment accuracy was about ~79% and emotion accuracy was about ~37%.

Next I applied the model on the video. \
[PM Lee Hsien Loong on Singapore's post-COVID-19 future, says "Do not fear" ](https://www.youtube.com/watch?v=rAhuD368Ij0) 

So as to see the emotions and sentiments of the general public. Here are the results:

![sentiment_image](sentiment.png)
![emotion_image](emotion.png)

It shows that Singaporeans seems to have an overall positive feel but are still feeling worried.\
You can see the final model output in out.csv
