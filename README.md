# redditTraders

Objective: Provide the information necessary to study the relationship between reddit activity and the stock market. 

This project was inspired by the 2021 GameStop To The Moon! event. Here's what it does so far!

## Dependencies

This project uses the [PRAW](https://praw.readthedocs.io/en/latest/index.html) API wrapper to access reddit and search for stock symbols/company names.

It also uses the wonderful [yfinance](https://github.com/ranaroussi/yfinance) package to access stock price history.

The last special package I want to highlight is [english-words](https://pypi.org/project/english-words/). Searching reddit for common english words(as stock symbols sometimes are) is counterproductive.

Finally, the standard list:

matplotlib
pandas
numpy

Here is the command to do it all:

`pip install matplotlib pandas numpy praw yfinance english-words`

or for python3 

`pip3 install matplotlib pandas numpy praw yfinance english-words`

## Installation

This isn't a python package yet so you can't pip install it. I would recommend cloning this repo and reading the documentation that I have not written as of writing this README; but hopefully will have written before you read this README...something about race conditions(?)

You can run the script with:

`python3 redditTrading.py`

If this is the first time you are running the script it will start searching r/all for each stock symbol, unless the symbol is a common english word, then it will search for the company name. During this search it counts the 10 most recent occurences and rejects any stocks that have less than 10 mentions. The resulting list is saved as rStocks.pickle.

You will then be presented with a list of 25 stocks in alphabetic order and a command line interface.

    Select a stock:
     A : Agilent Technologies, Inc. Common Stock 
     AA : Alcoa Inc. Common Stock 
     AA$B : Alcoa Inc. Depository Shares Representing 1/10th Preferred Convertilble Class B Series 1 
     AAC : AAC Holdings, Inc. Common Stock 
     AAN : Aaron's, Inc. Common Stock 
     AAP : Advance Auto Parts Inc Advance Auto Parts Inc W/I 
     AAT : American Assets Trust, Inc. Common Stock 
     AAV : Advantage Oil & Gas Ltd  Ordinary Shares 
     AB : Allianceberstein Holding L.P.  Units 
     ABB : ABB Ltd Common Stock 
     ABBV : AbbVie Inc. Common Stock 
     ABC : AmerisourceBergen Corporation (Holding Co) Common Stock 
     ABEV : Ambev S.A. American Depositary Shares (Each representing 1 Common Share) 
     ABG : Asbury Automotive Group Inc Common Stock 
     ABM : ABM Industries Incorporated Common Stock 
     ABR : Arbor Realty Trust Common Stock 
     ABR$A : Arbor Realty Trust Preferred Series A 
     ABR$B : Arbor Realty Trust Cumulative Redeemable Preferred Series B 
     ABR$C : Arbor Realty Trust Cumulative Redeemable Preferred Series C 
     ABRN : Arbor Realty Trust 7.375% Senior Notes due 2021 
     ABT : Abbott Laboratories Common Stock 
     ABX : Barrick Gold Corporation Common Stock 
     ACC : American Campus Communities Inc Common Stock 
     ACCO : Acco Brands Corporation Common Stock 
     ACE : Ace Limited Common Stock 
    Commands:
     s [STOCK SYMBOL] - plot stock symbol occurences and price
     d - scroll stock list down a page
     u - scroll stock list up a page
     q - quit
    >>:
    
    
When you select a stock with s, the script will search for occurences of the stock symbol in r/all and produce plots of occurences/day and price/day.

Have fun!






