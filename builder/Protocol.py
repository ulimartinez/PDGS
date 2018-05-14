from builder.Dissector import Dissector
from field.Field import Field
from builder.Construct import *
from LuaScript import LuaScript


class Protocol:
    def __init__(self, name):
        self.name = name
        self.dissector = Dissector(self)

    def get_dissector(self):
        return self.dissector


# TEST DRIVER CODE
proto = Protocol("Awesome icmp")
start = StartConstruct()
start.dependency = "ip.proto"
start.pattern = "1"
proto.dissector.dtree.add_construct(start)
f = Field("Type")
f.set_type("UINT8")
proto.dissector.dtree.add_construct(f)
f2 = Field("code")
f2.set_type("UINT8")
proto.dissector.dtree.add_construct(f2)
f3 = Field("Checksum")
f3.set_type("BYTES")
f3.size = 2
proto.dissector.dtree.add_construct(f3)
f4 = Field("Identifier")
f4.set_type("BYTES")
f4.size = 2
proto.dissector.dtree.add_construct(f4)
f5 = Field("Sequence Number")
f5.set_type("UINT16")
proto.dissector.dtree.add_construct(f5)
f6 = Field("Data")
f6.set_type("BYTES")
f6.size = -1
proto.dissector.dtree.add_construct(f6)
lua = LuaScript(proto)
print(lua.generate_script())
