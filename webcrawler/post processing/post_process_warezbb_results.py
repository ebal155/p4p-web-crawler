import csv
import operator
import sys

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def post_process_code_fields(self):
        with open(self.filename, 'rb') as preF:
            postFile = open('kickass_movies.csv', 'wb')
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

    def count_field(self, col_name, split_by_comma=False):
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

    my_analyser = analyser('kickass_movies.csv')
    field_name = "author"
    my_analyser.count_field(field_name , split_by_comma=True)
    # my_analyser.post_process_code_fields()
