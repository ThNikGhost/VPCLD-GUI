import sys
from designer.dialog_v1_ui import Ui_Dialog_new_category
from designer.main_v1_ui import Ui_mainWindowChoose
from designer.deleteFrom_v1_ui import Ui_From_deleteCategory
from designer.infowindow_v1_ui import Ui_infoWindow
from designer.contacts_v1_ui import Ui_contactswindow
from designer.table_v1_ui import Ui_tableWindow
from PyQt6.QtWidgets import QApplication, QCheckBox, QWidget, QMainWindow, QDialog, QPushButton, QMessageBox
from data.work_db import insert_data, delete, get_name_table


#from infowindow import Ui_Dialog
class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)                
        self.mainform = Ui_mainWindowChoose()
        self.mainform.setupUi(self)
        self.create_buttons()
        self.mainform.chooseCategory.clicked.connect(self.dialogYesNo)
        self.mainform.btn_DeleteCategory.clicked.connect(self.deleteCategory)
        self.mainform.actionQuit.triggered.connect(self.quit)
        self.mainform.actionAbout.triggered.connect(self.about)
        self.mainform.actionContacts.triggered.connect(self.contacts)

    def calltable(self):
        name = self.sender().text()
        if name in ["Аниме", "Фильмы", "Игры", "Книги"]:
            print("FDFDFDFDFDFDF")
        self.tablewindow = QWidget()
        self.tw = Ui_tableWindow()
        self.tw.setupUi(self.tablewindow)
        self.tablewindow.setWindowTitle(name)
        self.set_data_to_db()
        self.tablewindow.show()

    def set_data_to_db(self):
        pass        

    def contacts(self):
        self.contactswindow = QWidget()
        self.cw = Ui_contactswindow()
        self.cw.setupUi(self.contactswindow)
        self.cw.btn_ok.clicked.connect(self.quit)
        self.contactswindow.show()

    def about(self):
        self.infowindow = QWidget()
        self.iw = Ui_infoWindow()
        self.iw.setupUi(self.infowindow)
        self.iw.btn_ok.clicked.connect(self.quit)
        self.infowindow.show()

    def deleteCategory(self):
        self.deletewindow = QWidget()
        self.dw = Ui_From_deleteCategory()
        self.dw.setupUi(self.deletewindow)
        for i in get_name_table():
            self.dw.checkBox = QCheckBox(parent=self.deletewindow)
            self.dw.checkBox.setObjectName(i)
            self.dw.checkBox.setText(i)
            self.dw.verticalLayout.addWidget(self.dw.checkBox)
            self.dw.checkBox.stateChanged.connect(self.pressedBtn)
        self.list_ = []
        self.dw.buttonBox_delete.accepted.connect(self.accept_button_delete)
        self.dw.buttonBox_delete.rejected.connect(self.quit)
        self.deletewindow.show()

    def accept_button_delete(self):
        for i in self.list_:
            delete(i)
        self.clearLayout(self.mainform.verticalLayout)
        self.create_buttons()
        self.deletewindow.close()

    def pressedBtn(self):
        text = self.sender().objectName()
        if text in self.list_:
            self.list_.remove(text)
        elif text not in self.list_:
            self.list_.append(text)

    def dialogYesNo(self):
        """Окно для создания новой категории"""
        self.dialogYesNo = QDialog() # type: ignore
        self.dialog = Ui_Dialog_new_category()
        self.dialog.setupUi(self.dialogYesNo)
        self.dialogYesNo.show()
        self.dialog.Dialog_yesNo.accepted.connect(self.accept_button)
        self.dialog.Dialog_yesNo.rejected.connect(self.quit)

    def accept_button(self): 
        """Срабатывает при нажатии "Save"
        на окне infowindow"""
        text = self.dialog.lineEdit_newCateg.text()
        if len(text.replace(' ', '')) == 0:
            self.critical_message('Введите название!')
            return None
        elif text in get_name_table():
            self.critical_message('Такое название уже есть!')
            return None
        else:
            insert_data(text)
        self.clearLayout(self.mainform.verticalLayout)
        self.create_buttons()
        self.dialogYesNo.close()


    def critical_message(self, text=str):
        """Критическое окно с ошибкой"""
        critical = QMessageBox.critical(self, 'Critical message', text)
        #self.infowindow.close()

    def quit(self): 
        sender = self.sender()  # Получаем объект отправителя сигнала (кнопку)
        parent_widget = sender.parent()
        parent_widget.close()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_buttons(self):
        for i in get_name_table():
            self.mainform.pushButton = QPushButton(parent=self.mainform.centralwidget)
            self.mainform.pushButton.setObjectName(i)
            self.mainform.pushButton.setText(i)
            self.mainform.verticalLayout.addWidget(self.mainform.pushButton)
            self.mainform.pushButton.clicked.connect(self.calltable)

 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())