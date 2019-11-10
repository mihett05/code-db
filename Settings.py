import json
from PyQt5.QtWidgets import QDialog, QFontDialog
from PyQt5.QtGui import QFont
from ui.Ui_Settings import Ui_Settings


class Settings(QDialog, Ui_Settings):
    def __init__(self):
        QDialog.__init__(self)
        self.settings = self.load_settings()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setLayout(self.main_layout)
        self.font_button.clicked.connect(self.font_dialog)

    def font_dialog(self):
        dialog = QFontDialog()
        font = QFont()
        font.fromString(self.settings["font"])
        dialog.setFont(font)
        font = dialog.getFont()
        if font[1]:
            self.settings["font"] = font[0].toString()

    @staticmethod
    def load_settings():
        try:
            with open("settings.json", "r") as r:
                return json.loads(r.read())
        except FileNotFoundError:
            return {
                "project_path": None,
                "auto_indent": True,
                "tab_width": 4,
                "tabs": True,
                "font": QFont("Times", 8).toString(),
                "lang": "Python"
            }

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings[key]

    def save_settings(self):
        with open("settings.json", "w") as w:
            w.write(json.dumps(self.settings))
