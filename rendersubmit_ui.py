import os
import sys
import json
from PyQt5 import QtWidgets, uic, QtGui, QtCore

# Esto carga el archivo .ui
ui_path = os.path.join(os.path.dirname(__file__), 'rendersubmit_ui.ui')
generated_class, base_class = uic.loadUiType(ui_path)

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


# Definimos nuestra clase, en este caso un widget
class renderSubmit(base_class, generated_class):
    def __init__(self, *args, **kwargs):
        # Llamamos al constructor del padre
        super(renderSubmit, self).__init__(*args, **kwargs)

        # La llamada a setupUi siempre hay que hacerla
        self.setupUi(self)

        # En caso de que queramos podemos cargar una hoja de estilo
        with open(os.path.join(os.path.dirname(__file__), 'rendersubmit_ui.qss'), "r") as f:
            self.setStyleSheet(f.read())

        # Ponemos un titulo a la ventana
        self.setWindowTitle("AJ Render Submiter v0.0.1")
        
        #Leemos el dict bakeado con la data de las secuencias/shots
        self.dictread()

        #Rellenamos los combo box de episodios y secuencias
        self.populateCombo()

        # Setteamos los callcacks a los items
        self.sequence_comboBox.currentIndexChanged.connect(self.createkeyshots)

        delegate = AlignDelegate(self.shotlist_table)
        self.shotlist_table.setItemDelegate(delegate)
    
    # Definimos la funcion que se ejecuta al darle al boton
    # otro comentario mas que te pario che
        
    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)
    
    def seqlists(self):
        self.seqcombolist = ['']
        for seqs in self.seqsdict:
            self.seqcombolist.append(seqs)

    def populateCombo(self):
        self.seqlists()
        self.sequence_comboBox.addItems(self.seqcombolist)
        episodes = ['concept_animatic']
        self.episode_comboBox.addItems(episodes)
        
    def createkeyshots(self):
        rownumber = 0
        currentseq = str(self.sequence_comboBox.currentText())
        self.shotlist_table.setColumnCount(1)
        self.shotlist_table.setHorizontalHeaderLabels(['shot'])

        if currentseq in self.seqsdict:
            self.shotlist_table.horizontalHeader().setVisible(True)
            if not currentseq == '':
                for shots in self.seqsdict[currentseq]:
                    self.shotlist_table.setRowCount(rownumber)
                    self.shotlist_table.insertRow(rownumber)
                    self.shotlist_table.setItem(rownumber,0,QtWidgets.QTableWidgetItem(shots))
                    rownumber = rownumber + 1
        else:
            self.shotlist_table.setRowCount(rownumber)
            self.shotlist_table.insertRow(rownumber)
            self.shotlist_table.horizontalHeader().setVisible(False)


        # self.shotlist_table.setRowCount(rownumber)
        # self.shotlist_table.setColumnCount(1)
        # rowposition = self.shotlist_table.rowCount()
        # colposition = self.shotlist_table.columnCount()
        # self.shotlist_table.insertRow(rowposition)
        # self.shotlist_table.insertColumn(colposition)
        
        # rowposition = 0
        # if currentseq in self.seqsdict:
        #     self.shotlist_table.setHorizontalHeaderLabels(['shot'])
        #     for shotlist in self.seqsdict[currentseq]:
        #         self.shotlist_table.setItem(rowposition,0,QtWidgets.QTableWidgetItem(shotlist))
        #         # self.shotlist_table.setItem(rowposition,1,QtWidgets.QTableWidgetItem('env_all'))
        #         rowposition = rowposition + 1

# def registerPanel():
#     import nuke
#     import nukescripts
#     from nukescripts import panels

#     ## make this work in a .py file and in 'copy and paste' into the script editor
#     moduleName = __name__
#     if __name__ == '__main__':
#         moduleName = ''
#     else:
#         moduleName = moduleName + '.'

#     panels.registerWidgetAsPanel( moduleName + 'renderSubmit', 'AJ Render Submiter v0.0.1', 'render.Submit')

def main():
    # Creamos nuestra aplicacion
    app = QtWidgets.QApplication(sys.argv)

    # Creamos nuestro widget y lo mostramos.
    widget = renderSubmit()
    widget.show()   # Para mostrarlo con el tamñano definido en el ui
    # widget.showMaximized()  # Para mostrarlo con la pantalla maximizada
    # widget.showFullScreen()  # Para mostrarlo en fullscreen

    # Ejecutamos la aplicacion
    app.exec_()

if __name__ == '__main__':
    # registerPanel()
    main()