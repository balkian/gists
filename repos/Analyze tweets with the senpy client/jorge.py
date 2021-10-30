import json
from senpy import Client

client = Client('http://senpy.cluster.gsi.dit.upm.es')

with open('madrid.json', 'r') as f:
    for line in f:
        tweet = json.loads(line.strip())
        results = client.analyse(input=tweet['text'], algorithm='sentiText')
        tweet['sentiment'] = results.entries[0].sentiments[0]
