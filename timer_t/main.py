from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5 import Qt3DCore ,Qt3DAnimation ,Qt3DExtras
from form import  Ui_MainWindow
from serv import  server
from multiprocessing import Process ,Queue ,Pool
from  O3d import GLWidget
from plotter import canva_Mat as canva_Mat
import random
class test_app(QtWidgets.QMainWindow,Ui_MainWindow):
    s = server()
    q=Queue()

    def __init__(self):
        super().__init__()
        self.q=self.s.q
        self.setupUi(self)
        self.scen_x=QtWidgets.QGraphicsScene()
        self.scen_y=QtWidgets.QGraphicsScene()
        self.scen_z=QtWidgets.QGraphicsScene()
        self.xy.setScene(self.scen_x)
        self.yz.setScene(self.scen_y)
        self.xz.setScene(self.scen_z)
        self.xy.show()
        self.xz.show()
        self.yz.show()

        self.glWidget = GLWidget()
        self.scrollArea.setWidget(self.glWidget)#this 3D

        self.sc = canva_Mat(self.centralwidget)
        self.Gr.addWidget(self.sc, 0, 1, 1, 1)

        self.Gra_V= [self.xy, self.yz, self.xz]
        self.scen=[self.scen_x,self.scen_y,self.scen_z]
        #creat elipse
        [i.addEllipse(0,-50, self.yz.width()-2, self.yz.width(),brush=QBrush(QtCore.Qt.darkRed),pen=QPen(QtCore.Qt.white)) for i in self.scen]
        [i.addEllipse(-10,-8, self.yz.width()/5, self.yz.width()/5,brush=QBrush(QtCore.Qt.darkYellow),pen=QPen(QtCore.Qt.green)) for i in self.scen]

        #creat polka
        [i.addRect(0,0,self.yz.width(),4,brush=QBrush(QtCore.Qt.yellow),pen=QPen(QtCore.Qt.darkYellow)) for i in self.scen]


        self.handle = QtCore.QThread()
        #self.receiver = MessageReceiver(queue)
        self.ok.clicked.connect(self.start_t)
        #self.end.clicked.connect(self.close_t)
        self.o_l=[float(0),float(0),float(0)]

    def start_t(self):
        self.process_one = Process(target=self.s.run, args=())
        self.process_one.start()

        self._status_update_timer = QtCore.QTimer(self)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(lambda: self.graf_update())
        self._status_update_timer.start(10)

        return 1

    def close_t(self):
        self.process_one.kill()
        return 1

    def graf_update(self):
        if not self.q.empty():
            l = self.q.get()
            self.sc.setDate(l[0], l[1], l[2])

            if (self.tabWidget.currentWidget() == self.tab):

                self.xy.rotate(self.o_l[0] - l[0])
                self.xz.rotate(self.o_l[1] - l[1])
                self.yz.rotate(self.o_l[2] - l[2])


                self.label_3.setText("yaw::"+str(l[0]))
                self.label_2.setText("pitch::"+str(l[1]))
                self.label.setText("roll::"+str(l[2]))

                #3D scen

                self.glWidget.setXRotation(l[1])
                self.glWidget.setYRotation(l[2])
                self.glWidget.setZRotation(l[0])
                self.glWidget.update()

            if (self.tabWidget.currentWidget() == self.tab_2):
                self.sc.paint()

            self.o_l = l
        else:
            self.s.__init__()
if __name__ == "__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=test_app()
    window.show()
    sys.exit(app.exec_())
