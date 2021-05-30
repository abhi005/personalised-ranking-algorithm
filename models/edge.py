
class Edge:
    def __init__(self, label, weight, dst):
        self.label = label
        self.weight = weight
        self.dst = dst

    def __str__(self) -> str:
        super().__str__()

        return str(self.label) + " " + str(self.weight) + " " + str(self.dst)

