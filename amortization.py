"""Calculates amortization table.

Given a principal, interest rate, and loan length it prints it out to the
screen or a CSV file.
"""

__author__ = "Eric Mesa"
__version__ = "v6.0"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2010-2022 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import argparse
import csv
from decimal import *

import numpy_financial as npf
import numpy as np

from rich.console import Console
from rich.table import Table

epilogue = """
    If you want to see the effect of extra monthly payments:\n
    -create a file called extraprincipal\n
    -put the values in one after another one line at a time.\n

    Ex:\n
    0\n
    200\n
    300\n
    0\n
\n
    would be 0 extra principal the first month, 200 extra the second month,etc
    """


def get_args():
    """ Grab the commandline arguments."""
    parser = argparse.ArgumentParser(epilog=epilogue)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--csv", action='store_true',
                       help="create a Comma Separated Values file to import into excel")
    group.add_argument('-s', '--screen', action='store_true', help="print the amortization table to the screen")
    parser.add_argument("-P", '--principal', required=True, help='enter the amount of the principal (no dollar sign')
    parser.add_argument('-i', '--interest', required=True,
                        help='enter interest as a decimal. eg: 4.44 percent interest would be 0.0444')
    parser.add_argument('-m', '--months', required=True, help='enter number of months in the loan')
    return parser.parse_args()


def nopayamort(principal: Decimal, interest: Decimal, months: Decimal) -> float:
    """Calculate total interest paid if no extra principal payments made."""
    per = np.arange(1 * months) + 1
    ipmt = npf.ipmt(interest, per, 1 * months, principal)
    return abs(np.sum(ipmt))


def titles(principal: Decimal, i: Decimal, monthly_payment: Decimal):
    """Print titles to screen or into CSV file."""
    print(f"Loan Amount: {principal}")
    print(f"Annual Interest: {i * 12 * 100}")
    print(f"Payment: {monthly_payment:10.2f}")


def extraprincialdict(number_of_payments: Decimal) -> dict:
    """Read in the extra principal text file and return a dictionary with the values."""
    extra = []
    count = 0
    with open('extraprincipal', 'r') as extraprincipal_file:
        for line in extraprincipal_file:
            if "#" not in line:
                extra.append(line)
                count = count + 1
    line = 0
    while line < number_of_payments - count:
        extra.append(0)
        line += 1

    dictkey = range(1, 361)

    dictitems = zip(dictkey, extra)

    return dict(dictitems)


def output(principal: Decimal, i: Decimal, number_of_payments: Decimal, monthly_payment: Decimal, destination: str):
    """Create the amortization table and outputs to CSV or screen."""
    csv_final = []
    no_extra_total_interest = nopayamort(principal, i, number_of_payments)
    (total_principal, total_interest, total_payment) = (0, 0, 0)

    # generate titles
    if destination == "csv":
        csv_final.append([None, "Payment", "Principal", "Interest",
                         "Extra Principal", "Balance"])
    elif destination == "screen":
        titles(principal, i, monthly_payment)

    table = Table(title="Loan Amortization Table")
    table.add_column("Month")
    table.add_column("Total Payment")
    table.add_column("Principal")
    table.add_column("Interest")
    table.add_column("Extra Principal Paid")
    table.add_column("Remaining Loan Balance")
    # read in extra principal data
    principaldict = extraprincialdict(number_of_payments)

    period = 1

    # generate amortization table
    while period < number_of_payments + 1:
        interest_payment = (principal * i)
        extra_principal_this_period = Decimal(principaldict[period])
        if period == number_of_payments:
            monthly_payment = principal + interest_payment

        # this should handle finishing early because of extra interest payments
        if principal < monthly_payment:
            monthly_payment = principal + interest_payment
            principal = principal - (monthly_payment - interest_payment) - extra_principal_this_period
            if destination == "screen":
                table.add_row(f"{period:d}", f"${monthly_payment:,.2f}", f"${monthly_payment - interest_payment:,.2f}",
                              f"${interest_payment:,.2f}", f"${extra_principal_this_period:,.2f}", f"${principal:,.2f}")
            elif destination == "csv":
                csv_final.append([period, monthly_payment,
                                 (monthly_payment - interest_payment).quantize(Decimal('.01')),
                                 interest_payment.quantize(Decimal('.01')),
                                 extra_principal_this_period.quantize(Decimal('.01')),
                                 principal])
            # this should handle to totals being slightly off by amount of last payment
            total_principal = total_principal + (monthly_payment - interest_payment) + extra_principal_this_period
            total_interest = total_interest + interest_payment
            total_payment = total_payment + monthly_payment + extra_principal_this_period
            break

        principal = principal - (monthly_payment - interest_payment) - extra_principal_this_period

        if destination == "screen":
            table.add_row(f"{period:d}", f"${monthly_payment:,.2f}", f"${monthly_payment - interest_payment:,.2f}",
                          f"${interest_payment:,.2f}", f"${extra_principal_this_period:,.2f}", f"${principal:,.2f}")
        elif destination == "csv":
            csv_final.append([period, monthly_payment,
                             (monthly_payment - interest_payment).quantize(Decimal('.01')),
                             interest_payment.quantize(Decimal('.01')),
                             extra_principal_this_period.quantize(Decimal('.01')),
                             principal])
        # total stuff
        total_principal = total_principal + (monthly_payment - interest_payment) + extra_principal_this_period
        total_interest = total_interest + interest_payment
        total_payment = total_payment + monthly_payment + extra_principal_this_period

        period += 1

    # generate totals
    if destination == "screen":
        table.add_row("Totals", f"${total_payment:,.2f}", f"${total_principal:,.2f}", f"${total_interest:,.2f}" )
        console = Console()
        console.print(table)
        print(f"Saved ${no_extra_total_interest - total_interest:,.2f} in interest payments")
    elif destination == "csv":
        csv_final.extend(([None, f"${total_payment:,.2f}", f"${total_principal:,.2f}", f"${total_interest:,.2f}"],
                          ["Saved", f"${no_extra_total_interest - total_interest:,.2f}", "in interest", None]))

        writer = csv.writer(open("amort.csv", "w"))
        writer.writerows(csv_final)


def main():
    """Grab the arguments and run the program."""
    getcontext().prec = 28
    arguments = get_args()
    # #################setup variables#####################
    principal = Decimal(arguments.principal)
    i = Decimal(arguments.interest) / Decimal(12)
    number_of_payments = Decimal(arguments.months)
    monthly_payment = (principal * i) / (Decimal(1) - pow((Decimal(1) + i), -number_of_payments))
    # ####################################################

    if arguments.csv:
        output(principal, i, number_of_payments, monthly_payment, "csv")
    elif arguments.screen:
        output(principal, i, number_of_payments, monthly_payment, "screen")


if __name__ == "__main__":
    main()
