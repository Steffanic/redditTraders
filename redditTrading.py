#
# Author: Patrick Steffanic
# Strategy: I want to read the submissions and comments of r/pennystocks and count the number
#           of times a particular stock symbol appears in either the submission title, 
#           the submission body, or any of the comment bodies. 
# Observables: # of times in submission title / day
#              # of times in submission body / day
#              # of times in any comment body / day
#              # of times in a comment body whose submission's body or title contains stock symbol / day

from re import search
import praw
from datetime import datetime as dt
from datetime import timedelta, date
import matplotlib
import pandas as pd
import numpy as np
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import sys
from dateutil.parser import parse
import yahooquery as yq
from english_words import english_words_set as ew
import pickle
import os



# Utility Functions

def handle_cl_args():
    stk_symb = "SXTC"
    if(len(sys.argv)>1):
        stk_symb = sys.argv[1]
        print(f"Looking for occurences of {stk_symb}")
    return stk_symb,


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_start_date(all_occurences):
    all_occurences_keys = [list(x.keys()) for x in all_occurences]
    for x in all_occurences_keys:
        print(x)
    all_mins = [dt.now().date().__str__() if x==[] else min(x) for x in all_occurences_keys]
    print(all_mins)
    return min( all_mins ) 

# Reddit functions

def count_occurences(stk_symb):
    n_sub_title, n_sub_body, n_any_com_body, n_sub_title_com_body, n_sub_body_com_body={}, {}, {}, {}, {}
    
    query_result = reddit.subreddit("pennystocks").search(stk_symb, sort='new', limit=1000, time_filter="month")
    i=0
    for sub in query_result: # search through all posts in r/all for stk_symb
        i+=1
        if(i%10==0):
            print(f"\rProcessing post {i}", end="")
        sub_date = dt.fromtimestamp(sub.created_utc) # record date
        comments = sub.comments # get comments tree
        comments.replace_more(limit=0) # Exapand comment tree completely

        if (stk_symb in sub.title): # if stk_symb in the post's title
            n_sub_title[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_title else n_sub_title[sub_date.date().__str__()] + 1 # Add 1 to the day of post or create day in dict and set to 1
            for com in comments: # Check the comments for stk_symb
                if(stk_symb in com.body): 
                    n_sub_title_com_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_title_com_body else n_sub_title_com_body[sub_date.date().__str__()] + 1
            
        if (stk_symb in sub.selftext): # if stk_symb in post's body
            n_sub_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_body else n_sub_body[sub_date.date().__str__()] + 1
            for com in comments:
                if(stk_symb in com.body):
                    n_sub_body_com_body[sub_date.date().__str__()] = 1 if sub_date.date().__str__() not in n_sub_body_com_body else n_sub_body_com_body[sub_date.date().__str__()] + 1
    print("")
    return n_sub_title, n_sub_body, n_sub_title_com_body, n_sub_body_com_body, n_any_com_body

def plot_reddit_occurences_price(stk_symb, search_term):
    print(f"\n\n\n\n\n\nCounting occurences of {search_term}")

    # count the occurences of our stock symbol in r/all and load the into dictionaries
    # {key:value} = {day:frequency}

    n_sub_title, n_sub_body, n_sub_title_com_body, n_sub_body_com_body, n_any_com_body = count_occurences(search_term)
    
    # Let's consolidate these into a big tuple so we can get the earliest mention of a stock symbol concisely

    all_occurences = (n_sub_title, n_sub_body, n_sub_title_com_body, n_sub_body_com_body, n_any_com_body)

    start_date = get_start_date(all_occurences)  # get the earliest mention
    
    end_date = dt.now().date().__str__()# max(max(n_sub_body.keys()), max(n_sub_title.keys())) # I like to set the end date to today rather than the last mention so that I can see the longer term behaviour of the price
    
    print(start_date)
    print(end_date)



    stk = yq.Ticker(stk_symb, status_forcelist=[404, 429, 500, 502, 503, 504])
    print("Retrieving Stock History")
    price_history = stk.history(start=start_date, end=end_date)

    print(price_history)
    
    mean_close = np.mean(price_history['close'])
    
    dates = [d for d in daterange(parse(start_date), parse(end_date))]

    frequency_imputer = lambda occurence_dict, dates: [0 if (d.date().__str__() not in occurence_dict.keys()) else occurence_dict[d.date().__str__()] for d in dates]
    
    body_plot = frequency_imputer(n_sub_body,  dates)
    title_plot = frequency_imputer(n_sub_title, dates)
    title_com_plot =frequency_imputer( n_sub_title_com_body, dates)
    body_com_plot = frequency_imputer(n_sub_body_com_body, dates)

    price_imputer = lambda history, dates: [None if (d.date() not in history.index.get_level_values("date").to_list()) else history.loc[history.index.get_level_values('date')==d.date(), 'close'] for d in dates]

    price_history_plot = price_imputer(price_history, dates)
    

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

def get_stocks_mentioned():
    all_stocks = pd.read_csv("nasdaq.csv")     # Read all stocks from csv
    reddit_stocks=all_stocks
    earliest_dates = []
    num_mentions = []
    for stock in all_stocks["Symbol"]:
        earliest_date = 999999999999
        search_term = stock
        if stock in ew:
            search_term = all_stocks.loc[all_stocks['Symbol']==stock]["Name"].iloc[0]
            print("The stock symbol is a standard english word, searching for company name instead!")
        mentions=0
        print(f"Searching for {search_term}")
        query_result = reddit.subreddit("pennystocks").search(search_term, sort='new', limit=100, time_filter="month")
        for sub in query_result:
            if(stock in sub.title or stock in sub.selftext):
                mentions+=1
                if(sub.created_utc<earliest_date):
                    earliest_date=sub.created_utc
        print(f"{stock} has {mentions} mentions.")
        if mentions<1 or mentions>40:
            print(f"Throwing away {stock}")
            reddit_stocks = reddit_stocks[reddit_stocks["Symbol"]!=stock]
        else:
            print("Adding date and mentions to stock")
            earliest_dates.append(earliest_date)
            num_mentions.append(mentions)  
    reddit_stocks["Earliest Date"] = pd.Series(earliest_dates)
    reddit_stocks["Mentions"] = pd.Series(num_mentions)
    with open("rStocks.pickle", "wb") as f:
        pickle.dump(reddit_stocks, f)
    return reddit_stocks

def get_stocks():
    if(os.path.exists("rStocks.pickle")):
        with open("rStocks.pickle", "rb") as f:
            return pickle.load(f)
    else:
        return get_stocks_mentioned()

def remove_common_words(name):
    words = name.split(" ")
    new_name = ""
    for word in words:
        if word.lower() not in ew:
            new_name += (word)
            new_name += " "
    return new_name


if __name__=="__main__":
    
    # Get the user's desired stock symbol from the command line

    # Get the reddit client

    reddit = praw.Reddit(client_id="DkudDANPavT6uw"
                        ,client_secret="9nJrIkk-YPHpiI87fFCObE1JrtY0bg"
                        ,user_agent="Stock Symbol Search Tool by u/Steffanic")

    reddit_stocks = get_stocks()


    scroll_offset = 0
    to_quit=False

    while not to_quit:
        print("Select a stock:")
        for i in range(25):
            print(f" { (reddit_stocks['Symbol']).iloc[i+scroll_offset] } : { (reddit_stocks['Name']).iloc[i+scroll_offset] } : First mentioned in top 100 results { -1 if np.isnan((reddit_stocks['Earliest Date']).iloc[i+scroll_offset]) else dt.fromtimestamp((reddit_stocks['Earliest Date']).iloc[i+scroll_offset]).date().__str__() } : Number of Mentions in top 100 results { -1 if np.isnan((reddit_stocks['Mentions']).iloc[i+scroll_offset]) else (reddit_stocks['Mentions']).iloc[i+scroll_offset] }")
        
        print("Commands:")
        print(" s [STOCK SYMBOL] - plot stock symbol occurences and price")
        print(" d - scroll stock list down a page")
        print(" u - scroll stock list up a page")
        print(" q - quit")

        selection = input(">>:")

        if selection=='q':
            to_quit=True
            break
        elif selection=="u":
            if scroll_offset==0:
                print("Nice try, buddy.")
                break
            else:
                scroll_offset-=25
        elif selection=="d":
            scroll_offset+=25
        else:
            stk_symb = selection[2:]
            search_term=stk_symb
            if stk_symb in ew or len(stk_symb)==1:
                search_term = remove_common_words(reddit_stocks.loc[reddit_stocks['Symbol']==stk_symb]["Name"].iloc[0]).replace(" ", " OR ")
                print("The stock symbol is a standard english word, searching for Name instead!")
            plot_reddit_occurences_price(stk_symb, search_term)



    # plot_reddit_occurences_price(stk_symb)


    