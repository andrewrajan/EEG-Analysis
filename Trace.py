from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
import os
from functions import eeg_data, print_plots, welch_data, band_graph, print_psd, extract_features


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 820)
        self.MainWindow = MainWindow

        self.seizure_files = []
        self.nonseizure_files = []
        self.eeg = None
        self.band_powers = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.psd = QtWidgets.QPushButton(self.centralwidget)
        self.psd.setGeometry(QtCore.QRect(640, 20, 75, 23))
        self.psd.setObjectName("psd")
        self.bandPower = QtWidgets.QPushButton(self.centralwidget)
        self.bandPower.setGeometry(QtCore.QRect(640, 60, 75, 23))
        self.bandPower.setObjectName("bandPower")
        self.eegPlots = QtWidgets.QPushButton(self.centralwidget)
        self.eegPlots.setGeometry(QtCore.QRect(640, 100, 75, 23))
        self.eegPlots.setObjectName("eegPlots")
        self.addSbtn = QtWidgets.QPushButton(self.centralwidget)
        self.addSbtn.setGeometry(QtCore.QRect(60, 210, 150, 30))
        self.addSbtn.setObjectName("addSbtn")
        self.addNonsbtn = QtWidgets.QPushButton(self.centralwidget)
        self.addNonsbtn.setGeometry(QtCore.QRect(350, 210, 150, 30))
        self.addNonsbtn.setObjectName("addNonsbtn")
        self.seizurelist = QtWidgets.QListWidget(self.centralwidget)
        self.seizurelist.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.seizurelist.setObjectName("seizurelist")
        self.nonseizurelist = QtWidgets.QListWidget(self.centralwidget)
        self.nonseizurelist.setGeometry(QtCore.QRect(300, 10, 256, 192))
        self.nonseizurelist.setObjectName("nonseizurelist")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 270, 371, 481))
        self.tableWidget.setMinimumSize(QtCore.QSize(311, 0))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 270, 161, 41))
        self.pushButton.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(480, 400, 256, 61))
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.addSbtn.clicked.connect(self.add_seizure_files)
        self.addNonsbtn.clicked.connect(self.add_nonseizure_files)
        self.psd.clicked.connect(self.show_psd)
        self.bandPower.clicked.connect(self.show_band_power)
        self.eegPlots.clicked.connect(self.show_eeg_plots)
        self.seizurelist.itemClicked.connect(self.load_selected_file)
        self.nonseizurelist.itemClicked.connect(self.load_selected_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.psd.setText(_translate("MainWindow", "PSD"))
        self.bandPower.setText(_translate("MainWindow", "Band Power"))
        self.eegPlots.setText(_translate("MainWindow", "EEG plots"))
        self.addSbtn.setText(_translate("MainWindow", "Add Seizure File"))
        self.addNonsbtn.setText(_translate("MainWindow", "Add Non Seizure File"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Feature"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        self.pushButton.setText(_translate("MainWindow", "Export File (CSV)"))
    
    def update_feature_table(self, features):
        self.tableWidget.setRowCount(len(features))

        for row, (name, value) in enumerate(features.items()):
            name_item = QtWidgets.QTableWidgetItem(str(name))
            value_item = QtWidgets.QTableWidgetItem(f"{value:.3f}")
            self.tableWidget.setItem(row, 0, name_item)
            self.tableWidget.setItem(row, 1, value_item)
    
    def add_seizure_files(self):
        files, _ = QFileDialog.getOpenFileNames(
        self.MainWindow,
        "Select Seizure EDF Files",
        "",
        "EDF Files (*.edf)"
        )

        for file_path in files:
            if file_path not in self.seizure_files:
                self.seizure_files.append(file_path)

                item = QtWidgets.QListWidgetItem(os.path.basename(file_path))
                item.setData(QtCore.Qt.UserRole, file_path)
                self.seizurelist.addItem(item)

    

    def show_psd(self):
        print_psd(self.eeg[1])

    
    def show_band_power(self):
        band_graph(self.band_powers)
    
    def show_eeg_plots(self):
        print_plots(self.eeg[1])



    
    def add_nonseizure_files(self):
        files, _ = QFileDialog.getOpenFileNames(
        self.MainWindow,
        "Select Non-Seizure EDF Files",
        "",
        "EDF Files (*.edf)"
    )

        for file_path in files:
            if file_path not in self.nonseizure_files:
                self.nonseizure_files.append(file_path)

                item = QtWidgets.QListWidgetItem(os.path.basename(file_path))
                item.setData(QtCore.Qt.UserRole, file_path)
                self.nonseizurelist.addItem(item)
        

    def load_selected_file(self, item):
        file_path = item.data(QtCore.Qt.UserRole)

        try:
            self.eeg = eeg_data(file_path)

            raw = self.eeg[0]
            raw_filt = self.eeg[1]
            sfreq = self.eeg[2]

            self.band_powers = welch_data(raw_filt, sfreq)
            features = extract_features(raw_filt, sfreq)

            self.update_feature_table(features)

            print(f"Loaded: {file_path}")

        except Exception as e:
            self.eeg = None
            self.band_powers = None

            QMessageBox.critical(
                self.MainWindow,
                "Error",
                f"Failed to load EEG data:\n{str(e)}"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())