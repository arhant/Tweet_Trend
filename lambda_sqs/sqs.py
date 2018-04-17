from __future__ import print_function
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
import boto3
import requests

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tweet_trend')
queue_url = ""
t_end = 0
t_end = time.time() + 60 * 1
i=0
print('Loading function')
# print ("one:::" + str(time.time()) + " current " + str(t_end))


def lambda_handler(event, context):
    global t_end
    t_end = time.time() + 60 * 1
    global i
    print (str(time.time()) + " current " + str(t_end))
    if time.time() < t_end-10:  
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        stream = Stream(auth, StdOutListener())
        stream.filter(languages=['en'], track=['trump','missuniverse','messi','MissUniverse','bush','thursday','josh brown','#indvsnz','samsung','apple',
                         'location','amazon','dollar','lenovo','hugh','pizza','snapchat','money','hrithik','vodka',
                         'election','https','lol','instagram','twitter','fb','facebook','nba','birthday',
                         'technology', 'hillary', 'food', 'travel','vote','nintendo', 'fashion', 'soccer',
                         'sports','modi','debate','america','india','obama','song','punjab','new york','bernie',
                         'news','logan','usa','london','health','Dangal','spain','music','travel','skyline','bigboss',
                         'foodie','sharktank','neverkock','missuniverse2017','october','rodgers','harvey','menwillbemen','mondaymotivation'])
    else:    
        stream.disconnect()          
        i = 1
        del stream
        return "time over early"
        
        
        
        
        
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        global t_end
        if time.time() < t_end-10:
            global queue
            data_json = json.loads(data)
            try:
                coordinates = data_json['place']['bounding_box']['coordinates']
                tweet = data_json['text']
                #print tweet
                place = data_json['place']
                language = data_json[u'user'][u'lang']
                #print language
                if place is not None and language== u'en':
                    if coordinates[0] is not None and len(coordinates[0]) > 0:
                        avg_x = 0
                        avg_y = 0
                        for c in coordinates[0]:
                            avg_x = (avg_x + c[0])
                            avg_y = (avg_y + c[1])
                        avg_x /= len(coordinates[0])
                        avg_y /= len(coordinates[0])
                        coordinates = [avg_x, avg_y]
                
                    e_data = {
                        'Tweet': {'DataType': 'String', 'StringValue': (tweet).encode("utf-8")},
                        'Latitude': {'DataType': 'Number', 'StringValue':str(avg_x)},
                        'Longitude': {'DataType': 'Number', 'StringValue': str(avg_y)}
                    
                    }
                    print(e_data)
                    queue.send_message(QueueUrl=queue_url, MessageBody="tweet",MessageAttributes=e_data)
                
            except (KeyError, TypeError):
                pass
        else:
            return False

        def on_status(self, status):
            print (status)        
