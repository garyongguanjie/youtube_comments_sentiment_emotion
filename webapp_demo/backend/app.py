from downloader import download_comments
import json

import pandas as pd
from transformers import pipeline
import torch
from torch import nn
from transformers import DistilBertTokenizer, DistilBertModel
from tqdm import tqdm

from flask import Flask,request
from flask_cors import CORS

import functools

app = Flask(__name__)

def deEmojify(inputString):
    string = inputString.encode('ascii', 'ignore').decode('ascii')
    return string

def get_comments(youtube_id):
    ls = []
    comments = download_comments(youtube_id)
    for comment in comments:
        comment_json = json.dumps(comment, ensure_ascii=False)
        text = comment['text']
        if text != "":
            ls.append(deEmojify(text))
    return ls

def deEmojify(inputString):
    string = inputString.encode('ascii', 'ignore').decode('ascii')
    return string

class Config:
    MAX_LEN=512
    TRAIN_BATCH_SIZE=16
    VALID_BATCH_SIZE=16
    INFERENCE_BATCH_SIZE=1
    TOKENIZER = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    CSV_PATH = '../input/complete-tweet-sentiment-extraction-data/tweet_dataset.csv'
    EPOCHS = 5

class CommentModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.dropouts = nn.ModuleList([nn.Dropout(0.15) for _ in range(5)])
        self.l1 = nn.Linear(768,3) # for sentiment
        self.l2 = nn.Linear(768,13) # for emotion
    def forward(self,ids,mask):
        x = self.bert(input_ids=ids,attention_mask=mask)[0]
        for i,dropout in enumerate(self.dropouts):
            if i == 0:
                out_sum = dropout(x)
            else:
                out_sum += dropout(x)
        out = out_sum/len(self.dropouts)
        out = torch.mean(out,dim=1)
        sentiment = self.l1(out)
        emotion = self.l2(out)
        return sentiment,emotion

class TweetDataset:
    """
    Dataset which stores the tweets and returns them as processed features
    """
    def __init__(self, tweet):
        self.tweet = tweet
        self.tokenizer = Config.TOKENIZER
        self.max_len = Config.MAX_LEN
    
    def __len__(self):
        return len(self.tweet)

    def __getitem__(self, item):
        tweet = str(self.tweet[item])
        tweet = " ".join(tweet.split())

        inputs = self.tokenizer.encode_plus(
            tweet,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            pad_to_max_length=False,
        )

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]

        return {
            'ids': torch.tensor(ids),
            'mask':torch.tensor(mask)
        }

def eval_fn(data_loader, model, device):
    model.eval()

    tk0 = tqdm(data_loader, total=len(data_loader))
    s_ls = []
    e_ls = []
    with torch.no_grad():
        for bi, d in enumerate(tk0):

            ids = d["ids"]
            mask = d["mask"]

            ids = ids.to(device, dtype=torch.long)
            mask = mask.to(device, dtype=torch.long)

            pred_sentiment,pred_emotion= model(
                ids=ids,
                mask=mask,
            )

            pred_sentiment = torch.argmax(torch.softmax(pred_sentiment,dim=-1),dim=-1)
            for pred in pred_sentiment:
              s_ls.append(pred.item())
            pred_emotion = torch.argmax(torch.softmax(pred_emotion,dim=-1),dim=-1)
            for pred in pred_emotion:
              e_ls.append(pred.item())
    return s_ls,e_ls

def flipdict(a):
    return dict((v,k) for k,v in a.items())

def print_test(df,i):
    row = df.iloc[i]
    print(row.sentiment)
    print(row.emotion)



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = CommentModel()
model.to(device)
model.load_state_dict(torch.load('model.bin',map_location=torch.device('cpu')))
model = torch.quantization.quantize_dynamic(model,{torch.nn.Linear},dtype=torch.qint8)

@functools.lru_cache(128)
def get_se(youtube_id):
    comments =  get_comments(youtube_id)  

    valid_dataset = TweetDataset(
        tweet=comments
    )

    valid_data_loader = torch.utils.data.DataLoader(
        valid_dataset,
        batch_size=Config.INFERENCE_BATCH_SIZE,
        num_workers=2
    )


    s_ls,e_ls = eval_fn(valid_data_loader,model,device)

    df = pd.DataFrame({'s':s_ls,'e':e_ls})

    emotion_dict = {'anger':0,'boredom':1,'empty':2,'enthusiasm':3,'fun':4,
                    'happiness':5,'hate':6,'love':7,'neutral':8,'relief':9,
                    'sadness':10,'surprise':11,'worry':12}
    emotion_dict = flipdict(emotion_dict)

    sentiment_dict = {'negative':0,'neutral':1,'positive':2}
    sentiment_dict = flipdict(sentiment_dict)


    df['sentiment'] = df['s'].apply(lambda x: sentiment_dict[x])
    df['emotion'] = df['e'].apply(lambda x:emotion_dict[x])

    return df

def get_percentage(ls):
    item_set = set(ls)
    dic = {}
    length = len(ls)
    for item in item_set:
        dic[item] = ls.count(item)/length*100
    return dic

@app.route("/")
def get():
    youtube_id = request.args.get('youtubeid',default="",type=str)
    print(youtube_id)
    df = get_se(youtube_id)
    sentiment = df['sentiment'].tolist()
    emotion = df['emotion'].tolist()
    sent_p = get_percentage(sentiment)
    emotion_p = get_percentage(emotion)

    return {"sentiment":sent_p,"emotion":emotion_p}

if __name__ == "__main__":
    CORS(app)
    app.run(debug=False,host='localhost')
    