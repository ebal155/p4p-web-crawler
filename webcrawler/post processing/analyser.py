import csv
import operator

class analyser():
    def __init__(self, filename):
        self.filename = filename

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
                        field = row[col_num].split("-")[0]
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
            # f1=open('results.csv', 'wb')
            writer = csv.writer(open('results2.csv', 'wb'))
            # f1.write(col_name + ': occurence\n')
            # for field in sorted_dict:
            #     f1.write(field[0] + ": " + str(field[1]) + "\n")
            for key, value in count_dict.items():
                writer.writerow([key, value])



if __name__ == "__main__":
    my_analyser = analyser('kickass_movies_new.csv')
    field_name = "post_date"
    my_analyser.count_field(field_name , split_by_comma=False)
