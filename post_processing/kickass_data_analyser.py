from analyser import analyser
from my_printer import my_printer

#This script is used to analyse the processed kickass metadata
#Results of the queries in this class should be printed out to a .csv in the same directory
class kickass_data_analyser():
    def __init__(self):
        self.filename = "kickass_movies_processed.csv"
        self.kickass_analyser = analyser(self.filename)
        self.printer = my_printer()

    def get_number_of_authors(self, newfilename):
        """Gets number of authors that posted for every day/year (depending on post_date format)."""
        date_dictionary = self.kickass_analyser.count_two_fields('post_date', 'author')
        for date in date_dictionary:
            date_dictionary[date] = len(set(date_dictionary[date]))

        self.printer.print_dict_to_csv(date_dictionary, newfilename)

    def get_number_of_posts(self, newfilename):
        """Gets number of posts made for every day/year (depending on post_date format)."""
        date_dictionary = self.kickass_analyser.count_field('post_date', return_as_dict=True)

        self.printer.print_dict_to_csv(date_dictionary, newfilename)

    def get_number_of_downloads(self, newfilename):
        """Gets the number of donwloads made for every day/year (depending on post_date format)."""
        downloads_dictionary = self.kickass_analyser.count_two_fields('post_date', 'downloads')

        for post_date in downloads_dictionary:
            sum = 0
            for item in downloads_dictionary[post_date]:
                sum += int(item)
            downloads_dictionary[post_date] = sum

        self.printer.print_dict_to_csv(downloads_dictionary, newfilename)

    def get_author_download_averages(self, newfilename):
        """Get average number of downloads per author"""
        author_count = self.kickass_analyser.count_field('author', return_as_dict=True)
        author_downloads = self.kickass_analyser.count_two_fields('author', 'downloads')

        author_average_downloads = {}

        for author in author_downloads:
            sum = 0
            for item in author_downloads[author]:
                sum += int(item)
            author_downloads[author] = sum

        for author in author_downloads:
            if author in author_count:
                author_average_downloads[author] = author_downloads[author] / author_count[author]

        self.printer.print_dict_to_csv(author_average_downloads, newfilename)

    def get_year_download_averages(self, newfilename):
        """Get the average download numbers per year"""
        year_count = self.kickass_analyser.count_field('post_date', return_as_dict=True)
        year_downloads = self.kickass_analyser.count_two_fields('post_date', 'downloads')

        for year in year_downloads:
            sum = 0
            for item in year_downloads[year]:
                sum += int(item)
            year_downloads[year] = sum

        year_average_downloads = {}

        for year in year_downloads:
            year_average_downloads[year] = year_downloads[year] / year_count[year]

        self.printer.print_dict_to_csv(year_average_downloads, newfilename)

    def total_number_of_downloads_per_author(self, newfilename):
        """Get the total number of downloads per author"""
        author_view_dictionary = self.kickass_analyser.count_two_fields('author', 'downloads')
        for author in author_view_dictionary:
            sum = 0
            for item in author_view_dictionary[author]:
                sum += int(item)
            author_view_dictionary[author] = sum

        self.printer.print_dict_to_csv(author_view_dictionary, newfilename)

        return author_view_dictionary

    def total_number_of_posts_per_author(self, newfilename):
        """Get the total number of posts per author"""
        author_post_dictionary = self.kickass_analyser.count_field('author', return_as_dict=True)

        self.printer.print_dict_to_csv(author_post_dictionary, newfilename)

    def get_reputation_per_author(self, newfilename):
        """Get the reputation value per author"""
        author_reputation_dictionary = self.kickass_analyser.count_field_unique('author', 'author_reputation')

        for reputation in author_reputation_dictionary:
            if author_reputation_dictionary[reputation] == "N/A":
                author_reputation_dictionary[reputation] = "0"

        self.printer.print_dict_to_csv(author_reputation_dictionary, newfilename)

    def count_unique_movies(self, newfilename):
        """Get the number of unique movies per day/year (depending on post_date format)"""
        year_movie_dictionary = self.kickass_analyser.count_two_fields('post_date', 'title')

        movie_count_per_year_dictionary = {}

        for year in year_movie_dictionary:
            movie_count_per_year_dictionary[year] = len(set(year_movie_dictionary[year]))

        self.printer.print_dict_to_csv(movie_count_per_year_dictionary, newfilename)

    def count_unique_content(self, newfilename):
        """Get the number of unique versions of movies per day/year (depending on post_date format)"""
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

        self.printer.print_dict_to_csv(content_count_per_year_dictionary, newfilename)

    def count_qualities(self, newfilename):
        """Count the number of quality types that each movie is uploaded in."""
        movie_quality = self.kickass_analyser.count_two_fields("title", "detected_quality")
        hd_movie = {}
        cam_movie = {}
        vhs_movie = {}
        web_movie = {}
        dvd_movie = {}

        for movie in movie_quality:
            for quality in movie_quality[movie]:
                for qua in quality.split(","):
                    t = self.kickass_analyser.get_quality_type(qua)  # Assign the quality into one of HD,DVD,Web,VHS,Cam
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

        # A separate csv file is created to show how many times each movie is uploaded for a particular quality
        self.printer.print_dict_to_csv(hd_movie, "hd_movies.csv")
        self.printer.print_dict_to_csv(cam_movie, "cam_movies.csv")
        self.printer.print_dict_to_csv(vhs_movie, "vhs_movies.csv")
        self.printer.print_dict_to_csv(web_movie, "web_movies.csv")
        self.printer.print_dict_to_csv(dvd_movie, "dvd_movies.csv")

if "__main__" == __name__:
    kickass_analyser = kickass_data_analyser()
