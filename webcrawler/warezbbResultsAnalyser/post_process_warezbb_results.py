import csv
import operator

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def post_process_code_fields(self):
        with open(self.filename, 'rb') as preF:
            postFile = open('postResultWarez.csv', 'wb')
            wr = csv.writer(postFile, dialect='excel')
            reader = csv.reader(preF)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                    wr.writerow(header)
                else:
                    try:
                        code_fields = row[0].split(",")
                        for i in range(0,len(code_fields)):
                            code = code_fields[i]
                            code = code.strip()
                            if "http://" in code or "https://" in code:
                                code = code[code.index("//")+2:]
                                if "www" in code:
                                    code = code[4:]
                                code = code[:code.index(".")]
                                code_fields[i] = code
                        row[0] = code_fields
                        wr.writerow(row)
                        print row[0]
                    except Exception as e:
                        print e
                rownum += 1

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
    my_analyser.post_process_code_fields()