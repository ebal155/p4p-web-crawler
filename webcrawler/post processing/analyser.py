import csv
import operator
import math

class analyser():
    def __init__(self, filename):
        self.filename = filename

    def print_dict_to_csv(self, myDict, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for key in myDict:
            writer.writerow([key, myDict[key]])

    def print_array_to_csv(self, myArray, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for x in range(0,len(myArray)):
            writer.writerow([x,myArray[x]])

    def print_logged_array_to_csv(self, myArray, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for x in range(0,len(myArray)):
            print 0
            print math.log(x+1)
            print math.log(myArray[x])
            writer.writerow([math.log(x+1),math.log(myArray[x])])

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
                        field = row[col_num]
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


    def count_field_unique(self, col_1, col_2, split_by_comma=False, print_to_file=False):
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

            unique_dict = {}

            if first_col_num is not -1 and second_col_num is not -1:
                for row in reader:
                    try:
                        first_field = row[first_col_num]
                        second_field = row[second_col_num]
                    except IndexError:
                        pass
                    if first_field in unique_dict:
                        pass
                    else:
                        unique_dict[first_field] = second_field

            if print_to_file:
                self.print_dict_to_csv(unique_dict, str(col_1) + '_' + str(col_2) + '_' + 'Count.csv')
            return unique_dict

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
                        first_field = row[first_col_num].split("-")[0]
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

    def count_two_fields_matching_value(self, col_1, col_2, value, print_to_file=False):
        """ gets all cols for certain field that match input"""
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
                    if second_field == value:
                        if first_field in count_dict:
                            count_dict[first_field] += 1
                        else:
                            count_dict[first_field] = 1

            if print_to_file:
                self.print_dict_to_csv(count_dict, str(col_1) + '_' + str(col_2) + '_' + 'Count.csv')
            return count_dict

    def count_two_fields_matching_value_in_third_field(self, col_1, col_2, col_3, value, print_to_file=False):
        """ gets all cols for certain field that match input"""
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            first_col_num = -1
            second_col_num = -1
            third_col_num = -1

            for i in range(0, len(column_names)):
                if column_names[i] == col_1:
                    first_col_num = i
                if column_names[i] == col_2:
                    second_col_num = i
                if column_names[i] == col_3:
                    third_col_num = i

            count_dict = {}

            if first_col_num is not -1 and second_col_num is not -1 and third_col_num is not -1:
                for row in reader:
                    try:
                        first_field = row[first_col_num]
                        second_field = row[second_col_num]
                    except IndexError:
                        pass
                    if third_col_num == value:
                        if first_field in count_dict:
                            count_dict[first_field].append(second_field)
                        else:
                            count_dict[first_field] = [second_field]

            if print_to_file:
                self.print_dict_to_csv(count_dict, str(col_1) + '_' + str(col_2) + '_' + 'Count.csv')
            return count_dict
        
    def count_two_fields_matching_third_field(self, col_1, col_2, col_3, value, print_to_file=False):
        """ gets all cols for certain field that match input"""
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            first_col_num = -1
            second_col_num = -1
            third_col_num = -1

            for i in range(0, len(column_names)):
                if column_names[i] == col_1:
                    first_col_num = i
                if column_names[i] == col_2:
                    second_col_num = i
                if column_names[i] == col_3:
                    third_col_num = i

            count_dict = {}

            if first_col_num is not -1 and second_col_num is not -1 and third_col_num is not -1:
                for row in reader:
                    try:
                        first_field = row[first_col_num]
                        second_field = row[second_col_num]
                        third_field = row[third_col_num].split("-")[0] ##HARD-CODED TO FORMAT POST DATES
                    except IndexError:
                        pass
                    if third_field == value:
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
            col_2 = -1
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

    def get_col(self, col_name):
        col = []
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            column_names = reader.next()
            col_no = -1
            for i in range(0, len(column_names)):
                if column_names[i] == col_name:
                    col_no = i
            if col_no is not -1:
                for row in reader:
                    try:
                        field = row[col_no]
                        col.append(field)
                    except IndexError:
                        pass
        return col

    def get_quality_type(self, quality):
        """qualities is a list of all the qualities that appear"""

        #CAM telesync, cam, hdts, iphone
        # VHS vcd, vhs, vhsrip, 
        #DVD dvd, dvdrip,telecine, workprint, screener, tc, ppv, 480p, tvrip, "dvdsrc"
        #HD 1080p, blu-ray, hdrip, 720p, bdrip, brrip, hdtv, 'x264'
        #Web web-dl, bdrip, webrip, vodrip, web dl, mp4, "MPEG-4"
        #unkown N/A, Unknown

        quality = quality.lower()

        cam_dict = {"telesync": 0, "cam": 0, "hdts": 0, "iphone": 0}
        vhs_dict = {"vcd": 0, "vhs": 0, "vhsrip": 0}
        dvd_dict = {"dvd": 0, "dvdrip": 0, "telecine": 0, "workprint": 0,
        "screener": 0, "dvdsrc": 0, "tc": 0, "ppv": 0, "480p": 0}
        web_dict = {"web-dl": 0, "bdrip": 0, "webrip": 0, "vodrip": 0, "web dl": 0, "mp4": 0, "MPEG-4": 0}
        hd_dict = {"1080p": 0,"blu-ray": 0,"hdrip": 0,"720p": 0,"bdrip": 0, "brrip": 0, "hdtv": 0, 'x264': 0,"bluray":0}
        na_dict = {"":0, "n/a":0, "unknown":0}

        if quality in cam_dict:
            return "cam"
        if quality in vhs_dict:
            return "vhs"
        if quality in dvd_dict:
            return "dvd"
        if quality in web_dict:
            return "web"
        if quality in hd_dict:
            return "hd"
        if quality in na_dict:
            return "n/a"

if __name__ == "__main__":
    my_analyser = analyser('allWarezbbBlockResults.csv')
    field_name1 = "post_date"
    field_name2 = "author"
    my_analyser.count_field("author", split_by_comma=False, print_to_file=True)
    # my_analyser.count_field(field_name , split_by_comma=False)
