from PyQt5.QtWidgets import QDialog, QApplication
import sys
from gui import *
import amortization

class AmortGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AmortGUI()
    w.show()
    sys.exit(app.exec_())
