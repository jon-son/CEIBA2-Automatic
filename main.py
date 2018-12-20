#-coding:utf-8
from PyQt5.QtCore import Qt,QThread,QMutex,QMutexLocker
from PyQt5 import QtCore, QtWidgets
import PyQt5.sip  #得加这个不然用pyinstaller打包exe时会出现 no module name pyqt5.sip的问题
import api
import sys,time
from home import Ui_Home
class msgThread(QThread):
    trigger = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(msgThread, self).__init__(parent)
    def run_(self, message):
        self.trigger.emit(message)

class startThread(QThread):
    trigger = QtCore.pyqtSignal(str)
    def __init__(self, UI):
        super(startThread, self).__init__()
        self.stoped = False
        self.mutex = QMutex()

        self.path = UI.lineEdit.text()
        self.line1 = UI.lineEdit_1.text()
        self.line2 = UI.lineEdit_2.text()
        self.line3 = UI.lineEdit_3.text()
        self.line4 = UI.lineEdit_4.text()
        self.line5 = UI.lineEdit_5.text()
        self.line6 = UI.lineEdit_6.text()
        self.line7 = UI.lineEdit_7.text()
        self.line8 = UI.lineEdit_8.text()
        self.list = UI.list.isChecked()
        self.error = UI.error.isChecked()
        self.person = UI.person.isChecked()
        self.five = UI.five.isChecked()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False

        if self.line1 == "" or self.line2 == "" \
                or self.line3 == "" or self.line4 == "" or self.line5 == "" \
                or self.line6 == "" or self.line7 == "" or self.line8 == "":

            self.trigger.emit("坐标为空")
        elif self.path == "":
            self.trigger.emit("工作目录为空")
        else:
            type = ""
            dirPath = self.path
            positions = []
            positions = api.addPos(self.line1, positions)
            positions = api.addPos(self.line2, positions)
            positions = api.addPos(self.line3, positions)
            positions = api.addPos(self.line4, positions)
            positions = api.addPos(self.line5, positions)
            positions = api.addPos(self.line6, positions)
            positions = api.addPos(self.line7, positions)
            positions = api.addPos(self.line8, positions)

            if self.list:
                self.trigger.emit("视频类型：list")
                type = "list"
            if self.error:
                self.trigger.emit("视频类型：error")
                type = "error"
            if self.person:
                self.trigger.emit("视频类型：行人检测")
                type = "person"
            if self.five:
                self.trigger.emit("视频类型：小五专用")
                type = "five"
            self.trigger.emit("工作目录：" + dirPath)
            self.trigger.emit("视频剪辑坐标：(" + str(positions[0][0]) + "," + str(positions[0][1]) + ")")
            self.trigger.emit("确定按钮坐标：(" + str(positions[1][0]) + "," + str(positions[1][1]) + ")")
            self.trigger.emit("保存路径坐标：(" + str(positions[2][0]) + "," + str(positions[2][1]) + ")")
            self.trigger.emit("开始时间坐标：(" + str(positions[3][0]) + "," + str(positions[3][1]) + ")")
            self.trigger.emit("结束时间坐标：(" + str(positions[4][0]) + "," + str(positions[4][1]) + ")")
            self.trigger.emit("转AVI坐标：(" + str(positions[5][0]) + "," + str(positions[5][1]) + ")")
            self.trigger.emit("新任务坐标：(" + str(positions[6][0]) + "," + str(positions[6][1]) + ")")
            self.trigger.emit("剪辑开始坐标：(" + str(positions[7][0]) + "," + str(positions[7][1]) + ")")

            files = api.fileList(dirPath, 2)
            txtstr = []
            f = open(dirPath + "\\" + files[0], encoding='gb18030', errors='ignore')
            get = f.read()
            result = get.split('\n')
            f.close()
            if type == "five":
                for i in range(0, len(result)):
                    if result[i] != '':
                        txtstr.append(result[i].split(" ")[0])

                for j in range(0, len(txtstr)):
                    while self.stoped:
                        time.sleep(1)
                    times = []
                    time1 = txtstr[j].split("-")[0]
                    time2 = txtstr[j].split("-")[1]
                    temp = ""
                    for k in range(0,len(time1)):
                        if k%2==0 and k>0:
                            temp+=":"
                        temp+=time1[k]
                    times.append(temp)
                    temp = ""
                    for l in range(0,len(time2)):
                        if l%2==0 and l>0:
                            temp+=":"
                        temp+=time2[l]
                    times.append(temp)
                    scr = api.getScreenshot(positions[6][0], positions[6][1])
                    self.trigger.emit("开始转换AVI格式：" + txtstr[j])
                    self.trigger.emit("time：" + times[0] + "-" + times[1])
                    api.doAVI(positions,dirPath ,times, scr)
                    self.trigger.emit("AVI格式转换完成：" + txtstr[j])


            else:
                for i in range(0, len(result)):
                    if result[i] != '':
                        flag = api.mkdir(dirPath + "\\" + result[i].split(" ")[0])
                        if flag == 1:
                            self.trigger.emit(result[i].split(" ")[0] + "目录新建成功")
                            txtstr.append(result[i].split(" ")[0])
                        elif flag == 2:
                            self.trigger.emit(result[i].split(" ")[0] + "目录已存在，请查证")

                for j in range(0, len(txtstr)):
                 
                    while self.stoped:
                        time.sleep(1)
                    times = api.splitTime(txtstr[j], type)
                
                    scr = api.getScreenshot(positions[6][0], positions[6][1])
    
                    self.trigger.emit("开始剪辑：" + txtstr[j])
                    self.trigger.emit("time：" + times[0] + "-" + times[1])
                    api.doWork(dirPath, positions, txtstr[j], times, scr)
                    self.trigger.emit("剪辑完成：" + txtstr[j])
                    while self.stoped:
                        time.sleep(1)
                    self.trigger.emit("开始转换AVI格式：" + txtstr[j])
                    self.trigger.emit("time：" + times[0] + "-" + times[1])
                    api.doAVI(positions,"", times, scr)
                    self.trigger.emit("AVI格式转换完成：" + txtstr[j])
        self.trigger.emit("startDone")

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
    def recovery(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stoped





#有问题，以后再改
# class checkThread(QThread):
#     trigger = QtCore.pyqtSignal(str)
#     def __init__(self, UI):
#         super(checkThread, self).__init__()
#         self.stoped = False
#         self.mutex = QMutex()
#
#         self.path = UI.lineEdit.text()
#         self.list = UI.list.isChecked()
#         self.error = UI.error.isChecked()
#         self.person = UI.person.isChecked()
#         self.five = UI.five.isChecked()
#     def run(self):
#         with QMutexLocker(self.mutex):
#             self.stoped = False
#
#         if self.stoped:
#             return
#         error = []
#         errorAVI = []
#         type = ""
#         dirPath = self.path
#         if self.path == "":
#             self.trigger.emit("工作目录为空")
#         else:
#             if self.list:
#                 type = "list"
#             if self.error:
#                 type = "error"
#             if self.person:
#                 type = "person"
#             if self.five:
#                 type = "five"
#             if type == "five":
#                 self.trigger.emit("小五专用不能检查视频")
#             else:
#                 dirs = api.fileList(dirPath, 1)
#                 for dir in dirs:
#                     self.trigger.emit("开始检查：" + dir)
#                     flag = api.check(dirPath + "\\" + dir, type)
#                     flagAVI = api.checkAVI(dirPath + "\\" + dir, type)
#                     if flag == False:
#                         error.append(dir)
#                     if flagAVI == False:
#                         errorAVI.append(dir)
#                 for err in error:
#                     self.trigger.emit("剪辑出错：" + err)
#                 for errAVI in errorAVI:
#                     self.trigger.emit("格式转换出错：" + errAVI)
#         self.trigger.emit("checkDone")
#
#     def stop(self):
#         with QMutexLocker(self.mutex):
#             self.stoped = True
#
#     def isStoped(self):
#         with QMutexLocker(self.mutex):
#             return self.stoped

class mywindow(QtWidgets.QWidget,Ui_Home):

    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.toolButton.clicked.connect(self.choseDir)
        self.threads = msgThread(self)
        self.threads.trigger.connect(self.update_text)
        self.list.toggle()
        self.startthread = startThread(self)
        self.pushButton_Start.clicked.connect(self.start)
        self.pushButton_suspend.clicked.connect(self.suspend)
        self.pushButton_suspend.setEnabled(False)

    def choseDir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"浏览" ,"" )
        self.lineEdit.setText(path)

    def update_text(self, message):
        if message == "startDone":
            self.pushButton_Start.setEnabled(True)
            self.pushButton_suspend.setEnabled(False)
            self.startthread.stop()
        self.textBrowser.append(message)

    def keyPressEvent(self, event):
        #这里event.key（）显示的是按键的编码
        if (event.key() == Qt.Key_1):
            pos = api.getPosition()
            self.lineEdit_1.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_2):
            pos = api.getPosition()
            self.lineEdit_2.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_3):
            pos = api.getPosition()
            self.lineEdit_3.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_4):
            pos = api.getPosition()
            self.lineEdit_4.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_5):
            pos = api.getPosition()
            self.lineEdit_5.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_6):
            pos = api.getPosition()
            self.lineEdit_6.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_7):
            pos = api.getPosition()
            self.lineEdit_7.setText(str(pos[0])+","+str(pos[1]))
        if (event.key() == Qt.Key_8):
            pos = api.getPosition()
            self.lineEdit_8.setText(str(pos[0])+","+str(pos[1]))
    def suspend(self):
        self.startthread.stop()
        self.pushButton_suspend.setText("恢复剪辑")
        self.pushButton_suspend.clicked.connect(self.recovery)
    def recovery(self):

        self.startthread.recovery()
        self.pushButton_suspend.setText("暂停剪辑")
        self.pushButton_suspend.clicked.connect(self.suspend)
    def start(self):
        self.startthread = startThread(self)
        self.startthread.trigger.connect(self.update_text)
        self.pushButton_Start.setEnabled(False)
        self.pushButton_suspend.setEnabled(True)
        self.startthread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    app.exec_()