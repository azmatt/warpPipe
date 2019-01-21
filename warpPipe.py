#5f56a16d90362d2ab1544bd26d539f45
#Matt Edmondson
#@matt0177

import geoip2.webservice
import xlsxwriter
import time
import datetime
from geocreds import *
import argparse

ts = time.time()
logo = """
 _     _  _______  ______    _______        _______  ___   _______  _______ 
| | _ | ||   _   ||    _ |  |       |      |       ||   | |       ||       |
| || || ||  |_|  ||   | ||  |    _  |      |    _  ||   | |    _  ||    ___|
|       ||       ||   |_||_ |   |_| |      |   |_| ||   | |   |_| ||   |___ 
|       ||       ||    __  ||    ___|      |    ___||   | |    ___||    ___|
|   _   ||   _   ||   |  | ||   |          |   |    |   | |   |    |   |___ 
|__| |__||__| |__||___|  |_||___|          |___|    |___| |___|    |_______|



"""

print logo

###CLI Options
parser = argparse.ArgumentParser()

parser.add_argument('-s', nargs='?', dest='ipTextFile', default='ips.txt', help='a textfile with the IP addresses to be submitted. defaults to ips.txt')
args = parser.parse_args()
print "[+] Processing: %s" % (args.ipTextFile)

stringTime = datetime.datetime.fromtimestamp(ts).strftime('%m%d%y_%H%M%S')
reportName = 'warpPipeReport_' + stringTime + ".xlsx"

# account ID and license key pulled from geocreds.py
client = geoip2.webservice.Client(account_id, license_key)


###Create xlsx
workbook = xlsxwriter.Workbook(reportName)
bold = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet('IP Results')
worksheet2 = workbook.add_worksheet('Legend')
worksheet3 = workbook.add_worksheet('log')
format1 = workbook.add_format({'bg_color':   '#FFC7CE', 'font_color': '#9C0006'}) #highlight red
worksheet.conditional_format('H2:H65000', {'type':'cell','criteria':'equal to','value':'TRUE','format':format1})
worksheet.conditional_format('I2:I65000', {'type':'cell','criteria':'equal to','value':'TRUE','format':format1})
worksheet.set_column(0, 3, 16) #(first col, last col, width)
worksheet.set_column(4, 5, 20) 
worksheet.set_column(6, 6, 15) 
worksheet.set_column(7, 7, 18)
worksheet.set_column(8, 8, 15)
worksheet.write('A1', 'IP Address', bold)
worksheet.write('H1', 'Anonymous Network', bold)
worksheet.write('B1', 'City', bold)
worksheet.write('D1', 'Country', bold)
worksheet.write('E1', 'ISP', bold)
worksheet.write('F1', 'Registered Country', bold)
worksheet.write('I1', 'TOR Exit Node', bold)
worksheet.write('G1', 'User Type', bold)
worksheet.write('C1', 'Region', bold)
worksheet.write('J1', 'Longitude', bold)
worksheet.write('K1', 'Latitude', bold)

#### Create legend
worksheet2.set_column(0, 0, 20) 
worksheet2.set_column(1, 1, 50)
worksheet2.write('A1', 'Country:', bold)
worksheet2.write('B1', 'The country where MaxMind believes the end user is located.')
worksheet2.write('A2', 'ISP:', bold)
worksheet2.write('B2', 'The name of the Internet Service Provider associated with the IP address.')
worksheet2.write('A3', 'Registered Country:', bold)
worksheet2.write('B3', 'The country in which the ISP has registered the IP address.')
worksheet2.write('A4', 'Anonymous Network:', bold)
worksheet2.write('B4', 'This is true if the IP address belongs to any sort of anonymous network like a VPN or Proxy.')
worksheet2.write('A5', 'TOR Exit Node:', bold)
worksheet2.write('B5', 'This is true if the IP address is a Tor exit node.')

#### KML icon styles
kmlIcons = '''
   <Style id="college">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal2/icon10.png</href>
        </Icon>
      </IconStyle>
    </Style>
	   <Style id="residential">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal2/icon20.png</href>
        </Icon>
      </IconStyle>
    </Style>
		   <Style id="content_delivery_network">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal4/icon10.png</href>
        </Icon>
      </IconStyle>
    </Style>
			   <Style id="cellular">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal5/icon50.png</href>
        </Icon>
      </IconStyle>
    </Style>
	<Style id="hosting">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal3/icon21.png</href>
        </Icon>
      </IconStyle>
    </Style>
	<Style id="business">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal2/icon58.png</href>
        </Icon>
      </IconStyle>
    </Style>
	<Style id="shady">
      <IconStyle>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal3/icon37.png</href>
        </Icon>
      </IconStyle>
    </Style>
'''

#### KML Prologue
mapName = 'warpPipeMap_' + stringTime + ".kml"
kmlOutput = open(mapName, 'w')
kmlOutput.write("<?xml version='1.0' encoding='UTF-8'?>\n")
kmlOutput.write("<kml xmlns='http://earth.google.com/kml/2.1' xmlns:gx='http://www.google.com/kml/ext/2.2'>n" )
kmlOutput.write("<Document>\n")
kmlOutput.write("   <name> General Locations </name>\n")
kmlOutput.write(kmlIcons)


### Main Logic
row = 1
col = 0
ipDupList = []  ##Will add every IP here so we can later check for and avoid duplicates
dupCount = 0

with open(args.ipTextFile) as ipList:
	for line in ipList:
		strLine = str(line).strip('\n')
		if strLine in ipDupList:        ####Skiping and counting duplicates
			dupCount += 1
		else:
			if len(strLine) > 2:  #Checking to make sure the line isn't blank
				try:
					ipDupList.append(strLine)
					response = client.insights(str(line).strip('\n'))  ##Query maxmind with the cleaned up IP address
					worksheet3.write(row, col, str(response))
					worksheet.write(row, col, line)
					worksheet.write(row, col + 7, response.traits.is_anonymous)
					worksheet.write(row, col + 1, response.city.name )
					worksheet.write(row, col + 3, response.country.name)
					worksheet.write(row, col + 4, response.traits.isp )
					worksheet.write(row, col + 5, response.registered_country.name )
					worksheet.write(row, col + 8, response.traits.is_tor_exit_node)
					worksheet.write(row, col + 6, response.traits.user_type)
					worksheet.write(row, col + 2, response.subdivisions.most_specific.name)
					worksheet.write(row, col + 9, response.location.longitude)
					worksheet.write(row, col + 10, response.location.latitude)
					row += 1
					long = str(response.location.longitude)
					lat =  str(response.location.latitude)
					anonVPN = str(response.traits.is_anonymous)
					anonTOR = str(response.traits.is_tor_exit_node)
					userType = str(response.traits.user_type)
					if lat and long != "None":                          ######Setting Icon Styles for KML
						if  anonVPN == "True" or anonTOR  == "True":
							iconStyle = "shady"
						else:
							iconStyle = userType
						kml_contents = " <Placemark>\n <name>" + strLine + "</name>\n <styleUrl>#" + iconStyle + "</styleUrl> \n <description> <p><b>Description:</b> " + "placeHolda" + "</p> </description>\n <Point>\n <coordinates>" + long + "," + lat + ",0 </coordinates>\n </Point>\n </Placemark>\n"
						kmlOutput.write(kml_contents)
					else:
						pass
				except Exception as e:
					print "an error occurred with: %s :" % strLine + str(e)
			else:
				pass

print "[+] Ignored %d Duplicates" % (dupCount)
print "[+] Processed %d IP Addresses" % (row-1)



sourceInfo = raw_input("[+] Please type the requester information then hit ENTER:  ") #Lets users see the results if they double click instead of run from CLI
worksheet3.write(row, col, "requester: " + str(sourceInfo)) #Puts the requesters name on the bottom of the log tab in the xlsx report

### Epilogue
workbook.close()
print "[+] Generated report"
kmlOutput.write("</Document>\n")
kmlOutput.write("</kml>\n")
kmlOutput.close()
print"[+] Generated KML file"
