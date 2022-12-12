import mysql.connector
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow,QLabel,QPushButton, 
                            QTableWidget,QTableWidgetItem, QComboBox,QLineEdit,QPushButton)
import sys

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'sakila'

myConnection = mysql.connector.connect( 
    host=hostname, 
    user=username, 
    passwd=password, 
    db=database )

cur = myConnection.cursor()

def Select_all_Query(table) :
    cur.execute( f"SELECT * FROM {table}" )
    return cur.fetchall()

def Select_where_Query(table, column, text) :
    cur.execute(f"SELECT * FROM {table} WHERE {column}='{text}'")
    return cur.fetchall()


class TableView(QTableWidget):
    def __init__(self, data, x, y, *args):
        QTableWidget.__init__(self, *args)
        self.udpate_tablewidget(data, x, y)

    def udpate_tablewidget(self, data, x, y):
        self.data = data
        self.setRowCount(x)
        self.setColumnCount(y)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        self.setWindowTitle("Python")

        self.setGeometry(50, 50, 1080, 620)

        self.UiComponents()
        self.show()
  

    def UiComponents(self):
        label = QLabel("<u><b>Table:</u></b>", self)
        label.setStyleSheet('font: 80 11pt "Arial";')
        label.setGeometry(240, 10, 200, 30)

        self.button = QPushButton("SELECT * FROM", self)
        self.button.setStyleSheet('font: 75 11pt "Arial";')
        self.button.setGeometry(20, 50, 200, 30)
        self.button.clicked.connect(self.update_table)

        self.option = QComboBox(self)
        #self.option.setEditable(True)
        #self.option.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.option.setGeometry(240, 50, 200, 30)
        self.option.setStyleSheet('font: 75 11pt "Arial";')

        label = QLabel("<u><b>Columns:</u></b>", self)
        label.setStyleSheet('font: 80 11pt "Arial";')
        label.setGeometry(240, 90, 200, 30)

        label = QLabel("<u><b>Search value:</u></b>", self)
        label.setStyleSheet('font: 80 11pt "Arial";')
        label.setGeometry(470, 90, 200, 30)

        self.col = QComboBox(self)
        self.col.setGeometry(240, 130, 200, 30)
        self.col.setStyleSheet('font: 75 11pt "Arial";')

        label = QLabel("<b>=</b>", self)
        label.setStyleSheet('font: 80 11pt "Arial";')
        label.setGeometry(450, 130, 200, 30)

        self.search_input = QLineEdit(self)
        self.search_input.setAlignment(QtCore.Qt.AlignCenter)
        self.search_input.textChanged.connect(self.on_text_changed)
        self.search_input.setGeometry(470, 130, 200, 30)
        self.search_input.setStyleSheet('font: 75 11pt "Arial";')

        self.button_search = QPushButton("WHERE", self)
        self.button_search.setStyleSheet('font: 75 11pt "Arial";')
        self.button_search.setGeometry(20, 130, 200, 30)
        self.button_search.clicked.connect(lambda: self.update_table(where=True))

        cur.execute("SHOW TABLES")
        for i in cur.fetchall():
            self.option.addItem(i[0])

        self.table = None
        self.update_table()


    def update_table(self, where=False):
        op = str(self.option.currentText())
        dataframe, x, y, columns = self.get_table(op, where)
        self.col.clear()
        self.col.addItems(columns)

        if self.table:
            self.table.clear()
            self.table.udpate_tablewidget(dataframe, x, y)
        else:
            self.table = TableView(dataframe, x, y, self)
            self.table.setGeometry(10, 180, 1060, 430)          
        

    def get_table(self, table, where):
        cur.execute(f"show columns from {table}")
        query = cur.fetchall()
        #print(query)
        columns = [i[0] for i in query]
        if where:
            text = Select_where_Query(table,
                self.col.currentText(), 
                self.search_input.text())
        else:
            text = Select_all_Query(table)
        data = []

        for i in range(len(columns)):
            aux = []
            for j in range(len(text)):
                aux.append(str(text[j][i]))
            data.append(aux)

        dataframe = dict(zip(columns, data))
        x,y = len(text), len(columns)
        return dataframe, x, y, columns

    def on_text_changed(self, text):
        width = self.search_input.fontMetrics().width(text)
        self.search_input.setMinimumWidth(width)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())






cad = """
drop table IF EXISTS db.Persona;
drop table IF EXISTS db.Bank;

CREATE TABLE IF NOT EXISTS db.Bank (
  idBank INT NOT NULL,
  name_bank VARCHAR(45) NULL,
  PRIMARY KEY (idBank));
  
CREATE TABLE IF NOT EXISTS db.Persona (
    dni INT NOT NULL,
    name VARCHAR(45) NULL,
    PRIMARY KEY (dni));

insert into db.Persona values (1,"carlos");
insert into db.Persona values (3,"YUTU");
select * from db.Persona;
"""