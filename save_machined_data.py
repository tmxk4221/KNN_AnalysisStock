import csv
from matplotlib import pyplot as plt

# 0. 날짜, 1. 종목명, 2. 주식코드, 3. 시가, 4. 고가, 5.저가, 6. 종가, 7. 거래량
# 8. 종가 일간 변화량, 9. 종가 일간 변화율, 10. 종가의 N일 이동평균, 11. 종가의 N일 이동평균의 일간 변화율, 12. ud_Nd, 13. N일간의 종가 상승률
# 14. 거래량 일간 변화량, 15. 거래량 일간변화율, 16. 거래량의 5일 이동평균, 17. 거래량의 5일 이동평균의 일간 변화율
names=['basic_date', 'stock_name', 'stock_code', 'open_value', 'high_value', 'low_value', 'close_value', 'volume_value',
       'cv_diff_value', 'cv_diff_rate','cv_ma5_value', 'cv_ma5_rate','ud_3d', 'cv5d_diff_rate', 'vv_diff_value', 'vv_diff_rate',
       'vv_ma5_value', 'vv_ma5_rate']

# stock_history1.csv에 있는 값들 읽어오기
lines=list(csv.reader(open('stock_history.csv')))
stock_name = [lines[n][1] for n in range(1, len(lines))]
stock_name = list(set(stock_name))
N=5

# 선택된 종목에 대한 값을 newlines에 리스트형식으로 저장 -------------------------------------------------------------------
def sel_stcokname(sel_stock_name):
    newlines=[]
    for line in lines:
        if sel_stock_name==line[1]:
            newlines.append(line[:8])
    newlines.sort() # 오름차순으로 정렬
    return newlines

# 8. cv_diff_value(종가 일간 변화량) ------------------------------------------------------------------------------------
# 계산 방법 : 종가 일간 변화량 = 금일 종가 - 전일 종가, 첫 번째 인덱스는 전일 종가가 없으므로 0
def cal_cv_diff_value(newlines):
    newlines[0].append(0)
    for n in range(len(newlines)-1):
        newlines[n+1].append(int(newlines[n+1][6])-int(newlines[n][6]))
    return newlines

# 9. cv_diff_rate(종가 일간 변화율) -------------------------------------------------------------------------------------
# 계산 방법 : 종가 일간 변화율 = 금일 종가 일간 변화량 / 전일 종가 * 100, 소수점 세 번째에서 반올림
def cal_cv_diff_rate(newlines):
    newlines[0].append(0)
    for n in range(1, len(newlines)):
        newlines[n].append(round(newlines[n][8]/int(newlines[n-1][6])*100, 2))
    return newlines

# 10. cv_ma5_value(종가의 5일 이동평균) ----------------------------------------------------------------------------------
# 계산 방법 : newlines[n+2]의 cv_ma5_value 인덱스에 (n-2, n-1, n, n+1, n+2)/5 삽입,
# 0~3번째 인덱스는 0으로 세팅 --> 5일이 안되는 기간, 4번째 인덱스부터 계산
def cal_cv_ma5_value(newlines):
    for num in range(0, N-1):
        newlines[num].append(0)
    for n in range(int(N/2), len(newlines)-int(N/2)):
        newlines[n + 2].append(round((int(newlines[n + 2][6]) + int(newlines[n + 1][6]) + int(newlines[n][6]) + int(
            newlines[n - 1][6]) + int(newlines[n - 2][6]))/5, 2))
    return newlines

# 11. cv_ma5_rate(종가의 5일 이동평균의 일간 변화율) -----------------------------------------------------------------------
# 계산 방법 : 금일 5일 이동평균 - 전일 5일 이동평균 / 전일 5일 이동평균 * 100
# (-) : 금일 종가가 5일 이동평균 값보다 작은 값을 가짐, (+) : 금일 종가가 5일 이동평균 값보다 큰 값을 가짐.
def cal_ma5_rate(newlines):
    for num in range(0, N):
        newlines[num].append(0)
    for n in range(N, len(newlines)):
        newlines[n].append(round((int(newlines[n][10]) - newlines[n - 1][10]) / int(newlines[n - 1][10]) * 100, 2))
    return newlines

# 12. ud_3d(N일 연속 -> 종가상승: 1, 종가하락: -1, 해당x: 0)----------------------------------------------------------------
# 계산 방법 : cv_diff_value(5일 연속) > 0 : 1, < 0 : -1, else : 0 --> N-1인덱스에 저장
def cal_ud_3d(newlines):
    newlines[0].append(0)
    for n in range(2, len(newlines)):
        if newlines[n-2][8] > 0 and newlines[n-1][8] > 0 and newlines[n][8] > 0:
            newlines[n-1].append(1)
        elif newlines[n-2][8] < 0 and newlines[n-1][8] < 0 and newlines[n][8] < 0:
            newlines[n-1].append(-1)
        else:
            newlines[n-1].append(0)
    newlines[n].append(0)
    return newlines

# 13. cv5d_diff_rate(5일간의 종가 상승률) --------------------------------------------------------------------------------
# 계산 방법 : (N일 종가 - (N-5)일 종가) / (N-5)일 종가 * 100--> N-1인덱스에 저장.
def cal_cv5d_diff(newlines):
    for num in range(0, N-1):
        newlines[num].append(0)
    for n in range(N-1, len(newlines)-1):
        newlines[n].append(round((int(newlines[n + 1][6]) - int(newlines[n - 4][6])) / int(newlines[n - 4][6]) * 100, 2))
    newlines[n+1].append(0)
    return newlines

# 14. vv_diff_value(거래량 일간변화량) -----------------------------------------------------------------------------------
def cal_vv_diff_value(newlines):
    newlines[0].append(0)
    for n in range(len(newlines) - 1):
        newlines[n + 1].append(int(newlines[n + 1][7]) - int(newlines[n][7]))
    return newlines

# 15. vv_diff_rate(거래량 일간변화율) ------------------------------------------------------------------------------------
def cal_vv_diff_rate(newlines):
    newlines[0].append(0)
    for n in range(1, len(newlines)):
        if int(newlines[n-1][7])==0:
            newlines[n].append(0)
        else:
            newlines[n].append(round(newlines[n][14] / int(newlines[n - 1][7]) * 100, 2))
    return newlines

# 16. vv_ma5_value(거래량의 5일 이동평균) --------------------------------------------------------------------------------
def cal_vv_ma5_value(newlines):
    for num in range(0, N - 1):
        newlines[num].append(0)
    for n in range(int(N / 2), len(newlines) - int(N / 2)):
        newlines[n + 2].append(round((int(newlines[n + 2][7]) + int(newlines[n + 1][7]) + int(newlines[n][7]) + int(
            newlines[n - 1][7]) + int(newlines[n - 2][7])) / 5, 2))
    return newlines

# 17. vv_ma5_rate(거래량의 5일 이동평균의 일간 변화율) ---------------------------------------------------------------------
def cal_vv_ma5_rate(newlines):
    for num in range(0, N):
        newlines[num].append(0)
    for n in range(N, len(newlines)):
        if int(newlines[n-1][16]) == 0:
            newlines[n].append(0)
        else:
            newlines[n].append(round((int(newlines[n][16]) - newlines[n - 1][16]) / int(newlines[n - 1][16]) * 100, 2))
    return newlines

# line_chart 생성(N일 이동평균선에 대해)
def show_line_chart(newlines, sel_stock_name):
    newlist=[]
    for n in range(1, len(newlines)):
        if newlines[n][10]!=0:
            newlist.append(newlines[n][10])

    xs = range(1, len(newlines)-4)
    plt.plot(xs, newlist, 'g-', label='5 Moving average')

    plt.legend(loc=9)
    plt.xlabel("year")
    plt.title(sel_stock_name)
    plt.show()

# un_Nd 확인 (1이 20회이상 발생하는지)
def check_ud_Nd(newlines):
    i=0
    j=0
    for number in range(len(newlines)):
        if newlines[number][12]==1:
            i+=1
        if newlines[number][12]==-1:
            j+=1
    if i>=20 and j>=20:
        return i,j
        #print("20회 이상 발생", i, j)
    else:
        return 0
        #print("Noop...")

# ud_Nd에서 1의 개수를 반환
def count_ud_Nd_1(newlines):
    i=0
    for number in range(len(newlines)):
        if newlines[number][12] == 1:
            i += 1
    return i

# ud_Nd에서 -1의 개수를 반환
def count_ud_Nd_N1(newlines):
    i = 0
    for number in range(len(newlines)):
        if newlines[number][12] == -1:
            i += 1
    return i


# stock_histroy_added.csv에 읽어온 값들 다시 저장
def save_machined_data(lines):
    wf = open('stock_history_added.csv','w', newline='')
    csv_writer=csv.writer(wf)
    for line in lines:
        csv_writer.writerow(line)

if __name__ == "__main__":


    # 원하는 종목 1개에 대하여 독립 변수 추가하여 stock_history_added.csv파일에 저장
    # 원하는 종목을 선택하여 변수를 추가, 데이터 형식은 리스트안에 리스트 --> [[],[],...,[]]
    sel_stock_name = input("종목을 선택하시오")     # '에이원알폼'으로 선택 (udNd=1,-1이 제일 많음)
    newlines = sel_stcokname(sel_stock_name)

    if len(newlines) > 5:
        cal_cv_diff_value(newlines)
        cal_cv_diff_rate(newlines)
        cal_cv_ma5_value(newlines)
        cal_ma5_rate(newlines)
        cal_ud_3d(newlines)
        cal_cv5d_diff(newlines)
        cal_vv_diff_value(newlines)
        cal_vv_diff_rate(newlines)
        cal_vv_ma5_value(newlines)
        cal_vv_ma5_rate(newlines)
        newlines.insert(0, names)
        save_machined_data(newlines)                  # 가공된 데이터 stock_history_added.csv로 저장
        show_line_chart(newlines, sel_stock_name)     # 5일 이동평균선 출력
    else:
        print("데이터가 5개보다 적습니다.")

    """
    # 모든 종목에 대해 udNd의 1과 -1이 20이상인 종목 추출
    ud_Nd_list = []
    for n in range(len(stock_name)):
        i=0
        j=0
        newlines = sel_stcokname(stock_name[n])
        if len(newlines) > 5:
            cal_cv_diff_value(newlines)
            cal_cv_diff_rate(newlines)
            cal_cv_ma5_value(newlines)
            cal_ma5_rate(newlines)
            cal_ud_3d(newlines)
            if check_ud_Nd(newlines):
                i = count_ud_Nd_1(newlines)
                j = count_ud_Nd_N1(newlines)
                ud_Nd_list.append([stock_name[n], i, j])
    ud_Nd_list = sorted(ud_Nd_list, key=lambda line_n: line_n[:][1])
    for list in ud_Nd_list:
        print(list)
    """