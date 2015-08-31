import csv
import operator
import sys
import datetime
import re

class Processor:
    def __init__(self, filename):
        self.filename = filename

    def post_process_post_dates(self):
        with open(self.filename, 'rb') as f:
            postFile = open('COMPLETELEYNEWKICKASS.csv', 'wb')
            wr = csv.writer(postFile, dialect='excel')
            reader = csv.reader(f)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                    wr.writerow(header)
                else:
                    try:
                        
                        # row[5] = datetime.datetime.fromtimestamp(int(row[5])).strftime('%Y-%m-%d') #'%Y-%m-%d %H:%M:%S' for time as well
                        
                        #format row
                        # title = row[13]
                        # new_title = self.get_movie_title(title)
                        # row[13] = new_title

                        author_reputation = row[17]
                        formatted_reputation = self.format_reputation_value(author_reputation)
                        row[17] = formatted_reputation

                        wr.writerow(row)

                    except Exception as e:
                        print e
                rownum += 1

    def get_movie_title(self,title):
        try:
            if ']' in title:
                title = title[title.index("]")+1:].strip()
            if re.search('\d{4}', title):
                m =  re.search('\d{4}', title)
                if m:
                    title = title[:m.start()]
                if "(" in title:
                    title = title[:title.index('(')]
                if "." in title:
                    title = title.replace('.', ' ')
                return title.strip()
        except Exception as e:
            print e
            return None

    def format_reputation_value(self,reputation):
        try:
            if 'K' in reputation:
                new_reputation = int(float(reputation.split("K")[0]) * 1000)
                return new_reputation
            else:
                return reputation
        except Exception as e:
            print e
            return None


if __name__ == "__main__":
    p = Processor('kickass_movies_no_na.csv')
    p.post_process_post_dates()
