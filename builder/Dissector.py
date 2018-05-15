from DTree import DecisionTree
from LuaScript import LuaScript
import sys, os, subprocess, re


class Dissector:
    def __init__(self, protocol):
        self.dtree = DecisionTree()
        self.protocol = protocol
        self.tshark = TShark()

    def dissect_packet(self, packet):
        print("printing packet")
        tshark = TShark()
        lua = LuaScript(self.protocol)
        script = lua.generate_script()
        tshark.dissect_packet(packet, script)

    def get_packets(self, packet="icmp.pcap"):
        lua = LuaScript(self.protocol)
        script = lua.generate_script()
        return self.tshark.dissect_packet(packet, script)

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

    def dissect_packet(self, packet, lua_script):
        params = [self.path, "-Xlua_script:"+lua_script, "-r", packet]
        print(params)
        out = self.run_command(params, stderr=None).decode("ascii")
        print(out)

    def get_packets(self, packet, lua_script):
        params = [self.path, "-Xlua_script:" + lua_script, "-r", packet]
        print(params)
        out = self.run_command(params, stderr=None).decode("ascii")
        return out

    def get_match(self, packet, lua_script):
        self.dissect_packet(packet, lua_script)

