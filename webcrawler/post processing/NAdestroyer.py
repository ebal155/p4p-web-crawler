import csv

class destroyer_of_na():
	def __init__(self,filename):
		self.filename = filename


	def delete_na(self, newfile):
		with open(self.filename, 'rb') as f:
			reader = csv.reader(f)
			

			new = open(newfile, "wb")
   			writer = csv.writer(new)

   			writer.writerow(reader.next())

			for row in reader:
				if not (row[14] == "N/A"):
					writer.writerow(row)

if "__main__" == __name__:
	destroyer = destroyer_of_na("kickass_movies_new.csv")
	destroyer.delete_na("kickass_movies_no_na.csv")