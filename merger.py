import os, os.path, sys
import glob
from xml.etree import ElementTree

def run(files):
    xml_files = glob.glob(files +"/*.xml")
    xml_element_tree = None
    for xml_file in xml_files:
        data = ElementTree.parse(xml_file).getroot()
        # print ElementTree.tostring(data)
        for result in data.iter('DEFTABLE'):
            if xml_element_tree is None:
                xml_element_tree = data
                insertion_point = xml_element_tree.findall("./DEFTABLE")[0]
            else:
                insertion_point.extend(result)
    if xml_element_tree is not None:
        print(ElementTree.tostring(xml_element_tree))
        tree = ElementTree.ElementTree(xml_element_tree)
        tree.write(files+"merge.xml")


def main():
    print("hello world!")
    run("C:\\Users\\rgu107\\Desktop\\merge\\")

if __name__== "__main__":
  main()