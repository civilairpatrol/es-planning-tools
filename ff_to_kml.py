#!/usr/bin/env python

"""ff_to_kml.py: Converts ForeFlight flight plan files (.fpl) to Keyhole Markup Language (KML)."""

import sys
import xml.etree.ElementTree as ET

__author__      = "Nick McLarty"
__copyright__   = "Copyright 2018, Nick McLarty"
__license__     = "GPL v3"
__version__     = "0.9.0"
__email__       = "nick@inick.net"
__status__      = "Beta"

tree = ET.parse(sys.argv[1])
root = tree.getroot()

ns = {'garmin': 'http://www8.garmin.com/xmlschemas/FlightPlan/v1'}

coords = ""
for table in root.findall('garmin:waypoint-table', ns):
    for waypoint in table.findall('garmin:waypoint', ns):
        coords += '%s,%s,100\r\n' % (waypoint.find('garmin:lon', ns).text, waypoint.find('garmin:lat', ns).text)

xml_kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
xml_doc = ET.SubElement(xml_kml, 'Document')
ET.SubElement(xml_doc, 'Name').text = 'Search Pattern'
xml_style = ET.SubElement(xml_doc, 'Style', id='yellowLine')
xml_lnstyle = ET.SubElement(xml_style, 'LineStyle')
ET.SubElement(xml_lnstyle, 'color').text = '7f00ffff'
ET.SubElement(xml_lnstyle, 'width').text = '4'
xml_plmk = ET.SubElement(xml_doc, 'Placemark')
ET.SubElement(xml_plmk, 'Name').text = 'Search Pattern'
ET.SubElement(xml_plmk, 'styleUrl').text = '#yellowLine'
xml_lnst = ET.SubElement(xml_plmk, 'LineString')
ET.SubElement(xml_lnst, 'tessellate').text = '1'
ET.SubElement(xml_lnst, 'altitudeMode').text = 'relativeToGround'
ET.SubElement(xml_lnst, 'coordinates').text = coords

xml_tree = ET.ElementTree(xml_kml)
xml_tree.write(sys.argv[1] + ".kml", xml_declaration=True, encoding='utf-8')
