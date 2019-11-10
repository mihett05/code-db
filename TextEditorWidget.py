from PyQt5.QtGui import QFont
from PyQt5 import Qsci
from EditorWidget import EditorWidget


class Editor(Qsci.QsciScintilla):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings.settings
        self.setUtf8(True)
        self.setAcceptDrops(True)
        self.setAutoCompletionThreshold(0)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setWrapMode(Qsci.QsciScintilla.WrapWord)
        self.setWrapIndentMode(Qsci.QsciScintilla.WrapIndentIndented)

        self.setIndentationGuides(True)
        self.setAutoIndent(self.settings["auto_indent"])
        self.setTabWidth(self.settings["tab_width"])
        self.setIndentationsUseTabs(self.settings["tabs"])

        self.setMarginType(1, Qsci.QsciScintilla.NumberMargin)

        font = QFont()
        font.fromString(self.settings["font"])

        self.setMarginsFont(font)
        self.setFont(font)

        self.textChanged.connect(self.changed)

    def changed(self):
        self.autoCompleteFromAll()


class TextEditorWidget(EditorWidget):
    def __init__(self, settings, lang=None):
        EditorWidget.__init__(self, Editor(settings))
        self.lang = lang if lang is not None else settings.settings["lang"]
        self.editor().setLexer(eval(f"Qsci.QsciLexer{self.lang}")(self))
        self.name = None

    def change_language(self, name):
        if isinstance(name, tuple):
            self.lang = name[1]
            self.editor().setLexer(eval(f"Qsci.QsciLexer{name[0]}")(self))
        elif isinstance(name, str):
            self.lang = name
            self.editor().setLexer(eval(f"Qsci.QsciLexer{self.lang}")(self))
