from builder.Construct import *
from field.Field import Field
import re


class LuaScript:
    def __init__(self, protocol):
        self.protocol = protocol
        self.dtree = self.protocol.dissector.dtree

    def generate_script(self):
        script = ""
        # generate protocol name
        proto_name = self.protocol.name
        lower_proto_name = self._get_lower(proto_name)
        proto_id = lower_proto_name + "_proto"
        script += '{} = Proto("{}","{}")\n'.format(proto_id, lower_proto_name, proto_name)

        # generate fields
        fields = []
        for c in self.dtree.nodes:
            if isinstance(c, Field):

                lower_field = self._get_lower("f " + c.name)
                script += '{} = ProtoField.new("{}", "{}.{}", ftypes.{})\n'.format(
                    lower_field, c.name, lower_proto_name, lower_field, c.data_type
                )
                fields.append(lower_field)
        script += '{}.fields = '.format(proto_id) + "{" + ",".join(fields) + "}\n"

        # generate dissector function
        script += 'function {}.dissector(buffer,pinfo,tree)\n'.format(proto_id)
        script += '\tpinfo.cols.protocol = "{}"\n'.format(lower_proto_name.upper())
        script += '\tlocal subtree = tree:add({},buffer(),"{} Data")\n'.format(proto_id, proto_name)

        # add fields to subtree
        location = 0
        for c in self.dtree.nodes:
            if isinstance(c, Field):
                lower_f = self._get_lower(c.name)
                script += '\tsubtree:add(f_{}, buffer({}, {}))\n'.format(lower_f, location, c.size)
                location += c.size
        script += "end\n"

        # add dependency info
        start_field = self.dtree.nodes[0]
        script += 'table = DissectorTable.get("{}")\n'.format(start_field.dependency)
        script += 'table:add({},{})\n'.format(start_field.pattern, proto_id)
        script_file = open("{}.lua".format(lower_proto_name), "w")
        script_file.write(script)
        script_file.close()
        return lower_proto_name + ".lua"

    def _get_lower(self, ustr):
        return re.sub('\s', "_", ustr.lower())

