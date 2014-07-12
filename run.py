import sys
import urllib2
import json
import polyline
from xml.sax.saxutils import escape

base_otp = 'http://planner.plannerstack.org/otp-rest-servlet/ws/plan?time=1%3A09am&date=07-12-2014&mode=CAR&maxWalkDistance=750&arriveBy=false&'

if len(sys.argv) != 2:
    print  "Usage: %s test.csv" % (sys.argv[0])
    sys.exit(-1)

f = open(sys.argv[1])

hit = set([])
nothit = set([])

print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Concat</name>"""
"""    <Style id="GreenLine">
      <LineStyle>
        <color>007fff00</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="RedLine">
      <LineStyle>
        <color>7f000000</color>
        <width>1</width>
      </LineStyle>
    </Style>"""

for line in f:
    name, x1, y1, x2, y2 = line[:-1].split(',')
    output = json.loads(urllib2.urlopen(base_otp+'fromPlace='+y1+'%2C'+x1+'&toPlace='+y2+'%2C'+x2).read())

    if output['plan'] is not None:
        for itin in output['plan']['itineraries']:
            for leg in itin['legs']:
                print """    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <styleUrl>#GreenLine</styleUrl>
        <LineString>
            <coordinates>""" % (escape(name), leg['legGeometry']['length'])
                print ' '.join([','.join([str(p[0]), str(p[1])]) for p in polyline.decode(leg['legGeometry']['points'])])

                print """            </coordinates>
        </LineString>
    </Placemark>"""
        hit.add(x1+','+y1)
        hit.add(x2+','+y2)

    else:
        if (x2+','+y2 not in hit and x2+','+y2 not in nothit) or (x1+','+y1 not in hit and x1+','+y1 not in nothit):
            print """    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <styleUrl>#redLine</styleUrl>""" % (escape(name), "No result")
            if True:
                if (x2+','+y2 not in hit and x2+','+y2 not in nothit):
                    print """        <Point>
            <coordinates>
%s,%s
            </coordinates>
        </Point>""" % (x2, y2)
                    nothit.add(x2+','+y2)
                else:
                    print """        <Point>
            <coordinates>
%s,%s
            </coordinates>
        </Point>""" % (x1, y1)
                    nothit.add(x1+','+y1)

            else:
                print """        <LineString>
            <coordinates>"""
                print ' '.join([','.join([str(p[0]), str(p[1])]) for p in [(x1, y1), (x2, y2)]])
                print """            </coordinates>
        </LineString>"""

            print """    </Placemark>"""

print """  </Document>
</kml>"""
