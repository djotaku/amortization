__author__ = "Eric Mesa"
__version__ = "v3.0"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2010-2019 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import csv
import sys

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

def getargs():
    """Grab the commandline arguments and put them into a list.  Also give help if no arguments provided."""
    args = []

    try:
        args = sys.argv[1:]
    except:
        print(USAGE)
    if len(args) < 7:
        sys.exit(USAGE)
    return args


def printtoscreen(P,i,n,MonthlyPayment,totalPrincipal,totalInterest,totalPayment):

    print(f"Loan Amount: {P}")
    print(f"Annual Interest: {i*12*100}")
    print(f"Payment: {MonthlyPayment:10.2f}")
    
    period = 1
    #generate titles
    print("\t Payment \t Principal \t Interest \t Extra Principal  Balance")

    #generate amortization table
    while period < n+1:
        intpayment = (P*i)
        if period == n:
            MonthlyPayment = P + intpayment

        

        #this should handle finishing early because of extra interest payments
        if P < MonthlyPayment:
            MonthlyPayment = P + intpayment
            P = P - (MonthlyPayment - intpayment) - float(principaldict[period])
            print(f"{period:d} \t {MonthlyPayment:10.2f} \t {MonthlyPayment-intpayment:10.2f} \t {intpayment:10.2f} \t {float(principaldict[period]):10.2f} \t {P:10.2f}")  
            #this should handle to totals being slightly off by amount of last payment
            totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
            totalInterest = totalInterest + intpayment
            totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])
            break

        P = P - (MonthlyPayment - intpayment) - float(principaldict[period])

        print(f"{period:d} \t {MonthlyPayment:10.2f} \t {MonthlyPayment-intpayment:10.2f} \t {intpayment:10.2f} \t {float(principaldict[period]):10.2f} \t {P:10.2f}") 
        
        #total stuff
        totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
        totalInterest = totalInterest + intpayment
        totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])
        
        period = period + 1

    #generate totals
    print(f"Totals \t {totalPayment:10.2f} \t {totalPrincipal:10.2f} \t {totalInterest:10.2f}")

def makecsv(P,i,n,MonthlyPayment,totalPrincipal,totalInterest,totalPayment):
    #create itereable
    csvfinal = []
    csvthisime = []
    period = 1
    
    #generate titles
    csvthistime = [None, "Payment","Principal","Interest","Extra Principal", "Balance"]
    csvfinal.append(csvthistime)
    
    #generate amortization table
    while period < n+1:
        intpayment = (P*i)
        if period == n:
            MonthlyPayment = P + intpayment

        #this should handle finishing early because of extra interest payments
        if P < MonthlyPayment:
            MonthlyPayment = P + intpayment
            P = P - (MonthlyPayment - intpayment) - float(principaldict[period])
            csvfinal.append([period, MonthlyPayment, MonthlyPayment-intpayment, intpayment, float(principaldict[period]),P])
            #this should handle to totals being slightly off by amount of last payment
            totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
            totalInterest = totalInterest + intpayment
            totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])
            break

        P = P - (MonthlyPayment - intpayment) - float(principaldict[period])

        csvfinal.append([period, MonthlyPayment, MonthlyPayment-intpayment, intpayment, float(principaldict[period]),P]) 

        #total stuff
        totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
        totalInterest = totalInterest + intpayment
        totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])

        period = period + 1
        
    #generate totals
    csvfinal.append([None,totalPayment, totalPrincipal, totalInterest]) #not correct in CSV, correct when printed on screen

    writer = csv.writer(open("amort.csv", "wb"))
    writer.writerows(csvfinal)


arguments = getargs()
##################setup variables#####################
P=int(arguments[2])
i=float(arguments[4])/12
n=int(arguments[6])
MonthlyPayment = (P*i)/(1-pow((1+i),-n))
(totalPrincipal,totalInterest,totalPayment) = (0,0,0)
#####################################################


##read in the extra principal amounts###
extra = []
count = 0
f = open('extraprincipal','r')
for line in f:
    if "#" not in line:
        extra.append(line)
        count = count + 1
f.close()

for number in range(0,n-count):
    extra.append(0)

dictkey = range(1,361)

dictitems = zip(dictkey,extra)

principaldict = dict(dictitems)
####################################

if arguments[0] == '-csv':
    makecsv(P,i,n,MonthlyPayment,totalPrincipal,totalInterest,totalPayment)
elif arguments[0] == '-screen':
    printtoscreen(P,i,n,MonthlyPayment,totalPrincipal,totalInterest,totalPayment)
else:
    print(USAGE)
