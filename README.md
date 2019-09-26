# Amortization

[![Actions Status](https://github.com/djotaku/amortization/workflows/Lint_Test/badge.svg)](https://github.com/djotaku/amortization/actions)

Amortization Program for creating a table of payments

This is an amortization table for home mortgages, but it should work for anything else that follows that type of math - say a car loan.

## Commandline
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

## GUI

Runs on QT. Install those libraries via pip (especially if you run on Windows) or your package manager (on Linux).

Run amortization-gui.py

After entering data into the fields, hit calculate. It will print the data into the field below in a spreadsheet-like view. It will also create a CSV file called amort.csv. You can import this into any program that can take in CSV files. If you import it into a spreadsheet program you can then create a PDF (or anything else you'd do with a spreadsheet.
