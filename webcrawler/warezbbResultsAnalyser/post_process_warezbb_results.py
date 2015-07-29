import csv
import operator
import sys

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
                    except IndexError as e:
                        print rownum

                    if author in authorDict:
                        authorDict[author] += 1
                    else:
                        authorDict[author] = 1
                rownum += 1

            sorted_dict = sorted(authorDict.items(), key=operator.itemgetter(1), reverse=True)
            f1 = open('authorCount.txt', 'w+')
            f1.write('author: occurence\n')
            for author in sorted_dict:
                f1.write(author[0] + ": " + str(author[1]) + "\n")

    def quality_count(self):
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            rownum = 0
            qualityDict = {}
            for row in reader:
                if rownum == 0:
                    pass
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
            f1 = open('qualityCount.txt', 'w+')
            f1.write('quality: occurence\n')
            for quality in sorted_dict:
                f1.write(quality[0] + ": " + str(quality[1]) + "\n")

    def count_field(self, col_name, split_by_comma=False, output_to_file=False):
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            col_num = -1

            for i in range(0, len(column_names)):
                if column_names[i] == col_name:
                    col_num = i

            count_dict = {}
            rownum = 1

            if col_num != -1:
                for row in reader:
                    try:
                        field = row[col_num]
                    except IndexError as e:
                        print rownum

                    if (split_by_comma):
                        field_array = field.strip().split(",")
                        for f in field_array:
                            if f in count_dict:
                                count_dict[f] += 1
                            else:
                                count_dict[f] = 1
                    else:
                        if field in count_dict:
                                count_dict[field] += 1
                        else:
                                count_dict[field] = 1
                    rownum += 1

            sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
            f1=open('count.txt', 'w+')
            f1.write(col_name + ': occurence\n')
            for field in sorted_dict:
                f1.write(field[0] + ": " + str(field[1]) + "\n")


if __name__ == "__main__":
    print str(sys.argv)
    my_analyser = analyser('warezbbMoviesResults.csv')
    # my_analyser.quality_count()
    # my_analyser.total_author_count()
    my_analyser.count_field("detected_quality", split_by_comma=True)
