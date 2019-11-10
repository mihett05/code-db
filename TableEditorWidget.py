import contextlib
import sqlite3
from PyQt5.QtWidgets import QTableWidget, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton
from EditorWidget import EditorWidget


class InsertDialog(QDialog):
    def __init__(self, columns: list, cb):
        QDialog.__init__(self)
        self.main_layout = None
        self.columns = columns
        self.cols = dict()
        self.add_button = None
        self.cb = cb

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Insert Row")
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        for i, col in enumerate(self.columns):
            self.main_layout.addWidget(QLabel(str(col)), i, 0)
            self.cols[col] = QLineEdit()
            self.main_layout.addWidget(self.cols[col], i, 1)
        self.add_button = QPushButton("Insert Row")
        self.add_button.clicked.connect(self.insert_row)
        self.main_layout.addWidget(self.add_button, len(self.columns), 1)

    def insert_row(self):
        res = dict()
        for col in self.cols.keys():
            text = self.cols[col].text()
            if text:
                res[col] = text
        self.cb(res)
        self.close()


class TableEditorWidget(EditorWidget):
    def __init__(self, render_method):
        EditorWidget.__init__(self, QTableWidget())
        self.table_names = None
        self.con = None
        self.path = None
        self._active_table = None
        self._is_reading_db = False
        self._columns = dict()
        self.render_method = render_method
        self.structure = []
        self.initUI()

    def initUI(self):
        self._editor: QTableWidget
        self._editor.itemChanged.connect(self.changed)

    def changed(self, item):  # Доделать Update в таблице + структура columns + доделать settings
        if not self._is_reading_db:
            row = self._editor.row(item)
            cols = list(range(self.get_columns_len(self._active_table)))
            cols.remove(item.column())
            cols_values = [self._editor.item(row, i).text() for i in cols]
            columns = [self._columns[self._active_table][i] for i in cols]
            column = self._columns[self._active_table][item.column()]
            self.con.execute(f"""
            UPDATE {self._active_table}
            SET {column} = ?
            WHERE {' AND '.join([f"({col} = ?)" for col in columns])}
            """, [item.text(), *cols_values])

    def apply_changes(self):
        if self.con is not None:
            self.con.commit()

    def active_table(self):
        return self._active_table

    def __enter__(self):
        self._is_reading_db = True
        return self.editor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_reading_db = False
        self._editor.resizeColumnsToContents()
        return isinstance(exc_type, TypeError)

    def get_columns_len(self, table_name):
        return len(self._columns[table_name])

    def add_row(self):
        if self._active_table is not None:
            res = []
            InsertDialog(self._columns[self._active_table], lambda x: res.append(x)).exec_()
            res = res[0] if len(res) > 0 else None
            columns = []
            values = []
            if res:
                for col in res.keys():
                    columns.append(col)
                    values.append(res[col])

            with contextlib.closing(self.con.cursor()) as cur:
                try:
                    cur.execute(f"""INSERT INTO {self._active_table}
                    ({', '.join(columns)}) VALUES
                    ({', '.join(['?' for _ in range(len(values))])})""",
                                values)
                except sqlite3.Error:
                    pass
                else:
                    self.render_method(self)

    def remove_row(self):
        if self._active_table is not None and isinstance(self.con, sqlite3.Connection):
            removed_rows = []
            for index in self._editor.selectedIndexes():
                row = index.row()
                if row not in removed_rows:
                    where = {col: self._editor.item(row, i).text()
                             for i, col in enumerate(self._columns[self._active_table])}
                    with contextlib.closing(self.con.cursor()) as cur:
                        try:
                            cur.execute(f"""
                            DELETE FROM {self._active_table} WHERE
                            {' AND '.join([f'({key} = ?)' for key in where.keys()])}
                            """, [value for value in where.values()])
                        except sqlite3.Error:
                            pass
                        else:
                            removed_rows.append(row)
            self.render_method(self)

    def close_con(self):
        if self.con is not None:
            self.con.close()


