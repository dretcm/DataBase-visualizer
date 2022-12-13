import mysql.connector
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow,QLabel,QPushButton, QWidget,
                            QTableWidget,QTableWidgetItem, QComboBox,QLineEdit,QPushButton)
import sys

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'mydb'

myConnection = mysql.connector.connect( 
    host=hostname, 
    user=username, 
    passwd=password, 
    db=database )

cur = myConnection.cursor()

def Select_all_Query(table):
    cur.execute( f"SELECT * FROM {table}")
    return cur.fetchall()

def Select_where_Query(table, column, text):
    #print(f"SELECT * FROM {table} WHERE {column}='{text}'")
    cur.execute(f"SELECT * FROM {table} WHERE {column}='{text}'")
    return cur.fetchall()

def insert_Query(table, cols, data):
    if data:
        try:
            n = ("%s," * len(cols))[:-1]
            cols = "(" + ",".join(cols) + ")"
            #print(f"INSERT INTO {table} {cols} VALUES ({n})")
            cur.executemany(f"INSERT INTO {table} {cols} VALUES ({n})", data)
            myConnection.commit()
        except Exception as e:
            print(str(e))

def remove_Query(table, cols, data):
    if data:
        try:
            for sub_data in data:
                cad = ""
                for i in range(len(cols)):
                    cad += cols[i] + "=" + "'" + sub_data[i] + "'" + " AND "
                cad = cad[:-5]
                cur.execute(f"DELETE FROM {table} WHERE {cad}")
            myConnection.commit()
        except Exception as e:
            print(str(e))

def general_Query(query):
    cur.execute(query)
    return cur.fetchall()


class TableView(QTableWidget):
    def __init__(self, data, x, y, *args):
        QTableWidget.__init__(self, *args)
        self.udpate_tablewidget(data, x, y)

    def udpate_tablewidget(self, data, x, y):
        self.data = data
        self.data_querys = []
        self.data_removes = {}
        self.size_columns_ = y
        self.size_rows_ = x+1
        self.setRowCount(self.size_rows_)
        self.setColumnCount(y)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(list(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def new_row_widget(self):
        self.size_rows_ += 1
        self.setRowCount(self.size_rows_)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        querys = []
        for i in range(self.size_columns_):
            querys.append(self.item(self.size_rows_-2, i).text())
        self.data_querys.append(querys)
        print(self.data_querys)

    def remove_row_widget(self):
        n = self.currentRow()
        if n not in self.data_removes:
            self.data_removes[n] = [self.item(n, i).text() for i in range(self.size_columns_)]
        print(self.data_removes)

class Input_Table(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Jola",self)
        self.move(150,150)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        self.setWindowTitle("Visualizer")
        self.setGeometry(50, 50, 1080, 660)

        self.querys = {"Full Cliente": [["cliente", "cliente_hace_pedido", "medicamento_está_en_pedido", "boleta", "medicamento"]
            ,"""select * from cliente x inner join cliente_hace_pedido y 
            on y.CLIENTE_PERSONA_idPERSONA=x.ID_cliente 
            inner join medicamento_está_en_pedido z 
            on z.PEDIDO_idPEDIDO=y.PEDIDO_idPEDIDO 
            inner join boleta w 
            on w.PEDIDO_idPEDIDO=z.PEDIDO_idPEDIDO inner join medicamento v 
            on z.MEDICAMENTO_ID_medicamento = v.ID_medicamento"""],

            "Full Farmacéutico":[["personal", "farmacéutico", "farmacia_tiene_medicamento"
            , "medicamento", "farmacia", "ubicación"], """select * from personal x inner join farmacéutico y 
            on y.PERSONAL_ID_personal1=x.ID_personal
            inner join farmacia_tiene_medicamento z 
            on z.FARMACIA_idFARMACIA=y.FARMACIA_idFARMACIA 
            inner join medicamento w 
            on w.ID_medicamento=z.MEDICAMENTO_ID_medicamento 
            inner join farmacia v 
            on z.FARMACIA_idFARMACIA = v.idFARMACIA
            inner join ubicación u
            on v.UBICACIÓN_idUBICACIÓN=u.idUBICACIÓN"""],

            "Full Empleado":[["personal", "empleado", "empleado_trabaja_farmacia"
            , "farmacia", "ubicación", "banco"], """select * from personal x inner join empleado y 
            on y.PERSONAL_ID_personal1=x.ID_personal
            inner join empleado_trabaja_farmacia z 
            on y.PERSONAL_ID_empleado=z.EMPLEADO_PERSONAL_ID_personal 
            inner join farmacia w 
            on w.idFARMACIA=z.FARMACIA_idFARMACIA 
            inner join ubicación v 
            on v.idUBICACIÓN = w.UBICACIÓN_idUBICACIÓN
            inner join banco u
            on w.BANCO_idBANCO=u.idBANCO"""]}

        self.UiComponents()
        self.show()
  

    def UiComponents(self):
        label = QLabel("<u><b>Table:</u></b>", self)
        label.setStyleSheet('font: 80 11pt "Arial";')
        label.setGeometry(240, 10, 200, 30)

        self.button = QPushButton("SELECT * FROM", self)
        self.button.setStyleSheet('font: 75 12pt "Arial";')
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
        self.col_items = []

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


        self.more = QPushButton("+", self)
        self.more.setStyleSheet('font: 80 12pt "Arial";')
        self.more.setGeometry(860, 10, 100, 30)
        self.more.clicked.connect(self.add_row)

        self.less = QPushButton("-", self)
        self.less.setStyleSheet('font: 100 16pt "Arial";')
        self.less.setGeometry(860, 50, 100, 30)
        self.less.clicked.connect(self.remove_row)

        self.save = QPushButton("Save", self)
        self.save.setStyleSheet('font: 75 11pt "Arial";')
        self.save.setGeometry(970, 10, 100, 30)
        self.save.clicked.connect(self.save_all)

        self.inners = QComboBox(self)
        self.inners.setGeometry(20, 190, 200, 30)
        self.inners.setStyleSheet('font: 75 11pt "Arial";')
        self.inners.addItems(list(self.querys.keys()))

        bt = QPushButton("Run", self)
        bt.setStyleSheet('font: 75 11pt "Arial";')
        bt.setGeometry(240, 190, 100, 30)
        bt.clicked.connect(self.general_operation)

        cur.execute("SHOW TABLES")
        for i in cur.fetchall():
            self.option.addItem(i[0])

        self.table = None
        self.update_table()

    def update_table(self, where=False):
        cur.execute(f"show columns from {self.option.currentText()}")
        self.col_items = [i[0] for i in cur.fetchall()]

        dataframe, x, y = self.get_table(self.option.currentText(),where, self.col_items)

        self.col.clear()
        self.col.addItems(self.col_items)

        if self.table:
            self.table.clear()
            self.table.udpate_tablewidget(dataframe, x, y)
        else:
            self.table = TableView(dataframe, x, y, self)
            self.table.setGeometry(10, 240, 1060, 410)          
        

    def get_table(self, table, where, columns, inners=""):
        if inners!="":
            text = general_Query(inners)
        elif where:
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

        dataframe = {} #dict(zip(columns, data))
        con = 2
        x,y = len(text), len(columns)
        for i in range(y):
            if columns[i] in dataframe:
                columns[i] += "_" + str(con)
                con += 1
            dataframe[columns[i]] = data[i]
        return dataframe, x, y

    def general_operation(self):
        columns_query, inners = self.querys[self.inners.currentText()]
        self.col_items = []
        for i in columns_query:
            cur.execute(f"show columns from {i}")
            self.col_items.extend([c[0] for c in cur.fetchall()])

        dataframe, x, y = self.get_table(None, False, self.col_items, inners)
        self.col.clear()
        self.col.addItems(self.col_items)

        if self.table:
            self.table.clear()
            self.table.udpate_tablewidget(dataframe, x, y)

    def on_text_changed(self, text):
        width = self.search_input.fontMetrics().width(text)
        self.search_input.setMinimumWidth(width)

    def add_row(self):
        self.table.new_row_widget()

    def remove_row(self):
        self.table.remove_row_widget()

    def save_all(self):
        insert_Query(self.option.currentText(),
            self.col_items,
            self.table.data_querys)
        remove_Query(self.option.currentText(),
            self.col_items, 
            list(self.table.data_removes.values()))
        self.update_table()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    cur.close()
    myConnection.close()