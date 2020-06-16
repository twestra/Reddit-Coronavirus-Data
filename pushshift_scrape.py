3import praw
import datetime
from pprint import pprint
import pandas
import requests
import json
import time
#reddit = praw.Reddit(client_id="XDZu6owcUbESSw",
#                     client_secret="OEVxLiF7QOrtKtW8sD4EXovHtkg",
#                     user_agent="personal:westrascraper:v0.5(by /u/scrapertest123)")

#Url and pushshift data- we will update more throughout

class Scraper:


    def __init__(self):
    
        self.url = 'https://api.pushshift.io/reddit/search/submission'
        self.subdata = {'subreddit':'Coronavirus', 'size':500}
        self.submissions = {}

        self.last_requested = None
        self.processed_subs = 0

        self.tr = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit=coronavirus&metadata=true&size=0')
        self.totalposts = json.loads(self.tr.text)['metadata']['total_results']

    def getpushshiftdata(self,before = None, size = None):
        """
        Get data in specified time range. Use in a loop to get data back to start
        :param before: Get submissions before this date
        :param size: Number of submissions to get

        :return: data requested
        """
        if self.last_requested is not None:
            if self.last_requested:
                self.subdata['before'] = self.last_requested[-1]['created_utc']
            else: return [] #if the last thing we pulled was empty we're done with the data
        r = requests.get(self.url, params = self.subdata)
        if not r.ok:
            raise Exception("Server returned status code {}".format(results.status_code))

        return json.loads(r.text)['data']

    def getsubmissionupdates(self,after, size = None):
        #print(self.last_requested)
        if self.last_requested is not None:
            print("hello")
            if self.last_requested:
                print('yo')
                self.subdata['before'] = self.last_requested[-1]['created_utc']
                print(f"Stopping at utc:{after}. Current utc:{self.subdata['before']}")
                if after > self.subdata['before']:
                    return []
        r = requests.get(self.url, params = self.subdata)
        if not r.ok:
            raise Exception("Server returned status code {}".format(results.status_code))
        blabh = len(json.loads(r.text)['data'])
        print(f"length of request = {blabh}")
        return json.loads(r.text)['data']

    def generateEntries(self,jsonData):
        """
        Create an entry for the given data and add it to our dictionary, using the format:
        data{
        date1:
                [{title:x,
                id:x,
                comments:x,
                link:x,
                },
                {title:x,
                id:x,
                comments:x,
                link:x,
                }]
        date2:
        date3:
        etc.
        }
        :param jsonData: Data returned from json.loads() on a page of data
        :return: Nothing
        """
        x = 0
        for entry in range(len(jsonData)):
            if 'created_utc' in jsonData[entry]:
                date = ((datetime.datetime.utcfromtimestamp(jsonData[entry]['created_utc']).date()).isoformat())
                if date not in self.submissions:
                    self.submissions[date] = []
                id = jsonData[entry].get('id', -1)
                title = jsonData[entry].get('title', -1)
                url = jsonData[entry].get('url', -1)
                selftext = jsonData[entry].get('selftext', -1)
                newDict = {'id':id, 'title':title, 'url':url, 'selftext': selftext}
                self.submissions[date].append(newDict)
                x+=1
        return x


    def create_submissions_json(self):
        """
        Create a json doc containing all of submission data for a subreddit
        :param last_requested: last page we retrieved
        :param submissions: this is our big array of all json data that we will eventually write
        :param processed_subs: used to keep track of how many submissions we have read
        """
        while(self.last_requested != [] and len(self.submissions)<158):
            self.last_requested = self.getpushshiftdata()
            self.processed_subs += self.generateEntries(self.last_requested)
            print(f"Processed {self.processed_subs} submissions out of {self.totalposts}")
            time.sleep(.1)
        with open("reddit_corona_data.json", "w") as out:
            json.dump(self.submissions, out, indent=4)

    def update_submissions(self):
        with open("reddit_corona_data.json", "r") as rd:
            old_json = json.load(rd)
        old_utc = round(datetime.datetime.fromisoformat(list(old_json.keys())[0]).timestamp())
        print(old_utc)
        while(self.last_requested != []):
            self.last_requested = self.getsubmissionupdates(old_utc, 500)
            #print(self.last_requested)
            self.processed_subs += self.generateEntries(self.last_requested)
            print(f"Processed {self.processed_subs} submissions out of 4581")
            time.sleep(.1)
            
        dupdates = []
        for date in old_json:
            if date in self.submissions:
                for dict in old_json[date]:
                    artid = dict['id']
                    for dict in self.submissions[date]:
                        if dict['id'] == artid:
                            continue
                    self.submissions[date].append(dict)
                dupdates.append(date)
        for date in dupdates:
            old_json.pop(date)
        
        for date in old_json:
            self.submissions[date] = old_json[date]
        with open("test.json", "w+") as out:
            json.dump(self.submissions, out, indent=4)

scraper = Scraper()
scraper.update_submissions()
    #create_submissions_json(last_requested, submissions, processed_subs)


        
        
