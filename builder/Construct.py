class Construct:
    def __init__(self, node_type):
        self.x = 0
        self.y = 0
        self.expanded = True
        self.type = node_type
        self.parent = None
        self.l_child = None
        self.r_child = None


class StartConstruct(Construct):
    def __init__(self):
        Construct.__init__(self, "start")
        self.dependency = None
        self.pattern = None


class EndConstruct(Construct):
    def __init__(self):
        Construct.__init__(self, "end")


class DecisionConstruct(Construct):
    def __init__(self):
        Construct.__init__(self, "decision")
        self.expression = ExpressionConstruct()


class ExpressionConstruct(Construct):
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQ = "=="
    NEQ = "~="

    def __init__(self):
        Construct.__init__(self, "expression")
        self.operand = None
        self.operator = None

    def set_operand(self, o):
        self.operand = o

    def set_operator(self, o):
        self.operator = o

    def get_operand(self):
        return self.operand

    def get_operator(self):
        return self.operator


class ConnectorConstruct(Construct):
    def __init__(self, src=None, dest=None):
        Construct.__init__(self, "connector")
        self.src = src
        self.dest = dest