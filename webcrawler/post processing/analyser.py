import csv
import operator

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def print_dict_to_csv(self, myDict, filename):
        writer = csv.writer(open(filename), 'wb'))
        for field in my_dict:
            writer.writerow([field[0],str(field[1])])

    def count_field(self, col_name, split_by_comma=False, print_to_file=True):
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
            if print_to_file:
                self.print_dict_to_csv(sorted_dict, col_name + '_count.csv')
            return sorted_dict


    def count_two_fields(self, col_1, col_2, split_by_comma=False, print_to_file=False):
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            col_num1 = -1
            col_num2 = -1

            #Do something here if the same fields were passed
            if col_1 == col_2:
                pass #TODO

            #Get the column index of both fields that is trying to be found
            for i in range(0, len(column_names)):
                if column_names[i] == col_1:
                    col_num1 = i
                if column_names[i] == col_2:
                    col_num2 = i

            count_dict = {}
            rownum = 1


            if col_num1 != -1 and col_num2 != -1:

                #For every row in the csv file, fetch the data for post_date and author
                for row in reader:
                    try:
                        post_date = row[col_num1]
                        author = row[col_num2]
                    except IndexError as e:
                        print rownum

                    #Logic if the entries in the field is seperated by a comma (e.g. "120p,240p,360p")
                    if (split_by_comma):
                        pass
                    else:
                        #If the post_date is already in the dictionary, add the author to the set inside it.
                        if post_date in count_dict:
                            count_dict[post_date].add(author)
                        #If the post_date is not yet in the dictionary, create a new set and add the author to it
                        else:
                            count_dict[post_date] =  set()
                            count_dict[post_date].add(author)
                    #Search the next row
                    rownum += 1

            if print_to_file:
                self.print_dict_to_csv(sorted_dict, col1 + "_" + col2 + '_count.csv')
            return sort_dict

if __name__ == "__main__":
    my_analyser = analyser('kickass_movies_new.csv')
    field_name1 = "post_date"
    field_name2 = "author"
    my_analyser.count_two_fields(field_name1, field_name2, split_by_comma=False,print_to_file=True)
    # my_analyser.count_field(field_name , split_by_comma=False)
