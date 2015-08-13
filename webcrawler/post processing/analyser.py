import csv
import operator

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def print_dict_to_csv(self, myDict, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for key in myDict:
            writer.writerow([key, myDict[key]]) 

    def count_field(self, col_name, split_by_comma=False, print_to_file=False, return_as_dict=False):
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
                    except IndexError:
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
                    self.print_dict_to_csv(count_dict, col_name + '_count.csv')
                if return_as_dict:
                    return count_dict
                return sorted_dict


    def count_two_fields(self, col_1, col_2, split_by_comma=False, print_to_file=False):
        """ gets all cols for certain field"""
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            first_col_num = -1
            second_col_num = -1

            for i in range(0, len(column_names)):
                if column_names[i] == col_1:
                    first_col_num = i
                if column_names[i] == col_2:
                    second_col_num = i

            count_dict = {}

            if first_col_num is not -1 and second_col_num is not -1:
                for row in reader:
                    try:
                        first_field = row[first_col_num]
                        second_field = row[second_col_num]
                    except IndexError:
                        pass
                    if first_field in count_dict:
                        count_dict[first_field].append(second_field)
                    else:
                        count_dict[first_field] = [second_field]

            if print_to_file:
                self.print_dict_to_csv(count_dict, str(col_1) + '_' + str(col_2) + '_' + 'Count.csv')
            return count_dict

    def get_rows_by_field(self, field):
        """returns a dict of rows sorted by a 
        given field """

        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            col_num = -1

            count_dict = {}
            rownum = 1

            for i in range(0, len(column_names)):
                    if column_names[i] == field:
                        col_num = i
            if col_num is not -1:
                for row in reader:
                    try:
                        field_input = row[col_num]
                    except IndexError:
                        print rownum
                    if field_input in count_dict:
                        count_dict[field_input].append(row)
                    else:
                        count_dict[field_input] = [row]
                return count_dict

    def get_rows_by_field_that_have_given_value(self, field_to_sort,
        field_to_match, value):
        """returns a dict of rows sorted by a given field that match an input"""

        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            col_1 = -1
            col_2 = 1
            count_dict = {}


            for i in range(0, len(column_names)):
                    if column_names[i] == field_to_sort:
                        col_1 = i
                    if column_names[i] == field_to_match:
                        col_2 = i

            if col_1 is not -1 and col_2 is not -1:
                for row in reader:
                    try:
                        field_to_sort = row[col_1]
                        field_to_match = row[col_2]
                    except IndexError:
                        pass
                    if row[field_to_match] == row[value]:
                        if field_to_sort in count_dict:
                            count_dict[field_to_sort].append(row)
                        else:
                            count_dict[field_to_sort] = [row]
                return count_dict


if __name__ == "__main__":
    my_analyser = analyser('allWarezbbBlockResults.csv')
    field_name1 = "post_date"
    field_name2 = "author"
    my_analyser.count_field("author", split_by_comma=False, print_to_file=True)
    # my_analyser.count_field(field_name , split_by_comma=False)
