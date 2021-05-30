import math

props = ['genres', 'rating', 'cast', 'director', 'languages']


class Ranking:

    @staticmethod
    def process_ranking(graph, user, method):
        nodes = graph.nodes
        theta = math.ceil(math.log(len(graph.nodes)))
        weights = {}
        if method == 1:
            weights = Ranking.process_initial_weights_personalised(nodes, user)
        elif method == 0:
            weights = Ranking.process_initial_weights_non_personalised(nodes)
        l = 1
        while l < theta:
            for u in nodes:
                edges = nodes[u].edges
                nu = Ranking.get_number_of_unique_neighbors(edges)
                for v in edges:
                    w = weights[u]
                    nv = Ranking.get_number_of_unique_neighbors(nodes[v.dst].edges)
                    for s in props:
                        w[s] += ((weights[v.dst][s] * v.weight) ** (1 / (l * 2))) / (nu + nv)
            l += 1
        return Ranking.normalize_weights(weights)

    @staticmethod
    def normalize_weights(weights):
        new_weights = {}
        for n in weights:
            temp = 0
            for w in weights[n]:
                temp += weights[n][w]
            new_weights[n] = temp
        return new_weights

    @staticmethod
    def get_number_of_unique_neighbors(data):
        unique = set()
        for item in data:
            unique.add(item.dst)

        return len(unique)

    @staticmethod
    def process_initial_weights_personalised(nodes, user):
        weights = {}
        for n in nodes:
            prop = nodes[n].props
            w = {}
            count = 0.0
            for g in prop.genres:
                if g in user['genres']:
                    count += user['genres'][g]

            w['genres'] = count
            count = 0.0
            for c in prop.cast:
                if c in user['cast']:
                    count += user['cast'][c]

            w['cast'] = count
            count = 0.0
            for d in prop.director:
                if d in user['director']:
                    count += user['director'][d]

            w['director'] = count
            count = 0.0
            for l in prop.languages:
                if l in user['languages']:
                    count += user['languages'][l]

            w['languages'] = count
            w['rating'] = prop.rating / 10
            weights[n] = w

        return weights

    @staticmethod
    def process_initial_weights_non_personalised(nodes):
        weights = {}
        for n in nodes:
            prop = nodes[n].props
            w = {}
            count = 0.0
            for g in prop.genres:
                count += 1

            w['genres'] = count
            count = 0.0
            for c in prop.cast:
                count += 1

            w['cast'] = count
            count = 0.0
            for d in prop.director:
                count += 1

            w['director'] = count
            count = 0.0
            for l in prop.languages:
                count += 1

            w['languages'] = count
            w['rating'] = prop.rating / 10
            weights[n] = w

        return weights
