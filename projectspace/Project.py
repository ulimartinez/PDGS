import os
import xml.etree.ElementTree as ET


# Class Project collaborates with GUI and LUA script
# Displays project name and its specific protocol.
# Projects can be imported and exported from the workspace
# @param (name, path, protocol, layout, description)


class Project:
    def __init__(self, name, path, protocol, layout, description):
        self.name = name
        self.path = path
        self.protocol = protocol
        self.layout = layout
        self.description = description

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_path(self):
        return self.path

    def set_path(self, value):
        self.path = value

    def get_protocol(self):
        return self.protocol

    def set_protocol(self, value):
        self.protocol = value

    def get_layout(self):
        return self.layout

    def set_layout(self, value):
        self.layout = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value


# creates new project object and directory
# @\requires (name != null or contain illegal characters) && (save_path exists)
# @\ensures project exists at save_path with description text file
def new_project(name, save_path, description):
    # Check if path exists
    try:
        verify_path(save_path)
        os.chdir(save_path)
        try:
            # If project dne create new project
            os.makedirs(name, 1)  # Create directory at specified path
            new_p = Project(name, save_path, "protocol", "layout", description)

            #
            #   TODO Load new project onto canvas(empty)
            #

            # Create text file that holds description
            desc_file = open(name + "_description.txt", "w")
            desc_file.write(description)
        except OSError as e:
            print('Directory already exists: Directory not created.')

    except OSError as e:
        print('Path not found')


# Loads existing xml_project
# @\requires xml_project != null
# @\ensures saved xml_project is loaded
def load_project(xml_project):  # TODO untested needs gui
    try:
        #   parses xml file
        with open(xml_project, 'r') as f:
            data = f.read()
        tree = ET.fromstring(data)
        # print 'Name:', tree.find('name').text
        # print 'Path:', tree.find('path').text

        #
        #   TODO Load xml Project onto canvas
        #

    except IOError as e:
        print "Unable to open file"


# save current project and save as XML
# @\REQUIRES collaboration with layout & protocol to continue
# @\ensures (new)project state is saved
def save_project(project):  # TODO save in class ??
    name = project.get_name()
    path = project.get_path()
    protocol = project.get_protocol()
    layout = project.get_layout()
    description = project.get_description()


# export dissector in LUA script format
# REQUIRES collaboration with lua script
# @\ensure file == lua format
def export_lua_dissector(xml_project, save_path):  # not working / take in project or xml file???
    try:
        #   Change path
        verify_path(save_path)
        os.chdir(save_path)
        try:
            #   Parse xml_file
            with open(xml_project, 'r') as f:
                data = f.read()
            tree = ET.fromstring(data)
            dissector_protocol = tree.find('protocol').text
            dissector_name = tree.find('name').text

            #
            #   TODO Convert dissector_protocol to LUA format
            #

            lua_dissector = dissector_protocol

            try:
                #   Create dis.lua file in save_path
                lua_dissector_name = dissector_name + ".lua"
                fd = os.open(lua_dissector_name, os.O_CREAT | os.O_EXCL)
                os.fdopen(fd, 'w')

                #   write lua_dissector to LUA file
                with open(lua_dissector_name, 'r') as f:  # TODO can't write to lua file??
                    f.write(lua_dissector)

            except OSError:
                print('LUA dissector already exists: Dissector not created.')

        except IOError as e:
            print "Unable to open file"

    except OSError as e:
        print('Path not found')


# verify directory path
def verify_path(path):
    if os.path.exists(path):
        return 1


def main():
    print "\n"
    #   testing

    # path1 = r"C:\Users\*HOMEDIR*\Desktop\test"  # annoying path requires char 'r' before string
    # dis = r"C:\Users\*HOMEDIR*\Desktop\test\new_project555"
    # new_project("new_project555", path1, "description")
    # new_project = Project("test_project", path1, "protocool", "layout")  # works

    # export_lua_dissector(new_project, path1)
    # open_project("test.txt") # untested with projec
    # ts on gui
    # data = r"C:\Users\*HOMEDIR*\PycharmProjects\Projectspace_Subsystem\data\xml_file.xml"
    # load_project(data)
    # export_lua_dissector(data, path1)


if __name__ == "__main__":
    main()
