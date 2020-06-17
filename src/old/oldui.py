# user interface class
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class1 = uic.loadUiType("untitled.ui")[0]
form_class2 = uic.loadUiType("phoneNumber.ui")[0]
form_class3 = uic.loadUiType("popup.ui")[0]
form_class4 = uic.loadUiType("popup2.ui")[0]



def printE(mesg) :
    #main_window.error_pop(mesg)
    main_window.show_popup_ok_cancel('a','b')
    '''ep = errorPOP
    ep.show()
    print('a')
    app2 = QApplication(sys.argv) 
    app2.exec_()
    print('a')'''


class error_sig(QObject) :

    signal1 = pyqtSignal(int)

    def on(self, f):
        self.signal1.emit(f)

class end_sig(QObject) :

    signal1 = pyqtSignal()

    def on(self):
        self.signal1.emit()

# 화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :

    m1 = '쓰레기를 넣어 주세요'
    m2 = ''
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #self.pbtn_test_c.clicked.connect(self.test_c)
        #self.pbtn_test_p.clicked.connect(self.test_p)
        self.pbtn_start.clicked.connect(self.button_start)
        self.err_sig = error_sig()
        self.end_sig = end_sig()
        self.err_sig.signal1.connect(self.error_pop)
        self.end_sig.signal1.connect(self.end_pop)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load('img/can.PNG')
        self.label_10.setPixmap(self.qPixmapVar)
        self.qPixmapVar.load('img/pet.PNG')
        self.label_17.setPixmap(self.qPixmapVar)


    def set_message_big(self,message) :
        self.m1 = message
        self.label_intro.setText(self.m1)

    def set_message_small(self,message) :
        self.m2 = message
        self.label_intro_2.setText(self.m2)

    def can_pet(self) :
        self.label_can_num.setText(str(RVM_status.recycling_number['can'])+'개')
        self.label_pet_num.setText(str(RVM_status.recycling_number['pet'])+'개')

    

    # 시작, 종료 버튼 기능
    def button_start(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            RVM_status.startRVM()
            self.button_text()
        elif RVM_status.machine_stat == RVM_STATE_ON:
            RVM_status.terminationRVM()
            self.button_text()
            
        #phone_window.ready()
        #main_window.close()
        #phone_window.show()
    
    def button_text(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat != EXEC_NONE_TYPE:
                self.pbtn_start.setText('waiting')
            else :
                self.pbtn_start.setText('start')
        elif RVM_status.machine_stat == RVM_STATE_ON:
            self.pbtn_start.setText('end')
    
    def error_report(self,f):
        self.err_sig.on(f)

    def error_pop(self,mesg) :
        self.set_message_big('에러가 발생했습니다.')
        self.set_message_small('Error')

        p = errPopDialog()
        p.exec_()
        
        """
        qmb =QMessageBox()
        result = qmb.warning(self,'Error','error occurs in step %s' %mesg,QMessageBox.Ok)
        if result == QMessageBox.Ok :
            RVM_status.error_stat=retValOK
        """

    def end_report(self):
        self.end_sig.on()
    
    def end_pop(self):
        p = endPopDialog()
        p.exec_()


def printU(mesg) :
    main_window.set_message_small(mesg)

def printB(mesg) :
    main_window.set_message_big(mesg)

class errPopDialog(QDialog,form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_err_mesg.setText('Error occurs in\nStep %s' %RVM_status.exec_stat)
        self.pushButton.clicked.connect(self.errorOk)

    def errorOk(self):
        RVM_status.terminationRVM()
        RVM_status.updateStatus(0)
        self.close()
        RVM_status.error_stat = retValOK
        

class endPopDialog(QDialog,form_class4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.can_num.setText('can : %s개' %RVM_status.recycling_number['can'])
        self.pet_num.setText('pet : %s개' %RVM_status.recycling_number['pet'])
        self.pushButton.clicked.connect(self.endOk)

    def endOk(self):
        RVM_status.exec_stat = EXEC_NONE_TYPE
        self.close()
    
            
class phoneWindow(QMainWindow, form_class2) :
    current_PN = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.button_0.clicked.connect(lambda: self.buttonClick(0))
        self.button_1.clicked.connect(lambda: self.buttonClick(1))
        self.button_2.clicked.connect(lambda: self.buttonClick(2))
        self.button_3.clicked.connect(lambda: self.buttonClick(3))
        self.button_4.clicked.connect(lambda: self.buttonClick(4))
        self.button_5.clicked.connect(lambda: self.buttonClick(5))
        self.button_6.clicked.connect(lambda: self.buttonClick(6))
        self.button_7.clicked.connect(lambda: self.buttonClick(7))
        self.button_8.clicked.connect(lambda: self.buttonClick(8))
        self.button_9.clicked.connect(lambda: self.buttonClick(9))
        self.button_bs.clicked.connect(self.bsClick)
        self.button_enter.clicked.connect(self.enClick)

    def ready(self) :
        self.current_PN=""
        self.phone_number.setText(str(self.current_PN))

    def buttonClick(self, num) :
        self.current_PN = self.current_PN + str(num)
        self.phone_number.setText(str(self.current_PN))

    def bsClick(self) :
        self.current_PN = self.current_PN[:-1]
        self.phone_number.setText(str(self.current_PN))

    def enClick(self) :
        phone_window.close()
        main_window.show()
# 시작, 종료 버튼 기능
    def button_start(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat == EXEC_NONE_TYPE:
                RVM_status.startRVM()
                self.p1.setText('페트병 혹은 캔을\n하나씩 넣어주세요')
                self.p2.setStyleSheet('background-image:url("img/pic4.png")')
                self.can_pet()
                self.p3.setText('종료')
        elif RVM_status.machine_stat == RVM_STATE_ON:
            RVM_status.terminationRVM()
            
        #phone_window.ready()
        #main_window.close()
        #phone_window.show()
    
    def button_end(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat == EXEC_NONE_TYPE:
                self.p1.setText(self.title)
                self.p2.setStyleSheet('background-image:url("img/pic2.png")')
                self.p2_1.setText('')
                self.p2_2.setText('')
                self.p3.setText('시작')