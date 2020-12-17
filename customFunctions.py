import tweepy as tw
from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
import csv
from datetime import datetime, timedelta

# Takes in screenname of user to get tweets from, word to check for, api instance, tuple of datetimes,
# page of tweets to start on. 
def wordCheck(screenname, word, api, daterange, cursor = 1):
    
    resultList = [[]]
    
    start = daterange[0]
    end = daterange[1]
    try:
        timeline = api.user_timeline(screenname, page=str(cursor))
        if(len(timeline) == 0): return None 
        while(timeline[-1].created_at >= start):
            cursor+=1
            timeline = timeline + api.user_timeline(screenname, page=str(cursor))
        for tweet in timeline:
            tweetdate = tweet.created_at
            if (tweetdate > end): pass
            elif (tweetdate <= end and tweetdate >= start):
                tweetList = [tweetdate]
                tweetList.append(word.lower() in tweet.text.lower())
                resultList = resultList + [tweetList]
            else: return resultList
            
    except tw.TweepError as ex:
        if ex.reason == "Not authorized.": return resultList

# Takes in a list of MoC twitter handles, word to check for, api instance, tuple of datetimes, number of days in timespan.
# Returns a tuple of list of dates and list of # tweet frequency containing keyword, ready for plotting
def dataForPlot(MoCList, word, api, timespan, days):
    
    times = np.empty([])
    
    for day in range(days): times = np.append(times, timespan[0] + timedelta(day))
    
    wordResults = np.zeros([days])
    
    for MoC in MoCList:
        results = wordCheck(MoC[0], word, api, timespan)
        if(results == None): pass
        else:
            results = results[1:]
            results = results[::-1]
            for day in range(days):
                for tweet in results:
                    if(len(tweet) == 2 and tweet[0].date() == (timespan[0] + timedelta(day)).date()): 
                        wordResults[day] = wordResults[day] + tweet[1]
                        
    times = times[1:]
    return times,wordResults

# Scrapes tweets with given keywords and writes them to csv. If no keywords desired then it scrapes all tweets
# in date range.
# Takes in screenname of user to get tweets from, api instance, tuple of datetimes, 
# path to csv to write tweets to, page of tweets to start on, words to check for, whether to exclude retweets (with no quote from user).
def writeTweets(screenname, api, daterange, csvpath, cursor = 1,  keywords=None, exclude_RT = True):
    print("Working on:   " + screenname)
    resultList = [[]]
    
    start = daterange[0]
    end = daterange[1]
    try:
        timeline = api.user_timeline(screenname, page=str(cursor), tweet_mode='extended')
        #print("Timeline fetched") #commented out to limit output
        if(len(timeline) == 0): return None 
        
        #Use to make sure we haven't hit the beginning of the user's posts if it's after start date
        last_timeline_date = timeline[-1].created_at
        
        while(timeline[-1].created_at >= start):
            cursor+=1
            next_timeline = api.user_timeline(screenname, page=str(cursor), tweet_mode='extended')
            
            try:
                n = next_timeline[-1].created_at
                timeline = timeline + next_timeline
                last_timeline_date = timeline[-1].created_at
                
            except IndexError:
                #print("loop caught") #commented out to limit output
                break
        
        with open(csvpath, 'w', encoding='utf-8-sig', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            print(".csv opened")
            for tweet in timeline:
                
                if(exclude_RT and tweet.full_text[0:2] != 'RT'):
                    
                    tweetdate = tweet.created_at
                    
                    if (tweetdate > end): pass
                    
                    elif (tweetdate <= end and tweetdate >= start):
                        
                        if(keywords is not None):
                            k=""
                            for keyword in keywords:
                                if(keyword.lower() in tweet.full_text.lower()):
                                    k = k + keyword.lower() + "; "
                            if (k!=""):
                                #print("Writing to (with keywords):    " + csvpath) #commented out to limit output
                                filewriter.writerow([tweet.full_text.replace(',', '').replace("\n", " "),
                                                     tweet.created_at, tweet.source,
                                                     tweet.retweet_count, tweet.favorite_count, k])
                        elif (keywords is None):
                            #print("Writing to (without keywords):    " + csvpath) #commented out to limit output
                            filewriter.writerow([tweet.full_text.replace(',', '').replace("\n", " "), 
                                                 tweet.created_at, tweet.source,
                                                 tweet.retweet_count, tweet.favorite_count])
        print("----------------------------------")

    except tw.TweepError as ex:
        print(ex.reason)
        if ex.reason == "Not authorized.": 
            return None
        