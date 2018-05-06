from DTree import DecisionTree
import sys, os, subprocess, re


class Dissector:
    def __init__(self):
        self.dtree = DecisionTree()

    def dissect_packet(self, packet):
        print("printing packet")


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
        # Windows search order: configuration file's path, common paths.
        if sys.platform.startswith('win'):
            for env in ('ProgramFiles(x86)', 'ProgramFiles'):
                program_files = os.getenv(env)
                if program_files is not None:
                    possible_paths.append(
                        os.path.join(program_files, 'Wireshark', '%s.exe' % "tshark")
                    )
        # Linux, etc. search order: configuration file's path, the system's path
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
        out = self.run_command(params, stderr=None).decode("ascii")

