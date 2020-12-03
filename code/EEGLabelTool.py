from sys import argv, exit
import json
from os.path import dirname, basename, exists
from numpy import ones, arange
from pandas import DataFrame, read_csv
from pandas.core import frame
from scipy import signal
from PyQt5.QtCore import QThread, pyqtSignal, QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QInputDialog,QTableWidgetItem,QMessageBox,QMenu
from pyqtgraph import InfiniteLine, LabelItem, mkPen, SignalProxy, LinearRegionItem
from Ui_MainUi import Ui_MainWindow
from SettingDialog import SettingDialog
from SavingDialog import SavingDialog
from EDFreader import EDFreader

class LoadThread(QThread):
    loadFinished = pyqtSignal(frame.DataFrame)
    def __init__(self, path):
        super(LoadThread, self).__init__()
        self.path = path

    def run(self):
        edfReader = EDFreader(filepath=self.path)
        Data = edfReader.OriginalData
        self.loadFinished.emit(Data)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.initComBox()

        self.setCentralWidget(self.ui.mainWidget_2)
        self.ui.splitter_2.setStretchFactor(0, 10)
        self.ui.splitter_2.setStretchFactor(1, 4)
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 6)
        self.ui.splitter.setStretchFactor(2, 3)

        self.ui.tableSetting.setColumnWidth(0, 100)
        self.ui.tableSetting.setColumnWidth(1, 100)
        self.ui.tableSetting.setColumnWidth(2, 80)
        self.ui.tableLabel.setColumnWidth(0, 35)
        self.ui.tableLabel.setColumnWidth(1, 160)
        self.ui.tableLabel.setColumnWidth(2, 120)
        self.ui.tableLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableLabel.customContextMenuRequested.connect(self.tabelMenu)

        self.ui.actionOpen.triggered.connect(self.OpenFile)
        self.ui.actionSave.triggered.connect(self.SaveLabel)
        self.ui.addNewLabel.clicked.connect(self.add)
        self.ui.deleteLabel.clicked.connect(self.delete)
        self.ui.saveSetting.clicked.connect(self.saveSetting)
        self.ui.removeLabel.clicked.connect(self.removeLabel)

        self.filepath = None
        self.OriginalData = None
        self.ProcessedData = None
        self.ShowData = None
        self.labelNameList = []
        self.labelValueList = []
        self.labels = None
        self.labelTypes = None
        self.labelColors = None

        self.items = []
        self.items2color = {}

        self.filename = None
        self.Age = (0,0)
        self.gender = "无"
        self.text = "无"
        self.length = 0
        self.label_num = 0
        self.label_types = None

        self.chns_hl_list = [False] * 24
        self.ui.label_1.clicked.connect(self.highlightDraw)
        self.ui.label_2.clicked.connect(self.highlightDraw)
        self.ui.label_3.clicked.connect(self.highlightDraw)
        self.ui.label_4.clicked.connect(self.highlightDraw)
        self.ui.label_5.clicked.connect(self.highlightDraw)
        self.ui.label_6.clicked.connect(self.highlightDraw)
        self.ui.label_7.clicked.connect(self.highlightDraw)
        self.ui.label_8.clicked.connect(self.highlightDraw)
        self.ui.label_9.clicked.connect(self.highlightDraw)
        self.ui.label_10.clicked.connect(self.highlightDraw)
        self.ui.label_11.clicked.connect(self.highlightDraw)
        self.ui.label_12.clicked.connect(self.highlightDraw)
        self.ui.label_13.clicked.connect(self.highlightDraw)
        self.ui.label_14.clicked.connect(self.highlightDraw)
        self.ui.label_15.clicked.connect(self.highlightDraw)
        self.ui.label_16.clicked.connect(self.highlightDraw)
        self.ui.label_17.clicked.connect(self.highlightDraw)
        self.ui.label_18.clicked.connect(self.highlightDraw)
        self.ui.label_19.clicked.connect(self.highlightDraw)
        self.ui.label_20.clicked.connect(self.highlightDraw)
        self.ui.label_21.clicked.connect(self.highlightDraw)
        self.ui.label_22.clicked.connect(self.highlightDraw)
        self.ui.label_23.clicked.connect(self.highlightDraw)
        self.ui.label_24.clicked.connect(self.highlightDraw)

        self.Sens = int(self.ui.cb_sens.currentText()[:-2])
        self.HF = int(self.ui.cb_HF.currentText()[:-2])
        self.Pat = self.ui.cb_Pat.currentText()
        self.placement = int(self.ui.cb_TC.currentText())
        self.Screen = 10000
        self.location = self.ui.Slider.value()
        self.windowIndex = self.getwindowIndex()
        

        self.ui.cb_Screen.currentTextChanged.connect(lambda:self.changeScreen(self.ui.cb_Screen))
        self.ui.cb_HF.currentTextChanged.connect(lambda:self.changeHF(self.ui.cb_HF))
        self.ui.cb_Pat.currentTextChanged.connect(lambda:self.changePat(self.ui.cb_Pat))
        self.ui.cb_sens.currentTextChanged.connect(lambda:self.changeSens(self.ui.cb_sens))
        self.ui.cb_TC.currentTextChanged.connect(lambda:self.changePlacement(self.ui.cb_TC))

        self.ui.Slider.valueChanged.connect(lambda:self.changeLocation(self.ui.Slider))
        
        self.ui.Back.clicked.connect(self.backLoc)
        self.ui.Go.clicked.connect(self.goLoc)
        self.ui.Start.clicked.connect(self.startLoc)
        self.ui.End.clicked.connect(self.endLoc)
        self.ui.Reset.clicked.connect(self.resetLabelGraph)

        self.ui.MainGraph.setBackground(background = '#000000')
        self.vLine = InfiniteLine(angle=90, movable=False)
        self.hLine = InfiniteLine(angle=0, movable=False)
        self.initGraph()
        
        self.ui.LabelGraph.setBackground(background = '#000000')
        self.initLabelGraph()

        self.initPathCache()
        self.initLabelSetting()
        self.initSettingTable()
        self.changeLabelDialog()

    def highlightDraw(self, Name, hl):
        loc = int(Name[6:])
        self.chns_hl_list[loc-1] = hl
        self.draw()


    def initPathCache(self):
        f = open('pathcache.txt', encoding='utf-8')
        for s in f.readlines():
            self.openPathCache = s + '/'
            self.savePathCache = s + '/'
        return None

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
                                    '本程序',
                                    "是否要退出程序？",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.saveSetting()
            event.accept()
        else:
            event.ignore()

    def SaveLabel(self):
        self.initPathCache()
        self.initSave()

        if self.ui.spinYear.value() == 0 and self.ui.spinMonth.value() == 0:
            QMessageBox.critical(self,'警告','请添加该样本的年龄信息')
            return None
        if (not self.ui.rBmale.isChecked()) and (not self.ui.rBfemale.isChecked()):
            QMessageBox.critical(self,'警告','请添加该样本的性别信息')
            return None
        
        # dialog = SavingDialog()
        dialog = SavingDialog(filename = self.filename,
                            age = self.Age,
                            gender = self.gender,
                            l = self.length,
                            text = self.text,
                            num = self.label_num,
                            types = self.label_types)
        # dialog.setWindowModality(Qt.ApplicationModal)
        output = dialog.exec()
        if output:
            filename, kk = QFileDialog.getSaveFileName(self, '保存文件', self.savePathCache+self.filename[:-4]+'.json', '文本文件(*.json)')
            if filename:
                label_info = {"filename":self.filename,
                            "Age":("{}岁{}个月".format(self.Age[0],self.Age[1]),self.Age),
                            "Gender":self.gender,
                            "Signal length":self.length,
                            "Diagnosis text":self.text,
                            "Label number":self.label_num,
                            "Label types":self.label_types,
                            "LabelName":self.labelNameList,
                            "LabelIndex":self.labelValueList}
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(json.dumps(label_info, ensure_ascii=False,indent=4,separators=(',',':')))
        else:
            return None

    def initSave(self):
        self.filename = basename(self.filepath)
        self.Age = (self.ui.spinYear.value(), self.ui.spinMonth.value())
        self.gender = "无"
        if self.ui.rBmale.isChecked():
            self.gender = "男"
        else:
            self.gender = "女"
        self.text = self.ui.textEdit.toPlainText()
        self.length = self.OriginalData.shape[0]/1000
        self.label_num = int(len(self.labelValueList)/2)
        self.label_types = list(set([label[:-4] for label in self.labelNameList if label[-3:] == "end"]))


    def changePathCache(self, path):
        fh = open('pathcache.txt', 'r', encoding='utf-8')
        pathList = [f for f in fh.readlines()]

        fh = open('pathcache.txt', 'w', encoding='utf-8')
        
        fh.write(path)
        fh.close()

    def tabelMenu(self, pos):
        for i in self.ui.tableLabel.selectionModel().selection().indexes():
            rowNum = i.row()

        menu = QMenu()
        item1 = menu.addAction("定位")
        item2 = menu.addAction("删除")
        screenPos = self.ui.tableLabel.mapToGlobal(pos)
        action = menu.exec(screenPos)
        if action == item1:
            loc = int(max(0,self.labelValueList[rowNum] - self.Screen/2/1000)*1000)
            self.ui.Slider.setValue(loc)
        elif action == item2:
            self.ui.tableLabel.removeRow(rowNum)
            del self.labelNameList[rowNum]
            del self.labelValueList[rowNum]
            self.draw()
            self.drawLabel()

    def removeLabel(self):
        ok = QMessageBox.question(self,'确认','您确认要清除所有标注吗？',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ok == QMessageBox.Yes:
            self.ui.tableLabel.clearContents()
            self.ui.tableLabel.setRowCount(0)
            self.labelNameList = []
            self.labelValueList = []
            self.draw()
            self.drawLabel()
        else:
            return

    def initLabelSetting(self):
        setting = read_csv("LabelSetting.txt", sep='\t')
        self.labels = list(setting['Names'].values)
        self.labelTypes = list(setting['Types'].values)
        self.labelColors = [eval(color) for color in setting['Colors'].values]

    def initSettingTable(self):
        i = 0
        self.ui.tableSetting.clearContents()
        for label, labeltype, color in zip(self.labels, self.labelTypes, self.labelColors):
            labelItem = QTableWidgetItem(label)
            typeItem = QTableWidgetItem(labeltype)
            colorItem = QTableWidgetItem(' ')
            colorItem.setBackground(QBrush(QColor(*color)))
            self.ui.tableSetting.setItem(i,0,labelItem)
            self.ui.tableSetting.setItem(i,1,typeItem)
            self.ui.tableSetting.setItem(i,2,colorItem)
            i = i + 1
        
    def changeLabelDialog(self):
        self.items = []
        self.items2color = {}
        for label, tp, color in zip(self.labels, self.labelTypes, self.labelColors):
            if tp == '区间标签':
                self.items.append(label+'-start')
                self.items.append(label+'-end')
                self.items2color[label+'-start'] = color
                self.items2color[label+'-end'] = color
            elif tp == '点标签':
                self.items.append(label)
                self.items2color[label] = color
        
    def add(self):
        dialog = SettingDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        
        output = dialog.exec()
        if output:
            self.labelColors.append(dialog.NewLabelColor)
            self.labels.append(dialog.NewLabelName)
            self.labelTypes.append(dialog.LabelType)
            self.initSettingTable()
            self.changeLabelDialog()

    def delete(self):
        items = self.ui.tableSetting.selectedIndexes()
        deleteIndex = []
        finalIndex = []

        for i in range(0,len(items),3):
            deleteIndex.append(items[i].row())
        
        for i in deleteIndex:
            logic = self.labels[i] in self.labelNameList or\
                    self.labels[i]+'-end' in self.labelNameList or\
                    self.labels[i]+'-start' in self.labelNameList
            if logic:
                QMessageBox.critical(self,'警告','该标签已在信号上标注，不能删除')
            else:
                finalIndex.append(i)
        self.labels = [label for i, label in enumerate(self.labels) if i not in finalIndex]
        self.labelColors = [color for i, color in enumerate(self.labelColors) if i not in finalIndex]
        self.labelTypes = [tp for i, tp in enumerate(self.labelTypes) if i not in finalIndex]
        self.initSettingTable()
        self.changeLabelDialog()

    def saveSetting(self):
        setting_dict = {'Names': self.labels, 'Types':self.labelTypes, 'Colors':self.labelColors}
        setting = DataFrame(setting_dict)
        setting.to_csv('LabelSetting.txt', sep='\t', index=False)


    def changePat(self, cb):
        self.Pat = cb.currentText()
        self.patternChoosen()
        self.draw()
    def changePlacement(self, cb):
        self.placement = int(cb.currentText())
        self.draw()
    def changeScreen(self, cb):
        text = cb.currentText()
        value = 0
        if text[-1] == 's':
            value = int(float(text[:-1]) * 1000)
        elif text[-1] == 'm':
            value = int(text[:-1]) * 1000 * 60
        self.Screen = value
        self.windowIndex = self.getwindowIndex()
        self.sliderSetting()
        self.draw()
    def changeHF(self, cb):
        self.HF = int(cb.currentText()[:-2])
        self.eegFilter()
        self.patternChoosen()
        self.draw()
    def changeSens(self, cb):
        self.Sens = int(cb.currentText()[:-2])
        self.draw()
    def changeLocation(self, slider):
        self.location = slider.value()
        self.windowIndex = self.getwindowIndex()
        self.draw()
        self.drawLabel()
    def getwindowIndex(self):
        return [self.location, self.location+self.Screen]

    def sliderSetting(self):
        self.ui.Slider.setMaximum(self.OriginalData.shape[0]-self.Screen)
        self.ui.Slider.setSingleStep(int(self.Screen/4))
        self.ui.Slider.setPageStep(int(self.Screen/4))

    def backLoc(self):
        self.ui.Slider.setValue(self.ui.Slider.value() - int(self.Screen/3))
    def goLoc(self):
        self.ui.Slider.setValue(self.ui.Slider.value() + int(self.Screen/3))
    def startLoc(self):
        self.ui.Slider.setValue(0)
    def endLoc(self):
        self.ui.Slider.setValue(self.OriginalData.shape[0] - self.Screen)
    def resetLabelGraph(self):
        self.p2.setXRange(0, self.ShowData.shape[0]/1000)
        self.draw()

    def initComBox(self):
        self.ui.cb_sens.addItems(['500uV', '300uV', '200uV', '150uV', '100uV',
                                 '75uV', '50uV', '30uV', '20uV', '15uV', '10uV',
                                 '7uV', '5uV', '3uV', '2uV', '1uV'])
        self.ui.cb_sens.setCurrentIndex(6)

        self.ui.cb_HF.addItems(['15Hz', '30Hz', '35Hz', '50Hz', '60Hz', '70Hz', '120Hz', '300Hz'])
        self.ui.cb_HF.setCurrentIndex(5)

        self.ui.cb_TC.addItems(['60', '120', '240', '360', '480',
                                 '960', '1200', '1600'])
        self.ui.cb_TC.setCurrentIndex(1)

        self.ui.cb_Pat.addItems(['Original','新平均导联'])
        self.ui.cb_Pat.setCurrentIndex(1)

        self.ui.cb_Screen.addItems(['0.1s', '0.2s', '0.5s', '1s', '2s', '5s', '10s',
                                     '15s', '20s', '30s', '60s', '2m', '3m', '5m'])
        self.ui.cb_Screen.setCurrentIndex(6)

    def OpenFile(self):
        self.initPathCache()
        fname,_ = QFileDialog.getOpenFileName(self,'打开文件',self.openPathCache,'EDF文件(*.edf)')
        if fname:
            self.changePathCache(dirname(fname))
            self.filepath = fname
            label_path = fname[:-4]+".json"
            self.ui.Slider.setValue(0)
            if exists(label_path):
                with open(label_path, mode='r', encoding='utf-8') as f:
                    label_info = json.load(f)
                    self.filename = label_info['filename']
                    self.Age = label_info['Age'][1]
                    self.gender = label_info['Gender']
                    self.text = label_info['Diagnosis text']
                    self.length = label_info['Signal length']
                    self.label_num = label_info['Label number']
                    self.label_types = label_info['Label types']
                    self.labelNameList = label_info['LabelName']
                    self.labelValueList = label_info['LabelIndex']
                self.initLabelInfo()
            else:
                self.ui.tableLabel.clearContents()
                self.labelNameList = []
                self.labelValueList = []
                self.filename = None
                self.Age = (0,0)
                self.gender = "无"
                self.text = "无"
                self.length = 0
                self.label_num = 0
                self.label_types = None
                self.initLabelInfo()

            self.backend = LoadThread(self.filepath)
            self.backend.loadFinished.connect(self.loadOver)
            self.backend.start()


    def initLabelInfo(self):
        self.ui.spinYear.setValue(self.Age[0])
        self.ui.spinMonth.setValue(self.Age[1])
        if self.gender == "男":
            self.ui.rBmale.setChecked(True)
        elif self.gender == "女":
            self.ui.rBfemale.setChecked(True)
        elif self.gender == "无":
            self.ui.rBfemale.setCheckable(False)
            self.ui.rBfemale.setCheckable(True)
            self.ui.rBmale.setCheckable(False)
            self.ui.rBmale.setCheckable(True)
        self.ui.textEdit.setText(self.text)

        self.ui.tableLabel.setRowCount(len(self.labelValueList))
        i = 0
        for label, index in zip(self.labelNameList, self.labelValueList):
            
            labelItem = QTableWidgetItem(label)
            valueItem = QTableWidgetItem()
            valueItem.setData(Qt.DisplayRole, index)
            color = self.items2color[label]
            colorItem = QTableWidgetItem()
            if label[-3:] == "end":
                colorItem.setIcon(QIcon("./image/e.png"))
            elif label[-5:] == "start":
                colorItem.setIcon(QIcon("./image/s.png"))
            else:
                colorItem.setIcon(QIcon("./image/point.png"))
            colorItem.setBackground(QColor(*color))
            self.ui.tableLabel.setItem(i,1,labelItem)
            self.ui.tableLabel.setItem(i,2,valueItem)
            self.ui.tableLabel.setItem(i,0,colorItem)
            self.ui.tableLabel.sortItems(2, Qt.AscendingOrder)
            i = i+1

    def loadOver(self, data):
        self.OriginalData = data
        self.ProcessedData = self.OriginalData.copy(deep = True)
        self.p2.setXRange(0, self.ShowData.shape[0]/1000)
        self.eegFilter()
        self.patternChoosen()
        self.sliderSetting()
        self.draw()
        self.drawLabel()

    def initGraph(self):
        self.ShowData = ones((10000))
        self.label = LabelItem(justify = "right")
        self.ui.MainGraph.addItem(self.label)
        self.plt = self.ui.MainGraph.addPlot(row=1, col=0)
        self.plt.plot(y = self.ShowData, pen=mkPen(color='r', width=1.0))
        self.plt.showAxis("left", False)
        self.plt.showGrid(x=True, y=True)
        self.plt.addItem(self.vLine, ignoreBounds=True)
        # self.plt.addItem(self.hLine, ignoreBounds=True)
        
        self.vb = self.plt.vb
        self.proxy = SignalProxy(self.plt.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.proxy2 = SignalProxy(self.plt.scene().sigMouseClicked, slot=self.mouseClicked)

    def initLabelGraph(self):
        self.p2 = self.ui.LabelGraph.addPlot(row=0, col=0)
        self.p2.setXRange(0, self.ShowData.shape[0])
        self.p2.showAxis("left", False)
        self.lr = LinearRegionItem(self.windowIndex, pen='w', brush=[255,246,143,60])
        self.lr.setMovable(False)

    def draw(self):
        N, n = self.ShowData.shape
        columns = self.ShowData.columns

        start_time, end_time = max(self.windowIndex[0], 0), min(self.windowIndex[1], N - 1)
        self.plt.clear()
        self.plt.setMouseEnabled(x=True, y=False)
        self.plt.enableAutoRange(x=False, y=True)
        self.plt.setXRange(start_time/1000, end_time/1000)
        self.plt.addItem(self.vLine, ignoreBounds=True)
        # self.plt.addItem(self.hLine, ignoreBounds=True)

        i = 0
        x = arange(start_time, end_time)/1000.0
        for col, hl in zip(list(columns[::-1]), self.chns_hl_list[::-1]):
            if col in ["X1", "X2", "X3", "X4", "X5"]:
                ratio = 40.0 / self.Sens
                placement = self.placement
            elif col in ["X5"]:
                ratio = 20.0 / self.Sens
                placement = self.placement
            else:
                placement = self.placement
                ratio = 50.0 / self.Sens
            y = self.ShowData[col][start_time:end_time] * ratio + i * placement
            if col == "X5":
                y = y * 0.15
            color = "#ffffff"
            wid = 1.0
            if hl == True:
                color = "#ffff00"
                wid = 1.5
            self.plt.plot(x = x, y = y, pen=mkPen(color=color, width=wid))
            i += 1
        
        j = 0

        for item, value in zip(self.labelNameList, self.labelValueList):
            
            if value >= self.windowIndex[0]/1000.0 and value <= self.windowIndex[1]/1000.0:
                exec("vLine{} = InfiniteLine(angle=90, pen=mkPen({}, width=1.5),\
                     movable=False, label='{}')".format(j,self.items2color[item],item))
                exec("self.plt.addItem(vLine{})".format(j))
                exec("vLine{}.setPos({})".format(j, value))
            j = j + 1

        region = [start_time/1000, end_time/1000]
        self.lr.setRegion(region)
        self.p2.addItem(self.lr)

        message = "File <" + basename(self.filepath) + "> was viewed from " + str(min(x)) + "s to " + str(max(x)) + \
            "s with " + "【HF】=" + str(self.HF) + "Hz; 【Sens】=" + str(self.Sens) + "uV; 【Pat】 is \"" + self.Pat + "\""
        self.ui.statusbar.showMessage(message)

    def drawLabel(self):
        j = 0
        
        region = [self.windowIndex[0]/1000, self.windowIndex[1]/1000]
        self.p2.setXRange(region[0], region[1])
        self.p2.clear()
        self.lr.setRegion(region)
        self.p2.addItem(self.lr)
        
        for item, value in zip(self.labelNameList, self.labelValueList):
            exec("vLine2{} = InfiniteLine(angle=90, pen=mkPen({}, width=1.5),\
                    movable=False, label='{}')".format(j,self.items2color[item],item))
            exec("self.p2.addItem(vLine2{})".format(j))
            exec("vLine2{}.setPos({})".format(j, value))
            j = j + 1

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plt.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.label.setText("<span style='font-size: 14pt; color: white'> t = %0.2f s  y = %0.2f </span>"% (mousePoint.x(), mousePoint.y()))
            self.vLine.setPos(mousePoint.x())
    
    def mouseClicked(self, evt):
        pos = QPointF(evt[0].scenePos())
        mousePoint = self.vb.mapSceneToView(pos)
        
        item, ok =QInputDialog.getItem(self,'请选择标记类型','类别列表',self.items)
        if ok and item:
            self.labelNameList.append(item)
            self.labelValueList.append(round(mousePoint.x(),3))
            self.draw()
            self.drawLabel()
            numRow = len(self.labelValueList)
            self.ui.tableLabel.setRowCount(numRow)
            labelItem = QTableWidgetItem(self.labelNameList[-1])
            valueItem = QTableWidgetItem()
            valueItem.setData(Qt.DisplayRole, self.labelValueList[-1])
            color = self.items2color[self.labelNameList[-1]]
            colorItem = QTableWidgetItem()
            if self.labelNameList[-1][-3:] == "end":
                colorItem.setIcon(QIcon("./image/e.png"))
            elif self.labelNameList[-1][-5:] == "start":
                colorItem.setIcon(QIcon("./image/s.png"))
            else:
                colorItem.setIcon(QIcon("./image/point.png"))
            colorItem.setBackground(QColor(*color))
            self.ui.tableLabel.setItem(numRow-1,1,labelItem)
            self.ui.tableLabel.setItem(numRow-1,2,valueItem)
            self.ui.tableLabel.setItem(numRow-1,0,colorItem)
            self.ui.tableLabel.sortItems(2, Qt.AscendingOrder)


    def patternChoosen(self):
        self.ShowData = self.ProcessedData.copy(deep = True)
        self.ShowData.drop(['A1', 'A2'], axis = 1, inplace = True)
        if self.Pat == 'Original':
            pass
        elif self.Pat == '新平均导联':
            av = (self.ProcessedData['A1'].values + self.ProcessedData['A2'].values)/2.0
            self.ShowData[self.ShowData.columns[:19]] = self.ShowData[self.ShowData.columns[:19]].apply(lambda x: x - av, axis = 0)

    def eegFilter(self):
        data = self.OriginalData.values
        columns = self.ProcessedData.columns
        if self.HF == 300:
            self.ProcessedData = self.OriginalData.copy(deep = True)
        else:
            data = data[:,:21].T
            filtedData = self._band_pass_filter(LowHz=0.5, HigHz=self.HF, data=data)
            self.ProcessedData[columns[:21]] = filtedData.T

    def _band_pass_filter(self, LowHz, HigHz, data):
        hf = HigHz * 2.0 / 1000
        lf = LowHz * 2.0 / 1000
        N = 2
        b, a = signal.butter(N, [lf, hf], "bandpass")
        filted_data = signal.filtfilt(b, a, data)
        return filted_data


if __name__=="__main__":
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
