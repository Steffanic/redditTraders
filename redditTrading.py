#
# Author: Patrick Steffanic
# Strategy: I want to read the submissions and comments of r/pennystocks and count the number
#           of times a particular stock symbol appears in either the submission title, 
#           the submission body, or any of the comment bodies. 
# Observables: # of times in submission title / day
#              # of times in submission body / day
#              # of times in any comment body / day
#              # of times in a comment body whose submission's body or title contains stock symbol / day

import praw
from datetime import datetime as dt
from datetime import timedelta, date
import matplotlib
import numpy as np
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import sys
from dateutil.parser import parse
import yfinance as yf


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__=="__main__":
    stk_symb = "SXTC"
    if(len(sys.argv)>1):
        stk_symb = sys.argv[1]
        print(f"Looking for occurences of {stk_symb}")

    reddit = praw.Reddit(client_id="DkudDANPavT6uw"
                        ,client_secret="9nJrIkk-YPHpiI87fFCObE1JrtY0bg"
                        ,user_agent="Stock Symbol Search Tool by u/Steffanic")

    n_sub_title = {}
    n_sub_body = {}
    n_any_com_body = {}
    n_sub_title_com_body = {}
    n_sub_body_com_body = {}

    for sub in reddit.subreddit("all").search(stk_symb, sort='new'):
        sub_date = dt.fromtimestamp(sub.created_utc)
        comments = sub.comments
        comments.replace_more(limit=0)

        if (stk_symb in sub.title):
            n_sub_title[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_title else n_sub_title[sub_date.date().__str__()] + 1
            for com in comments:
                if(stk_symb in com.body):
                    n_sub_title_com_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_title_com_body else n_sub_title_com_body[sub_date.date().__str__()] + 1
            
        if (stk_symb in sub.selftext):
            n_sub_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_body else n_sub_body[sub_date.date().__str__()] + 1
            for com in comments:
                if(stk_symb in com.body):
                    n_sub_body_com_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_body_com_body else n_sub_body_com_body[sub_date.date().__str__()] + 1

    print(n_sub_title, n_sub_body, n_sub_title_com_body, n_sub_body_com_body)

    start_date = min(min(n_sub_body.keys()), min(n_sub_title.keys()))
    end_date = dt.now().date().__str__()# max(max(n_sub_body.keys()), max(n_sub_title.keys()))
    print(start_date)
    print(end_date)
    stk = yf.Ticker(stk_symb)
    price_history = stk.history(start=start_date, end=end_date)
    print(price_history)
    mean_close = np.mean(price_history['Close'])
    dates = [d for d in daterange(parse(start_date), parse(end_date))]

    body_plot = [0 if (d.date().__str__() not in n_sub_body.keys()) else n_sub_body[d.date().__str__()] for d in dates]
    title_plot = [0 if (d.date().__str__() not in n_sub_title.keys()) else n_sub_title[d.date().__str__()] for d in dates]
    title_com_plot = [0 if (d.date().__str__() not in n_sub_title_com_body.keys()) else n_sub_title_com_body[d.date().__str__()] for d in dates]
    body_com_plot = [0 if (d.date().__str__() not in n_sub_body_com_body.keys()) else n_sub_body_com_body[d.date().__str__()] for d in dates]
    price_history_plot = [None if (d.date().__str__() not in price_history.index) else price_history['Close'].loc[d.date().__str__()] for d in dates]


    assert(len(dates)==len(body_plot))

    plt.figure(figsize=(15,5))
    plt.subplot(2,1,1)
    plt.plot(range(len(dates)),body_plot, label="Occurences in body of submission")
    plt.plot(range(len(dates)),title_plot, label="Occurences in title of submission")
    plt.plot(range(len(dates)),body_com_plot, label="Occurences in body of comments if in submission title")
    plt.plot(range(len(dates)),title_com_plot, label="Occurences in body of comments if in submission body")
    plt.subplot(2,1,2)
    plt.plot(range(len(dates)),price_history_plot, label="Closing Price")
    # plt.plot(range(len(dates)),np.ones(len(dates))*mean_close, label="Mean Close")

    plt.title(f"Frequency of {stk_symb} in r/all")
    plt.xticks(ticks=range(len(dates)), labels=list(map(lambda x: x.date(),dates)), rotation=70)
    # plt.grid()
    plt.legend()
    plt.show()