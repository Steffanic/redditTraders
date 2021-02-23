# redditTraders

Objective: Provide the information necessary to study the relationship between reddit activity and the stock market. 

This project was inspired by the 2021 GameStop To The Moon! event. Here's what it does so far!

## Dependencies

This project uses the [PRAW](https://praw.readthedocs.io/en/latest/index.html) API wrapper to access reddit and search for stock symbols/company names.

~~It also uses the wonderful [yfinance](https://github.com/ranaroussi/yfinance) package to access stock price history.~~ I actually ended up using the even better [yahooquery](https://yahooquery.dpguthrie.com/) library. It is very similar to yfinance and uses the same Yahoo Finance API(which is maybe deprecated entirely?) except that:

(1) It was more recently developed.
(2) It is still being maintained to some extent
(3) It solves an issue in yfinance relating to API calls and retries.

The last special package I want to highlight is [english-words](https://pypi.org/project/english-words/). Searching reddit for common english words(as stock symbols sometimes are) is counterproductive.

Finally, the standard list:

matplotlib
pandas
numpy

Here is the command to do it all:

`pip install matplotlib pandas numpy praw yahooquery english-words`

or for python3 

`pip3 install matplotlib pandas numpy praw yahooquery english-words`

## Installation

This isn't a python package yet so you can't pip install it. I would recommend cloning this repo and reading the documentation that I have not written as of writing this README; but hopefully will have written before you read this README...something about race conditions(?)

You can run the script with:

`python3 redditTrading.py`

If this is the first time you are running the script it will start searching r/pennystocks for each stock symbol, unless the symbol is a common english word, then it will search for the company name. During this search it counts the mentions in the 100 most recent search results and rejects any stocks that have less than 1 mentions or more than 40 mentions. The resulting list is saved as rStocks.pickle.

You will then be presented with a list of 25 stocks in alphabetic order and a command line interface.

    Select a stock:
     AACG : ATA Creativity Global American Depositary Shares : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 5.0
     AAL : American Airlines Group Inc. Common Stock : First mentioned in top 100 results 2021-01-25 : Number of Mentions in top 100 results 2.0
     AAPL : Apple Inc. Common Stock : First mentioned in top 100 results 2021-02-12 : Number of Mentions in top 100 results 1.0
     ABEO : Abeona Therapeutics Inc. Common Stock : First mentioned in top 100 results 2021-01-20 : Number of Mentions in top 100 results 1.0
     ABIO : ARCA biopharma Inc. Common Stock : First mentioned in top 100 results 2021-01-20 : Number of Mentions in top 100 results 18.0
     ABNB : Airbnb Inc. Class A Common Stock : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 3.0
     ABUS : Arbutus Biopharma Corporation Common Stock : First mentioned in top 100 results 2021-01-25 : Number of Mentions in top 100 results 7.0
     ACER : Acer Therapeutics Inc. Common Stock (DE) : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 6.0
     ACHC : Acadia Healthcare Company Inc. Common Stock : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 3.0
     ACHV : Achieve Life Sciences Inc. Common Shares : First mentioned in top 100 results 2021-01-25 : Number of Mentions in top 100 results 1.0
     ACRX : AcelRx Pharmaceuticals Inc. Common Stock : First mentioned in top 100 results 2021-01-24 : Number of Mentions in top 100 results 13.0
     ACST : Acasti Pharma Inc. Class A Common Stock : First mentioned in top 100 results 2021-01-25 : Number of Mentions in top 100 results 12.0
     ACTG : Acacia Research Corporation (Acacia Tech) Common Stock : First mentioned in top 100 results 2021-01-22 : Number of Mentions in top 100 results 1.0
     ADIL : Adial Pharmaceuticals Inc Common Stock : First mentioned in top 100 results 2021-02-09 : Number of Mentions in top 100 results 5.0
     ADMA : ADMA Biologics Inc Common Stock : First mentioned in top 100 results 2021-01-26 : Number of Mentions in top 100 results 1.0
     ADMP : Adamis Pharmaceuticals Corporation Common Stock : First mentioned in top 100 results 2021-02-06 : Number of Mentions in top 100 results 19.0
     ADTX : ADiTx Therapeutics Inc. Common Stock : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 5.0
     ADV : Advantage Solutions Inc. Class A Common Stock : First mentioned in top 100 results 2021-02-03 : Number of Mentions in top 100 results 5.0
     ADXS : Advaxis Inc. Common Stock : First mentioned in top 100 results 2021-02-15 : Number of Mentions in top 100 results 2.0
     AEMD : Aethlon Medical Inc. Common Stock : First mentioned in top 100 results 2021-01-22 : Number of Mentions in top 100 results 1.0
     AESE : Allied Esports Entertainment Inc. Common Stock : First mentioned in top 100 results 2021-01-27 : Number of Mentions in top 100 results 1.0
     AEZS : Aeterna Zentaris Inc. Common Stock : First mentioned in top 100 results 2021-01-21 : Number of Mentions in top 100 results 10.0
     AGBA : AGBA Acquisition Limited Ordinary Share : First mentioned in top 100 results 2021-02-16 : Number of Mentions in top 100 results 2.0
     AGRX : Agile Therapeutics Inc. Common Stock : First mentioned in top 100 results 2021-01-20 : Number of Mentions in top 100 results 3.0
     AGTC : Applied Genetic Technologies Corporation Common Stock : First mentioned in top 100 results 2021-02-09 : Number of Mentions in top 100 results 3.0
    Commands:
     s [STOCK SYMBOL] - plot stock symbol occurences and price
     d - scroll stock list down a page
     u - scroll stock list up a page
     q - quit
    >>:

    
    
When you select a stock with s, the script will search for occurences of the stock symbol in the 1000 most recent search results of r/pennystocks and produce plots of occurences/day and price/day.

Have fun!






