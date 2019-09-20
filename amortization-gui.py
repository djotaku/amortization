from PyQt5.QtWidgets import QDialog, QApplication
import sys
from gui import *
import amortization

class AmortGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonCalculate.clicked.connect(self.calculate)
    def calculate(self):
        self.principal = int(self.ui.lineEditPrinciple.text())
        self.interest = float(self.ui.lineEditInterest.text())/12
        self.number_of_payments = int(self.ui.lineEditMonth.text())
        self.monthly_payment = (self.principal*self.interest)/(1-pow((1+self.interest), -self.number_of_payments))
        amortization.output(self.principal, self.interest, self.number_of_payments, self.monthly_payment, "csv")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AmortGUI()
    w.show()
    sys.exit(app.exec_())
