import os
from PyQt5.QtWidgets import QTreeWidgetItem
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    def __init__(self, project):
        super(Handler).__init__()
        self.project = project

    def on_created(self, event):
        self.project.render(self.project.path)

    def on_deleted(self, event):
        self.project.render(self.project.path)

    def on_moved(self, event):
        self.project.render(self.project.path)


class Project:
    def __init__(self, dirs_widget, files_widget):
        self.dirs = dirs_widget
        self.files = files_widget
        self.dirs.setHeaderLabel("Dirs")
        self.files.setHeaderLabel("Files")
        self.path = None

    def hide(self):
        self.dirs.hide()
        self.files.hide()

    def show(self):
        self.dirs.show()
        self.files.show()

    def open(self, path):
        if path is not None:
            self.path = path
            self.render(self.path)
            self.show()

    def render(self, path):
        if path is not None:
            tree = os.walk(path)
            try:
                top_level = next(tree)
                top_level_dirs = top_level[1]
                top_level_files = top_level[2]
            except StopIteration:
                pass
            else:
                self.clear()
                self.dirs.addTopLevelItems(map(lambda x: QTreeWidgetItem([x]), ["../", *top_level_dirs]))
                self.files.addTopLevelItems(map(lambda x: QTreeWidgetItem([x]), top_level_files))

    def clear(self):
        self.dirs.clear()
        self.files.clear()
