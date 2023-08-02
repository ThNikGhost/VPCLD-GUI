import sys
from designer.ui_v1 import Ui_mainWindowChoose
from designer.ui_dialog_v1 import Ui_Dialog_new_category
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QMessageBox
from data.work_db import insert_data, get_list_db


#from infowindow import Ui_Dialog
class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)                
        self.mainform = Ui_mainWindowChoose()
        self.mainform.setupUi(self)
        self.create_buttons()
        self.mainform.chooseCategory.clicked.connect(self.DialogYesNo)
    
    def DialogYesNo(self):
        """Окно для создания новой категории"""
        self.dialogYesNo = QDialog() # type: ignore
        self.dialog = Ui_Dialog_new_category()
        self.dialog.setupUi(self.dialogYesNo)
        self.dialogYesNo.show()
        self.dialog.Dialog_yesNo.accepted.connect(self.accept_button)
        self.dialog.Dialog_yesNo.rejected.connect(self.reject_button)

    def accept_button(self): 
        """Срабатывает при нажатии "Save"
        на окне infowindow"""
        try:
            insert_data(self.dialog.lineEdit_newCateg.text())
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: Data.Category':
                self.critical_message('Такая категория уже существует!')

        self.clearLayout(self.mainform.verticalLayout)
        self.create_buttons()
        self.dialogYesNo.close()

    def critical_message(self, text=str):
        """Критическое окно с ошибкой"""
        critical = QMessageBox.critical(self, 'Critical message', text)
        #self.infowindow.close()

    def reject_button(self): 
        """Срабатывает при нажатии "Отмена"
        на окне infowindow"""
        self.dialogYesNo.close()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_buttons(self):
        for i in get_list_db():
            self.mainform.pushButton = QPushButton(parent=self.mainform.centralwidget)
            self.mainform.pushButton.setObjectName(i)
            self.mainform.pushButton.setText(i)


            self.mainform.verticalLayout.addWidget(self.mainform.pushButton)

 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())