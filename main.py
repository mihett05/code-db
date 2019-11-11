import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
# Handles all unhandled bugs (if such will be)
excepthook = sys.excepthook


def except_hook(ex_type, ex_val, traceback):
    global main_window
    main_window.show_error(f"Error: {ex_val}")


sys.excepthook = except_hook
while True:
    try:
        main_window.show()
        break
    except BaseException as e:
        main_window.show_error(str(e))
sys.exit(app.exec_())
