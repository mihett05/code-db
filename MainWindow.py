import os
import sqlite3
import contextlib
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel, QSizePolicy, QTreeWidgetItem, QTableWidgetItem,\
    QInputDialog, QLineEdit
from watchdog.observers import Observer
from ui.Ui_MainWindow import Ui_MainWindow
from TextEditorWidget import TextEditorWidget
from TableEditorWidget import TableEditorWidget
from Project import Project, Handler
from Settings import Settings


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.languages = sorted([
            "AVS", "Batch", "CoffeeScript", ("CSharp", "C#"), "Java", "CSS", "Diff", "JSON", "Makefile", "Matlab",
            "Pascal", "Python", "Spice", "TCL", "Verilog", "YAML", "Bash", "CMake", ("CPP", "C++"), "IDL",
            "JavaScript", "D", "Fortran", "Markdown", "Octave", "Perl", "PostScript", "Ruby", "SQL",
            "TeX", "VHDL"
        ], key=lambda x: x[1] if isinstance(x, tuple) else x)
        self.settings = Settings(self.languages)
        self.statusbar_lang = QLabel(self.settings.settings["lang"])
        self.project = None
        self.observer = None

        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """
        Setting UI
        :return: None
        """
        self.setWindowTitle("CodeDB")
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.main_layout)
        self.new_file_trigger()
        self.tabs.setTabsClosable(True)
        for language in self.languages:
            if isinstance(language, tuple):
                action = QAction(language[1], self)
                action.triggered.connect(self.generate_lang_action_trigger(language))
            else:
                action = QAction(language, self)
                action.triggered.connect(self.generate_lang_action_trigger(language))
            self.menuSwitch_language.addAction(action)

        self.project = Project(self.dirs_widget, self.files_widget)

        self.dirs_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.files_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.tabs.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.tables.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.table_columns.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.project.hide()
        self.db_layout_hide()

        self.statusbar.addPermanentWidget(self.statusbar_lang)
        self.settings_action.triggered.connect(self.settings_open)

        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.changed_tab)

        self.project_close.triggered.connect(self.project_close_trigger)
        self.project_open.triggered.connect(self.project_open_trigger)

        self.project_hide.triggered.connect(self.project.hide)
        self.project_show.triggered.connect(self.project.show)

        self.save_file.triggered.connect(self.save_file_trigger)
        self.save_as_file.triggered.connect(self.save_as_file_trigger)
        self.new_file.triggered.connect(self.new_file_trigger)
        self.open_file.triggered.connect(self.open_file_dialog_trigger)

        self.tables.setHeaderLabel("Tables")
        self.tables.currentItemChanged.connect(self.table_changed)

        self.files_widget.itemClicked.connect(self.open_file_project_trigger)
        self.dirs_widget.doubleClicked.connect(self.change_project_dir)

        self.new_db.triggered.connect(self.new_db_trigger)

        self.db_create.triggered.connect(self.create_table)
        self.db_remove.triggered.connect(self.remove_table)
        self.db_rename.triggered.connect(self.rename_table)
        self.db_add_row.triggered.connect(self.add_row)
        self.db_del_row.triggered.connect(self.remove_row)

        self.open_project(self.settings.settings["project_path"])

    def generate_lang_action_trigger(self, name):
        """
        Generating Method for QActions in Switch Menu for languages
        :param name: Name of language(str or tuple)
        :return: trigger Method for QAction
        """
        def trigger():
            nonlocal name, self
            widget = self.tabs.currentWidget()
            if isinstance(widget, TextEditorWidget):
                if isinstance(name, tuple):
                    widget.change_language(name)
                    self.statusbar_lang.setText(name[1])
                elif isinstance(name, str):
                    widget.change_language(name)
                    self.statusbar_lang.setText(name)
        return trigger

    def close_tab(self, index):
        """
        Method for handling closing tab event
        :param index: index of tab that will be closed
        :return: None
        """
        widget = self.tabs.widget(index)
        if isinstance(widget, TableEditorWidget):
            widget.close_con()
        if not isinstance(self.tabs.widget(index - 1), TableEditorWidget):
            self.db_layout_hide()
        self.tabs.removeTab(index)

    def changed_tab(self, index):
        """
        Method for handling changing tab event
        :param index: index of new tab
        :return: None
        """
        if isinstance(self.tabs.widget(index), TextEditorWidget):
            self.statusbar_lang.setText(self.tabs.widget(index).lang)
            self.db_layout_hide()
        elif isinstance(self.tabs.widget(index), TableEditorWidget):
            self.show_db_others()

    def save_file_trigger(self):
        """
        Save Method for QAction of File Menu
        :return: None
        """
        widget = self.tabs.currentWidget()
        index = self.tabs.currentIndex()
        if isinstance(widget, TextEditorWidget):
            if widget.name is None:  # Save As if None
                name = self.save_as_file_trigger()
                if not name == "":
                    widget.name = name
                    self.tabs.setTabText(index, os.path.basename(widget.name))
            else:  # Save
                with open(widget.name, "w") as w:
                    w.write(widget.editor().text())
        elif isinstance(widget, TableEditorWidget):
            if widget.path is not None:
                widget.apply_changes()
            else:
                name = self.save_as_file_trigger()
                widget.path = name
                self.tabs.setTabText(index, os.path.basename(name))

    def save_as_file_trigger(self):
        """
        Open "Save as" dialog
        :return: filename from dialog
        """
        widget = self.tabs.currentWidget()
        name = QFileDialog.getSaveFileName(self, "Save as", '')[0]
        try:
            if isinstance(widget, TextEditorWidget):
                with open(name, "w") as w:
                    w.writelines(widget.editor().text().split("\n"))
            elif isinstance(widget, TableEditorWidget):
                with open(name, "w"):
                    pass
                con = sqlite3.connect(name)
                if widget.con is not None:
                    widget.con.commit()
                    for query in widget.con.iterdump():
                        try:
                            con.execute(query)
                        except sqlite3.OperationalError:
                            self.statusbar.showMessage("Some technical sweets", 20000)
                    con.commit()
                    widget.con = con
        except FileNotFoundError:
            pass
        return name

    def new_file_trigger(self):
        """
        Creating new tab
        :return: None
        """
        self.tabs.addTab(TextEditorWidget(self.settings), "New File")

    def new_db_trigger(self):
        """
        Createing new datebase with table "new_table"
        :return: None
        """
        editor = TableEditorWidget(self.render_active_table)
        editor.con = sqlite3.connect(":memory:")
        with contextlib.closing(editor.con.cursor()) as cur:
            cur.execute("""
                CREATE TABLE new_table (
                    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    `name` varchar(255) NOT NULL
                );
            """)
            self.render_tables_names(editor)
            if isinstance(self.tabs.currentWidget(), QTableWidgetItem):
                self.show_db_others()
        self.tabs.addTab(editor, "New db")

    def file_open(self, name):
        """
        Open file with param name
        :param name: name of the file
        :return: None
        """
        try:
            if name.endswith(".db"):
                editor = TableEditorWidget(self.render_active_table)
                editor.con = sqlite3.connect(name)
                editor.path = name
                self.render_tables_names(editor)
                if isinstance(self.tabs.currentWidget(), QTableWidgetItem):
                    self.show_db_others()
                self.tabs.addTab(editor, os.path.basename(name))
            else:
                with open(name, "r") as r:
                    editor = TextEditorWidget(self.settings)
                    editor.editor().setText(r.read())
                    self.tabs.addTab(editor, os.path.basename(name))
                    editor.name = name
        except FileNotFoundError:
            self.statusbar.showMessage("File not found", 10000)
        except UnicodeDecodeError:
            try:
                with open(name, "rb") as r:
                    editor = TextEditorWidget(self.settings)
                    editor.editor().setText(r.read().decode("utf-8"))

            except UnicodeDecodeError:
                self.statusbar.showMessage("Can't read binary file", 10000)
            else:
                self.tabs.addTab(editor, os.path.basename(name))
        except PermissionError:
            self.statusbar.showMessage(f"Can't open {os.path.basename(name)}: Permission denied", 10000)

    def open_file_dialog_trigger(self):
        """
        Open file Method for QAction in File Menu
        :return: None
        """
        self.file_open(QFileDialog.getOpenFileName(self, "Open", '')[0])

    def open_file_project_trigger(self, item):
        """
        Open file Method for file tree in project
        :return: None
        """
        if item is not None and self.settings.get_setting("project_path") is not None:
            self.file_open(os.path.join(self.settings.get_setting("project_path"), item.text(0)))

    def change_project_dir(self, index):
        """
        Method for changing project directory from directories' tree widget
        :param index:
        :return: None
        """
        if index is not None and self.settings.get_setting("project_path") is not None:
            self.open_project(os.path.join(self.settings.get_setting("project_path"),
                                           self.dirs_widget.itemFromIndex(index).text(0)))

    def settings_open(self):
        """
        Method opens settings' dialog
        :return: None
        """
        self.settings.exec_()

    def project_open_trigger(self):
        """
        Open project from directory dialog
        :return: None
        """
        self.open_project(QFileDialog.getExistingDirectory(self, "Open project", ''))

    def open_project(self, path):
        """
        Method for opening project
        :param path: full path to project
        :return: None
        """
        if path != "":
            self.settings.set_setting("project_path", path)
            if isinstance(self.observer, Observer):
                self.observer.stop()
            if self.settings.get_setting("project_path") is not None:
                self.project.open(self.settings.get_setting("project_path"))
                self.observer = Observer()
                self.observer.schedule(Handler(self.project),
                                       path=self.settings.get_setting("project_path"), recursive=True)
                self.observer.start()

    def project_close_trigger(self):
        """
        Method for closing project
        :return: None
        """
        self.project.hide()
        self.settings.set_setting("project_path", None)
        self.project.clear()
        if self.observer is not None:
            self.observer.stop()

    def db_layout_hide(self):
        """
        Method hides elements from self.db_layout
        :return: None
        """
        self.table_columns.hide()
        self.tables.hide()

    def db_layout_show(self):
        """
        Method shows elements from self.db_layout
        :return: None
        """
        self.table_columns.show()
        self.tables.show()

    def table_changed(self, item: QTreeWidgetItem):
        """
        Method shows data from selected table
        :param item: selected item from QTreeWidget
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget):
            with contextlib.closing(widget.con.cursor()) as cur:
                if self.tables.indexFromItem(item).data() is not None:
                    widget._active_table = self.tables.indexFromItem(item).data()
                    widget._columns[widget.active_table()] = list()
                    try:
                        cur.execute(f"SELECT * FROM {widget._active_table}")
                        res = cur.fetchall()
                        with widget as table:
                            columns = list(map(lambda x: x[0], cur.description))
                            table.setColumnCount(len(columns))
                            table.setHorizontalHeaderLabels(columns)
                            widget._columns[widget.active_table()] = columns.copy()
                            table.setRowCount(len(res))
                            for i, row in enumerate(res):
                                for j, cell in enumerate(row):
                                    table.setItem(i, j, QTableWidgetItem(str(cell)))
                    except sqlite3.Error:
                        pass

    def show_table_list(self):
        """
        Method sets table_list to tables from current tab
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget):
            self.tables.clear()
            if widget.table_names is not None:
                self.tables.addTopLevelItems(map(lambda x: QTreeWidgetItem([x]), widget.table_names))

    def show_db_others(self):
        """
        Method shows special db preferences
        :return: None
        """
        self.db_layout_show()
        self.show_table_list()
        self.statusbar_lang.setText("DateBase")

    def render_tables_names(self, editor: TableEditorWidget):
        """
        Method updates list of table from date base
        :param editor: TableEditorWidget where from will be taken tables' names
        :return: None
        """
        if editor.con is not None:
            with contextlib.closing(editor.con.cursor()) as cur:
                editor.table_names = list(map(lambda x: x[0],
                                              cur.execute("SELECT name FROM 'sqlite_master' WHERE type = 'table'")
                                              .fetchall()))
                if "sqlite_sequence" in editor.table_names:
                    editor.table_names.remove("sqlite_sequence")
                self.tables.clear()
                self.tables.addTopLevelItems(map(lambda x: QTreeWidgetItem([str(x)]), editor.table_names))

    def create_table(self):
        """
        Method creates table from dialog's query
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget) and isinstance(widget.con, sqlite3.Connection):
            with contextlib.closing(widget.con.cursor()) as cur:
                text, ok = QInputDialog.getMultiLineText(self, "Creating table", "Enter query", """
                CREATE TABLE new_table (
                    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    `name` varchar(255) NOT NULL
                );
                """.strip().replace("                ", ""))
                if ok and text:
                    try:
                        cur.execute(text)
                    except sqlite3.OperationalError as e:
                        self.statusbar.showMessage(str(e), 15000)
                    self.render_tables_names(widget)

    def remove_table(self):
        """
        Method removes selected table
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget) and isinstance(widget.con, sqlite3.Connection)\
                and len(self.tables.selectedIndexes()) > 0:
            with contextlib.closing(widget.con.cursor()) as cur:
                try:
                    cur.execute(f"DROP TABLE {self.tables.itemFromIndex(self.tables.selectedIndexes()[0]).text(0)}")
                except sqlite3.OperationalError as e:
                    self.statusbar.showMessage(str(e))
                self.render_tables_names(widget)

    def rename_table(self):
        """
        Method renames selected table from dialog
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget) and isinstance(widget.con, sqlite3.Connection) \
                and len(self.tables.selectedIndexes()) > 0:
            name = self.tables.itemFromIndex(self.tables.selectedIndexes()[0]).text(0)
            text, ok = QInputDialog.getText(self, "Rename table", "Table name:", QLineEdit.Normal, name)
            if ok and text:
                with contextlib.closing(widget.con.cursor()) as cur:
                    try:
                        cur.execute(f"ALTER TABLE {name} RENAME TO {text}")
                    except sqlite3.OperationalError as e:
                        self.statusbar.showMessage(str(e))
                    self.render_tables_names(widget)

    def add_row(self):
        """
        Method creates row by calling add_row() from current TableEditorWidget
        :return: None
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget) and widget.active_table() is not None:
            widget.add_row()

    def remove_row(self):
        """
        Method removes selected rows by calling remove_row() from TableEditorWidget
        :return:
        """
        widget = self.tabs.currentWidget()
        if isinstance(widget, TableEditorWidget):
            widget.remove_row()

    @staticmethod
    def render_active_table(widget):
        """
        Special method for updating table in TableEditorWidget
        :param widget:
        :return:
        """
        if isinstance(widget, TableEditorWidget) and isinstance(widget.con, sqlite3.Connection):
            with contextlib.closing(widget.con.cursor()) as cur:
                try:
                    res = cur.execute(f"SELECT * FROM {widget._active_table}").fetchall()
                    with widget as table:
                        table.setRowCount(len(res))
                        for i, row in enumerate(res):
                            for j, cell in enumerate(row):
                                table.setItem(i, j, QTableWidgetItem(str(cell)))
                except sqlite3.Error:
                    pass








