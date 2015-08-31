from analyser import analyser
import operator


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

    def get_col(self, col_name):
        return self.myAnalyser.get_col(col_name)

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
                sum += int(view.replace(',', ''))
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

    def caculate_author_rank_by_no_of_views(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict = self.get_author_total_views()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        myArray = []
        for author in sorted_dict:
            myArray.append(author[1])
        return myArray

    def caculate_author_rank_by_no_of_replies(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict= self.get_author_total_replies()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        myArray = []
        for author in sorted_dict:
            myArray.append(author[1])
        return myArray

    def caculate_author_rank_by_no_of_threads(self):
        """caculates the rank of the authors
        rank 1 = author with most threads
        rank n = author with least threads"""
        count_dict= self.get_author_counts()
        sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
        myArray = []
        for author in sorted_dict:
            myArray.append(author[1])
        return myArray

    def caculate_movies_by_quality(self):
        movie_quality = self.myAnalyser.count_two_fields("movie title", "detected_quality")
        hd_movie = {}
        cam_movie = {}
        vhs_movie = {}
        web_movie = {}
        dvd_movie = {}
        for movie in movie_quality:
            for quality in movie_quality[movie]:
                for qua in quality.split(","):
                    t = get_quality_type(qua)
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
        self.myAnalyser.print_dict_to_csv(hd_movie, "hd_movies.csv")
        self.myAnalyser.print_dict_to_csv(cam_movie, "cam_movies.csv")
        self.myAnalyser.print_dict_to_csv(vhs_movie, "vhs_movies.csv")
        self.myAnalyser.print_dict_to_csv(web_movie, "web_movies.csv")
        self.myAnalyser.print_dict_to_csv(dvd_movie, "dvd_movies.csv")






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

    def get_qualities(self):
        qualities = self.get_col("detected_quality")
        formated_list = []
        for quality in qualities:
            for q in quality.split(","):
                formated_list.append(q)
        quality_dict = {}
        for quality in formated_list:
            quality_type = get_quality_type(quality)
            if quality_type in quality_dict:
                quality_dict[quality_type] += 1
            else:
                quality_dict[quality_type] = 1
        return quality_dict


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

    def print_qualities(self):
        self.myAnalyser.print_dict_to_csv(self.get_qualities(),
            'total_quality_types.csv')

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

    def print_author_rank_by_no_of_views(self):
        ranks = self.caculate_author_rank_by_no_of_views()
        self.myAnalyser.print_logged_array_to_csv(ranks, "loggedauthorRankbyviews.csv")

    def print_author_rank_by_no_of_replies(self):
        ranks = self.caculate_author_rank_by_no_of_replies()
        self.myAnalyser.print_logged_array_to_csv(ranks, "loggedauthorRankbyreplies.csv")

    def print_author_rank_by_no_of_threads(self):
        ranks = self.caculate_author_rank_by_no_of_threads()
        self.myAnalyser.print_logged_array_to_csv(ranks, "loggedauthorRankbythreads.csv")

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

class kickass_data_analyser():
    def __init__(self):
        self.filename = "COMPLETELEYNEWKICKASS.csv"
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

        
def  get_quality_type(quality):
    """qualities is a list of all the qualities that appear"""

    #CAM telesync, cam, hdts, iphone
    # VHS vcd, vhs, vhsrip, 
    #DVD dvd, dvdrip,telecine, workprint, screener, tc, ppv, 480p, tvrip, "dvdsrc"
    #HD 1080p, blu-ray, hdrip, 720p, bdrip, brrip, hdtv, 'x264'
    #Web web-dl, bdrip, webrip, vodrip, web dl, mp4, "MPEG-4"
    #unkown N/A, Unknown

    cam_dict = {"telesync": 0, "cam": 0, "hdts": 0, "iphone": 0}
    vhs_dict = {"vcd": 0, "vhs": 0, "vhsrip": 0}
    dvd_dict = {"dvd": 0, "dvdrip": 0, "telecine": 0, "workprint": 0,
    "screener": 0, "dvdsrc": 0, "tc": 0, "ppv": 0, "480p": 0}
    web_dict = {"web-dl": 0, "bdrip": 0, "webrip": 0, "vodrip": 0, "web dl": 0, "mp4": 0, "MPEG-4": 0}
    hd_dict = {"1080p": 0,"blu-ray": 0,"hdrip": 0,"720p": 0,"bdrip": 0, "brrip": 0, "hdtv": 0, 'x264': 0,"bluray":0}

    if quality in cam_dict:
        return "cam"
    if quality in vhs_dict:
        return "vhs"
    if quality in dvd_dict:
        return "dvd"
    if quality in web_dict:
        return "web"
    if quality in hd_dict:
        return "hd"
    if quality.strip() is "":
        return "not given"
    return "n/a"


if "__main__" == __name__:
        jay = warezbb_data_analyser()
        jay.caculate_movies_by_quality()

