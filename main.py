from utilities.util import Util
from utilities.ranking import Ranking

if __name__ == '__main__':
    nodes = Util.read_movie_data()
    # Util.process_genre_edge_data(nodes)
    # Util.process_cast_edge_data(nodes)
    # Util.process_director_edge_data(nodes)
    # Util.process_lang_edge_data(nodes)
    graph = Util.generate_graph(nodes)
    user = Util.get_user_profile()
    weights = Ranking.process_ranking(graph, user, 0)
    res = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True))
    rank = 1
    for r in res:
        print(str(rank) + " " + str(nodes[r].name) + " " + str(res[r]))
        rank += 1