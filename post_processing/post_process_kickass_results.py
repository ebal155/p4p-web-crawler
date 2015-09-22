import csv
import datetime
import re


class Processor:
    """This script is used to post process the raw kickass.csv file."""
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        with open(self.filename, 'rb') as f:
            postFile = open('kickass_movies_processed.csv', 'wb')
            wr = csv.writer(postFile, dialect='excel')
            reader = csv.reader(f)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                    wr.writerow(header)
                else:
                    try:
                        if not (row[14] == "N/A"):
                            #convert all download values to an int type
                            download_string = row[2]
                            row[2] = self.format_downloads_value(download_string)

                            #convert the linux date to Y/M/D format
                            linux_date = int(row[5])
                            row[5] = self.convert_linux_date_to_standard(linux_date, year_only=True)

                            #Extract the movie title out of the post title
                            post_title = row[13]
                            movie_title = self.get_movie_title(post_title)
                            row[13] = movie_title

                            #convert all the reputation values to an int type
                            author_reputation = row[17]
                            formatted_reputation = self.format_reputation_value(author_reputation)
                            row[17] = formatted_reputation

                            wr.writerow(row)

                    except Exception as e:
                        print e
                        print row
                rownum += 1

    def format_downloads_value(self, downloads):
        try:
            if downloads == "once.":
                downloads = 1
            else:
                downloads = downloads.replace(',', '')
            return downloads

        except Exception as e:
            print e
            return None

    def convert_linux_date_to_standard(self, date, year_only=False):
        try:
            newdate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
            if year_only:
                return newdate.split("-")[0]
            else:
                return newdate
        except Exception as e:
            print e
            return None

    def get_movie_title(self, post_title):
        try:
            #regular expression that searches for a 4 digit number
            #most kickass post titles are in the format "[Movie title] [Year] [Other]"
            m = re.search('\d{4}', post_title)

            if (m is None):
                return post_title
            else:
                movie_title = post_title[:m.start()-1]
                return movie_title
        except Exception as e:
            print e
            return None

    def format_reputation_value(self, reputation):
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
    p = Processor('kickass_movies.csv')
    p.process()
