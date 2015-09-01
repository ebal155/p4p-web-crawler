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

    def count_unique_movies(self,newfilename):
        year_movie_dictionary = self.kickass_analyser.count_two_fields('post_date', 'title')

        movie_count_per_year_dictionary = {}

        for year in year_movie_dictionary: 
            movie_count_per_year_dictionary[year] = len(set(year_movie_dictionary[year]))

        self.kickass_analyser.print_dict_to_csv(movie_count_per_year_dictionary,newfilename)

    def count_unique_content(self,newfilename):
        year_movie_dictionary = self.kickass_analyser.count_two_fields('post_date', 'title')

        for year in year_movie_dictionary:
            movie_quality_dictionary = self.kickass_analyser.count_two_fields_matching_third_field('title', 'detected_quality', 'post_date', year)
            for movie in movie_quality_dictionary:
                movie_quality_dictionary[movie] = set(movie_quality_dictionary[movie])

            year_movie_dictionary[year] = movie_quality_dictionary

        content_count_per_year_dictionary = {}

        for year in year_movie_dictionary:
            number_of_unique_content = 0
            movie_quality_dict = year_movie_dictionary[year]
            for movie in movie_quality_dict:
                quality_set = set()
                for quality in movie_quality_dict[movie]:
                    quality_set.add(self.kickass_analyser.get_quality_type(quality))  
                number_of_unique_content = number_of_unique_content + len(quality_set)

            content_count_per_year_dictionary[year] = number_of_unique_content
            print year + " " + str(number_of_unique_content)

        self.kickass_analyser.print_dict_to_csv(content_count_per_year_dictionary,newfilename)        

    def count_qualities(self, newfilename):
        movie_quality = self.kickass_analyser.count_two_fields("title", "detected_quality")
        hd_movie = {}
        cam_movie = {}
        vhs_movie = {}
        web_movie = {}
        dvd_movie = {}
        for movie in movie_quality:
            for quality in movie_quality[movie]:
                for qua in quality.split(","):
                    t = self.kickass_analyser.get_quality_type(qua)
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

            if movie not in hd_movie:
                hd_movie[movie] = 0

            if movie not in cam_movie:
                cam_movie[movie] = 0

            if movie not in vhs_movie:
                vhs_movie[movie] = 0

            if movie not in web_movie:
                web_movie[movie] = 0

            if movie not in dvd_movie:
                dvd_movie[movie] = 0

        self.kickass_analyser.print_dict_to_csv(hd_movie, "hd_movies.csv")
        self.kickass_analyser.print_dict_to_csv(cam_movie, "cam_movies.csv")
        self.kickass_analyser.print_dict_to_csv(vhs_movie, "vhs_movies.csv")
        self.kickass_analyser.print_dict_to_csv(web_movie, "web_movies.csv")
        self.kickass_analyser.print_dict_to_csv(dvd_movie, "dvd_movies.csv")

if "__main__" == __name__:
    kickass_analyser = kickass_data_analyser()
    # kickass_analyser.get_number_of_authors("number_authors_per_year.csv")
    # kickass_analyser.get_number_of_posts("number_posts_per_day.csv")
    # kickass_analyser.total_number_of_downloads_per_author("test111.csv")
    # kickass_analyser.total_number_of_posts_per_author("number_posts_per_author.csv")
    # kickass_analyser.count_qualities("./qualities/movie")
    # kickass_analyser.get_reputation_per_author("reputation_per_author.csv");
    kickass_analyser.count_qualities("balblabla")
    # kickass_analyser.count_unique_content("unique_content_per_year.csv")
