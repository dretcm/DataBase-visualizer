import mysql.connector
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QPushButton, QTableWidget,QTableWidgetItem, QComboBox
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

def Select_all_Query(table ) :
    cur.execute( f"SELECT * FROM {table}" )
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

        self.setGeometry(100, 100, 820, 360)

        self.UiComponents()
        self.show()
  

    def UiComponents(self):
    	self.button = QPushButton("Print", self)
    	self.button.setStyleSheet('font: 75 11pt "Arial";')
    	self.button.setGeometry(250, 10, 200, 30)
    	self.button.clicked.connect(self.update_table)

    	self.option = QComboBox(self)
    	self.option.setGeometry(20, 10, 200, 30)
    	self.option.setStyleSheet('font: 75 11pt "Arial";')

    	cur.execute("SHOW TABLES")
    	for i in cur.fetchall():
    		self.option.addItem(i[0])
    	self.table = None
    	self.update_table()

    def update_table(self):
    	op = str(self.option.currentText())
    	dataframe, x, y = self.get_table(op)
    	if self.table:
    		self.table.clear()
    		self.table.udpate_tablewidget(dataframe, x, y)
    	else:
    		self.table = TableView(dataframe, x, y, self)
    		self.table.setGeometry(10, 50, 800, 300)    		
    	

    def get_table(self, table):
    	cur.execute(f"show columns from {table}")
    	columns = [i[0] for i in cur.fetchall()]
    	text = Select_all_Query(table)
    	data = []

    	for i in range(len(columns)):
    		aux = []
    		for j in range(len(text)):
    			aux.append(str(text[j][i]))
    		data.append(aux)

    	dataframe = dict(zip(columns, data))
    	x,y = len(text), len(columns)
    	return dataframe, x, y


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