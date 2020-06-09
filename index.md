# Training methodology
As I could not find and dataset on youtube comments, I used a tweet dataset that I got from kaggle with both sentiment and emotion labels. Then I used a pretrained DistilBert model to train the data. 

# Model Output
The model outputs two things namely emotion and sentiment. 

Here are the possible emotions
* anger
* boredom,empty
* enthusiasm
* fun
* happiness
* hate
* love
* neutral
* relief
* sadness
* surprise
* worry

Here are the possible sentiments:
* neutral
* negative
* positive

# Applying it the model on a COVID19 announcement by our Prime Minister

Next I used this model on comments of this video. [PM Lee Hsien Loong on Singapore's post-COVID-19 future, says "Do not fear" ](https://www.youtube.com/watch?v=rAhuD368Ij0) 

By using a youtube comment scraper, I scraped the comments and applied the model to the comments on the video. For text that are too long, they are cut off at around ~500 words.

The results are I would say pretty good!
Here are some examples

| Comment | Sentiment | Emotion |
| --- | --- | --- |
| LKY came out from his grave and disapproved this message. | negative | sadness |
| Thank you PM LEE, not easy for the government. Well done so far! | positive | hapiness |
| thank you daddy lee | positive | love |
| Opposition & Opposition Supporter go away la.  Dont try to Divide SG United & brain  wash Singaporean to vote you for corruption.  Disgusting ! Not happy with PAP & Singapore.  Migrate to Hongkong or Taiwan protest & protest la.  Singaporean dont want Political fight.  Just want stability in the hand  of PAP.    So Regret voting for Opposition party last time | negative | hate |
| I'm always inspired and motivated by PM's speeches.  With our PM and his Cabinet leading us, I'm confident we will overcome any obstacles and come out stronger than before #SGUnited | positive | relief |
| time for the ministers to cut pay. 4G leaders make a mess, refused to apologies for their mistakes and blame us. Paid so well doing a roaring business themselves and still got face to take such high salaries. Vietnam did better than us. 0 fatalities. less than 10% got infected. We your citizens who are paying you are not dumbass. You guys better buckle up or be shipped (sheep) out | negative | sadness | 
| Thank you Singapore!  It is proud to be a Singaporean | positive | hapiness |

Next I plot the data into a pie chart to see the general sentiments and emotions of the public.

![sentiment_image](sentiment.png)

![emotion_image](emotion.png)

It shows that Singaporeans seems to have an overall positive feel but are still feeling worried.
You can see the final model output in out.csv

# Running the model yourself on any video
## Download the model
https://www.kaggle.com/garyongguanjie/comments-analysis

You can download the model here under **output**

## Run it on colab
No installation is required! Youtube comments scraper is included in this notebook all you need to do is to put in the video id.
Mount the trained model onto your google drive and run the notebook below.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/garyongguanjie/youtube_comments_sentiment_emotion/blob/master/sentiment.ipynb)
