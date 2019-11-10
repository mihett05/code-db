import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


excepthook = sys.excepthook


def except_hook(ex_type, ex_val, traceback):
    print(ex_type, ex_val, traceback)
    excepthook(ex_type, ex_val, traceback)
    sys.exit(1)


sys.excepthook = except_hook
app = QApplication(sys.argv)
main_window = MainWindow()
while True:
    try:
        main_window.show()
        break
    except BaseException:
        pass
sys.exit(app.exec_())
