# IRCTC - Main
# this will be the main centre for the irctc program
# all the function will be called from this module to other modules
__author__ = 'rvisharma'

import irctc_pnr_xml
import time

print '''IRCTC PNR STATUS
This Program will call the railpnrAPI to get the PNR status
author - rvisharma\n'''

get_pnr = raw_input('To get PNR Status, Type P and press ENTER: ')
if get_pnr.lower() == 'p':
    print '================================'
    irctc_pnr_xml.get_pnr_xml()
    print round((irctc_pnr_xml.t2 - irctc_pnr_xml.t1), 3), 'seconds'
    print 'XML REPORT COMPLETED'
    print '================================'
    time.sleep(10)
