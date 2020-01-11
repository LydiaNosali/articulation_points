import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import networkx as nwx
import numpy as np


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget()
        self.layout = QVBoxLayout()
        self.title = 'Création du graphe'
        self.left = 100
        self.top = 100
        self.width = 880
        self.height = 700

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon("c.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        btn = QPushButton('Suivant', self)
        btn.setToolTip('Cliquez pour afficher le graphe')
        btn.resize(btn.sizeHint())
        btn.move(350, 500)
        btn.clicked.connect(self.on_click)
        # Show widget
        self.show()

    def createTable(self):
        # Create table
        i, okPressed = QInputDialog.getInt(self, "Nombre de sommets", "Nombre de sommets:", 5, 0, 100, 1)
        if okPressed:
            self.tableWidget.setRowCount(i)
            self.tableWidget.setColumnCount(i)
            for j in range(i):
                for k in range(i):
                    self.tableWidget.setItem(k, j, QTableWidgetItem("0"))
                    self.tableWidget.setItem(j, k, QTableWidgetItem("0"))
            self.tableWidget.move(0, 0)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        # for currentQTableWidgetItem in self.tableWidget.selectedItems():
        #    print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        row = self.tableWidget.rowCount()
        column = self.tableWidget.columnCount()
        text = ''
        for r in range(row):
            for c in range(column):
                text = text + ' ' + self.tableWidget.item(r, c).text()
        entries = list(map(int, text.split()))
        A = np.array(entries).reshape(row, column)
        G = nwx.from_numpy_matrix(np.matrix(A), create_using=nwx.Graph)
        color_map = []
        for node in G:
            if node in list(articulation_points(G)):
                color_map.append('red')
            else:
                color_map.append('green')
        labels = nwx.get_edge_attributes(G, "")
        layout = nwx.spring_layout(G)
        nwx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        nwx.draw(G, layout, node_color=color_map, with_labels=True)
        # self.resultat = QLabel("Le nombre de points d'articulation est : " + str(len(list( articulation_points(
        # G)))) + "\n" + "La liste des points d'articulation est : " + "\n" + str(list(articulation_points(G))))
        # self.resultat.setWindowIcon(QtGui.QIcon("c.png")) self.resultat.setWindowTitle(self.title)
        # self.resultat.setGeometry(self.left, self.top, self.width, self.height)

        # self.resultat.setAlignment(Qt.AlignCenter)

        # p = self.resultat.palette()
        # p.setColor(self.resultat.backgroundRole(), Qt.green)
        # self.resultat.setPalette(p)

        # newfont = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        # self.resultat.setFont(newfont)

        # self.resultat.show()

        plt.show()


def articulation_points(G):
    seen = set()
    for articulation in dfs_i(G, components=False):
        if articulation not in seen:
            seen.add(articulation)
            yield articulation


def dfs_i(G, components=True):
    visited = set()
    for start in G:
        if start in visited:
            continue
        discovery = {start: 0}
        low = {start: 0}
        root_children = 0
        visited.add(start)
        edge_stack = []
        stack = [(start, start, iter(G[start]))]
        while stack:
            grandparent, parent, children = stack[-1]
            try:
                child = next(children)
                if grandparent == child:
                    continue
                if child in visited:
                    if discovery[child] <= discovery[parent]:  # back edge
                        low[parent] = min(low[parent], discovery[child])
                        if components:
                            edge_stack.append((parent, child))
                else:
                    low[child] = discovery[child] = len(discovery)
                    visited.add(child)
                    stack.append((parent, child, iter(G[child])))
                    if components:
                        edge_stack.append((parent, child))
            except StopIteration:
                stack.pop()
                if len(stack) > 1:
                    if low[parent] >= discovery[grandparent]:
                        if components:
                            ind = edge_stack.index((grandparent, parent))
                            yield edge_stack[ind:]
                            edge_stack = edge_stack[:ind]
                        else:
                            yield grandparent
                    low[grandparent] = min(low[parent], low[grandparent])
                elif stack:  # length 1 so grandparent is root
                    root_children += 1
                    if components:
                        ind = edge_stack.index((grandparent, parent))
                        yield edge_stack[ind:]
        if not components:
            if root_children > 1:
                yield start


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
