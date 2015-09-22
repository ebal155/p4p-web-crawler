import csv
import operator
class my_printer():
    def print_dict_to_csv(self, myDict, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for key in myDict:
            writer.writerow([key, myDict[key]])

    def print_array_to_csv(self, myArray, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for x in range(0,len(myArray)):
            writer.writerow([x] + myArray[x])

    def print_array_to_csv_with_header(self, myArray, header, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        writer.writerow(header)
        for x in range(0,len(myArray)):
            writer.writerow(myArray[x])

    def print_logged_array_to_csv(self, myArray, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for x in range(0,len(myArray)):
            writer.writerow([math.log(x+1),math.log(myArray[x])])

    def print_dict_sorted_to_csv(self, myDict, filename):
        myArray = sorted(myDict.items(), key=operator.itemgetter(1),reverse=True)
        f = open(filename, "wb")
        writer = csv.writer(f)
        for x in range(0,len(myArray)):
            writer.writerow([myArray[x][0], myArray[x][1]])
