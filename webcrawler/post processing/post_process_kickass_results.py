import csv
import operator
import sys
import datetime

class Processor:
    def __init__(self, filename):
        self.filename = filename

    def post_process_post_dates(self):
        with open(self.filename, 'rb') as f:
            postFile = open('kickass_movies_new.csv', 'wb')
            wr = csv.writer(postFile, dialect='excel')
            reader = csv.reader(f)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                    wr.writerow(header)
                else:
                    try:
                        row[5] = datetime.datetime.fromtimestamp(int(row[5])).strftime('%Y-%m-%d') #'%Y-%m-%d %H:%M:%S' for time as well
                        wr.writerow(row)
                    except Exception as e:
                        print e
                rownum += 1

if __name__ == "__main__":
    p = Processor('kickass_movies.csv')
    p.post_process_post_dates()
