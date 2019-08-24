__author__ = "Eric Mesa"
__version__ = "v2.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2010 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import csv,sys

def getargs():
    """Grab the commandline arguments and put them into a list.  Also give help if no arguments provided"""
    args = []

    try:
        args = sys.argv[1:]
    except:
        print """
    Usage:
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
    if len(args) < 7:
        sys.exit("""
    Usage:
    amortization.py -csv|screen -P # -i # -n #

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
    """)
    return args


def printtoscreen(P,i,n,MonthlyPayment,totalPrincipal,totalInterest,totalPayment):

    print "Loan Amount:", P
    print "Annual Interest:",  i*12*100
    print "Payment: %10.2f\n" % MonthlyPayment
    
    period = 1
    #generate titles
    print "\t Payment \t Principal \t Interest \t Extra Principal  Balance"

    #generate amortization table
    while period < n+1:
        intpayment = (P*i)
        if period == n:
            MonthlyPayment = P + intpayment

        

        #this should handle finishing early because of extra interest payments
        if P < MonthlyPayment:
            MonthlyPayment = P + intpayment
            P = P - (MonthlyPayment - intpayment) - float(principaldict[period])
            print "%d \t %10.2f \t %10.2f \t %10.2f \t %10.2f \t %10.2f"% (period, MonthlyPayment, MonthlyPayment-intpayment, intpayment, float(principaldict[period]),P)
            break

        P = P - (MonthlyPayment - intpayment) - float(principaldict[period])

        print "%d \t %10.2f \t %10.2f \t %10.2f \t %10.2f \t %10.2f"% (period, MonthlyPayment, MonthlyPayment-intpayment, intpayment, float(principaldict[period]),P) 
        
        #total stuff
        totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
        totalInterest = totalInterest + intpayment
        totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])
        
        period = period + 1

    #generate totals
    print "Totals \t %10.2f \t %10.2f \t %10.2f" % (totalPayment, totalPrincipal, totalInterest)

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
            break

        P = P - (MonthlyPayment - intpayment) - float(principaldict[period])

        csvfinal.append([period, MonthlyPayment, MonthlyPayment-intpayment, intpayment, float(principaldict[period]),P]) 
        period = period + 1

        #total stuff
        totalPrincipal = totalPrincipal + (MonthlyPayment - intpayment) + float(principaldict[period])
        totalInterest = totalInterest + intpayment
        totalPayment = totalPayment + MonthlyPayment + float(principaldict[period])

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
    print """
    Usage:
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
