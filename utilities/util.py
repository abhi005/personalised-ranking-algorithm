import pandas as pd
import requests

from models.node import Node
from models.properties import Properties
from models.edge import Edge
from models.graph import Graph

LINK_FILE = './links.csv'
URL = 'http://www.omdbapi.com/'
API_KEY = '68bbd801'
DATASET = './processed_data.csv'
EDGE_DATA = './edge_data.csv'


class Util:

    @staticmethod
    def get_movie_data():
        movies = pd.read_csv(LINK_FILE, dtype=str)
        df = pd.DataFrame(columns=['id', 'title', 'year', 'rated', 'duration', 'genre', 'cast', 'director', 'language',
                                   'imdb_rating', 'votes'])
        movies = movies[:900]
        for i in range(len(movies)):
            movie_id = 'tt' + movies.loc[i]['imdbId']
            print(movie_id)
            params = {'i': movie_id, 'plot': 'full', 'apikey': API_KEY}
            r = requests.get(url=URL, params=params)
            data = r.json()
            temp = [data['imdbID'], data['Title'], data['Year'], data['Rated'], data['Runtime'], data['Genre'],
                    data['Actors'], data['Director'], data['Language'], data['imdbRating'], data['imdbVotes']]
            df.loc[len(df.index)] = temp

        df.to_csv(DATASET)

    @staticmethod
    def read_movie_data():
        df = pd.read_csv(DATASET)
        nodes = {}
        for i in range(50):
            n = df.loc[i]
            p = Properties([x.strip() for x in n['genre'].split(',')], n['imdb_rating'],
                           [x.strip() for x in n['cast'].split(',')],
                           [x.strip() for x in n['director'].split(',')], n['year'], n['duration'], n['rated'],
                           n['votes'],
                           [x.strip() for x in n['language'].split(',')])
            node = Node(n['id'], n['title'], p)
            nodes[node.id] = node
        return nodes

    @staticmethod
    def process_genre_edge_data(data):
        columns = ['node1', 'node2', 'label', 'weight']
        genre_to_movie = {}
        print('pre processing starting')
        for key in data:
            node = data[key]
            curr_genres = node.props.genres
            for genre in curr_genres:
                if genre in genre_to_movie:
                    genre_to_movie[genre].append(key)
                else:
                    genre_to_movie[genre] = [key]

        print('pre processing completed')

        print('node processing starting')
        for key in data:
            print('processing node : ', key)
            node = data[key]
            curr_genres = node.props.genres
            count = {}
            for genre in curr_genres:
                neighbors = genre_to_movie[genre]
                for n in neighbors:
                    if n != key:
                        if n in count:
                            count[n] += 1
                        else:
                            count[n] = 1

            for neighbor in count:
                weight = count[neighbor] / (len(curr_genres) + len(data[neighbor].props.genres) - count[neighbor])
                new_data = [[key, neighbor, 'genre', weight],
                            [neighbor, key, 'genre', weight]]
                new_df = pd.DataFrame(new_data, columns=columns)
                # df.loc[len(df.index)] = [key, neighbor, 'genre', weight]
                # df.loc[len(df.index)] = [neighbor, key, 'genre', weight]
                new_df.to_csv(EDGE_DATA, mode='a', header=False, index=False)

        print('node processing completed')
        print('storing to csv file')

    @staticmethod
    def process_cast_edge_data(data):
        columns = ['node1', 'node2', 'label', 'weight']
        cast_to_movie = {}
        print('pre processing starting')
        for key in data:
            node = data[key]
            curr_cast = node.props.cast
            for cast in curr_cast:
                if cast in cast_to_movie:
                    cast_to_movie[cast].append(key)
                else:
                    cast_to_movie[cast] = [key]

        print('pre processing completed')

        print('node processing starting')
        for key in data:
            print('processing node : ', key)
            node = data[key]
            curr_cast = node.props.cast
            print('cast : ', curr_cast)
            count = {}
            for cast in curr_cast:
                neighbors = cast_to_movie[cast]
                for n in neighbors:
                    if n != key:
                        if n in count:
                            count[n] += 1
                        else:
                            count[n] = 1

            for neighbor in count:
                weight = count[neighbor] / (len(curr_cast) + len(data[neighbor].props.cast) - count[neighbor])
                new_data = [[key, neighbor, 'cast', weight],
                            [neighbor, key, 'cast', weight]]
                new_df = pd.DataFrame(new_data, columns=columns)
                new_df.to_csv(EDGE_DATA, mode='a', header=False, index=False)

        print('node processing completed')
        print('storing to csv file')

    @staticmethod
    def process_director_edge_data(data):
        columns = ['node1', 'node2', 'label', 'weight']
        dir_to_movie = {}
        print('pre processing starting')
        for key in data:
            node = data[key]
            curr_dir = node.props.director
            for dir in curr_dir:
                if dir in dir_to_movie:
                    dir_to_movie[dir].append(key)
                else:
                    dir_to_movie[dir] = [key]

        print('pre processing completed')

        print('node processing starting')
        for key in data:
            print('processing node : ', key)
            node = data[key]
            curr_dir = node.props.director
            print('director : ', curr_dir)
            count = {}
            for dir in curr_dir:
                neighbors = dir_to_movie[dir]
                for n in neighbors:
                    if n != key:
                        if n in count:
                            count[n] += 1
                        else:
                            count[n] = 1

            for neighbor in count:
                weight = count[neighbor] / (len(curr_dir) + len(data[neighbor].props.director) - count[neighbor])
                new_data = [[key, neighbor, 'director', weight],
                            [neighbor, key, 'director', weight]]
                new_df = pd.DataFrame(new_data, columns=columns)
                new_df.to_csv(EDGE_DATA, mode='a', header=False, index=False)

        print('node processing completed')
        print('storing to csv file')

    @staticmethod
    def process_lang_edge_data(data):
        columns = ['node1', 'node2', 'label', 'weight']
        lang_to_movie = {}
        print('pre processing starting')
        for key in data:
            node = data[key]
            curr_lang = node.props.languages
            for lang in curr_lang:
                if lang in lang_to_movie:
                    lang_to_movie[lang].append(key)
                else:
                    lang_to_movie[lang] = [key]

        print('pre processing completed')

        print('node processing starting')
        for key in data:
            print('processing node : ', key)
            node = data[key]
            curr_lang = node.props.languages
            print('languages : ', curr_lang)
            count = {}
            for lang in curr_lang:
                neighbors = lang_to_movie[lang]
                for n in neighbors:
                    if n != key:
                        if n in count:
                            count[n] += 1
                        else:
                            count[n] = 1

            for neighbor in count:
                weight = count[neighbor] / (len(curr_lang) + len(data[neighbor].props.languages) - count[neighbor])
                new_data = [[key, neighbor, 'language', weight],
                            [neighbor, key, 'language', weight]]
                new_df = pd.DataFrame(new_data, columns=columns)
                new_df.to_csv(EDGE_DATA, mode='a', header=False, index=False)

        print('node processing completed')
        print('storing to csv file')

    @staticmethod
    def generate_graph(nodes):
        df = pd.read_csv(EDGE_DATA)
        graph = Graph(nodes)
        for i in range(10):
            e = df.loc[i]
            src = nodes[e.node1]
            edge = Edge(e.label, e.weight, e.node2)
            src.edges.append(edge)

        return graph

    @staticmethod
    def get_user_profile():
        user = {'genres': {'8': 0.8, '7': 0.6, '15': 1.0, '6': 0.9, '10': 1.0},
                'cast': {'26': 1.0, '74': 0.5, '15': 0.6, '18': 0.7, '55': 0.5, '99': 1.0, '100': 1.0, '75': 1.0,
                         '76': 1.0},
                'director': {'77': 0.5},
                'languages': {'0': 1.0, '1': 0.7}}
        return user
