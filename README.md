IRCTC PNR STATUS CHECKER

pre-requisites -> Python 2.x, Requests Module

@author - Ravi Sharma
github - rvisharma

rvisharma91@gmail.com

This program contains 2 separate programs, each do the same task but calls different APIs

irctc_main_xml -> calls PNRbuddy API to get the PNR status in XML format
					and used XML parsing methods

irctc_main_json -> call railpnrAPI to get the PNR status in JSON format
					amd uses JSON parsing methods

in my experience, railpnrAPI has more success rate in searching the PNR than of pnrbuddyAPI
also. railpnrAPI is more faster.

Features list to be implemented :
	1 - Get station namea from Station codes
	2 - Trains between stations in PNR
	3 - UI ...??

Note - if you find any bugs, please report