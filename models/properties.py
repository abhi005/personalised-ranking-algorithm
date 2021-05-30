
class Properties:
    def __init__(self, genres, rating, cast, director, year, duration, rated, votes, languages):
        self.genres = genres
        self.rating = rating
        self.cast = cast
        self.director = director
        self.year = year
        self.duration = duration
        self.rated = rated
        self.votes = votes
        self.languages = languages

    def __str__(self) -> str:
        super().__str__()
        return str(self.genres) + ' ' + str(self.rating) + ' ' + str(self.cast) + ' ' + str(self.director)

