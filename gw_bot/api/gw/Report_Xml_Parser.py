import xml.etree.ElementTree         as ET
from functools import lru_cache

default_config = {
                    "include_policy"            : True,
                    "include_content_groups"    : True ,
                    "include_content_items"     : True,
                    "include_issue_items"       : True,
                    "include_remedy_items"      : True,
                    "include_sanitisation_items": True
                }

class Report_Xml_Parser():
    def __init__(self, report_xml, config = None):
        self.report_xml            = report_xml
        self.config                = config or default_config
        self._root                 = None

        self.remove_namespace_references()


    # helper methods
    def remove_namespace_references(self):
        root_with_namespaces    = '<gw:GWallInfo xsi:schemaLocation="http://glasswall.com/namespace/gwallInfo.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gw="http://glasswall.com/namespace">'
        root_without_namespaces = '<GWallInfo>'
        self.report_xml = self.report_xml.replace(root_with_namespaces, root_without_namespaces) \
                                         .replace('<gw:' , '<')                                  \
                                         .replace('</gw:', '</')

        return self

    def set_config(self,config):
        self.config = config
        return self
    # element methods
    @lru_cache(maxsize=None)            # cache return value
    def root(self):
            return ET.fromstring(self.report_xml)

    def document_statistics(self):
        return self.root()[0]

    def document_summary(self):
        return self.document_statistics()[0]

    def content_content_management_policy(self):
        return self.document_statistics()[1]

    def content_groups(self):
        return self.document_statistics()[2]

    def extracted_items(self):                  # not implemented (test file doesn't contain data
        return self.document_statistics()[3]

    # Parse methods

    def parse_document_summary(self):
        element = self.document_summary()
        return { "TotalSizeInBytes": element[0].text ,
                 "FileType"        : element[1].text ,
                 "Version"         : element[2].text}

    def parse_content_management_policy(self):
        result =  {}
        for child in self.document_statistics()[1]:
            name   =  child.attrib['cameraName']
            camera = {}
            result[name] = camera
            for item in child:
                camera[item[0].text] = item[1].text
        return result

    def parse_content_groups(self):
        target = self.content_groups()
        result = {}
        for item in target:
            content_item      = {}
            brief_description = ""
            for value in item:
                if value.tag == 'BriefDescription':
                    brief_description = value.text
                else:
                    if self.config.get(f"include_{value.tag.lower().replace('items','_items')}"):
                        content_item[value.tag] = self.parse_content_group(value)
            result[brief_description] = content_item
        return result

    def parse_content_group(self, target):
        content_group = {}
        for item in target:
            content_item         = {}
            technical_description = ""
            for value in item:
                if value.tag == 'TechnicalDescription':
                    technical_description = value.text
                else:
                    content_item[value.tag] = value.text
            content_group[technical_description] = content_item
        return content_group


    def parse_document(self):
        result = { 'Document_Summary' : self.parse_document_summary()}
        if self.config["include_policy"]:
            result['Content_Management_Policy'] = self.parse_content_management_policy()
        if self.config["include_content_groups"]:
            result['Content_Groups'] = self.parse_content_groups()
        return result