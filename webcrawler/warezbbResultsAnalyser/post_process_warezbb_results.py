import csv
import operator

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def total_author_count(self):
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            rownum = 0
            authorDict = {}
            for row in reader:
                if rownum == 0:
                    header = row
                else:
                    try:
                        author = row[1]
                    except IndexError:
                        print rownum

                    if author in authorDict:
                        authorDict[author] += 1
                    else:
                        authorDict[author] = 1
                rownum += 1

            sorted_dict = sorted(authorDict.items(), key=operator.itemgetter(1), reverse=True)
            f1=open('authorCount.txt', 'w+')
            f1.write('author: occurence\n')
            for author in sorted_dict:
                f1.write(author[0] + ": " + str(author[1]) + "\n")

    def quality_count(self):
        print "here"
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            rownum = 0
            qualityDict = {}
            for row in reader:
                if rownum == 0:
                    header = row
                else:
                    try:
                        quality_array = row[8].strip().split(",")
                    except IndexError:
                        print rownum
                    for quality in quality_array:
                        quality = quality.strip()
                        if quality in qualityDict:
                            qualityDict[quality] += 1
                        else:
                            qualityDict[quality] = 1
                rownum += 1
            sorted_dict = sorted(qualityDict.items(), key=operator.itemgetter(1), reverse=True)
            f1=open('qualityCount.txt', 'w+')
            f1.write('quality: occurence\n')
            for quality in sorted_dict:
                f1.write(quality[0] + ": " + str(quality[1]) + "\n")



if __name__ == "__main__":
    my_analyser = analyser('warezbbMoviesResults.csv')
    my_analyser.quality_count()