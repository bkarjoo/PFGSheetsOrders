import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from HydraOrderFactory import HydraOrderFactory
from HydraQuoteManager import HydraQuoteManager
from HydraOrderManager import HydraOrderManager
import sys
import threading
from observer import *

# initialize interactive connection with command line arguments (port numbers for HAPIServer)
args = sys.argv[1:]
es_port = int(args[0])
is_port = int(args[1])
print es_port, is_port
qm = HydraQuoteManager(is_port)
em = HydraOrderManager(es_port)
from Positions import Positions

class Interactive(object):

    def __init__(self):
        pass






# how to get the sheet using client_secret.json file
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open('PFGOrders').sheet1

# a better way to print
pp = pprint.PrettyPrinter()

# order factory
order_factory = HydraOrderFactory()

# order dictionaries
open_orders = {}
open_orders_lock = threading.Lock()
closed_orders = {}
closed_orders_lock = threading.Lock()
positions = Positions()


class OrderStatusObserver(Observer):
    def __init__(self, outer):
        self.outer = outer
        self.orderStatusObserver = OrderStatusObserver(self)

    def update(self, arg):
        self.outer.on_order_status(arg)

class Orchestrator(object):
    pass


def submit_order(order):
    # add order to open orders
    with open_orders_lock:
        open_orders[order.parent_id] = order

    # subscribe to the order status


    # set a submit flag

    # submit the order
    em.send_order(order)

def flag_row(row_num):
    if row_num > 1 and row_num <= sheet.row_count:
        sheet.update_cell(row_num,10,'@')

def submit_row(cells):
    pp.pprint(cells)

    account = cells[0]
    quantity = cells[1]
    symbol = cells[2]
    limit_price = cells[3]
    type = cells[4]
    route = cells[5]
    vwap_start_time = cells[6]
    vwap_end_time = cells[7]
    stop_price = cells[8]
    submit_flag = cells[9]
    if route == 'CSFB':
        if type == 'MOO':
            o = order_factory.generate_opg_market_order(quantity,symbol,account)
            print o
        elif type == 'MOC':
            o = order_factory.generate_moc_market_order(quantity,symbol,account)
            print o
        elif type == 'LOO':
            o = order_factory.generate_opg_limit_order(quantity,symbol,limit_price,account)
            print o
        elif type == 'LOC':
            o = order_factory.generate_loc_limit_order(quantity,symbol,limit_price,account)
            print o
        elif type == 'CROSSFINDER':
            o = order_factory.generate_limit_order(quantity,symbol,limit_price,account)
            print o
        elif type == 'SLMT':
            o = order_factory.generate_stop_limit_order(quantity,symbol,stop_price,limit_price,account)
            print o
        elif type == 'SMKT':
            o = order_factory.generate_stop_market_order(quantity,symbol,stop_price,account)
            print o
        else:
            print 'Type {} for {} route not implemented'.format(type, route)
    elif route == 'NITE':
        if type == 'LMT':
            o = order_factory.generate_limit_nite_order(quantity,symbol,limit_price,account)
            print o
        elif type == 'VWAP':
            o = order_factory.generate_nite_vwap_order(quantity,symbol,vwap_start_time,vwap_end_time,stop_price,account)
            print o
        else:
            print 'Type {} for {} route not implemented'.format(type, route)

while (True):
    input = raw_input('interactive>')
    try:
        if input.upper() == 'Q' or input.upper() == 'QUIT':
            break
        elif input.upper() == 'PRINT SHEET':
            pp.pprint(sheet.get_all_records())
        elif input.upper()[:9] == 'PRINT ROW':
            param = input.split(' ')[2]
            pp.pprint(sheet.row_values(param))
        elif input.upper() == 'ROW COUNT':
            print sheet.row_count
        elif input.upper()[:8] == 'FLAG ROW':
            flag_row(int(input.split(' ')[2]))
        elif input.upper()[:10] == 'SUBMIT ROW':
            row = int(input.split(' ')[2])
            if row < 2 or row > sheet.row_count:
                print 'Invalid row.'
            else:
                cells = sheet.row_values(row)
                submit_row(cells)

        # create a way to enter all orders
        # test submitting all orders
        # see if you can get fny labs in there as well
        # send order method
        # cancel order method
        # get order status
        # execution price goes on sheet


    except Exception as e:
        print e

qm.close_socket()
em.close_socket()

i = Interactive()
i.print_pars()

print 'done'