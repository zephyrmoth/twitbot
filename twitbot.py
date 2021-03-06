import tweepy
import sys, traceback
from pathlib import Path
import markov
#Loads the API keys from the config.txt file and authorizes the script
chain_length = 0
#Specifies the order of Markov chain you want used for generating the 
if len(sys.argv) == 0:
    chain_length = 3
else:
    chain_length = int(sys.argv[1])
if not (1 < int(chain_length) < 4):
    raise ValueError("Invalid chain length")
config = open("config.txt", "r")
consumer_token = (config.readline().rstrip("\n")).rstrip("\r")[15:]
consumer_secret = (config.readline().rstrip("\n")).rstrip("\r")[16:]
access_token = (config.readline().rstrip("\n")).rstrip("\r")[13:]
access_secret = (config.readline().rstrip("\n")).rstrip("\r")[14:]
source_file = (config.readline().rstrip("\n")).rstrip("\r")[12:]
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
#Method to format the Tweet using the provided Markov script
def tweetStr(file, chain_order):
    #Reads the provided source file and uses it to create a Markov tree
    file_input = Path(file).read_text()
    if chain_order == 3:
        markov.read3(file_input)
    elif chain_order == 2:
        markov.read2(file_input)
    raw_text = ""
    #Failsafe to ensure that the message is compatiable with Twitter 
    while len(raw_text) == 0 or len(raw_text) > 140:
        if chain_order == 3:
            raw_text = markov.speak3(50, True)
        elif chain_order == 2:
            raw_text = markov.speak2(50, True)
    formatted_text = ""
    #"Special sauce" to make it conform to English grammar conventions.
    valid = False
    while valid != True:
        if "." in raw_text:
            num = raw_text.rfind(".")
            formatted_text = raw_text[:num + 1]
        elif "!" in raw_text:
            num = raw_text.rfind("!")
            formatted_text = raw_text[:num + 1]
        elif "?" in raw_text:
            num = raw_text.rfind("?")
            formatted_text = raw_text[:num + 1]
        else:
            if chain_order == 3:
                raw_text = markov.speak3(50, True)
            elif chain_order == 2:
                raw_text = markov.speak2(50, True)
        if len(formatted_text) > 0:
            valid = True
    #Hacky way of preventing random parentheses in Tweet
    if ("(" in formatted_text and ")" not in formatted_text):
        formatted_text = formatted_text.replace("(", "")
    if (")" in formatted_text and "(" not in formatted_text):
        formatted_text = formatted_text.replace(")", "")
    return formatted_text

#Prints the tweet to the console and posts it to Twitter
api = tweepy.API(auth)
tweet = tweetStr(source_file, chain_length)
print(tweet)
api.update_status(tweet)