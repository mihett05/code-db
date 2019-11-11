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
        """
        Method sets UI
        :return: None
        """
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
        """
        Method changes font in settings
        :return: None
        """
        dialog = QFontDialog()
        font = QFont()
        font.fromString(self.settings["font"])
        dialog.setFont(font)
        font = dialog.getFont()
        if font[1]:
            self.settings["font"] = font[0].toString()
            self.save_settings()

    def set_space(self):
        """
        Method sets using tabs in settings
        :return: None
        """
        self.settings["tabs"] = False
        self.save_settings()

    def set_tabs(self):
        """
        Method sets using tabs in settings
        :return: None
        """
        self.settings["tabs"] = True
        self.save_settings()

    def auto_changed(self, state):
        """
        Method changes auto indent in settings
        :param state: use auto indent?
        :return: None
        """
        self.settings["auto_indent"] = bool(state)
        self.save_settings()

    def width_changed(self, width):
        """
        Method changes width of tab in settings
        :param width: width of tab
        :return: None
        """
        self.settings["tab_width"] = width
        self.save_settings()

    def lang_changed(self, lang):
        """
        Method changes default lang in settings
        :param lang: default lang
        :return: None
        """
        self.settings["lang"] = lang
        self.save_settings()

    def set_project(self, path):
        """
        Method changes project in settings
        :param path: project directory
        :return: None
        """
        self.settings["project"] = path
        self.save_settings()

    @staticmethod
    def load_settings():
        """
        Method load settings from if it exists else generate default
        :return: settings
        """
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
        """
        Setter for Settings.settings
        :param key: key in Settings.settings
        :param value: new value
        :return: None
        """
        self.settings[key] = value

    def get_setting(self, key):
        """
        Getter for Settings.settings
        :param key: key in Settings.settings
        :return: None
        """
        return self.settings[key]

    def save_settings(self):
        """
        Method saves settings in settings.json in local directory with programm
        :return: None
        """
        with open("settings.json", "w") as w:
            w.write(json.dumps(self.settings))
