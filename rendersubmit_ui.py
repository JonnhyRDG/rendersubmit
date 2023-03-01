import os
import sys
import json
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import rendersubmit

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
        
        delegate = AlignDelegate(self.shotTree)
        self.shotTree.setItemDelegate(delegate)
        self.shotTree.setAlternatingRowColors(True)

        self.connect_buttons()

        self.layers = ['env_all','env_bg','char_all','char_andre','fx_smoke','char_cigar','env_skyscraper']

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
        self.currentseq = str(self.sequence_comboBox.currentText())
        if not self.currentseq == '':
            self.shotTree.clear()
            self.shotTree.setHeaderHidden(False)
            headers = ['Shots']
            unique_shots = []
            for layer in self.layers:
                headers.append(layer)
                self.shotTree.setHeaderLabels(headers)


            for items in self.seqsdict[self.currentseq]:
                if self.seqsdict[self.currentseq][items]['type'] == 'key':
                        ml_item = QtWidgets.QTreeWidgetItem(self.shotTree, [items])
                        ml_button = QtWidgets.QLabel(parent=self.shotTree)
                        self.shotTree.setItemWidget(ml_item,0,ml_button)
                        ml_item.setExpanded(True)
                        childlist = self.seqsdict[self.currentseq][items]['childs'].rsplit(",")
                        for childshots in childlist:
                            layercolumn = 1
                            shot_item = QtWidgets.QTreeWidgetItem(ml_item, [childshots])
                            shot_button = QtWidgets.QLabel(parent=self.shotTree)
                            self.shotTree.setItemWidget(shot_item,0,shot_button)
                            for ls in range(len(self.layers)):
                                check_button = QtWidgets.QCheckBox(parent=self.shotTree)
                                self.shotTree.setItemWidget(shot_item,layercolumn,check_button)
                                layercolumn = layercolumn + 1

                if self.seqsdict[self.currentseq][items]['type'] == 'unique':
                    unique_shots.append(items)
            
            if unique_shots:
                unique_hierarchy = QtWidgets.QTreeWidgetItem(self.shotTree, ['uniques'])
                unique_item = QtWidgets.QLabel(self.shotTree)
                self.shotTree.setItemWidget(unique_hierarchy,0,unique_item)
                unique_hierarchy.setExpanded(True)
                for un_shots in unique_shots:
                    uniqueshot_item = QtWidgets.QTreeWidgetItem(unique_hierarchy, [un_shots])
                    uniqueshot_button = QtWidgets.QLabel(parent=self.shotTree)
                    self.shotTree.setItemWidget(uniqueshot_item,0,uniqueshot_button)
                    uniquecolumn = 1
                    for ls in range(len(self.layers)):
                        uniquecheck_button = QtWidgets.QCheckBox(parent=self.shotTree)
                        self.shotTree.setItemWidget(uniqueshot_item,uniquecolumn,uniquecheck_button)
                        uniquecolumn = uniquecolumn + 1
        else:
            self.shotTree.clear()
            self.shotTree.setHeaderHidden(True)

    def onRender(self):
        render_dict = {}
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        for i in range(key_count):
            key_item = root.child(i)
            child_count = key_item.childCount()
            for child_index in range(child_count):
                shot_name = key_item.child(child_index).text(0)
                layers_to_render = []        
                for j in range(len(self.layers)):
                    checkbox = self.shotTree.itemWidget(key_item.child(child_index), j+1)
                    if checkbox and checkbox.isChecked():
                        layer = self.layers[j]
                        layers_to_render.append(layer)
                if layers_to_render:
                    render_dict[shot_name] = layers_to_render
        rendersubmit.rendersubmit().submit(seq=self.currentseq, shotsdict=render_dict,userdcc=str(self.dcc_combo.currentText()),usercomment=str(self.comment_edit.toPlainText()),userstatus=str(self.submitStatus_combo.currentText()),userchunk=str(self.tasksize_line.text()),userpriority=str(self.prio_line.text()))
        submit_done = QtWidgets.QMessageBox(parent=self.shotTree,text='Shots have been submitted to DEADLINE')
        submit_done.setWindowTitle('Submit Check')
        submit_done.show()

    def enableAll(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                for j in range(len(self.layers)):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    checkbox.setChecked(True)
                
    def disableAll(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                for j in range(len(self.layers)):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    checkbox.setChecked(False)

    def enableKeys(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        keyshot = []
        for keyshots in self.seqsdict[self.currentseq]:
            if self.seqsdict[self.currentseq][keyshots]['type'] == 'key':
                keyshot.append(keyshots)
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                shotname = key_shots.child(child_index).text(0)
                for j in range(len(self.layers)):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    checkbox.setChecked(False)
                    if shotname in keyshot:
                        # checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                        checkbox.setChecked(True)

    def connect_buttons(self):
        self.sequence_comboBox.currentIndexChanged.connect(self.createkeyshots)
        self.submit_push.clicked.connect(self.onRender)
        self.enableall_push.clicked.connect(self.enableAll)
        self.disableall_push.clicked.connect(self.disableAll)
        self.enablekeys_push.clicked.connect(self.enableKeys)


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