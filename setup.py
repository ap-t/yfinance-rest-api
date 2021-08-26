#!/usr/bin/python

import yfinancerestapi.finance.stocks.services as stocks_services
import sys, getopt

# Init stocks collections
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h",["help", "rebuild", "run_analysis", "reset_analysis"])
    except getopt.GetoptError:
        print('setup.py --rebuild --run_analysis --reset_analysis')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('setup.py --rebuild --run_analysis --reset_analysis')
            sys.exit()
        elif opt == "--rebuild":
            stocks_services.rebuild_collection()
        elif opt == "--run_analysis":
            stocks_services.run_analysis()
        elif opt == "--reset_analysis":
            stocks_services.reset_analysis()


if __name__ == "__main__":
    main(sys.argv[1:])