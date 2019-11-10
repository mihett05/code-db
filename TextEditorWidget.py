from PyQt5.QtGui import QFont
from PyQt5 import Qsci
from EditorWidget import EditorWidget


class Editor(Qsci.QsciScintilla):
    def __init__(self, settings, parent=None):
        self.settings = settings
        super().__init__(parent)
        self.setLexer(Qsci.QsciLexerPython(self))
        self.setUtf8(True)
        self.setAcceptDrops(True)
        self.setAutoCompletionThreshold(0)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setWrapMode(Qsci.QsciScintilla.WrapWord)
        self.setWrapIndentMode(Qsci.QsciScintilla.WrapIndentIndented)

        self.setIndentationGuides(True)
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(True)

        self.setMarginType(1, Qsci.QsciScintilla.NumberMargin)
        self.setMarginsFont(QFont("Times", 8))
        self.setFont(QFont("Times", 8))

        self.textChanged.connect(self.changed)

    def changed(self):
        self.autoCompleteFromAll()


class TextEditorWidget(EditorWidget):
    def __init__(self, settings, lang=None):
        EditorWidget.__init__(self, Editor(settings))
        self.lang = lang if lang is not None else settings.settings["lang"]
        self.name = None

    def change_language(self, name):
        if isinstance(name, tuple):
            self.lang = name[1]
            self.editor().setLexer(eval(f"Qsci.QsciLexer{name[0]}")(self))
        elif isinstance(name, str):
            self.lang = name
            self.editor().setLexer(eval(f"Qsci.QsciLexer{self.lang}")(self))
