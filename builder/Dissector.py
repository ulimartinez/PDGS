from DTree import DecisionTree
from LuaScript import LuaScript
import sys, os, subprocess, re


class Dissector:
    def __init__(self, protocol):
        self.dtree = DecisionTree()
        self.protocol = protocol
        self.tshark = TShark()

    def dissect_packet(self, pcap="icpm.pcap"):
        tshark = TShark()
        lua = LuaScript(self.protocol)
        script = lua.generate_script()
        fields = self.protocol.dissector.dtree.get_fields()
        valid_fields = []
        for f in fields:
            valid_fields.append("{}.{}".format(self.protocol.name.lower(), f))
        f_string = " ".join(valid_fields)
        return tshark.dissect_packet(pcap, script, f_string)

    def get_packets(self, pcap="icmp.pcap"):
        lua = LuaScript(self.protocol)
        script = lua.generate_script()
        return self.tshark.get_packets(pcap, script)

    def get_tree(self):
        return self.dtree


class TSharkNotFoundException(Exception):
    pass


class TShark:
    def __init__(self):
        self.path = self.find_path()

    def run_command(self, *popenargs, **kwargs):
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        return output

    def find_path(self):
        possible_paths = []
        if sys.platform.startswith('win'):
            for env in ('ProgramFiles(x86)', 'ProgramFiles'):
                program_files = os.getenv(env)
                if program_files is not None:
                    possible_paths.append(
                        os.path.join(program_files, 'Wireshark', '%s.exe' % "tshark")
                    )
        else:
            os_path = os.getenv(
                'PATH',
                '/usr/bin:/usr/sbin:/usr/lib/tshark:/usr/local/bin'
            )
            for path in os_path.split(':'):
                possible_paths.append(os.path.join(path, "tshark"))

        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise TSharkNotFoundException('TShark not found.')

    def get_version(self):
        out = self.run_command([self.path, "-v"], stderr=None).decode("ascii")
        first_line = out.splitlines()[0]
        match = re.match('.*\s(\d+\.\d+\.\d+).*', first_line)
        return match.groups()[0]

    def dissect_packet(self, packet, lua_script, fields):
        params = [self.path, "-Xlua_script:"+lua_script, "-r", packet, "-T", "fields", "-e", fields]
        print(params)
        out = self.run_command(params, stderr=None)
        return out

    def get_packets(self, packet, lua_script):
        params = [self.path, "-Xlua_script:" + lua_script, "-r", packet]
        print(params)
        out = self.run_command(params, stderr=None)
        return out

    def get_match(self, packet, lua_script):
        self.dissect_packet(packet, lua_script)

