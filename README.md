# warpPipe
Uses maxmind API to generate a report of information on provided IP addresses.
File reports are generated in:
  A .xlsx file (with seperate tabs for a legend of terms and raw request logs). There are collums to detect if the IP address is currently being used as part of a mis-attribution service or TOR exit node. If either of this are true, that field will turn red for those colums.
  
  A .KML Google Earth file with seperate icons for connection type and if there is any indication of the IP addressed being used as a mis-attribution service.

A free trial of the Maxmind API with $5 in credits can be obtained from here: https://www.maxmind.com/en/request-service-trial?service_geoip=1

