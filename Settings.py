import json
from PyQt5.QtWidgets import QDialog, QFontDialog
from PyQt5.QtGui import QFont
from ui.Ui_Settings import Ui_Settings


class Settings(QDialog, Ui_Settings):
    def __init__(self, langs):
        QDialog.__init__(self)
        self.settings = self.load_settings()
        self.languages = list(map(lambda x: x[0] if isinstance(x, tuple) else x, langs))
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setLayout(self.main_layout)
        self.langs.addItems(self.languages)
        if self.settings["tabs"]:
            self.tabs.setChecked(True)
        else:
            self.spaces.setChecked(True)
        self.auto_2.setChecked(self.settings["auto_indent"])
        self.tab_width.setValue(self.settings["tab_width"])
        self.langs.setCurrentText(self.settings["lang"])

        self.font_button.clicked.connect(self.font_dialog)
        self.spaces.clicked.connect(self.set_space)
        self.tabs.clicked.connect(self.set_tabs)
        self.auto_2.stateChanged.connect(self.auto_changed)
        self.tab_width.valueChanged.connect(self.width_changed)
        self.langs.currentTextChanged.connect(self.lang_changed)

    def font_dialog(self):
        dialog = QFontDialog()
        font = QFont()
        font.fromString(self.settings["font"])
        dialog.setFont(font)
        font = dialog.getFont()
        if font[1]:
            self.settings["font"] = font[0].toString()
            self.save_settings()

    def set_space(self):
        self.settings["tabs"] = False
        self.save_settings()

    def set_tabs(self):
        self.settings["tabs"] = True
        self.save_settings()

    def auto_changed(self, state):
        self.settings["auto_indent"] = bool(state)
        self.save_settings()

    def width_changed(self, width):
        self.settings["tab_width"] = width
        self.save_settings()

    def lang_changed(self, lang):
        self.settings["lang"] = lang
        self.save_settings()

    def set_project(self, path):
        self.settings["project"] = path
        self.save_settings()

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
