from analyser import analyser

class kickass_data_analyser():
    def __init__(self):
        self.filename = "TESTMOVIENAMESKICKASS.csv"
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

    def total_number_of_posts_per_author(self, newfilename):
        author_post_dictionary = self.kickass_analyser.count_field('author', return_as_dict=True)

        self.kickass_analyser.print_dict_to_csv(author_post_dictionary, newfilename)

    def get_reputation_per_author(self, newfilename):
        author_reputation_dictionary = self.kickass_analyser.count_field_unique('author', 'author_reputation')

        for reputation in author_reputation_dictionary:
            if author_reputation_dictionary[reputation] == "N/A":
                author_reputation_dictionary[reputation] = "0"

        self.kickass_analyser.print_dict_to_csv(author_reputation_dictionary, newfilename)

    def count_qualities(self, newfilename):
        movietitle_quality_dictionary = self.kickass_analyser.count_two_fields('title','detected_quality')

        for field in movietitle_quality_dictionary:
            print field + ": " + str(movietitle_quality_dictionary[field])


if "__main__" == __name__:
    kickass_analyser = kickass_data_analyser()
    # kickass_analyser.get_number_of_authors("number_authors_per_year.csv")
    # kickass_analyser.get_number_of_posts("number_posts_per_day.csv")
    # kickass_analyser.total_number_of_downloads_per_author("test111.csv")
    # kickass_analyser.total_number_of_posts_per_author("number_posts_per_author.csv")
    # kickass_analyser.count_qualities("./qualities/movie")
    # kickass_analyser.get_reputation_per_author("reputation_per_author.csv");
    kickass_analyser.count_qualities("balblabla")
