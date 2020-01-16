from pbx_gs_python_utils.utils.Files import Files
import xml.etree.ElementTree as ET

from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser


def tag(element):
    return element.tag.split('}').pop()

def run(event, context):

    xml_report = event.get('xml_report')
    config     = event.get('config')

    return Report_Xml_Parser(xml_report,config).parse_document()
