from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
import os
from functions import eeg_data, print_plots, welch_data, band_graph, print_psd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.MainWindow = MainWindow

        self.seizure_files = []
        self.nonseizure_files = []
        self.eeg = None
        self.band_powers = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.No_seizure = QtWidgets.QComboBox(self.centralwidget)
        self.No_seizure.setGeometry(QtCore.QRect(80, 360, 91, 30))
        self.No_seizure.setObjectName("No_seizure")
        self.No_seizure.addItem("")
        self.No_seizure.addItem("")

        self.plotContainer = QtWidgets.QFrame(self.centralwidget)
        self.plotContainer.setGeometry(QtCore.QRect(50, 30, 691, 321))
        self.plotContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plotContainer.setObjectName("plotContainer")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.plotContainer)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 691, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.psd = QtWidgets.QPushButton(self.centralwidget)
        self.psd.setGeometry(QtCore.QRect(640, 360, 75, 23))
        self.psd.setObjectName("psd")

        self.bandPower = QtWidgets.QPushButton(self.centralwidget)
        self.bandPower.setGeometry(QtCore.QRect(640, 400, 75, 23))
        self.bandPower.setObjectName("bandPower")

        self.eeg_plots = QtWidgets.QPushButton(self.centralwidget)
        self.eeg_plots.setGeometry(QtCore.QRect(640, 450, 75, 23))
        self.eeg_plots.setObjectName("eeg_plots")

        self.dayCombo = QtWidgets.QComboBox(self.centralwidget)
        self.dayCombo.setGeometry(QtCore.QRect(190, 360, 321, 30))
        self.dayCombo.setObjectName("dayCombo")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 430, 150, 30))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 470, 150, 30))
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.No_seizure.currentIndexChanged.connect(self.update_days)
        self.dayCombo.currentIndexChanged.connect(self.set_file)
        self.pushButton.clicked.connect(self.add_seizure_files)
        self.pushButton_2.clicked.connect(self.add_nonseizure_files)
        self.psd.clicked.connect(self.show_psd)
        self.bandPower.clicked.connect(self.show_band_power)
        self.eeg_plots.clicked.connect(self.show_eeg_plots)

        self.update_days()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.No_seizure.setItemText(0, _translate("MainWindow", "No Seizure"))
        self.No_seizure.setItemText(1, _translate("MainWindow", "Seizure"))
        self.psd.setText(_translate("MainWindow", "PSD"))
        self.bandPower.setText(_translate("MainWindow", "Band Power"))
        self.eeg_plots.setText(_translate("MainWindow", "EEG plots"))
        self.pushButton.setText(_translate("MainWindow", "Add Seizure File"))
        self.pushButton_2.setText(_translate("MainWindow", "Add Non Seizure File"))

    def add_seizure_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.MainWindow,
            "Select Seizure EDF Files",
            "",
            "EDF Files (*.edf);;All Files (*)"
        )
        added = False
        for file_path in files:
            if file_path.lower().endswith(".edf") and file_path not in self.seizure_files:
                self.seizure_files.append(file_path)
                added = True

        if self.No_seizure.currentText() == "Seizure":
            self.update_days()
        if not added:
            QMessageBox.information(self, "No New Files", "No new EDF seizure files were added.")


    
    def add_nonseizure_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.MainWindow,
            "Select Non-Seizure EDF Files",
            "",
            "EDF Files (*.edf);;All Files (*)"
        )
        added = False
        for file_path in files:
            if file_path.lower().endswith(".edf") and file_path not in self.nonseizure_files:
                self.nonseizure_files.append(file_path)
                added = True

        if self.No_seizure.currentText() == "No Seizure":
            self.update_days()
        if not added and files:
            QMessageBox.information(self, "No New Files", "No new EDF non-seizure files were added.")  
        
    def update_days(self):
        self.dayCombo.clear()

        if self.No_seizure.currentText() == "Seizure":
            files = self.seizure_files
        else:
            files = self.nonseizure_files
        for file_path in files:
            self.dayCombo.addItem(os.path.basename(file_path), file_path)
        
        if self.dayCombo.count() > 0:
            self.set_file()
        else:
            self.eeg = None
            self.band_powers = None
            

    def set_file(self):
        file_path = self.dayCombo.currentData()

        if not file_path:
            self.eeg = None
            self.band_powers = None
            return
        
        try:
            self.eeg = eeg_data(file_path)
            self.band_powers = welch_data(self.eeg[1], self.eeg[2]) 
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load EEG data: {str(e)}")

            
    

    def show_psd(self):
        print_psd(self.eeg[1])

    
    def show_band_power(self):
        band_graph(self.band_powers)
    
    def show_eeg_plots(self):
        print_plots(self.eeg[1])



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.set_file()
    MainWindow.show()
    sys.exit(app.exec_())
