#!/usr/bin/python

import yfinancerestapi.finance.stocks.services as stocks_services
import sys, getopt

# Init stocks collections
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h",["help", "build", "run_analysis", "unset_analysis"])
    except getopt.GetoptError:
        print('setup.py --build --run_analysis --unset_analysis')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('setup.py --build --run_analysis --unset_analysis')
            sys.exit()
        elif opt == "--build":
            stocks_services.build_collection()
        elif opt == "--run_analysis":
            stocks_services.run_analysis()
        elif opt == "--unset_analysis":
            stocks_services.unset_analysis()


if __name__ == "__main__":
    main(sys.argv[1:])