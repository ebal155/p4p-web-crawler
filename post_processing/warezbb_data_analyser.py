"""This script is used to analysed the processed warezbb data"""

from analyser import Analyser
from my_printer import MyPrinter
from collections import Counter
import operator

class WarezbbDataAnalyser():
    """This class is used to analyse the process warezbb data"""
    def __init__(self):
        self.filename = "data/processedWarezbbMovieFile.csv"
        self.my_analyser = Analyser(self.filename)
        self.my_printer = MyPrinter()
        self.years = ['2015', '2014', '2013', '2012', '2011', '2010', '2009']

    def get_col(self, col_name):
        """returns a col for a given col name"""
        return self.my_analyser.get_col(col_name)

    def get_post_dates(self):
        """get all the posts dates"""
        my_dict = self.my_analyser.count_field('post_date', return_as_dict=True)
        new_dict = {}
        for date  in my_dict:
            new_date = date[:16]
            if new_date in new_dict:
                new_dict[new_date] += my_dict[date]
            else:
                new_dict[new_date] = my_dict[date]
        return new_dict

    def get_posts_dates_by_year(self):
        """"gets all the posts sorted by year"""
        return self.my_analyser.count_field('year', return_as_dict=True)

    def get_author_counts(self):
        """get all the author counts"""
        return self.my_analyser.count_field('author', return_as_dict=True)

    def get_author_total_views(self):
        """Get all the views an author has ever had"""
        author_views = self.my_analyser.count_two_fields('author', 'views')
        author_total_views = {}
        for author in author_views:
            my_sum = 0
            for view in author_views[author]:
                my_sum += int(view.replace(',', ''))
            author_total_views[author] = my_sum
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
                author_average_views[author] = 0
        return author_average_views

    def author_rank_by_no_of_views(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict = self.get_author_total_views()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        my_array = []
        for author in sorted_dict:
            my_array.append([author[1], author[0]])
        return my_array


    def author_rank_by_average_views(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict = self.caculate_author_view_averages()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        my_array = []
        for author in sorted_dict:
            my_array.append([author[1], author[0]])
        return my_array

    def caculate_author_rank(self):
        """ caculates author rank and information about the author """
        total_views = self.get_author_total_views()
        total_replies = self.get_author_total_replies()
        total_threads = self.get_author_counts()
        average_views = self.caculate_author_replies_averages()
        average_replies = self.caculate_author_view_averages()
        qualities = self.get_author_qualities_count()
        unique = self.get_movies_for_author()
        #rank 1 = author with most threads
        # quality_dict = {"cam":0,"vhs":0,"dvd":0,"web":0,"hd":0,"not given":0}

        sorted_dict = sorted(total_threads.items(), key=operator.itemgetter(1), reverse=True)
        my_array = []
        for x in range(0, len(sorted_dict)):
            # [author, rank, total_threads, total views
            # total_replies, average_replies, average_views ]
            author = sorted_dict[x][0]
            if author == "][,o0k~":
                print "fuck this nigga"
            else:
                my_array.append([
                    sorted_dict[x][0],
                    x,
                    sorted_dict[x][1],
                    total_views[author],
                    total_replies[author],
                    average_views[author],
                    average_replies[author],
                    qualities[author]["hd"],
                    qualities[author]["web"],
                    qualities[author]["dvd"],
                    qualities[author]["cam"],
                    qualities[author]["vhs"],
                    qualities[author]["n/a"],
                    unique[author]])
        return my_array



    def caculate_author_rank_by_no_of_replies(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict = self.get_author_total_replies()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        myArray = []
        for author in sorted_dict:
            myArray.append([author[1], author[0]])
        return myArray

    def caculate_author_rank_by_no_of_threads(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict = self.get_author_counts()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        myArray = []
        for author in sorted_dict:
            myArray.append([author[1], author[0]])
        return myArray

    def print_table(self):
        """Year, # of authors, # of posts, # of movies, # of verions"""
        # self.get_author_posts_in_year
        myDict = {}
        for year in self.years:
            myDict[year] = [year]
            author_posts = self.get_author_posts_in_year(year)
            myDict[year].append(len(author_posts))
            sum = 0
            for author in author_posts:
                sum += author_posts[author]
            myDict[year].append(sum)
            movies = self.get_total_movies_in_year(year)
            myDict[year].append(len(movies))
            movie_quality = self.get_movies_with_detected_quality_in_year(year)
            for movie in movie_quality:
                if len(movie_quality[movie]) > 1:
                    movie_quality[movie] = set(movie_quality[movie].split(","))
                    quality_list = []
                    for quality in movie_quality[movie]:
                        t = self.my_analyser.get_quality_type(quality)
                        if t not in quality_list:
                            quality_list.append(t)
                    movie_quality[movie] = len(quality_list)
            sum = 0
            for movie in movie_quality:
                if type(movie_quality[movie]) is int:
                    sum += movie_quality[movie]
                else:
                    sum += 1
            myDict[year].append(sum)
        self.my_analyser.make_table(myDict, "warezbbTable.csv")

    def get_movies_with_detected_quality_in_year(self, year):
        movie_quality = self.my_analyser.count_two_fields_matching_third_field(
            'movie title', 'detected_quality', 'year', year)
        my_dict = {}
        for movie in movie_quality:
            my_dict[movie] = movie_quality[movie][0]
            for i in range(1, len(movie_quality[movie])):
                my_dict[movie] = my_dict[movie] + "," + movie_quality[movie][i]
        return my_dict

    def get_author_total_replies(self):
        """get all the replies an author has ever had"""
        author_replies = self.my_analyser.count_two_fields('author', 'replies')
        author_total_replies = {}
        for author in author_replies:
            my_sum = 0
            for view in author_replies[author]:
                my_sum += int(view.replace(',', ''))
            author_total_replies[author] = my_sum
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
                author_average_replies[author] = 0
                pass
        return author_average_replies

    def get_author_qualities_count(self):
        quality_dict = {"cam":0, "vhs":0, "dvd":0, "web":0, "hd":0, "n/a":0}
        myArray = self.my_analyser.count_two_fields('author',
                                                    'detected_quality',
                                                    split_by_comma=False)
        authorDict = {}
        for author in myArray:
            array_of_qua = myArray[author]
            for qua in array_of_qua:
                qualities = qua.split(",")
                for q in qualities:
                    q_dict = {}
                    if author in authorDict:
                        q_dict = authorDict[author]
                    else:
                        q_dict = {"cam":0, "vhs":0, "dvd":0,
                                  "web":0, "hd":0, "n/a":0}
                    t = self.my_analyser.get_quality_type(q)
                    q_dict[t] += 1
                    authorDict[author] = q_dict
        return authorDict

    def get_author_posts_in_year(self, year):
        author_count = self.my_analyser.count_two_fields_matching_value('author',
                                                                        'year', year)
        return author_count

    def get_author_total_replies_in_year(self, year):
        author_replies = self.my_analyser.count_two_fields_matching_third_field('author', 'replies', 'year', year)
        author_total_replies = {}
        for author in author_replies:
            my_sum = 0
            for view in author_replies[author]:
                my_sum += int(view.replace(',', ''))
            author_total_replies[author] = my_sum
        return author_total_replies


    def get_qualities(self):
        """ gets the number of qualties in warezbb """
        qualities = self.get_col("detected_quality")
        formated_list = []
        for quality in qualities:
            for q in quality.split(","):
                formated_list.append(q)
        quality_dict = {}
        for quality in formated_list:
            quality_type = self.my_analyser.get_quality_type(quality)
            if quality_type in quality_dict:
                quality_dict[quality_type] += 1
            else:
                quality_dict[quality_type] = 1
        return quality_dict

    def caculate_movies_by_quality(self):
        """ gets movies with qualities information """
        movie_quality = self.my_analyser.count_two_fields("movie title", "detected_quality")
        hd_movie = {}
        cam_movie = {}
        vhs_movie = {}
        web_movie = {}
        dvd_movie = {}
        for movie in movie_quality:
            for quality in movie_quality[movie]:
                for qua in quality.split(","):
                    t = self.my_analyser.get_quality_type(qua)
                    if t == "hd":
                        if movie in hd_movie:
                            hd_movie[movie] += 1
                        else:
                            hd_movie[movie] = 1
                    if t == "cam":
                        if movie in cam_movie:
                            cam_movie[movie] += 1
                        else:
                            cam_movie[movie] = 1
                    if t == "vhs":
                        if movie in vhs_movie:
                            vhs_movie[movie] += 1
                        else:
                            vhs_movie[movie] = 1
                    if t == "web":
                        if movie in web_movie:
                            web_movie[movie] += 1
                        else:
                            web_movie[movie] = 1
                    if t == "dvd":
                        if movie in dvd_movie:
                            dvd_movie[movie] += 1
                        else:
                            dvd_movie[movie] = 1
        self.my_printer.print_dict_to_csv(hd_movie, "hd_movies.csv")
        self.my_printer.print_dict_to_csv(cam_movie, "cam_movies.csv")
        self.my_printer.print_dict_to_csv(vhs_movie, "vhs_movies.csv")
        self.my_printer.print_dict_to_csv(web_movie, "web_movies.csv")
        self.my_printer.print_dict_to_csv(dvd_movie, "dvd_movies.csv")


    def get_movies_for_author(self):
        """ get top five authors """
        authors = self.get_author_counts()
        cols = self.my_analyser.count_two_fields('author', 'movie title',
                                                 split_by_comma=False)
        new_cols = {}
        for author in authors:
            col = cols[author]
            movie_dict = Counter(col)
            new_cols[author] = len(set(movie_dict))


        return new_cols

    def print_qualities(self):
        self.my_printer.print_dict_to_csv(self.get_qualities(), 'total_quality_types.csv')

    def print_total_post_dates(self):
        self.my_printer.print_dict_to_csv(self.get_post_dates(),
            'alltime_posts.csv')

    def print_total_posts_by_year(self):
        self.my_printer.print_dict_to_csv(self.get_posts_dates_by_year(),
            'alltime_posts_by_year.csv')

    def print_total_author_count(self):
        self.my_printer.print_dict_to_csv(self.get_author_counts(),
            'alltime_author_count.csv')

    def print_author_view_averages(self):
        self.my_printer.print_dict_to_csv(self.caculate_author_view_averages(),
            'alltime_author_view_averages.csv')

    def print_logged_author_rank_by_no_of_views(self):
        ranks = self.author_rank_by_no_of_views()
        self.my_printer.print_logged_array_to_csv(ranks, "loggedauthorRankbyviews.csv")

    def print_logged_author_rank_by_no_of_replies(self):
        ranks = self.caculate_author_rank_by_no_of_replies()
        self.my_printer.print_logged_array_to_csv(ranks, "loggedauthorRankbyreplies.csv")

    def print_logged_author_rank_by_no_of_threads(self):
        ranks = self.caculate_author_rank_by_no_of_threads()
        self.my_printer.print_logged_array_to_csv(ranks, "loggedauthorRankbythreads.csv")

    def print_author_rank_by_no_of_views(self):
        ranks = self.author_rank_by_no_of_views()
        self.my_printer.print_array_to_csv(ranks, "authorRankbyviews.csv")

    def print_author_rank_by_no_of_average_views(self):
        ranks = self.author_rank_by_average_views()
        self.my_printer.print_array_to_csv(ranks, "authorRankbyviews.csv")

    def print_author_rank_by_no_of_replies(self):
        ranks = self.caculate_author_rank_by_no_of_replies()
        self.my_printer.print_array_to_csv(ranks, "authorRankbyreplies.csv")

    def print_author_rank_by_no_of_threads(self):
        ranks = self.caculate_author_rank_by_no_of_threads()
        self.my_printer.print_array_to_csv(ranks, "authorRankbythreads.csv")

    def print_author_total_views(self):
        self.my_printer.print_dict_to_csv(self.get_author_total_views(),
            'alltime_author_views_total.csv')

    def print_author_total_replies(self):
        self.my_printer.print_dict_to_csv(self.get_author_total_replies(),
            'alltime_author_replies_total.csv')

    def print_author_replies_averages(self):
        self.my_printer.print_dict_to_csv(self.caculate_author_replies_averages(),
            "alltime_author_replies_averages.csv")

    def print_author_posts_all_years(self):
        for year in self.years:
            self.print_author_posts_in_year(year)

    def print_author_replies_all_years(self):
        for year in self.years:
            self.print_author_total_replies_in_year(year)

    def print_author_posts_in_year(self, year):
        self.my_printer.print_dict_to_csv(self.get_author_posts_in_year(year),
            year + '_author_count.csv')

    def print_author_total_replies_in_year(self, year):
        self.my_printer.print_dict_to_csv(self.get_author_total_replies_in_year(year),
            year + "_author_replies_total.csv")

    def print_author_rank(self):
        header = ['author', 'rank', 'total_threads',
            'total_views', 'total_replies', 'average_replies',
            'average_views', "hd", "web", "dvd", "cam", "vhs", "not given",
            "unique content"]
        myArray = self.caculate_author_rank()
        self.my_printer.print_array_to_csv_with_header(myArray,
            header, "author_rank.csv")

if "__main__" == __name__:
    WAREZ = WarezbbDataAnalyser()
    WAREZ.print_author_rank()
