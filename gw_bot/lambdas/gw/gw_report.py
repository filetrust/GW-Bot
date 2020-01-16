from pbx_gs_python_utils.utils.Files import Files
import xml.etree.ElementTree as ET

from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser


def tag(element):
    return element.tag.split('}').pop()

def run(event, context):

    include_policy  = False
    include_content = True

    xml_report = event.get('xml_report')
    #
    # root = ET.fromstring(xml_report)
    #
    return Report_Xml_Parser(xml_report).parse_document()

    # data = {
    #     "DocumentSummary": { "TotalSizeInBytes": root[0][0][0].text ,
    #                          "FileType"        : root[0][0][1].text ,
    #                          "Version"         : root[0][0][2].text}}
    # if include_policy:
    #     data["ContentManagementPolicy"]: {}
    #     for child in root[0][1]:
    #         name   =  child.attrib['cameraName']
    #         camera = {}
    #         data['ContentManagementPolicy'][name] = camera
    #         for item in child:
    #             camera[item[0].text] = item[1].text

    def parse_content_group(target):
        result = {}
        for item in target:
            content_item = {}
            technical_description = ""
            for value in item:
                if tag(value) == 'TechnicalDescription':
                    technical_description = value.text
                else:
                    content_item[tag(value)] = value.text
            result[technical_description] = content_item
        return result

    if include_content:
        data["ContentGroups"] = {}
        for child in root[0][2]:
            contentGroups = {}
            description  =  child[0].text
            data["ContentGroups"][description] = contentGroups

            content_items = {}
            target = child[1]
            return parse_content_group(child[1])




    return data