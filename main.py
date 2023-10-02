from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTableWidget,\
    QVBoxLayout, QDialog, QTabWidget, QTableWidgetItem, \
    QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout, QLabel
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

import typing
import sys
import csv


class mouse(object): # Interactive Mouse Functions I want to incorporate
    def __init__(self):
        pass

    def leftClick(self, row, column):   # Highlight specific cells or blocks of cells 
        print("LEFT", row, column)
    
    def rightClick(self, row, column):  # Incorporate right click menu for specific options 
        print("RIGHT", row, column)

    def removeItem(self, row, column):  # Delete specific cells within the table 
        pass
    
    def highLighted(self, row, column): # Highlight blocks of cells in the item 
        pass

        


class MyTable(QDialog): # MyTable which is acting as a sub class to PyQT5 QDialog class which is responsible for a lot of the main applications in PyQT5
    def __init__(self): # Constructor
        QDialog.__init__(self)  # Parent class inheriting 

        # Load data from CSV file
        self.data = []
        with open('humans.csv', 'r') as infile:
            csv_reader = csv.reader(infile, delimiter=",")
            self.data = list(csv_reader)    # Easier to work with as a list for some reason.
        
        self.labels = self.data[0] # Top Labels: Index,User Id,First Name,Last Name,Sex,Email,Phone,Date of birth,Job Title (These work great for column traversing)
        self.data = self.data[1:] # Rest of the data excluding Labels
        self.filtered_data = self.data  # Copy of data that has been filtered by label

        self.layout = QVBoxLayout(self)     # Vertical Box Layout to start placing widgets inside there is also a horizontal option.

        self.table = QTableWidget()     # Initializing table and tabs objects from their PyQT5 imported classes 
        self.tabs = QTabWidget()

        self.mouse = mouse()        # Derived mouse class object to use

        self.create_tabs()     #   Calling methods and their functionalities within the class
        self.create_table() 
        self.create_buttons()


    def create_buttons(self):
        button_layout = QVBoxLayout()   # Vertical box layout for the buttons, for now!

        self.b_new = QPushButton("NEW")     # Titling new buttons 
        self.b_copy = QPushButton("COPY")
        self.b_remove = QPushButton("REMOVE")
        self.b_duplicates = QPushButton("DUPLICATE CHECK")

        self.b_new.clicked.connect(self.addRow)    # Mapping buttons to their respective functions 
        self.b_copy.clicked.connect(self.copyRow)
        self.b_remove.clicked.connect(self.deleteRow)
        self.b_duplicates.clicked.connect(self.duplicateCheck)

        button_layout.addWidget(self.b_new)     # Adding the stack of buttons to the vertical box layout
        button_layout.addWidget(self.b_copy)
        button_layout.addWidget(self.b_remove)
        button_layout.addWidget(self.b_duplicates)

        self.layout.addLayout(button_layout)  # Add the button layout to the main layout


    def create_tabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.currentChanged.connect(self.tab_changed)      # Connecting tab_changed function that keeps track of tab indexes
        self.tabs.addTab(self.tab1, "All")                      # Adding tabs and their filtered data, will add more later
        self.tabs.addTab(self.tab2, "Only Males")
        self.layout.addWidget(self.tabs)    # Adding to the default vertical layout on top of the table

    def create_table(self):
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)   #   This took me hours lmao only to find that there was a built in function for this.
        self.table.setStyleSheet('selection-background-color:white;')
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setRowCount(len(self.data))          # Row count limit using built in function and the data[]
        self.table.setColumnCount(len(self.labels))
        # self.table.setColumnWidth(0,25)
        self.table.setHorizontalHeaderLabels(self.labels)      # Adding the label titles to the top of the table, makes it easier to filter stuff

        for row in range(len(self.filtered_data)):
            for col in range(len(self.labels)):               
                item = QTableWidgetItem(str(self.filtered_data[row][col]))      # item gives it its own hexadecimal value within the cell and to access it's attributes!
                self.table.setItem(row, col, item)
        self.layout.addWidget(self.table)                       # Adding the table to the vertical layout 
        self.table.viewport().installEventFilter(self)          # Event listener to respond to my mouse actions

    def eventFilter(self, source, event):       
        if self.table.selectedIndexes() != []:          # if nothing has been selected 
            # if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:      # left mouse button press
                    row = self.table.currentRow()
                    col = self.table.currentColumn()
                    self.mouse.leftClick(row,col)           # debugging by printing their coordinates and seeing how it works.
                elif event.button() == QtCore.Qt.RightButton:
                    row = self.table.currentRow()
                    col = self.table.currentColumn()
                    self.mouse.rightClick(row,col)      # Need to incorporate menu method here
        return QtCore.QObject.event(source,event)

    def update_table(self, data_to_display):
        self.table.clearContents()              # Wipe table clean to populate with new data 

        self.table.setRowCount(len(data_to_display))
        self.table.setColumnCount(len(self.labels))

        for row in range(len(data_to_display)):     # populate it similar to creating the table only use a new data set (like the filtered data [])
            for col in range(len(self.labels)):
                item = QTableWidgetItem(str(data_to_display[row][col]))
                self.table.setItem(row, col, item)

    def tab_changed(self, index):   # This took a long time lol Tab indexes start at 0 
        if index == 0:
            # self.filtered_data = self.data
            self.update_table(self.data)
        elif index == 1:
            self.filtered_data = [row for row in self.data if row[self.labels.index("Sex")] == "Male"]  # filtering only the rows with under the column of sex that are Male 
            self.update_table(self.filtered_data)           # Updating new table with the filtered data[]

    def addRow(self):       # Adding a new row at the bottom of the table. Will make this a little more sophisticated later with data entry 
        # self.label.setText("I'm a good button!")

        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        print("Row Added")

    def deleteRow(self):    # Deleted row at the bottom of the table, will make this more specific later with the mouse. 
        rowPosition = self.table.rowCount()
        self.table.removeRow(rowPosition-1) # -1 less
        print("Row Deleted.")

    def copyRow(self):      # Had a lot of trouble with this one. Will fix soon.
        print("Copy Function, Coming soon.")

    def duplicateCheck(self):       # 
        rowPosition = self.table.rowCount()
        colPosition = self.labels.index("User Id")      # method only works with labels.index and not columnAt function for some reason.

        seen_values = set()  # No duplicates allowed in a python set. Should update this to be more dynamic. Cross checking values here.
        
        for row in range(rowPosition):
            item = self.table.item(row, colPosition)    # only traversing through that columns position to compare unique User IDs 
            if item:                                    # if there's something and not blank
                value = item.text()
                if value in seen_values:                # comparing with seen values!
                    print(f"DUPLICATE FOUND: {value}")   
                else:
                    seen_values.add(value)
    
        print("Duplicate Check Complete.")

    def updateSize(self):                               # Adjust size of elements.
        pass
        # self.label.adjustSize()


def main():
    app = QApplication(sys.argv)
    w = MyTable()
    w.resize(1000,1200)
    w.setWindowTitle('Humans and their jobs')
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
