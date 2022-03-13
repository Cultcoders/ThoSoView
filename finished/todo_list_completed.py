import json
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from MainWindow import Ui_MainWindow
tick = QtGui.QImage('tick.png')

# tag::model[]
class ToDoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(ToDoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]
            return text
        if role == Qt.DecorationRole:
            status, text = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)
# end::model[]

# Main-window
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = ToDoModel()
        self.load()
        # testdata
        # self.model = ToDoModel(todos=[(False, "Einkaufen"), (False, "Singen"), (False, "Radfahren"), (False, "Lesen")])
        self.todoView.setModel(self.model)
        self.addButton.pressed.connect(self.add)
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton.pressed.connect(self.complete)

    def load(self):
        try:
            with open('data.json', 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        try:
            with open('data.json', 'w') as f:
                data = json.dump(self.model.todos, f)
        except Exception:
            print("Error on saving data: " + str(Exception))

    def add(self):
        text = self.todoEdit.text()
        text = text.strip()

        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # clear selection (no longer valid)
            self.todoView.clearSelection()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)

            self.model.dataChanged.emit(index, index)
            self.todoView.clearSelection()
            self.save()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
