from __future__ import print_function
import json
import requests
import boto3
import urllib
import urllib2
from monkeylearn import MonkeyLearn
sqs = boto3.resource('sqs')
arn = ''
arn2 = ''
queue = sqs.get_queue_by_name(QueueName='tweet_trend')
queue_url = "https://sqs.us-east-2.amazonaws.com/448531576131/tweet_trend"
sns = boto3.client('sns', aws_access_key_id="" , aws_secret_access_key="")
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
module_id = 'cl_qkjxv9Ly'
ml = MonkeyLearn('')




def lambda_handler(event, context):
    sns.publish(TargetArn=arn2, Message=json.dumps("turning sqs on"))
    while True:
        messages = queue.receive_messages(QueueUrl=queue_url, MessageAttributeNames=['Tweet', 'Latitude', 'Longitude'])
        if len(messages)>0:
            for message in messages:
                if message.message_attributes is not None:
                    print("Received event: " + json.dumps(event, indent=2))
                    try:
                        text_word = event['params']['querystring']['options']
                        print (text_word)
                                
                        tweet =  [message.message_attributes.get('Tweet').get('StringValue')]
                        print(tweet)
                        #if True:
                        if str(text_word) in str(tweet):
                            lat = message.message_attributes.get('Latitude').get('StringValue')
                            lng = message.message_attributes.get('Longitude').get('StringValue')
                    
                            res = ml.classifiers.classify(module_id, tweet, sandbox=False)
                            sentiment = res.result[0][0]['label']
                    
                    
                    
                            print(sentiment)
                    
                            sns_message = {"tweet":tweet, "lat":lat, "lng": lng, "sentiment":sentiment}
                            print("SNS messsage: "+str(sns_message) + "\n\n")
                            sns.publish(TargetArn=arn, Message=json.dumps(sns_message))
                                    
                    except:
                        pass
    
                            
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' ,
            'Access-Control-Allow-Origin' : '*'
        },
        'body': sns_message
        } 
