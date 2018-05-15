
class DecisionTree:
    def __init__(self):
        self.root = None
        self.nodes = []
        self.links = []

    def add_construct(self, construct):
        self.nodes.append(construct)

    def add_link(self, link):
        self.links.append(link)

    def find_node(self, id):
        for node in self.nodes:
            if node.i == id:
                return node
        return None
