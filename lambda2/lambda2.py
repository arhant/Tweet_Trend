from __future__ import print_function
import json
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
import json

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

host = ''

aws_id =''
aws_key= ''
auth = AWSRequestsAuth(aws_access_key=aws_id,
                       aws_secret_access_key=aws_key,
                       aws_host=host,
                       aws_region='us-east-2',
                       aws_service='es')

client = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    use_ssl=True,
    http_auth=auth,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    
    try:
        content = json.loads(message)
        lat = (content['lat'])
        lng = (content['lng'])
        sentiment = (content['sentiment'])
        tweet = (content['tweet'])
    
    except:
        pass
        
    
    try:
                    client.index(index='tweepy', doc_type='tweet_trend', body={
                     'content': tweet,
                     'lat': lat,
                     'lng': lng,
                     'sentiment': sentiment
                     })
    except:
                    print('ElasticSearch indexing failed')
    
    return message

