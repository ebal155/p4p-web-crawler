from analyser import analyser

class kickass_data_analyser():
    def __init__(self):
        self.filename = "kickass_movies_no_na.csv"
        self.kickass_analyser = analyser(self.filename)

    def get_number_of_authors(self, newfilename):
        date_dictionary = self.kickass_analyser.count_two_fields('post_date', 'author')
        for date in date_dictionary:
            date_dictionary[date] = len(set(date_dictionary[date]))

        self.kickass_analyser.print_dict_to_csv(date_dictionary, newfilename)

    def get_number_of_posts(self, newfilename):
        date_dictionary = self.kickass_analyser.count_field('post_date')

        self.kickass_analyser.print_dict_to_csv(date_dictionary, newfilename)

    def total_number_of_downloads_per_author(self, newfilename):
        author_view_dictionary = self.kickass_analyser.count_two_fields('author', 'downloads')
        for author in author_view_dictionary:
            sum = 0
            for item in author_view_dictionary[author]:
                if item == 'once.':
                    sum += 1
                else:
                    sum += int(item.replace(",", ''))
                author_view_dictionary[author] = sum

        self.kickass_analyser.print_dict_to_csv(author_view_dictionary, newfilename)
        # print str(author) + " " + str(author_view_dictionary[author])

        return author_view_dictionary

if "__main__" == __name__:
    jay = kickass_data_analyser()
    print "fight me 1v1 earl"
