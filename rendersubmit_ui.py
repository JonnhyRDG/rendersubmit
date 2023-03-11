import subprocess
import os
import sys
import json
from functools import partial
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import rendersubmit
nukerun = '"C:/Program Files/Nuke13.2v5/Nuke13.2.exe"'
script = '"P:/AndreJukebox/pipe/ajbackend/rendersubmit/nukepublish.py"'

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
        self.currentseq = str(self.sequence_comboBox.currentText())
        self.layers = ['env_all','env_bg','char_all','char_andre','fx_smoke','char_cigar','env_skyscraper']
        self.expressionbtn.setVisible(0)

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
        if self.step_check.isChecked():
            self.stepson = 1
        else:
            self.stepson = 0

        argdict = {}
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
        
        argdict['stepstate']=self.stepson
        argdict['step']=self.step_spin.text()
        argdict['seq']=self.currentseq
        argdict['framesdict']=self.frame_combo.currentText()
        argdict['frameexp']=self.expressionbtn.text()
        argdict['shotsdict']=[render_dict]
        argdict['userdcc']=str(self.dcc_combo.currentText())
        argdict['usercomment']=str(self.comment_edit.toPlainText())
        argdict['userstatus']=str(self.submitStatus_combo.currentText())
        argdict['userchunk']=str(self.tasksize_line.text())
        argdict['userpriority']=str(self.prio_line.text())
        argdict['pool']=str(self.group_combo.currentText())
        
        if not self.currentseq == '':
            rendersubmit.rendersubmit().submit(katargs=argdict)
            submit_done = QtWidgets.QMessageBox(parent=self.shotTree,text='Shots have been submitted to DEADLINE')
            submit_done.setWindowTitle('Submit Check')
            submit_done.show()
        else:
            emptyseq = QtWidgets.QMessageBox(parent=self.shotTree,text='You need to select a sequence first...GENIUS!')
            emptyseq.setWindowTitle('Sequence check')
            emptyseq.show()

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
                        checkbox.setChecked(True)

    def enableUniques(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        keyshot = []
        for keyshots in self.seqsdict[self.currentseq]:
            if self.seqsdict[self.currentseq][keyshots]['type'] == 'unique':
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
                        checkbox.setChecked(True)

    def framesui(self):
        self.expressionbtn.setVisible(0)
        if self.frame_combo.currentText() == "Expression":# and self.frames_layout.count() == 0:
            self.expressionbtn.setVisible(1)
        else:
            if self.expressionbtn:
                self.expressionbtn.setVisible(0)
                self.frames_layout.removeWidget(self.expressionbtn)

    def stepspin(self):
        if self.step_check.isChecked():
            self.step_spin.setReadOnly(0)
        else:
            self.step_spin.setReadOnly(1)
    
    def enablesel(self,selmodel):
        root = self.shotTree.invisibleRootItem()
        for parent in selmodel:
            key_shot = root.child(parent.parent().row())
            if hasattr(key_shot,'child'):
                shot_child = key_shot.child(parent.row())
                checkbox = self.shotTree.itemWidget(shot_child,parent.column())
                if hasattr(checkbox, 'setChecked'):
                    checkbox.setChecked(True)
                else:
                    continue

    def enablelayer(self,selmodel):
        root = self.shotTree.invisibleRootItem()
        child_count = root.childCount() #rows
        for keys in range(child_count):
            key_childs = root.child(keys)
            shot_child_count = key_childs.childCount()
            for selected_child in range(shot_child_count):
                for shotitem in selmodel:
                    checkbox = self.shotTree.itemWidget(key_childs.child(selected_child),shotitem.column())
                    if hasattr(checkbox, 'setChecked'):
                        checkbox.setChecked(True)
                    else:
                        continue

    def enableshot(self,selmodel):
        root = self.shotTree.invisibleRootItem()
        for selected_shots in selmodel:
            for j in range(len(self.layers)):
                checkbox = self.shotTree.itemWidget(selected_shots,j+1)
                if hasattr(checkbox,'setChecked'):
                    checkbox.setChecked(True)
                else:
                    continue

    def clearselected(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            if hasattr(key_shots,'setSelected'):
                key_shots.setSelected(False)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                for j in range(len(self.layers)):
                    cell = key_shots.child(child_index)
                    if hasattr(cell,'setSelected'):
                        cell.setSelected(False)

    def onTreeContextMenuRequested(self, point):
        item = self.shotTree.itemAt(point)
        selection = self.shotTree.selectedItems()
        selmodel = self.shotTree.selectionModel().selectedIndexes()
        actions = [
            {'title': "Enable selection", 'name': 'enableSelection', 'callback': partial(self.enablesel, selmodel), 'enabled': True},
            {'title': "Enable shot", 'name': 'enableShot', 'callback': partial(self.enableshot, selection), 'enabled': True},
            {'title': "Enable layer", 'name': 'enableLayer', 'callback': partial(self.enablelayer, selmodel), 'enabled': True},
            {'title': "Pull comp from key", 'name': 'pullKeyComp', 'callback': partial(self.pullKeyComp, selmodel), 'enabled': True}
            ]

        self.menu = QtWidgets.QMenu()
        for action_data in actions:
            action = self.menu.addAction(action_data['title'])
            action.setObjectName(action_data['name'])
            action.setEnabled(action_data['enabled'])
            action.triggered.connect(action_data['callback'])
        self.menu.popup(QtGui.QCursor.pos())


    def connect_buttons(self):
        self.shotTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shotTree.customContextMenuRequested.connect(self.onTreeContextMenuRequested)
        self.sequence_comboBox.currentIndexChanged.connect(self.createkeyshots)
        self.submit_push.clicked.connect(self.onRender)
        self.enableall_push.clicked.connect(self.enableAll)
        self.disableall_push.clicked.connect(self.disableAll)
        self.enablekeys_push.clicked.connect(self.enableKeys)
        self.frame_combo.currentIndexChanged.connect(self.framesui)
        self.step_check.clicked.connect(self.stepspin)
        self.clearsel_push.clicked.connect(self.clearselected)
        self.enableunique_push.clicked.connect(self.enableUniques)
        
    def pullKeyComp(self,selmodel):
        root = self.shotTree.invisibleRootItem()
        for parent in selmodel:
            key_shot = root.child(parent.parent().row())
            nukefile = f'P:/AndreJukebox_output/comp/concept_animatic/{self.currentseq}/{key_shot.text(0)}/workfile.nk'
            if os.path.isfile(nukefile):
                print('keys=',key_shot.text(0))
                child_count = key_shot.childCount()
                for childs in range(child_count):
                    children = key_shot.child(childs)
                    if self.seqsdict[self.currentseq][children.text(0)]['type'] != 'key':
                    # print('childs=',children.text(0))
                        nukecommand = f'{nukerun} -t {script} {self.currentseq} {children.text(0)} {key_shot.text(0)}'
                        print(nukecommand)
                        subprocess.call(nukecommand, shell=True)
                    else:
                        continue
            else:
                nocomp = QtWidgets.QMessageBox(parent=self.shotTree,text='There is no nuke file to pull from. Bravo!')
                nocomp.setWindowTitle('Nuke comp check')
                nocomp.show()

            
            # if hasattr(key_shot,'child'):
            #     shot_child = key_shot.child(parent.row())
            #     checkbox = self.shotTree.itemWidget(shot_child,parent.column())
            #     if hasattr(checkbox, 'setChecked'):
            #         checkbox.setChecked(True)
            #     else:
            #         continue    



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