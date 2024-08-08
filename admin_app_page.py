
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
import db_connect as db
import admin_functions as af
import csv


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 370)
        self.db_config = db.read_config()
        self.app_title_label = QtWidgets.QLabel(parent=Form)
        self.app_title_label.setGeometry(QtCore.QRect(250, 20, 131, 41))
        self.app_title_label.setObjectName("app_title_label")

        self.welcome_label = QtWidgets.QLabel(parent=Form)
        self.welcome_label.setGeometry(QtCore.QRect(80, 100, 141, 21))
        self.welcome_label.setObjectName("welcome_label")

        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(80, 140, 231, 21))
        self.label_2.setObjectName("label_2")

        self.logo_label = QtWidgets.QLabel(parent=Form)
        self.logo_label.setGeometry(QtCore.QRect(410, 20, 151, 101))
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap(".\\logo.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setObjectName("logo_label")

        self.add_doctor_radioButton = QtWidgets.QRadioButton(parent=Form)
        self.add_doctor_radioButton.setGeometry(QtCore.QRect(80, 180, 191, 21))
        self.add_doctor_radioButton.setObjectName("add_doctor_radioButton")
        self.add_doctor_radioButton.toggled.connect(self.option_selected)  # Connect radio button to method

        self.remove_doctor_radioButton_2 = QtWidgets.QRadioButton(parent=Form)
        self.remove_doctor_radioButton_2.setGeometry(QtCore.QRect(80, 220, 161, 21))
        self.remove_doctor_radioButton_2.setObjectName("remove_doctor_radioButton_2")
        self.remove_doctor_radioButton_2.toggled.connect(self.option_selected)  #Connect radio button to method

        self.admin_select_pushButton = QtWidgets.QPushButton(parent=Form)
        self.admin_select_pushButton.setGeometry(QtCore.QRect(120, 310, 75, 24))
        self.admin_select_pushButton.setObjectName("admin_select_pushButton")

        self.all_doctors_radioButton_3 = QtWidgets.QRadioButton(parent=Form)
        self.all_doctors_radioButton_3.setGeometry(QtCore.QRect(80, 260, 191, 21))
        self.all_doctors_radioButton_3.setObjectName("all_doctors_radioButton_3")
        self.admin_select_pushButton.clicked.connect(self.select_option)  #Connect select button to a method

        self.lineEdit = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit.setGeometry(QtCore.QRect(430, 160, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.hide()

        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(430, 200, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.hide()

        self.add_remove_pushButton = QtWidgets.QPushButton(parent=Form)
        self.add_remove_pushButton.setGeometry(QtCore.QRect(450, 300, 100, 24))
        self.add_remove_pushButton.setObjectName("add_remove_pushButton")
        self.add_remove_pushButton.hide()
        self.add_remove_pushButton.clicked.connect(self.perform_action)  #Connect select button to a method

        self.doctor_cnp_label = QtWidgets.QLabel(parent=Form)
        self.doctor_cnp_label.setGeometry(QtCore.QRect(360, 200, 61, 16))
        self.doctor_cnp_label.setObjectName("doctor_cnp_label")
        self.doctor_cnp_label.hide()

        self.doctor_name_label = QtWidgets.QLabel(parent=Form)
        self.doctor_name_label.setGeometry(QtCore.QRect(360, 160, 61, 21))
        self.doctor_name_label.setObjectName("doctor_name_label")
        self.doctor_name_label.hide()

        self.logout_pushButton = QtWidgets.QPushButton(parent=Form)
        self.logout_pushButton.setGeometry(QtCore.QRect(280, 340, 75, 24))
        self.logout_pushButton.setObjectName("logout_pushButton")
        self.logout_pushButton.clicked.connect(self.logout)  #Connect select button to logout function

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.app_title_label.setText(_translate("Form",
                                                "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700; color:#0055ff;\">Medical Registry</span></p></body></html>"))
        self.welcome_label.setText(_translate("Form",
                                              "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Welcome, Admin!</span></p></body></html>"))
        self.label_2.setText(_translate("Form",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">Please selected what you want to do:</span></p></body></html>"))
        self.add_doctor_radioButton.setText(_translate("Form", "Add new personal doctor"))
        self.remove_doctor_radioButton_2.setText(_translate("Form", "Remove personal doctor"))
        self.admin_select_pushButton.setText(_translate("Form", "Select"))
        self.all_doctors_radioButton_3.setText(_translate("Form", "See all personal doctors"))
        self.add_remove_pushButton.setText(_translate("Form", "Add/Remove"))
        self.doctor_cnp_label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:700;\">CNP</span></p></body></html>"))
        self.doctor_name_label.setText(_translate("Form",
                                                  "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:700;\">Name</span></p></body></html>"))
        self.logout_pushButton.setText(_translate("Form", "Logout"))

    def option_selected(self):

        """Show the select button when an option is selected"""
        self.admin_select_pushButton.setEnabled(True)

    def select_option(self):

        """Create function to display boxes depending on the radioButton checked."""

        if self.all_doctors_radioButton_3.isChecked():
            self.display_all_doctors()
            self.add_remove_pushButton.hide()
            self.doctor_name_label.hide()
            self.doctor_cnp_label.hide()
            self.lineEdit.hide()
            self.lineEdit_2.hide()
        else:
            if self.add_doctor_radioButton.isChecked():
                self.add_remove_pushButton.show()
                self.doctor_name_label.show()
                self.doctor_cnp_label.show()
                self.lineEdit.show()
                self.lineEdit_2.show()
                self.add_remove_pushButton.setText("Add Doctor")

            elif self.remove_doctor_radioButton_2.isChecked():
                self.doctor_name_label.show()
                self.doctor_cnp_label.show()
                self.lineEdit.show()
                self.lineEdit_2.show()

                self.add_remove_pushButton.show()
                self.add_remove_pushButton.setText("Remove Doctor")

    def add_doctor(self):

        """Create function to add a new personal doctor to database"""

        doctor_name = self.lineEdit.text()
        doctor_cnp = self.lineEdit_2.text()
        if doctor_name and doctor_cnp:
            result = af.add_personal_doctor(self.db_config, doctor_name, doctor_cnp)
            if result is None:
                QtWidgets.QMessageBox.warning(None, "Error", "Failed to add doctor.")
            elif isinstance(result, str):
                QtWidgets.QMessageBox.warning(None, "Input Error", result)
            else:
                QtWidgets.QMessageBox.information(None, "Success", f"Doctor added successfully with ID: {result}")
                self.lineEdit_2.clear()
                self.lineEdit.clear()
        else:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please enter both doctor name and CNP.")

    def remove_doctor(self):

        """Create function to remove a personal doctor to database"""

        doctor_cnp = self.lineEdit_2.text()
        doctor_name = self.lineEdit.text()
        if doctor_cnp and doctor_name:
            result = af.remove_personal_doctor(self.db_config, doctor_cnp, doctor_name)
            if result is None:
                QtWidgets.QMessageBox.warning(None, "Error", "Failed to remove doctor.")
            elif isinstance(result, str):
                QtWidgets.QMessageBox.warning(None, "Input Error", result)
            else:
                QtWidgets.QMessageBox.information(None, "Success", f"Doctor with ID {result} removed successfully.")
                self.lineEdit_2.clear()
                self.lineEdit.clear()
        else:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please enter both doctor name and CNP.")

    def display_all_doctors(self):

        """Create function to display all personal doctors. The function will export them to a csv file"""

        doctors = af.get_all_doctors(self.db_config)
        if doctors:
            self.export_to_csv(doctors)
        else:
            QtWidgets.QMessageBox.information(None, "All Doctors", "No doctors found in the database.")

    def export_to_csv(self, doctors):

        """Create a function to save the personal doctors in a csv"""

        file_name = "doctors_list.csv"
        try:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['doctor_name', 'doctor_cnp'])
                writer.writeheader()
                for doctor in doctors:
                    writer.writerow({'doctor_name': doctor['doctor_name'], 'doctor_cnp': doctor['doctor_cnp']})
            QtWidgets.QMessageBox.information(None, "Success", f"Doctor list exported successfully to {file_name}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Failed to export data: {str(e)}")

    def perform_action(self):

        """This function calls a function when a specific radioButton is checked"""

        if self.add_doctor_radioButton.isChecked():
            self.add_doctor()
        elif self.remove_doctor_radioButton_2.isChecked():
            self.remove_doctor()

    def logout(self):

        """Create function to stop the application by logging out"""

        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
