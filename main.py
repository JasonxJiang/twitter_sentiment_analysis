from twitter import *
from pprint import pprint 
import json





CONSUMER_KEY = 'FaVL08EBVXUXsGX9BRa9AmJyt'
CONSUMER_SECRET = 'RbR7O8fAJfjd3hVEwnDwTbBFTipPqgxfSj7PKubexg2SVEAfpb'
ACCESS_TOKEN = '4560655106-rcVbBfmBMJ3Hzm6BpolcqLBZ6DWZ7n7Xr7RPC4w'
ACCESS_SECRET ='M0iwBcIESxi61ELEIcHUzzv2qUrdE5gOcOCoUqGgvNe2g'
oauth = OAuth(ACCESS_TOKEN,ACCESS_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

#separate implementation
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input





def get_tweet_json(n, t_stream, topic,json_name):
	iterator = t_stream.statuses.filter(track="sanders")
	filename = json_name + ".json"
	fo = open(filename, "wb")
	fo.write("[\n")
	print "Entered get_tweet_json() and about to start loop"
	for tweet in iterator:
		print "Iteration:" + str(n) + "\n"
		n-=1
		if n >0:
			fo.write(json.dumps(tweet) + ",\n")
		elif (n == 0):
			fo.write(json.dumps(tweet))
			break
		else:
			break
	fo.write("]")
	fo.close()	

def load_json_file(json_file,save_filename, field):
	fo = open(save_filename +".txt", "wb")
	data = json_load_byteified(open(json_file))
	for obj in data: 
		fo.write(obj[field] + "\n")
	fo.close()

def get_tweet_hashtag(twitter,hashtag,num):
	print "success in get_tweet_hashtag"
	return json.dumps(twitter.search.tweets(q=hashtag, result_type='recent', lang='en', count=num))

#currently doesn't work 
def write_json_file(json_stream, filename,data):
	fo = open(filename + ".json", "wb")
	#for obj in json_stream: 
	#	fo.write(obj["text"] + "\n")
	fo.write(json_stream)
	fo.close()
	print "opening file"
	fo = open(filename+"tweets.txt", "wb")
	tweets_file = open(filename+".json", 'r')

	for line in tweets_file:
		try:
			print line
			tweet = json.loads(line.strip())
			if 'text' in tweet: 
				fo.write(tweet['text'])
				print "decoding successful"
		except:
			continue
	fo.close()


class PTweet:
	def __init__(self, filename):
		self.filename = filename

	def get_tweet_text(self):
		with open(self.filename) as data_file:
			data = json.load(data_file)
		for obj in data:
			print obj["text"] 

file = 'trump20.json'
def main():
	print "hello! welcome to my twitter app"
	#tweet_topic = raw_input('What tweet topic are you looking for?\n')
	#file_name = raw_input("What file name do you want to save the json data to?\n")
	#tweet_num = raw_input("How many tweets do you want?\n")
	#print file_name
	#json_data = open(file)
	tweet_topic = "sanders"
	file_name = "sanders100"
	print "about to retrieve json data"
	#get_tweet_json(100,twitter_stream,tweet_topic,file_name)
	print "Finished getting json data processing json data"
	json_filename = file_name + ".json"
	#load_json_file(json_filename, file_name, "text")
	twitter = Twitter(auth=oauth)
	json_stream = get_tweet_hashtag(twitter, "trump2016",10)
	write_json_file(json_stream, "trump10test", "text")
	print "Finished converting your tweets into a text file you can find it in " + file_name + ".txt"

if __name__ == "__main__":
	main()






