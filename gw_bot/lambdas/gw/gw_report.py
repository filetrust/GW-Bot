
#import xml.etree.ElementTree as ET

from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser


def tag(element):
    return element.tag.split('}').pop()

def run(event, context):

    xml_report  = event.get('xml_report')
    config      = event.get('config')
    report_type = event.get('report_type')

    parser      = Report_Xml_Parser(xml_report, config)
    json_report = parser.parse_document()
    if report_type == 'summary':
        return parser.analysis_report_summary(json_report)
    return json_report

