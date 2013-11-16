import requests
import requests.exceptions
import json
import time

__author__ = 'Rvisharma'

t1, t2 = 0,0

def extract_json_ticket_details(json_data):
    ''' docstring - json -> dict{}
    return dictionary of ticket details from json object'''
    ticket = {}
    ticket['train_num'] = json_data['tnum']
    ticket['train_name'] = json_data['tname']
    ticket['doj'] = json_data['tdate']
    ticket['from_station'] = json_data['from']
    ticket['to_station'] = json_data['to']
    ticket['boarding_point'] = json_data['from']
    ticket['reservation_upto'] = json_data['to']
    ticket['train_class'] = json_data['class']
    ticket['num_of_passengers'] = json_data['numofpax']
    ticket['chart_prep'] = json_data['charted']
    return ticket

def extract_json_passenger_details(json_data):
    ''' docstring -> (json_data) -> passenger_database dict'''
    passenger = {}
    passenger_list = json_data['pax']
    for each in range(len(passenger_list)): # each is index
        coach = passenger_list[each]['coach']
        seat = passenger_list[each]['berth']
        quota = passenger_list[each]['quota']
        current_status = passenger_list[each]['status']

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
    # passengers
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

def get_pnr_database_json(pnr_number):
    '''docstring -> (pnr_number) -> pnr_database
    takes the pnr number and calls the API to get the JSON data
    reformats it to suitable pnr_database'''
    
    print 'Looking for PNR..' # TESTING
    
    URL = 'http://www.railpnrapi.com/%s' %(pnr_number)
    #print URL
    
    try:
        r = requests.get(URL, timeout = 60)
    # if response takes more than 1 minutes, raise timeout exception        
    except requests.exceptions.Timeout:
        print '\nTimeout, connection taking too long to respond,'
        print 'Try again later'
        return
    # except connection probles
    except requests.exceptions.ConnectionError:
        print r.status_code
        print 'Connection Error, Please try again later.'
        return
    
    pnr_json = json.loads(r.content)
    
    if pnr_json['ok'] == '1':
        ticket = extract_json_ticket_details(pnr_json)
        passengers = extract_json_passenger_details(pnr_json)
        return [ticket, passengers] # -> pnr_database
    else:
        print '\nPNR Not found, or it has not been generated!'
        return None
    
# list to store the pnr details
pnr_database = [] #[ticket_details{}, passenger_details{}]

# get_pnr_json module for irctc_main_json.py
def get_pnr_json():
    global pnr_database, pnr_number, t1, t2
    # UNCOMMENT
    pnr_number = raw_input('Enter the 10-digit PNR Number ')
    # TESTING
    #pnr_number = '6620398229'
    # call the function to get the pnr database list
    if len(pnr_number) == 10 and pnr_number.isdigit():
        t1 = time.time()
        pnr_database = get_pnr_database_json(pnr_number) #TODO: IMPLEMENT
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
        get_pnr_json()

# TEST CODE offline
if __name__ == '__main__':

    # FOR JSON
    file = open('pnrjson.json').read()
    json_data= json.loads(file)
    database = [extract_json_ticket_details(json_data), extract_json_passenger_details(json_data)]
    print 'SAMPLE OUTPUT\n'
    print_pnr_database(database)
