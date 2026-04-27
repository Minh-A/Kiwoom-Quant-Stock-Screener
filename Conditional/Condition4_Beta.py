## 조건식을 뚱땅뚱땅!!!!
## 조건 항목을 뽑는 4번째 버전 (아직은 베타)
## 2021.02.08 시작

from PyQt5.QtTest import *  # 기다려

from utils.notifier import notify_stock_signal
from utils.output import append_condition_result


#######################
# 코스피 요청
def kospi(self, date=None):
    print("\n <코스피 요청> \n")
    self.dynamicCall("SetInputValue(QString, QString)", "업종코드", "001")
    self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "업종일봉조회", "opt20006", "0",
                     self.screen_calculation_stock)
    self.kospi_loop.exec_()

# 코스닥 요청
def kosdaq(self, date=None):
    print("\n <코스닥 요청> \n")
    self.dynamicCall("SetInputValue(QString, QString)", "업종코드", "101")
    self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "업종일봉조회", "opt20006", "0", self.screen_calculation_stock)
    self.kosdaq_loop.exec_()


# 조건문 종목DB
def day_kiwoom_db3(self, code=None, date=None, sPrevNext='0'):
    QTest.qWait(3605)  # 3.6초의 딜레이, 1시간에 1000개까지만 조회 및 주문가능 (1시간은 3600초따라서 3.6초가 1000개 달성)
                      # 1초에 5개 이상 조회 안됨 (5개 미만만 가능)

    self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
    self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

    # 주식일봉 불러오기
    if date == None:
        self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회", "opt10081", sPrevNext,
                     self.screen_calculation_stock)

    self.calculator_event_loop.exec_()


#######################
# 조건문
def trdata_slot3(self, sCrNo, sRQName, sTrCode, sRecordName, sPrevNext):

    ################################ 코스피,코스닥
    if sRQName == "업종일봉조회":

        self.kos_data = []  # 지수의 일일변동추정 허용치
        self.kos_mdf_data = []  # 지수의 이동일변동 허용치

        # 지수 데이터 생성 (Kospi, Kosdaq)
        for i in range(600):
            data = []  # 한 종목의 일봉데이터를 받는 곳

            high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
            high_price = abs(int(high_price.strip()))
            low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")
            low_price = abs(int(low_price.strip()))
            start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
            start_price = abs(int(start_price.strip()))
            current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
            current_price = abs(int(current_price.strip()))

            dfei = abs(high_price - low_price) / abs(current_price - start_price)

            data.append("")
            data.append(round(dfei, 10))  # 일일변동추정!!!
            data.append("")

            self.kos_data.append(data)

        # 지수 이동일변동 생성
        af_kos_data = 0  # 초기 값
        self.mo_kos_data = []  # 지수 이동일변동
        for i in range(600):
            data1 = abs(self.kos_data[i][1] - af_kos_data)
            af_kos_data = self.kos_data[i][1]  # 후의 데이터 저장

            self.mo_kos_data.append(data1)

            self.kos_mdf_data.append(round(self.mo_kos_data[i], 10))  # 이동일변동!!

        self.kospi_loop.exit()
        self.kosdaq_loop.exit()

    global f
    ################################ 종목분석 코드
    if sRQName == "주식일봉차트조회":
        self.calcul_data = []  # 분석용

        code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
        code = code.strip()
        # print("%s 일봉데이터 요청" % code)

        cnt = self.dynamicCall("GetRepeatCnt(QString,QString)", sTrCode, sRQName)
        # print("데이터 일수 %s " % cnt)

        if cnt < 600:  # 5일씩 1개월에 4주로 2개월치
            print("데이터 부족 \n")
            self.calculator_event_loop.exit()
        else:
            # 데이터 생성
            for i in range(600):
                data = []  # 한 종목의 일봉데이터를 받는 곳

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "현재가")  # 종가 = 현재가
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "거래대금")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "일자")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")
                code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

                data.append("")
                data.append(code_nm)
                data.append(date.strip())  # 날짜
                data.append(abs(int(start_price.strip())))  # 시가
                data.append(abs(int(current_price.strip())))  # 종가
                data.append(abs(int(high_price.strip())))  # 고가
                data.append(abs(int(low_price.strip())))  # 저가
                data.append(value.strip())  # 거래량
                data.append(trading_value.strip())  # 거래대금
                data.append("")

                self.calcul_data.append(data)
            print("종목 이름: %s" % self.calcul_data[0][1])

            #######################
            # 데이터 조건
            # 일일변동추정 지표 (Daily fluctuation estimation indicator) "DFEI")
            # 일일변동추정 지표를 생성함
            # 일일변동추정 지표는 일봉의 "고가와 저가의 차이"를 "시가와 종가의 차이"로 나눈 것으로 하루동안의 변동성을 얼마나 따라가는냐를 보여준다
            # 만일 단타일경우 지표는 클 것이고, 단타가 아닌 시장 상황일 경우 지표는 낮을 것임
            # 일일변동추정 지표는 최저를 1로 함!!
            #######################

            # 비교를 위한 초기값 생성
            sj_0 = self.calcul_data[0][4] - self.calcul_data[0][3]  # 초기 변수화 (현재가는 종가 - 그날 하루의 시작가인 시가)

            if self.calcul_data[0][5] - self.calcul_data[0][6] == 0:
                print("최근일자부터 거래 정지여? 뭐여?")
                self.calculator_event_loop.exit()

            elif self.calcul_data[0][4] - self.calcul_data[0][3] == 0:
                sj_0 = self.calcul_data[0][5] - self.calcul_data[0][6]
                af_day_v = (self.calcul_data[0][5] - self.calcul_data[0][6]) / sj_0

            else:
                af_day_v = (self.calcul_data[0][5] - self.calcul_data[0][6]) / (self.calcul_data[0][4] - self.calcul_data[0][3])  # 비교값 초기 생성


            ####################
            # 본격적으로 조건문 시작
            for idx in range(600):
                sj = self.calcul_data[idx][4] - self.calcul_data[idx][3]  # 종가-시가를 변수화

                if self.calcul_data[idx][5] - self.calcul_data[idx][6] == 0:  # 고가와 저가가 같으면 거래정지
                    print("거래정지인듯 ㅋㅋ \n")
                    break

                if sj == 0:
                    sj = (self.calcul_data[idx][5] - self.calcul_data[idx][6])  # 시가-종가가 0이면 지표가 1이 되도록 수정

                if self.kos_mdf_data[idx]*10 < 3:
                    self.kos_mdf_data[idx] = 0.3  # 코스 시장의 이동일변동이 5보다 작으면 5로 수정!!!, 여기서 종목의 이동변동의 하한성을 선정!!!

                else:
                    day_v = (self.calcul_data[idx][5] - self.calcul_data[idx][6]) / sj
                    # 일일변동추정 지표: "(고가-저가)/(종가-시가)"

                    # 변동성에 따른 조건
                    if day_v < 3:
                        print("%s일, 일일변동 낮음, 일일변동성: %s \n" % (idx, day_v))   # 여기서 일일변동의 제한을 검!!!!
                        break

                    if (day_v - af_day_v) < (self.kos_mdf_data[idx]*10):  # 코스피의 이동일변동
                        print("이동일변동 허용치 %s" % (self.kos_mdf_data[idx]*10))
                        print("%s일, 이동일변동 낮음, 이동일변동: %s \n" % (idx, (day_v - af_day_v)))
                        break

                    # # 가격에 제한을 검
                    # if self.calcul_data[idx][1] > 50000:
                    #     print("가격제한: %s" % self.calcul_data[idx][1])
                    #     break

                    if day_v >= 3 and (day_v - af_day_v) >= (self.kos_mdf_data[idx]*10) and idx == 599:
                        print("해당 종목이 조건 통과!! \n")

                        notify_stock_signal("DFEI 조건항목: %s" % code_nm)
                        append_condition_result("condition4_stock_0215.txt", code, code_nm)
                        break

                    af_day_v = day_v  # 여기해야지 과거 데이터가 어디에도 영향을 안주고 다음으로 넘어감

            self.calculator_event_loop.exit()
