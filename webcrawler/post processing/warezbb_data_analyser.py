from analyser import analyser


class warezbb_data_analyser():
    def __init__(self):
        self.filename = "processedWarezbbMovieFile.csv"
        self.myAnalyser = analyser(self.filename)

    def caculate_author_view_averages(self):
        author_count = self.get_author_counts()
        author_views = self.get_author_total_views()
        author_average_views = {}
        for author in author_views:
            author_average_views[author] = author_views[author] / author_count[author]
        return author_average_views

    def get_author_counts(self):
        return self.myAnalyser.count_field('author', print_to_file=False)

    def get_author_total_views(self):
        author_views = self.myAnalyser.count_two_fields('author', 'views')
        author_total_views = {}
        for author in author_views:
            sum = 0
            for view in author_views[author]:
                sum += int(view.replace(',', ''))
            author_total_views[author] = sum
        return author_total_views


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

    #author reputation to downloads ratio
    #file size to downloads ratio
    #file quality to downloads

if "__main__" == __name__:
    # jay = warezbb_data_analyser()
    # jay.caculate_author_view_averages()

    kickass_analyser = kickass_data_analyser()
    # kickass_analyser.get_number_of_authors("number_authors_per_year.csv")
    # kickass_analyser.get_number_of_posts("number_posts_per_day.csv")
    # kickass_analyser.total_number_of_downloads_per_author("test111.csv")
