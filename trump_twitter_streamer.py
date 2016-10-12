#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Import general libraries 
import urllib 
import httplib2
import json

# Import other python files
import config

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

# # # # SENTIMENT ANALYZER # # # #
class SentimentAnalyzer():
    """
    Uses the Google Cloud Natural Language Processing Tool to 
    analyze the sentiment of tweets. 
    """
    def __init__(self):
        pass


    def analyze_all_tweet_sentiment(self, tweet_file):
        twitter_sentiment_list = []
        with open(tweet_file,'r') as tf:
            for tweet in tf:
                polarity, magnitude = self.analyze_tweet_sentiment(tweet)
                tweet_and_sentiment = tweet +',' + "POLARITY::" + str(polarity) + "," + \
                                      "MAGNITUDE::" + str(magnitude) + '\n'
                twitter_sentiment_list.append(tweet_and_sentiment)                
        return twitter_sentiment_list

    

    def analyze_tweet_sentiment(self, tweet):
        http = httplib2.Http()

        credentials = GoogleCredentials.get_application_default().create_scoped(['https://www.googleapis.com/auth/cloud-platform'])
        http=httplib2.Http()
        credentials.authorize(http)

        service = discovery.build('language', 'v1beta1',
                                http=http, discoveryServiceUrl=DISCOVERY_URL)

        service_request = service.documents().analyzeSentiment(
            body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': tweet,
                }
            })

        response = service_request.execute()
        polarity = response['documentSentiment']['polarity']
        magnitude = response['documentSentiment']['magnitude']
        #print('Sentiment: polarity of %s with magnitude of %s' % (polarity, magnitude))
        return polarity, magnitude


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """


    def __init__(self):
        pass


    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)



# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.sa = SentimentAnalyzer()


    def on_data(self, data):
        tweet = data.split(',"text":"')[1].split('","source')[0]
        if not tweet.startswith('RT'):
            polarity, magnitude = self.sa.analyze_tweet_sentiment(tweet)
            tweet_and_sentiment = tweet +',' + "POLARITY::" + str(polarity) + "," + \
                                  "MAGNITUDE::" + str(magnitude) + '\n'            
            print(tweet_and_sentiment)
            print("\n")
            with open(fetched_tweets_filename,'a') as tf:
                tf.write(tweet_and_sentiment)
                #tf.write("\n")
        return True


    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    hash_tag_list = ['#2016election', '#election2016','#crookedhillary', '#trump2016', '#makeamericagreatagain', "trumptrain"]
    fetched_tweets_filename = "trump_tweets.txt"

    ts = TwitterStreamer()
    ts.stream_tweets(fetched_tweets_filename, hash_tag_list)
