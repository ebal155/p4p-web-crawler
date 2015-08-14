from analyser import analyser

class warezbb_data_analyser():
    def __init__(self):
        self.filename = "processedWarezbbMovieFile.csv"
        self.myAnalyser = analyser(self.filename)
        self.years = ['2015', '2014', '2013', '2012', '2011', '2010', '2009']

    def print_all(self):
        self.print_total_post_dates()
        self.print_total_posts_by_year()
        self.print_total_author_count()
        self.print_author_view_averages()
        self.print_author_total_views()
        self.print_author_total_replies()
        self.print_author_replies_averages()
        self.print_author_posts_all_years()
        self.print_author_replies_all_years()

    def get_post_dates(self):
        """get all the posts dates"""
        myDict = self.myAnalyser.count_field('post_date', print_to_file=False,
            return_as_dict=True)
        newDict = {}
        for date  in myDict:
            newDate = date[:16]
            if newDate in newDict:
                newDict[newDate] += myDict[date]
            else:
                newDict[newDate] = myDict[date]
        return newDict

    def get_posts_dates_by_year(self):
        """"gets all the posts sorted by year"""
        return self.myAnalyser.count_field('year', print_to_file=False,
            return_as_dict=True)


    def get_author_counts(self):
        """get all the author counts"""
        return self.myAnalyser.count_field('author', print_to_file=False,
            return_as_dict=True)

    def get_author_total_views(self):
        """Get all the views an author has ever had"""
        author_views = self.myAnalyser.count_two_fields('author', 'views')
        author_total_views = {}
        for author in author_views:
            sum = 0
            for view in author_views[author]:
                sum += int(view.replace(',',''))
            author_total_views[author] = sum
        return author_total_views

    def caculate_author_view_averages(self):
        """Caculates the average amount of views each author has"""
        author_count = self.get_author_counts()
        author_views = self.get_author_total_views()
        author_average_views = {}
        for author in author_views:
            try:
                author_average_views[author] = author_views[author] / author_count[author]
            except:
                pass
        return author_average_views

    def get_author_total_replies(self):
        """get all the replies an author has ever had"""
        author_replies = self.myAnalyser.count_two_fields('author', 'replies')
        author_total_replies = {}
        for author in author_replies:
            sum = 0
            for view in author_replies[author]:
                sum += int(view.replace(',',''))
            author_total_replies[author] = sum
        return author_total_replies

    def caculate_author_replies_averages(self):
        """Caculates the average amount of replies each author has"""
        author_count = self.get_author_counts()
        author_replies = self.get_author_total_replies()
        author_average_replies = {}
        for author in author_replies:
            try:
                author_average_replies[author] = author_replies[author] / author_count[author]
            except:
                pass
        return author_average_replies

    def get_author_posts_in_year(self, year):
        author_count = self.myAnalyser.count_two_fields_matching_value('author',
            'year', year)
        return author_count

    def get_author_total_replies_in_year(self, year):
        author_replies = self.myAnalyser.count_two_fields_matching_third_field('author', 'replies', 'year', year) 
        author_total_replies = {}
        for author in author_replies:
            sum = 0
            for view in author_replies[author]:
                sum += int(view.replace(',',''))
            author_total_replies[author] = sum
        return author_total_replies

    def print_total_post_dates(self):
        self.myAnalyser.print_dict_to_csv(self.get_post_dates(),
            'alltime_posts.csv')

    def print_total_posts_by_year(self):
        self.myAnalyser.print_dict_to_csv(self.get_posts_dates_by_year(),
            'alltime_posts_by_year.csv')

    def print_total_author_count(self):
        self.myAnalyser.print_dict_to_csv(self.get_author_counts(),
            'alltime_author_count.csv')

    def print_author_view_averages(self):
        self.myAnalyser.print_dict_to_csv(self.caculate_author_view_averages(), 
            'alltime_author_view_averages.csv')

    def print_author_total_views(self):
        self.myAnalyser.print_dict_to_csv(self.get_author_total_views(),
            'alltime_author_views_total.csv')

    def print_author_total_replies(self):
        self.myAnalyser.print_dict_to_csv(self.get_author_total_replies(),
            'alltime_author_replies_total.csv')

    def print_author_replies_averages(self):
        self.myAnalyser.print_dict_to_csv(self.caculate_author_replies_averages(),
            "alltime_author_replies_averages.csv")

    def print_author_posts_all_years(self):
        for year in self.years:
            self.print_author_posts_in_year(year)

    def print_author_replies_all_years(self):
        for year in self.years:
            self.print_author_total_replies_in_year(year)

    def print_author_posts_in_year(self, year):
        self.myAnalyser.print_dict_to_csv(self.get_author_posts_in_year(year),
            year + '_author_count.csv')

    def print_author_total_replies_in_year(self, year):
        self.myAnalyser.print_dict_to_csv(self.get_author_total_replies_in_year(year),
            year + "_author_replies_total.csv")




if "__main__" == __name__:
    jay = warezbb_data_analyser()
    jay.print_total_post_dates()