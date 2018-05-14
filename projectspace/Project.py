import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from XML_Project_Format import *


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


# creates new project object and directory in save path location
# @\requires (name != null or contain illegal characters) && (save_path exists)
# @\ensures project exists at save_path with description text file
def create_new_project(name, save_path, description):
    # Check if path exists
    try:
        verify_path(save_path)
        os.chdir(save_path)
        try:
            # If project dne create new project
            os.makedirs(name, 1)  # Create directory at specified path
            new_project = Project(name, save_path, "protocol", "layout", description)

            #
            #   TODO Load new project onto canvas(empty)
            #

        except OSError as e:
            print('Directory already exists: Directory not created.')

    except OSError as e:
        print('Path not found')


# Loads existing xml_project
# @\requires xml_project != null
# @\ensures saved xml_project is loaded
def load_project(xml_project):  # TODO untested needs gui
    try:
        parse_xml_project(xml_project)

        #
        #   TODO Load xml Project onto canvas
        #

    except IOError as e:
        print "Unable to open file"


# saves project as XML
# @\REQUIRES collaboration with layout & protocol to continue
# @\ensures (new)project state is saved
def save_project(project):
    project_name = project.get_name()
    project_path = project.get_path()
    project_protocol = project.get_protocol()
    project_layout = project.get_layout()
    project_description = project.get_description()

    # TODO assign dtree, construct and field from canvas
    protocol_dtree = " dtree"
    protocol_construct = "construct"
    protocol_field = "field"
    protocol_dissector = "dissector"

    try:
        #   Change path
        verify_path(project_path)
        os.chdir(project_path)

        try:
            #   Create dis.xml file in save_path
            file = open('project_name.xml', "w")

            # Project XML
            project_root = Element('project')
            project_tree = ElementTree(project_root)

            name = Element('name')
            project_root.append(name)
            name.text = project_name

            # Protocol
            protocol_root = Element('protocol')
            project_root.append(protocol_root)
            protocol_root.text = project_protocol

            # Protocol : Dissector
            dissector_root = Element('dtree')
            protocol_root.append(dissector_root)
            dissector_root.text = protocol_dissector

            # Protocol : Dissector : dTree
            dtree_root = Element('dtree')
            dissector_root.append(dtree_root)
            dtree_root.text = protocol_dtree

            # Protocol: Dissector: dTree : construct
            construct = Element('construct')
            dtree_root.append(construct)
            construct.text = protocol_construct

            # Protocol: Dissector: dTree : field
            field = Element('field')
            dtree_root.append(field)
            field.text = protocol_field

            path = Element('path')
            project_root.append(path)
            path.text = project_path

            layout = Element('layout')
            project_root.append(layout)
            layout.text = project_layout

            description = Element('description')
            project_root.append(description)
            description.text = project_description

            save_name = project_name + '.xml'
            project_tree.write(open(save_name, 'w'))

        except OSError:
            print('LUA dissector already exists: Dissector not created.')

    except OSError as e:
        print('Path not found')


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
    # testing

    # save_path = r"C:\Users\luui9\Desktop\test"  # annoying path requires char 'r' before string
    # dis = r"C:\Users\*HOMEDIR*\Desktop\test\new_project555"
    xml_file = r"C:\Users\luui9\Desktop\test\test_project.xml"
    # new_project1 = Project("23456789", save_path, "protocool1", "layout2", "description3")  # works
    # new_project2("name2", save_path, "description")
    # save_project(new_project1)
    # export_lua_dissector(new_project, path1)
    # open_project("test.txt") # untested with project
    # ts on gui
    # data = r"C:\Users\*HOMEDIR*\PycharmProjects\Projectspace_Subsystem\data\xml_file.xml"
    # load_project(data)
    # export_lua_dissector(data, path1)

    # load_project(xml_file)

if __name__ == "__main__":
    main()
