from builder.Construct import Construct


class Field(Construct):
    size_map = {
        "UINT8": 1,
        "UINT16": 2
    }

    def __init__(self, name):
        Construct.__init__(self, "field")
        self.name = name
        self.abbreviation = None
        self.description = None
        self.reference_list = None
        self.data_type = None
        self.base = None
        self.mask = None
        self.constraint = None
        self.required = False
        self.size = None

    def set_type(self, dtype):
        self.data_type = dtype
        if dtype in Field.size_map:
            self.size = Field.size_map[dtype]


class ReferenceList(Construct):
    def __init__(self, name):
        Construct.__init__(self, "reference")
        self.name = name
        self.vals = []
        self. descriptions = []

    def add(self, val, description):
        self.vals.append(val)
        self.descriptions.append(description)