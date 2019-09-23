"""Calculates amortization table.

Given a principal, interest rate, and loan length it prints it out to the
screen or a CSV file.
"""

__author__ = "Eric Mesa"
__version__ = "v4.0"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2010-2019 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import csv
import sys
import numpy as np

USAGE = """
    Usage:
    python amortization.py -csv|screen -P # -i # -n #
    
    example with principle of $270,000, 4.44% interest, for 30 years:
    python amortization.py -csv -P 270000 -i .0444 -n 360
    
    -csv:     create a Comma Separated Values file to import into excel
    -screen:  print the amortization table to screen
    -P:       for # enter principal amount
    -i:       for # enter interest as a decimal
    -n:       for # enter number of months

    If you want to see the effect of extra monthly payments, create a file called extraprincipal and put the values in one after another one line at a time.  
    Ex:
    0
    200
    300
    0

    would be 0 extra principal the first month, 200 extra the second month, etc
    """

#helper functions
def getargs():
    """Grab the commandline arguments.

    Put them into a list and give help if no arguments provided.
    """
    args = sys.argv[1:]
    if len(args) < 7:
        sys.exit(USAGE)
    return args

def nopayamort(principal, interest, months):
    """Calculate total interest paid if no extra principal payments made."""
    per = np.arange(1*months)+1
    ipmt = np.ipmt(interest, per, 1*months, principal)
    total_interest = abs(np.sum(ipmt))
    return total_interest

def titles(principal, i, monthly_payment):
    """Print titles to screen or into CSV file."""
    print(f"Loan Amount: {principal}")
    print(f"Annual Interest: {i*12*100}")
    print(f"Payment: {monthly_payment:10.2f}")
    print("\t Payment \t Principal \t Interest \t Extra Principal  Balance")

def extraprincialdict(number_of_payments):
    """Read in the extra principal text file and return a dictionary with the values."""
    extra = []
    count = 0
    extraprincipal_file = open('extraprincipal', 'r')
    for line in extraprincipal_file:
        if "#" not in line:
            extra.append(line)
            count = count + 1
    extraprincipal_file.close()

    line = 0
    while line < number_of_payments-count:
        extra.append(0)
        line = line + 1

    dictkey = range(1, 361)

    dictitems = zip(dictkey, extra)

    return dict(dictitems)

def output(principal, i, number_of_payments, monthly_payment, destination):
    """Create the amortization table and outputs to CSV or screen."""
    csvfinal = []
    no_extra_total_interest = nopayamort(principal, i, number_of_payments)
    (total_principal, total_interest, total_payment) = (0, 0, 0)

    #generate titles
    if destination == "csv":
        csvfinal.append([None, "Payment", "Principal", "Interest",
                         "Extra Principal", "Balance"])
    elif destination == "screen":
        titles(principal, i, monthly_payment)

    #read in extra principal data
    principaldict = extraprincialdict(number_of_payments)

    period = 1

    #generate amortization table
    while period < number_of_payments+1:
        intpayment = (principal*i)
        extra_principal_this_period = float(principaldict[period])
        if period == number_of_payments:
            monthly_payment = principal + intpayment

        #this should handle finishing early because of extra interest payments
        if principal < monthly_payment:
            monthly_payment = principal + intpayment
            principal = principal - (monthly_payment - intpayment) - extra_principal_this_period
            if destination == "screen":
                print(f"{period:d} \t ${monthly_payment:,.2f}\
                    \t ${monthly_payment-intpayment:,.2f}\
                        \t ${intpayment:,.2f}\
                            \t ${extra_principal_this_period:,.2f}\
                                \t ${principal:,.2f}")
            elif destination == "csv":
                csvfinal.append([period, f"${monthly_payment:,.2f}",
                                 f"${monthly_payment-intpayment:,.2f}",
                                 f"${intpayment:,.2f}",
                                 f"${extra_principal_this_period:,.2f}",
                                 f"${principal:,.2f}"])
            #this should handle to totals being slightly off by amount of last payment
            total_principal = total_principal + (monthly_payment - intpayment)\
            + extra_principal_this_period
            total_interest = total_interest + intpayment
            total_payment = total_payment + monthly_payment + extra_principal_this_period
            break

        principal = principal - (monthly_payment - intpayment) - extra_principal_this_period

        if destination == "screen":
            print(f"{period:d} \t ${monthly_payment:,.2f}\
                \t ${monthly_payment-intpayment:,.2f}\
                    \t ${intpayment:,.2f}\
                        \t ${extra_principal_this_period:,.2f}\
                            \t ${principal:,.2f}")
        elif destination == "csv":
            csvfinal.append([period, f"${monthly_payment:,.2f}",
                             f"${monthly_payment-intpayment:,.2f}",
                             f"${intpayment:,.2f}",
                             f"${extra_principal_this_period:,.2f}",
                             f"${principal:,.2f}"])
        #total stuff
        total_principal = total_principal + (monthly_payment - intpayment)\
        + extra_principal_this_period
        total_interest = total_interest + intpayment
        total_payment = total_payment + monthly_payment + extra_principal_this_period

        period = period + 1

    #generate totals
    if destination == "screen":
        print(f"Totals \t ${total_payment:,.2f} \t ${total_principal:,.2f}\
            \t ${total_interest:,.2f}")
        print(f"Saved ${no_extra_total_interest-total_interest:,.2f} in interest payments")
    elif destination == "csv":
        csvfinal.append([None, f"${total_payment:,.2f}",
                         f"${total_principal:,.2f}", f"${total_interest:,.2f}"])
        csvfinal.append(["Saved", f"${no_extra_total_interest-total_interest:,.2f}",
                         "in interest", None])
        writer = csv.writer(open("amort.csv", "w"))
        writer.writerows(csvfinal)

def main():
    """Grab the arguments and run the program."""
    arguments = getargs()
    ##################setup variables#####################
    principal = int(arguments[2])
    i = float(arguments[4])/12
    number_of_payments = int(arguments[6])
    monthly_payment = (principal*i)/(1-pow((1+i), -number_of_payments))
    #####################################################

    if arguments[0] == '-csv':
        output(principal, i, number_of_payments, monthly_payment, "csv")
    elif arguments[0] == '-screen':
        output(principal, i, number_of_payments, monthly_payment, "screen")
    else:
        print(USAGE)

if __name__ == "__main__":
    main()
