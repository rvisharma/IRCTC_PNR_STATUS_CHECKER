
import xml.etree.ElementTree as ET
import requests
import requests.exceptions
import time

__author__ = 'Rvisharma'

t1, t2 = 0,0 # time values

# Extract the Ticket Details and return the dict
def extract_xml_ticket_details(xml):
    '''docstring - (xml) -> dict{}
    returns dictionary of ticket details
    '''
    ticket = {}
    ticket['train_num'] = xml.find('train_num').text
    ticket['train_name'] = xml.find('train_name').text
    ticket['doj'] = xml.find('doj').text
    ticket['from_station'] = xml.find('from_station/code').text
    ticket['to_station'] = xml.find('to_station/code').text
    ticket['boarding_point'] = xml.find('boarding_point').text
    ticket['reservation_upto'] = xml.find('reservation_upto').text
    ticket['train_class'] = xml.find('class').text
    ticket['num_of_passengers'] = xml.find('no_of_passengers').text
    ticket['chart_prep'] = xml.find('chart_prepared').text
    return ticket

def extract_xml_passenger_details(xml):
    passenger = {}
    passenger_list = xml.findall('passengers/passenger')
    num_passenger = int(xml.find('no_of_passengers').text)
    for each in range(num_passenger):
        #xml
        booking_status = passenger_list[each].find('booking_status').text
        # list of string
        booking_status = booking_status.split(',')
        coach = booking_status[0].strip()
        seat = booking_status[1].strip()
        quota = booking_status[2].strip()
        current_status = passenger_list[each].find('current_status').text.strip()
        
        passenger[each + 1] = (coach, seat, quota, current_status)
    return passenger   

def print_ticket_details(ticket):
    print 'Date of Jouney:', ticket['doj']
    print 'Train:', ticket['train_num'], ticket['train_name']
    
    from_station = ''
    if ticket['boarding_point'] in ['', None]:
        from_station = ticket['from_station']
    else:
        from_station = ticket['boarding_point']
    print 'From:', from_station

    to_station = ''
    if ticket['reservation_upto'] in ['', None]:
        to_station = ticket['to_station']
    else:
        to_station = ticket['reservation_upto']
    print 'To:', to_station

    if ticket['chart_prep'] in ['N', False]:
        print 'Chart NOT Prepared'
    else:
        print 'Chart Prepared'

    print 'Number of Passengers:', ticket['num_of_passengers']

def print_passenger_details(passenger):
    # Header
    print 'Sr.\tCoach\tSeat\tQuota\tStatus'
    for key, value in passenger.items():
        print key, '->\t', '\t'.join(value)

def print_pnr_database(database):
    ticket = database[0]
    passenger = database[1]

    try:
        print 'PNR DETAILS:', pnr_number # global->pnr_number
    except:
        pass
    
    print ''
    print_ticket_details(ticket)
    print ''
    print_passenger_details(passenger)

# get the pnr number and return list of pnr_database[ticket{},passenger{}]
def get_pnr_database(pnr_number):
    
    print 'Looking for PNR..' # TESTING
    
    URL = 'http://pnrbuddy.com/api/check_pnr/pnr/%s' %(pnr_number)
    try:
        r = requests.get(URL, timeout = 60)
    except requests.exceptions.Timeout:
        print '\nTimeout, connection taking too long to respond,'
        print 'Try again later'
        return
    except requests.exceptions.ConnectionError:
        print r.status_code
        print 'Connection Error, Please try again later.'
        return
    
    # generate xml from content
    pnr_xml = ET.fromstring(r.content)

    if pnr_xml.find('error').text == None:
        ticket = extract_xml_ticket_details(pnr_xml)
        passengers = extract_xml_passenger_details(pnr_xml)
        return [ticket, passengers]
    else:
        print pnr_xml.find('error').text
        return None

# list to store the pnr details
pnr_database = [] #[ticket_details{}, passenger_details{}]
# get_pnr_xml module for irctc_main.py
def get_pnr_xml():
    global pnr_database, pnr_number, t1, t2
    pnr_number = raw_input('Enter the 10-digit PNR Number ')
    # TESTING
    #pnr_number = '6620398229'
    # call the function to get the pnr database list
    if len(pnr_number) == 10 and pnr_number.isdigit():
        t1 = time.time()
        pnr_database = get_pnr_database(pnr_number)
        if pnr_database == None:
            t2 = time.time()
            return
        else:
            print_pnr_database(pnr_database)
            t2 = time.time()
            print '\nSuccess'
            print ''
    else:
        print 'Invalid PNR'
        get_pnr_xml()

# TEST CODE offline for xml parsing
if __name__ == '__main__':

    #FOR XML
    file = open('pnrxml.xml')
    xml = ET.fromstring(file.read())
    database = [extract_xml_ticket_details(xml), extract_xml_passenger_details(xml)]
    print 'SAMPLE OUTPUT: XML'
    print_pnr_database(database)
