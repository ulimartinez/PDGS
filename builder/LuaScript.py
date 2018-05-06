from builder.Construct import *
import re


class LuaScript:
    def __init__(self, protocol):
        self.protocol = protocol
        self.dtree = protocol.get_dissector().get_tree()

    def generate_script(self):
        script = ""
        # generate protocol name
        proto_name = self.protocol.name
        lower_proto_name = re.sub('\s', "_", proto_name.lower())
        proto_id = lower_proto_name + "_proto"
        script += '{} = Proto("{}","{}")\n'.format(proto_id, lower_proto_name, proto_name)

        # generate dissector function
        script += 'function {}.dissector(buffer,pinfo,tree)\n'.format(proto_id)
        script += '\tpinfo.cols.protocol = "{}"\n'.format(lower_proto_name.upper())
        # TODO: iterate self.dtree to generate code
        for node in self.dtree.get_nodes():
            print(isinstance(node, StartConstruct))
        script += "end\n"

        # add port info
        script += 'table = DissectorTable.get("udp.port")\n'
        script += 'table:add(50000,{})\n'.format(proto_id)
        script_file = open("{}.lua".format(lower_proto_name), "w")
        script_file.write(script)
        script_file.close()
        return lower_proto_name + ".lua"
