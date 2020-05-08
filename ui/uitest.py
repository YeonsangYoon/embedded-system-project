import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class1 = uic.loadUiType("untitled.ui")[0]
form_class2 = uic.loadUiType("phoneNumber.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :
    can_num = 0
    pet_num = 0
    phone_number = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pbtn_test_c.clicked.connect(self.test_c)
        self.pbtn_test_p.clicked.connect(self.test_p)
        self.pbtn_next_page.clicked.connect(self.next_page)

    def ready(self) :
        self.phone_number=phone_window.current_PN
        self.can_num=0
        self.pet_num=0
        self.label_intro.setText("쓰레기를 넣어 주세요.\nphone number : "+self.phone_number)

    def test_c(self) :
        self.can_num +=1
        self.label_can_num.setText(str(self.can_num)+'개')

    def test_p(self) :
        self.pet_num +=1
        self.label_pet_num.setText(str(self.pet_num)+'개')

    def next_page(self) :
        phone_window.ready()
        main_window.close()
        phone_window.show()
        

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
        main_window.ready()
        main_window.show()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    phone_window = phoneWindow() 
    main_window = mainWindow()

    #프로그램 화면을 보여주는 코드
    phone_window.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()