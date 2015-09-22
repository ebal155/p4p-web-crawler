import csv
import operator
import sys
import re

class WarezbbProcessor():
    """This script is used to post process the raw warezbb csv file."""
    def __init__(self, filename):
        self.filename = filename

    def post_process(self):
        with open(self.filename, 'rb') as orgi:
            outputFile = open('processedWarezbbMovieFile.csv','wb')
            wr = csv.writer(outputFile, dialect='excel')
            reader = csv.reader(orgi)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                    header = filter(None, header)
                    header.append('full source names')
                    header.append('unique full source names')
                    header.append('year')
                    header.append('month')
                    header.append('day')
                    header.append('hour')
                    header.append('day of the week')
                    header.append('movie title')
                    wr.writerow(header)
                else:
                    # full source names
                    row = row[:10]
                    allSources = self.clean_code_fields(row)
                    if allSources is not None:
                        row.append(','.join(allSources))
                        row.append(','.join(set(allSources)))
                    else:
                        row.append("")
                        row.append("")
                    # format date for easier reading
                    row.append(self.get_year(row))
                    row.append(self.get_month(row))
                    row.append(self.get_day(row))
                    row.append(self.get_hour(row))
                    row.append(self.get_week_day(row))
                    # get movie Title
                    row.append(self.get_movie_title(row))
                    wr.writerow(row)

                rownum += 1

    def clean_code_fields(self, row):
        code_fields = row[0]
        if "," in code_fields:
            code_fields = code_fields.split(",")
        else:
            code_fields = [code_fields]
        new_code_fields = []
        for i in range(0,len(code_fields)):
            code = code_fields[i]
            code = code.strip()
            if "http://" in code or "https://" in code:
                code = code[code.index("//")+2:]
                if "www" in code:
                    code = code[4:]
                if "." in code:
                    code = code[:code.index(".")]
                    new_code_fields.append(code)

        if len(new_code_fields) > 0:
            return new_code_fields
        else:
            return None

    def get_day(self, row):
        try:
            date = row[3]
            return date[8:10]
        except:
            return None

    def get_movie_title(self, row):
        try:
            title = row[9]
            if ']' in title:
                title = title[title.index("]")+1:].strip()
            if re.search('\d{4}', title):
                m = re.search('\d{4}', title)
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

    def get_month(self, row):
        try:
            date = row[3]
            return date[4:7]
        except:
            return None

    def get_year(self, row):
        try:
            date = row[3]
            return date[12:16]
        except:
            return None

    def get_hour(self, row):
        try:
            date = row[3]
            hour = date[17: date.index(":")]
            if 'am' in date:
                if '12' in hour:
                    hour = 0
                else:
                    hour = int(hour)
            else:
                if '12' not in hour:
                    hour = int(hour) + 12
                else:
                    hour = int(hour)
            return hour
        except:
            return None

    def get_week_day(self, row):
        try:
            date = row[3]
            return date[0:3]
        except:
            return None

if __name__ == "__main__":
    my_analyser = WarezbbProcessor('warezbbMoviesResults.csv')
    my_analyser.post_process()
