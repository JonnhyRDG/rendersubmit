import subprocess
import os
import sys
import json
from functools import partial
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
import rendersubmit
import project_dict
import requests
import jasondict

nukerun = '"P:/AndreJukebox/pipe/ajnuke/aj_nuke_14.bat"'
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
        super().__init__()
        # Llamamos al constructor del padre
        super(renderSubmit, self).__init__(*args, **kwargs)

        # La llamada a setupUi siempre hay que hacerla
        self.setupUi(self)

        # En caso de que queramos podemos cargar una hoja de estilo
        with open(os.path.join(os.path.dirname(__file__), 'rendersubmit_ui.qss'), "r") as f:
            self.setStyleSheet(f.read())

        # Ponemos un titulo a la ventana
        self.setWindowTitle("AJ Render Submiter v0.0.1")
        self.setWindowIcon(QIcon("P:/AndreJukebox/lib/logo/aj.ico"))

        # Nos bajamos el csv de googlesheets
        self.reload_csv()

        #Leemos el dict bakeado con la data de las secuencias/shots
        project_dict.proj_dict().dictread()
        
        # Create the dictionary for layering harvest functions
        self.functiondict()
        
        #Rellenamos los combo box de episodios y secuencias
        # self.populateCombo()

        # text for publish buttons according the userdcc data
        self.publishtexts()

        delegate = AlignDelegate(self.shotTree)
        self.shotTree.setItemDelegate(delegate)
        self.shotTree.setAlternatingRowColors(True)
        self.connect_buttons()
        self.currentseq = str(self.sequence_comboBox.currentText())
        self.layers = {'Katana':[''],'Nuke':['']}
        self.expressionbtn.setVisible(0)

    def functiondict(self):
        self.appdict = {"Katana": self.katanalayers, "Nuke": self.nukelayers}

    def layerfunc(self,func):
        func()
    
    def katanalayers(self):
        self.layerlist = []
        self.currentseq = str(self.sequence_comboBox.currentText())
        for self.shots in project_dict.proj_dict().seqsdict[self.currentseq]:
            self.shotslayer = project_dict.proj_dict().seqsdict[self.currentseq][self.shots]["layers"]
            self.singlelayers = self.shotslayer.split(",")
            for self.ly in self.singlelayers:
                if not self.ly in self.layerlist:
                    self.layerlist.append(self.ly)
        self.layers['Katana'] = self.layerlist

    def nukelayers(self):
        self.layers['Nuke'] = ['write_output']
    
    def seqlists(self):
        self.seqcombolist = ['']
        for seqs in project_dict.proj_dict().seqsdict:
            self.seqcombolist.append(seqs)
        # print(self.seqcombolist)

    def populateCombo(self):
        self.seqlists()
        self.sequence_comboBox.clear()
        self.sequence_comboBox.addItems(self.seqcombolist)
        episodes = ['concept_animatic']
        self.episode_comboBox.clear()
        self.episode_comboBox.addItems(episodes)

    def nukeshots(self):
        self.shotTree.clear()
        header = ['Shots','Output']
        self.shotTree.setHeaderLabels(header)
        self.shotTree.setColumnCount(2)
        
    def publishtexts(self):
        publishtext = {
            "Katana":"PUBLISH SHOT(s)",
            "Nuke":"PUBLISH COMP(s)"
        }
        self.publish_push.setText(publishtext[self.dcc_combo.currentText()])

    def applayerdict(self):
        self.layerdict = {'Katana':[''],'Nuke':['']}

    def checkbox_create(self,clm):
        self.check_button = QtWidgets.QCheckBox(parent=self.shotTree)
        self.shotTree.setItemWidget(self.shot_item,clm,self.check_button)


    def filtered_list(self,list1,list2):
        return list(set(list1) & set(list2))

    def hierarchy_create(self,items,headers,childlist):
        self.ml_item = QtWidgets.QTreeWidgetItem(self.shotTree, self.hierarchy[project_dict.proj_dict().seqsdict[self.currentseq][items]['type']])
        # ml_button = QtWidgets.QLabel(parent=self.shotTree)
        # # self.shotTree.setItemWidget(self.ml_item,0,ml_button)
        
        self.ml_item.setExpanded(True)
        
        for childshots in childlist:
            self.shot_item = QtWidgets.QTreeWidgetItem(self.ml_item, [childshots])

            shot_layer = project_dict.proj_dict().seqsdict[self.currentseq][childshots]["layers"]

            #dictionary with different type of lists according to the app.
            list_app = {"Katana":(self.filtered_list(shot_layer.split(","),self.layers[self.dcc_combo.currentText()])),"Nuke": self.layers[self.dcc_combo.currentText()]}
            for i in list_app[self.dcc_combo.currentText()]:
                self.layer_index = headers.index(i)
                self.checkbox_create(clm=self.layer_index)

    def createkeyshots(self):
        self.shotTree.clear()
        headers = {}
        self.currentseq = str(self.sequence_comboBox.currentText())
        icon = {
            'Nuke': QtGui.QPixmap("P:/AndreJukebox/pipe/ajbackend/rendersubmit/resources/nuke_icon.png"),
            'Katana': QtGui.QPixmap("P:/AndreJukebox/pipe/ajbackend/rendersubmit/resources/katana_icon.png")
            }
        self.publishtexts()
        self.dcc_image.setPixmap(icon[self.dcc_combo.currentText()])

        if self.dcc_combo.currentText() == "Nuke":
            self.shotTree.setColumnCount(2)

        # for anything that needs to be created when changing the seq/app now, put it under the next IF statement.
        if not self.currentseq == '':

            self.layerfunc(self.appdict[self.dcc_combo.currentText()])
            self.shotTree.setHeaderHidden(False)
            headers = ['Shots']
            unique_shots = []

            # This is where the headers for the layers are created.
            for layer in self.layers[self.dcc_combo.currentText()]:
                headers.append(layer)
            self.shotTree.setHeaderLabels(headers)

            for items in project_dict.proj_dict().seqsdict[self.currentseq]:
                self.hierarchy = {"key":[items], "child":[items],"unique":["Unique"]}
                childlist = []
                if project_dict.proj_dict().seqsdict[self.currentseq][items]['type'] == 'key':
                    for splits in (project_dict.proj_dict().seqsdict[self.currentseq][items]['childs'].rsplit(",")):
                        childlist.append(splits)
                    self.hierarchy_create(items,headers,childlist)

                elif project_dict.proj_dict().seqsdict[self.currentseq][items]['type'] == 'unique':
                    unique_shots.append(items)

            if unique_shots:
                self.hierarchy_create(items,headers,unique_shots)

        else:
            self.shotTree.clear()
            self.shotTree.setHeaderHidden(True)

    def onRender(self):
        if self.step_check.isChecked():
            self.stepson = 1
        else:
            self.stepson = 0

        if self.versio_up_checkbox.isChecked():
            self.versionup = 1
        else:
            self.versionup = 0

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
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
                    checkbox = self.shotTree.itemWidget(key_item.child(child_index), j+1)
                    if checkbox and checkbox.isChecked():
                        layer = self.layers[self.dcc_combo.currentText()][j]
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
        argdict['version']=self.versionup
        argdict['mode']=str(self.mode_combo.currentText())
        argdict['res']=str(self.res_combo.currentText())
        argdict['sampling']=str(self.sampling_combo.currentText())
        
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
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    if hasattr(checkbox, 'setChecked'):
                        checkbox.setChecked(True)
                
    def disableAll(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    if hasattr(checkbox, 'setChecked'):
                        checkbox.setChecked(False)

    def enableKeys(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        keyshot = []
        for keyshots in project_dict.proj_dict().seqsdict[self.currentseq]:
            if project_dict.proj_dict().seqsdict[self.currentseq][keyshots]['type'] == 'key':
                keyshot.append(keyshots)
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                shotname = key_shots.child(child_index).text(0)
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    if hasattr(checkbox, 'setChecked'):
                        checkbox.setChecked(False)
                    if shotname in keyshot:
                        if hasattr(checkbox, 'setChecked'):
                            checkbox.setChecked(True)
                    else:
                        continue


    def enableUniques(self):
        root = self.shotTree.invisibleRootItem()
        key_count = root.childCount() #rows
        keyshot = []
        for keyshots in project_dict.proj_dict().seqsdict[self.currentseq]:
            if project_dict.proj_dict().seqsdict[self.currentseq][keyshots]['type'] == 'unique':
                keyshot.append(keyshots)
        for shot_count in range(key_count):
            key_shots = root.child(shot_count)
            child_count = key_shots.childCount()
            for child_index in range(child_count):
                shotname = key_shots.child(child_index).text(0)
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
                    checkbox = self.shotTree.itemWidget(key_shots.child(child_index),j+1)
                    if hasattr(checkbox, 'setChecked'):
                        checkbox.setChecked(False)
                    if shotname in keyshot:
                        if hasattr(checkbox, 'setChecked'):
                            checkbox.setChecked(True)

    def framesui(self):
        self.expressionbtn.setVisible(0)
        if self.frame_combo.currentText() == "Expression":# and self.frames_layout.count() == 0:
            self.expressionbtn.setVisible(1)
        else:
            if self.expressionbtn:
                self.expressionbtn.setVisible(0)

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
            for j in range(len(self.layers[self.dcc_combo.currentText()])):
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
                for j in range(len(self.layers[self.dcc_combo.currentText()])):
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
        self.reload_push.clicked.connect(self.reload_csv)
        self.enableall_push.clicked.connect(self.enableAll)
        self.disableall_push.clicked.connect(self.disableAll)
        self.enablekeys_push.clicked.connect(self.enableKeys)
        self.frame_combo.currentIndexChanged.connect(self.framesui)
        self.step_check.clicked.connect(self.stepspin)
        self.clearsel_push.clicked.connect(self.clearselected)
        self.enableunique_push.clicked.connect(self.enableUniques)
        self.dcc_combo.currentIndexChanged.connect(self.createkeyshots)
        
        
    def pullKeyComp(self,selmodel):
        root = self.shotTree.invisibleRootItem()
        for parent in selmodel:
            key_shot = root.child(parent.parent().row())
            nukefile = f'P:/AndreJukebox/seq/{self.currentseq}/{key_shot.text(0)}/comp/workfile.nk'
            if os.path.isfile(nukefile):
                print('keys=',key_shot.text(0))
                child_count = key_shot.childCount()
                for childs in range(child_count):
                    children = key_shot.child(childs)
                    if project_dict.proj_dict().seqsdict[self.currentseq][children.text(0)]['type'] != 'key':
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

        pullcomp_done = QtWidgets.QMessageBox(parent=self.shotTree,text='Comps has been pulled from parent')
        pullcomp_done.setWindowTitle('Comp check')
        pullcomp_done.show()
        print('[[[PULL DONE]]]')

    def reload_csv(self):
        self.shotTree.clear()
        def getGoogleSeet(self,fileId, outDir, outFile):
  
            url = f'https://docs.google.com/spreadsheets/d/{fileId}/export?format=csv'
            self.response = requests.get(url)
            if self.response.status_code == 200:
                self.filepath = os.path.abspath(os.path.join(outDir, outFile))
                with open(self.filepath, 'wb') as f:
                    f.write(self.response.content)
                    print('CSV file saved to: {}'.format(self.filepath))    
            else:
                print(f'Error downloading Google Sheet: {self.response.status_code}')

        self.aj_seq_data_id = '1iH0H03bc48dr9Z6MQ5St-5dsiZZLiLvNPuZY_7LVb7o'
        self.aj_asset_data_id = '1_ijIUsmpBBhXnPV4l9ospjbaArNJQn_5Dvn1FRcC6r4'

        self.outDir = 'P:/AndreJukebox/'
        self.seqfile = 'aj_seq_data.csv'
        self.assetfile = 'aj_asset_data.csv'

        getGoogleSeet(self,self.aj_seq_data_id,self.outDir, self.seqfile)
        getGoogleSeet(self,self.aj_asset_data_id,self.outDir, self.assetfile)
        # jasondict.json_exp().seqsdict = {}
        jasondict.json_exp().seqsdict_export()
        jasondict.json_exp().assetdict_export()
        # project_dict.proj_dict().reload()
        project_dict.proj_dict().dictread

        self.populateCombo()
        self.createkeyshots()
        


def main():
    # Creamos nuestra aplicacion
    app = QtWidgets.QApplication(sys.argv)

    # Creamos nuestro widget y lo mostramos.
    widget = renderSubmit()
    widget.show()   

    # Ejecutamos la aplicacion
    app.exec_()

if __name__ == '__main__':
    main()