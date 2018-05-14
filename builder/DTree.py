from Construct import StartConstruct


class DecisionTree:
    def __init__(self):
        self.root = None
        self.nodes = []
        self.links = []

    def add_construct(self, construct):
        self.nodes.append(construct)

    def add_link(self, link):
        self.links.append(link)
