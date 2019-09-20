import sys
import csv
from PyQt5.QtWidgets import QDialog, QApplication
from gui import *
import amortization

class AmortGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonCalculate.clicked.connect(self.calculate)
        self.model = QtGui.QStandardItemModel(self)
        self.ui.tableViewCSV.setModel(self.model)
    def calculate(self):
        self.principal = int(self.ui.lineEditPrinciple.text())
        self.interest = float(self.ui.lineEditInterest.text())/12
        self.number_of_payments = int(self.ui.lineEditMonth.text())
        self.monthly_payment = (self.principal*self.interest)/(1-pow((1+self.interest), -self.number_of_payments))
        amortization.output(self.principal, self.interest, self.number_of_payments, self.monthly_payment, "csv")
        with open("amort.csv","r") as csvinput:
            for row in csv.reader(csvinput):
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AmortGUI()
    w.show()
    sys.exit(app.exec_())
