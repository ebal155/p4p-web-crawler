from analyser import analyser

class warezbb_data_analyser():
    def __init__(self):
        self.filename = "processedWarezbbMovieFile.csv"
        self.myAnalyser = analyser(self.filename)

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

    def get_author_counts(self):
        """get all the author counts"""
        return self.myAnalyser.count_field('author', print_to_file=False, return_as_dict=True)

    def get_author_total_views(self):
        """Get all the views an author has ever seen"""
        author_views = self.myAnalyser.count_two_fields('author', 'views')
        author_total_views = {}
        for author in author_views:
            sum = 0
            for view in author_views[author]:
                sum += int(view.replace(',',''))
            author_total_views[author] = sum
        return author_total_views

    def print_total_author_count(self):
        self.myAnalyser.count_field('author', print_to_file=True)

    def print_author_view_averages(self):
        self.myAnalyser.print_to_file(self.caculate_author_view_averages, 'overall_author_view_averages.csv')

    def print_author_total_views(self):
        self.myAnalyser.print_to_file(self.get_author_total_views, 'overall_author_total_views.csv')

    

if "__main__" == __name__:
    jay = warezbb_data_analyser()
    return jay.caculate_author_view_averages()