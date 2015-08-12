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
                sum += int(view.replace(',',''))
            author_total_views[author] = sum
        return author_total_views
    

if "__main__" == __name__:
    jay = warezbb_data_analyser()
    jay.caculate_author_view_averages()
