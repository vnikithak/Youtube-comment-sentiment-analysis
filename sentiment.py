# TextBlob is used to perform sentiment analysis on a text input
# apiclient and oauth2client is used to access YouTube video data via the YouTube API
# pafy is used to retrieve YouTube content and metadata
from textblob import TextBlob
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy

# The developer/API key the key given to a user when an API is enabled.
# This key is used to ensure secure access to a user’s data.
# The YouTube V3 API is used.

DEVELOPER_KEY = "ENTER YOUR KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("ENTER YOUR KEY")

# The youtube object is used to obtain YouTube data.
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

# The YouTube video ID is taken as a user input and it is used to obtain the URL of a video.
videoId = raw_input("ID of youtube video : \n")
url = "https://www.youtube.com/watch?v=" + videoId

# A video object is created using the URL. It is used to request metadata.
video = pafy.new(url)

# The 100 comments are accessed and stored in a list called results. If there are more than 100 # comments then this function is iterated.
results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoId,
		    textFormat="plainText"
		  ).execute()
totalResults = 0
totalResults = int(results["pageInfo"]["totalResults"])
count = 0
nextPageToken = ''
comments = []
further = True
first = True
while further:
	halt = False
	if first == False:
		print "."
		try:
	  		results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoId,
	  		  textFormat="plainText",
	  		  pageToken=nextPageToken
	  		).execute()
	  		totalResults = int(results["pageInfo"]["totalResults"])
	  	except HttpError, e:
			print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
			halt = True
	if halt == False:
	  	count += totalResults
	  	for item in results["items"]:
			comment = item["snippet"]["topLevelComment"]
			author = comment["snippet"]["authorDisplayName"]
			text = comment["snippet"]["textDisplay"]
			comments.append([text])
		if totalResults < 100:
			further = False
			first = False
		else:
			further = True
			first = False
			try:
				nextPageToken = results["nextPageToken"]
			except KeyError, e:
				print "An KeyError error occurred: %s" % (e)
				further = False

# This if-else condition is used to set the maximum of the comments range. If it is greater than
# 999 then only the top 1000 comments in the video are chosen. If the number of comments are
#less than 1000 then the length of the comments list is taken as the maximum.

if len(comments)>999:
	x=1000
else:
	x=len(comments)

# This section of code iterates through the comments and determines if each comment has a                          #positive, negative or neutral sentiment.
pos=0
neg=0
neutral=0
for com in range(0,x):
	text_sample=TextBlob(comments[com].__str__());
	if text_sample.sentiment.polarity > 0: pos+=1
	elif text_sample.sentiment.polarity == 0: neutral+=1
	else: neg+=1

print("\nANALYSIS OF YouTube VIDEO CONTENT (FROM VIEWERS' PERSPECTIVE):\n")
print("YouTube video chosen: ",video.title)

# Output the number of positive, negative and neutral comments.
print("\n\nVIEWERS' COMMENTS ANALYSIS:\n")
print("\nPositive: ",pos)
print("\nNeutral: ",neutral)
print("\nNegative: ",neg)

# Output the number of likes and dislikes.
print("\nVIEWERS' LIKES/DISLIKES:\n")
print("\n\nVideo Likes: ",video.likes)
print("\nVideo Dislikes: ",video.dislikes)

# If ‘p’ is chosen then output the positive comments, else if ‘n’ is chosen then output the positive # comments otherwise terminate.
inp=raw_input("\n\nEnter p to view positive comments and n to view negative comments.\n")

if inp=='p':
	for com in range(0,x):
		text_sample=TextBlob(comments[com].__str__());
		if text_sample.sentiment.polarity > 0: print(comments[com])
elif inp=='n':
	for com in range(0,x):
		text_sample=TextBlob(comments[com].__str__());
		if text_sample.sentiment.polarity < 0: print(comments[com])
