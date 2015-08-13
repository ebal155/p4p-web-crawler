from analyser import analyser

class warezbb_data_analyser():
    def __init__(self):
        self.filename = "processedWarezbbMovieFile.csv"
        self.myAnalyser = analyser(self.filename)

    def print_all(self):
        self.print_total_author_count()
        self.print_author_view_averages()
        self.print_author_total_views()
        self.print_author_total_replies()
        self.print_author_replies_averages()

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

if "__main__" == __name__:
    jay = warezbb_data_analyser()
    jay.print_all()