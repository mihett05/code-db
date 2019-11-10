from PyQt5.QtWidgets import QWidget, QGridLayout


class EditorWidget(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self)
        self.main_layout: QGridLayout

        self._editor = editor
        self.main_layout = None
        self.setupUI()

    def setupUI(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.editor())

    def editor(self):
        return self._editor





