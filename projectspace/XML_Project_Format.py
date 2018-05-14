import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


def parse_xml_project(xml_project):
    with open(xml_project, 'r') as f:
        data = f.read()

    tree = ET.fromstring(data)
    print 'Name:', tree.find('name').text
    print 'Path:', tree.find('path').text
    print 'Layout:', tree.find('layout').text
    print 'Description:', tree.find('description').text

    dtree_root = tree.findall('project/protocol/dissector/dtree')
    print
    for item in dtree_root:
        print 'Construct:', item.find('construct').text
        print 'Field:', item.find('field').text

    #
    #   Apply to object
    #

    return

def save_as_xml(project):
    print "save_as_xml"


def set_layout(project):
    print "save layout"


def main():
    print "\n"
    #   testing
    # save_path = r"C:\Users\luui9\Desktop\test"  # annoying path requires char 'r' before string
    # dis = r"C:\Users\*HOMEDIR*\Desktop\test\new_project555"

    xml_file = r"C:\Users\luui9\Desktop\test\test_project.xml"
    # data = r"C:\Users\*HOMEDIR*\PycharmProjects\Projectspace_Subsystem\data\xml_file.xml"

    parse_xml_project(xml_file)



if __name__ == "__main__":
    main()
