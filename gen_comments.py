import os
import json
import sys


class CommentGenerator:

    def __init__(self, filepath):
        self.fp = filepath
        self.newfiles = []
    def makeFiles(self):
        """
        Create file structure as follows:
        -'Comments'.dir
        -   -Date.dir
        -   -   -article.fil
        -   -   -article.fil
        -   -Date.dir
        -   -   -article.fil
        -   -   -etc.
        -   -etc.
        """
        try:
            os.mkdir("Comments")
        except OSError:
            print("Comments directory may already exist.")
        else:
            print("Comments directory created.")


        #make a dictionary of all date-article pairs (i.e. each date-key has a value which is an array of all article ids for that day
        dates = {}
        with open(self.fp, 'r') as f:
            jsondates = json.load(f)
            print(len(jsondates))
            x = 0
            for date in jsondates:
                artids = []
                for dict in jsondates[date]:
                    artids.append(dict['id'])
                dates[date] = artids
                
        #now make all date directories and a file for each article
        for date in dates:
            tempfp = "Comments/"+date
            try:
                os.mkdir(tempfp)
            except OSError:
                print(f"{date} directory may already exist.")
            else:
                print(f"{date} directory created.")
            for id in dates[date]:
                tempfp = "Comments/"+date+"/"+id
                if not os.path.exists((tempfp)):
                    self.newfiles.append(tempfp)
                    with open(tempfp, 'w+') as f:
                        continue
            
    

dog = CommentGenerator("test.json")
dog.makeFiles()

