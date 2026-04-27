import random  # 속도를 위해 랜덤추출

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *  # 로그인 오류
# from PyQt5.QtTest import *  #기다려(모듈 조합시 필요)

from kiwoom.ErrorCode import *

# 조건식 불러오기!!!!!!!!!!!!
# from Conditional.Condition3_main import *
from Conditional.Condition4_Beta import *

##########################


# Main Code
class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        print("Main Program Run")

        ##########EVENT loop
        self.login_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()  # 종목분석용(3제외)

        self.kospi_loop = QEventLoop()  # 코스피(3)
        self.kosdaq_loop = QEventLoop()  # 코스닥(3)

        ##########Screen Number
        self.screen_my_info = "2000"
        self.screen_calculation_stock = "4000"

        ##########함수 실행
        self.get_ocx_instance()  # API사용

        self.event_slots()  # API요청작업
        self.sinal_login_commconnect()  # login

        self.kospi()  # 코스피 지수
        self.calculator_fnc_kospi()  # 코스피 종목분석용

        self.kosdaq()  # 코스닥 지수
        self.calculator_fnc_kosdaq()  # 코스닥 종목분석용

    #############################################
    ###함수
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # API 사용

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)  # login요청
        self.OnReceiveTrData.connect(self.trdata_slot)  # Tr요청

    # 이벤트의 Login 요청
    def sinal_login_commconnect(self):  # 로그인 시작
        self.dynamicCall("CommConnect()")

        self.login_event_loop.exec_()

    def login_slot(self, errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    #############################################
    ### 종목분석 DB 함수

    # 시장코드용 -> 종목개수
    def get_code_list_by_market(self, market_code):  # 시장코드 가져오기
        code_list = self.dynamicCall("GetCodeListByMarket(QString", market_code)
        code_list = code_list.split(";")[:-1]

        return code_list

    # 종목 개수 -> 종목DB (Kospi)
    def calculator_fnc_kospi(self):
        code0_list = self.get_code_list_by_market("0")  # 코스피 확인
        # code0_list = random.sample(code0_list, 499)

        print("코스피 개수 %s" % len(code0_list))
        for idx, code in enumerate(code0_list):  # 코스피
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)  # 하나하나의 종목에 대해 스크린넘버를 지우고 다시
            print("%s / %s : KOSPI Stock Code : %s is Updating..." % (idx + 1, len(code0_list), code))
            self.day_kiwoom_db(code=code)

    # 종목 개수 -> 종목DB (Kosdaq)
    def calculator_fnc_kosdaq(self):
        code10_list = self.get_code_list_by_market("10")  # 코스닥 확인
        # code10_list = random.sample(code10_list, 499)

        print("코스닥 개수 %s" % len(code10_list))
        for idx, code in enumerate(code10_list):  #코스닥
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)
            print("%s / %s : KOSDAQ Stock Code : %s is Updating..." % (idx + 1, len(code10_list), code))
            self.day_kiwoom_db(code=code)

    #############################################
    ###Import 외부 조건문

    #############################################
    ###DB와 조건식(실행파일 import 필수)

    # 일일변동추정 지표
    day_kiwoom_db = day_kiwoom_db3
    kospi = kospi
    kosdaq = kosdaq
    trdata_slot = trdata_slot3

    #############################################
