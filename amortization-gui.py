import sys
import csv
from PyQt5.QtWidgets import QDialog, QApplication
from gui import *
import amortization


class AmortizationGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonCalculate.clicked.connect(self.calculate)
        self.model = QtGui.QStandardItemModel(self)
        self.ui.tableViewCSV.setModel(self.model)

    def calculate(self):
        principal = int(self.ui.lineEditPrinciple.text())
        interest = amortization.Decimal(self.ui.lineEditInterest.text())/12
        number_of_payments = int(self.ui.lineEditMonth.text())
        monthly_payment = (principal*interest)/(1-pow((1+interest), - number_of_payments))
        amortization.output(principal, interest, number_of_payments, monthly_payment, "csv")
        with open("amort.csv", "r") as csv_input:
            for row in csv.reader(csv_input):
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AmortizationGUI()
    w.show()
    sys.exit(app.exec_())
