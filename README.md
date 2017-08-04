# twitbot
## A plug-and-play Markov Twitter bot using Tweepy
### Usage
After obtaining an API key (both Consumer and Access), simply put these in the config.txt file (in the same directory as the script), as well as the source file for the Markov chain.
Then, just execute twitbot.py from the terminal! While by default it uses a third-order Markov chain, you can manually specify between second and third-order chains by passing an argument of 2 (better for smaller data sets) or 3 (produces more coherency on large data sets) to the program.
### Dependencies
Requires Python 3 and Tweepy (get it [here](https://github.com/tweepy/tweepy/) or with pip!)
