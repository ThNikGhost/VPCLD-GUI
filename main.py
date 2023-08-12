import sys
from designer import (
    contacts_v1_ui,
    dialog_v1_ui,
    deleteFrom_v1_ui,
    form_addrec_ui,
    infowindow_v1_ui,
    main_v1_ui,
    table_v1_ui,
    window_move_ui
)
from PyQt6.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QAbstractItemView, QTableView, QCheckBox, QWidget, QMainWindow, QDialog, QPushButton, QMessageBox, QAbstractItemView
from data.work_db import create_db, delete_cell, delete_table, get_name_table, insert_data
from PyQt6.QtSql     import QSqlDatabase, QSqlQueryModel

class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)                
        self.mainform = main_v1_ui.Ui_mainWindowChoose()
        self.mainform.setupUi(self)
        self.create_buttons()
        self.mainform.chooseCategory.clicked.connect(self.dialogYesNo)
        self.mainform.btn_DeleteCategory.clicked.connect(self.deleteCategory)
        self.mainform.actionQuit.triggered.connect(self.quit)
        self.mainform.actionAbout.triggered.connect(self.about)
        self.mainform.actionContacts.triggered.connect(self.contacts)
        

    def calltable(self):
        self.hide()
        self.name = self.sender().text()
        self.tablewindow = QWidget()
        self.tw = table_v1_ui.Ui_tableWindow()
        self.tw.setupUi(self.tablewindow)
        self.tablewindow.setWindowTitle(self.name)
        self.createtabwindow()
        self.tw.btn_move.clicked.connect(self.move_rec)
        self.tw.btn_addRecord.clicked.connect(self.addrec)
        self.tw.btn_removedRecord.clicked.connect(self.removerec)
        self.tw.btn_returnMenu.clicked.connect(self.returnMenu)
        self.tw.btn_settings.clicked.connect(self.btn_settings)
        self.tablewindow.show()

    def addrec(self):
        self.form_addrec = QWidget()
        self.fa = form_addrec_ui.Ui_form_addrec()
        self.fa.setupUi(self.form_addrec)
        
        self.fa.buttonBox_.accepted.connect(self.accept_button_addrec)
        self.fa.buttonBox_.rejected.connect(self.quit)
        self.form_addrec.show()

    def accept_button_addrec(self):
        text = self.fa.lineEdit_addrec.text().rstrip()
        cat = self.fa.comboBox_123.currentText()
        insert_data(self.name, cat, text)
        self.quit()
        index = self.list_.index(cat)
        self.clearLayout(self.tw.verticalLayout_5)
        self.createtabwindow()
        self.tw.tabWidget.setCurrentIndex(index)
        

    def removerec(self):
        index = self.current_index_tab
        try:
            delete_cell(self.text_cell, self.current_tab, self.name)
        except Exception as e:
            self.critical_message("Выберите ячейку.")
            return None
    
        self.clearLayout(self.tw.verticalLayout_5)
        self.createtabwindow()
        self.tw.tabWidget.setCurrentIndex(index)

    def cell_clicked(self, row):
        self.sender = self.sender()  # Получаем ссылку на объект, вызвавший сигнал
        selection_model = self.sender.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if selected_indexes:
            row = selected_indexes[0].row()
            column = selected_indexes[0].column()
            index = self.sender.model().index(row, column)  # Получаем индекс ячейки
            self.text_cell = index.data()
        else:
            print("No cell selected")

    def returnMenu(self):
        self.show()
        self.tablewindow.hide()

    def btn_settings(self):
        self.critical_message('Функция пока не работает')

    def move_rec(self):
        self.move_window = QWidget()
        self.mw = window_move_ui.Ui_form_move()
        self.mw.setupUi(self.move_window)
        try:
            self.mw.label_record.setText(self.text_cell)
        except Exception as e:
            self.critical_message("Выберите ячейку.")
            return None
        self.mw.buttonBox.accepted.connect(self.accept_move)
        self.mw.buttonBox.rejected.connect(self.quit)
        self.move_window.show()

    def accept_move(self):
        text_combobox = self.mw.comboBox_move.currentText()
        text_cell = self.text_cell
        index = self.current_index_tab
        active_tab_text = self.tw.tabWidget.tabText(index)
        name_table = self.name
        insert_data(name_table, text_combobox, text_cell)
        delete_cell(text_cell, active_tab_text, name_table)
        
        self.clearLayout(self.tw.verticalLayout_5)
        self.createtabwindow()
        self.tw.tabWidget.setCurrentIndex(index)
        self.move_window.hide()

    def createtabwindow(self):
        self.list_ = ["Смотрю", "Любимые", "Просмотренные", "Брошенные"]
        self.createConnection()
        self.tw.tabWidget = QTabWidget(parent=self.tablewindow)
        self.tw.tabWidget.setTabBarAutoHide(True)
        self.tw.tabWidget.setObjectName("tabWidget")
        self.tw.verticalLayout_5.addWidget(self.tw.tabWidget)
        self.tw.tabWidget.currentChanged.connect(self.active_tab_changed)
        for i in range(4):
            self.tw.tab = QWidget()
            self.tw.tab.setObjectName(f"tab_{i}")
            self.tw.verticalLayout = QVBoxLayout(self.tw.tab)
            self.tw.verticalLayout.setObjectName("verticalLayout")
            self.tw.tableView = QTableView(parent=self.tw.tab)
            self.tw.tableView.setObjectName("tableView")
            self.tw.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.tw.verticalLayout.addWidget(self.tw.tableView)
            self.tw.tableView.clicked.connect(self.cell_clicked)
            self.tw.tabWidget.addTab(self.tw.tab, self.list_[i])
            self.set_data_from_db(self.list_[i], self.tw.tableView)
        
    
    def active_tab_changed(self, index):
        self.current_tab = self.tw.tabWidget.tabText(index)
        self.current_index_tab = index


    def closeEvent(self, e):
        if (self.db.open()):
            self.db.close()

    def set_data_from_db(self, text, object_):

        self.createModel(text, self.name)
        object_.setModel(self.model)

    def createConnection(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data\DataBase.sqlite')
        if not self.db.open():
            QMessageBox.critical(None, ("Cannot open database"),
                                       ("Unable to establish a database connection.\n"
                                                     "This example needs SQLite support. Please read "
                                                     "the Qt SQL driver documentation for information "
                                                     "how to build it.\n\n"
                                                     "Click Cancel to exit."),
                                       QMessageBox.Cancel)
            return False


    def createModel(self, text, table):
        self.model = QSqlQueryModel()
        match table:
            case "Аниме":
                sql = f"""SELECT {text} as Название,
                            s.release_date as 'Дата выхода',
                            s.Score as Оценка,
                            s.Genres as Жанры,
                            s.episode as Эпизоды,
                            s.url as Ссылка
                        FROM {table} JOIN Anime_ as s 
                        ON {text} == s.Title"""
            case _:
                sql = f"""SELECT {text} FROM {table} WHERE ({text} IS NOT NULL) OR ({text} = '')"""
 
        self.model.setQuery(sql)

    def contacts(self):
        self.contactswindow = QWidget()
        self.cw = contacts_v1_ui.Ui_contactswindow()
        self.cw.setupUi(self.contactswindow)
        self.cw.btn_ok.clicked.connect(self.quit)
        self.contactswindow.show()

    def about(self):
        self.infowindow = QWidget()
        self.iw = infowindow_v1_ui.Ui_infoWindow()
        self.iw.setupUi(self.infowindow)
        self.iw.btn_ok.clicked.connect(self.quit)
        self.infowindow.show()

    def deleteCategory(self):
        self.deletewindow = QWidget()
        self.dw = deleteFrom_v1_ui.Ui_From_deleteCategory()
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
            delete_table(i)
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
        self.dialog = dialog_v1_ui.Ui_Dialog_new_category()
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
        elif text == 'Anime_':
            self.critical_message('Это имя зарезервированно, пожалуйста выберите другое.')
        else:
            create_db(text)
        self.clearLayout(self.mainform.verticalLayout)
        self.create_buttons()
        self.dialogYesNo.close()


    def critical_message(self, text=str):
        """Критическое окно с ошибкой"""
        critical = QMessageBox.critical(self, 'Critical message', text)

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