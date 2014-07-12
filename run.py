import sys
import urllib2
import json
import polyline

base_otp = 'http://planner.plannerstack.org/otp-rest-servlet/ws/plan?time=1%3A09am&date=07-12-2014&mode=CAR&maxWalkDistance=750&arriveBy=false&'

if len(sys.argv) != 2:
    print  "Usage: %s test.csv" % (sys.argv[0])
    sys.exit(-1)

f = open(sys.argv[1])

print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Concat</name>
    <Style id="GreenLine">
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
            <coordinates>""" % (name, leg['legGeometry']['length'])
                print ' '.join([','.join([str(p[0]), str(p[1])]) for p in polyline.decode(leg['legGeometry']['points'])])

                print """            </coordinates>
        </LineString>
    </Placemark>"""

    else:
        print """    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <styleUrl>#redLine</styleUrl>
        <LineString>
            <coordinates>""" % (name, "No result")
        print ' '.join([','.join([str(p[0]), str(p[1])]) for p in [(x1, y1), (x2, y2)]])
        print """            </coordinates>
        </LineString>
    </Placemark>"""



print """  </Document>
</kml>"""
