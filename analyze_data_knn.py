import csv
from collections import Counter
from linear_algebra import distance
import matplotlib.pyplot as plt

names = ['index1', 'index2', 'k=3', 'k=4', 'k=5', 'k=6','k=7']
k_list = [3, 4, 5, 6, 7]

# stock_history1.csv에 있는 값들 읽어오기
lines = list(csv.reader(open('stock_history_added.csv')))


# 값이 매우 큰 경우에 0.01을 곱하여 정규화시킴(인덱스3~8까지)
def Normalization_index(lines):
    newlines = []
    for line in lines[1:]:
        for n in range(3,9):
            line[n]=float(line[n])*0.01
        newlines.append(line)
    return newlines


# 선택한 독립변수로 새로운 레이블 만듦
def sel_idvVal_newLable(lines, index1, index2):
    newlines = []
    for n in range(1, len(lines)):
        tmplines = []
        tmplines.append(float(lines[n][index1]))
        tmplines.append(float(lines[n][index2]))
        tmplines.append(int(lines[n][12]))
        newlines.append(tmplines)
    return newlines


# knn을 실행하여 예측값 반환
def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""

    # order the labeled points from nearest to farthest
    by_distance = sorted(labeled_points,
                         key=lambda point_label: distance(point_label[0], new_point))
    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]]

    # and let them vote
    return majority_vote(k_nearest_labels)


# 근접한 k개수 중에서 빈도수가 제일 높은 값을 반환
def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)  # 각 ud_Nd에 대해 개수를 딕셔너리형태로 표현, vote_counts.values()는 각 요소에 대한 값들에 리스트형태로 표현
    winner, winner_count = vote_counts.most_common(1)[0]  # 빈도수가 제일 높은것 하나만 선택, 만약 k가 3이면 3개의 값을 가지는 레이블중에서 제일 많은 것을 선택, 값이랑 개수를 쌍으로 튜플로 표현

    # 동률인 값이 몇 개인지 정함
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count])

    # 동률인 경우 else문에서 맨 뒤에서 한 개를 제외, num_winners가 1이 될 때까지 재귀
    if num_winners == 1:
        return winner  # unique winner, so return it
    else:
        return majority_vote(labels[:-1])  # try again without the farthest


# csv 파일로 저장
def save_machined_data(lines):
    wf = open('stock_history_K.csv', 'w', newline='')
    csv_writer = csv.writer(wf)
    for line in lines:
        csv_writer.writerow(line)


def plot_state_borders(plt, color='0.8'):
    pass


# knn을 실행하여 scatter로 표현
def classify_and_plot_grid(k, index1, index2):
    plots = {0: ([], []), 1: ([], []), -1: ([], [])}
    markers = {0: "o", 1: "s", -1: "^"}
    colors = {0: "r", 1: "b", -1: "g"}

    plots1 = {0: ([], []), 1: ([], []), -1: ([], [])}
    markers1 = {0: "o", 1: "s", -1: "^"}
    colors1 = {0: "black", 1: "black", -1: "black"}

    NZ_lines = Normalization_index(lines)
    newlines = sel_idvVal_newLable(NZ_lines, index1, index2)
    newlines = [tuple(newlines[num]) for num in range(len(newlines))]  # knn 함수 이용하기 위해 리스트를 튜플로 변환

    # newlines(전체 데이터)의 30%를 test 데이터, 70%를 training 데이터
    test_data_lable = [([val1, val2], ud_Nd) for val1, val2, ud_Nd in newlines[int(len(newlines) * 0.7):]]
    training_data_lable = [([val1, val2], ud_Nd) for val1, val2, ud_Nd in newlines[:int(len(newlines) * 0.7)]]

    for val, ud_nd in test_data_lable:
        predicted_ud_Nd = knn_classify(k, training_data_lable, val)
        plots1[predicted_ud_Nd][0].append(val[0])
        plots1[predicted_ud_Nd][1].append(val[1])

    for val, ud_nd in training_data_lable:
        plots[ud_nd][0].append(val[0])
        plots[ud_nd][1].append(val[1])

    # create a scatter series for each language
    for ud_Nd, (x, y) in plots.items():
        plt.scatter(x, y, color=colors[ud_Nd], marker=markers[ud_Nd],
                    label=ud_Nd, zorder=0)

    for ud_Nd, (x, y) in plots1.items():
        plt.scatter(x, y, color=colors1[ud_Nd], marker=markers1[ud_Nd],
                    label=ud_Nd, zorder=0)

    plot_state_borders(plt, color='black')  # assume we have a function that does this

    plt.legend(loc=0)  # let matplotlib choose the location
    plt.title(str(k) + "-Nearest Neighbor ud_3d")
    plt.show()


# 새로운 레이블의 독립변수1,2를 통해 종속변수 ud_Nd의 정확도를 구함
def cal_testdata_correct(test_data_lable, training_data_lable):

    list_correct=[]
    for k in k_list:
        num_correct = 0
        for val, ud_nd in test_data_lable:
            predicted_ud_Nd = knn_classify(k, training_data_lable, val)
            if predicted_ud_Nd == ud_nd:
                num_correct += 1
        list_correct.append(num_correct)

    return list_correct


# k에 따른 정확도 리스트로 저장
def classify_k_correct(list_correct, test_data_lable, i1, i2):

    k_correct=[]
    k_correct.append(i1)
    k_correct.append(i2)
    for n in range(len(k_list)):
        k_correct.append(round(list_correct[n] / len(test_data_lable) * 100, 2))
    return k_correct


if __name__  =="__main__":

    tmp_lines = []
    NZ_lines = Normalization_index(lines)   # 값이 큰 인덱스에 대하여 0.01을 곱셈연산하여 정규화시킴

    # 가공된 데이터 레이블에서 독립변수1,2의 인덱스를 선택하여 새로운 레이블을 생성
    # index 3부터 13까지 모든 경우의 수에 대해 k=1부터 7까지 확률 계산(ud_Nd제외)
    for index1 in range(3, 18):
        if index1 == 12: continue

        for index2 in range(index1, 18):
            if (index2 == 12) or (index1 == index2): continue

            newlines = sel_idvVal_newLable(NZ_lines, int(index1), int(index2))
            newlines = [tuple(newlines[num]) for num in range(len(newlines))]  # knn 함수 이용하기 위해 리스트를 튜플로 변환

            # newlines(전체 데이터)의 30%를 test 데이터, 70%를 training 데이터
            test_data_lable = [([val1, val2], ud_Nd) for val1, val2, ud_Nd in newlines[int(len(newlines) * 0.7):]]
            training_data_lable = [([val1, val2], ud_Nd) for val1, val2, ud_Nd in newlines[:int(len(newlines) * 0.7)]]

            list_correct = cal_testdata_correct(test_data_lable, training_data_lable)
            k_correct = classify_k_correct(list_correct, test_data_lable, index1, index2)

            # 리스트안에 리스트 형식으로 저장
            tmp_lines.append(k_correct[:])

    tmp_list = []
    # 오버피팅 처리하기 위해 오차범위를 넘어서는 리스트 삭제
    for num in range(len(tmp_lines)):
        i=0
        j=0
        for n1 in range(2, 7):
            for n2 in range(3, 7):
                if n1 == n2: break
                if int(abs(tmp_lines[num][n1]-tmp_lines[num][n2])) < 5:
                    i+=1
                else:
                    j+=1
        if i>0 and j==0:
            tmp_list.append(tmp_lines[num])

    # k=3,5,7 순으로 정렬하여 csv파일로 저장
    for n in range(2, len(k_list)+2):
        new_list = sorted(tmp_list, key=lambda line_n: line_n[:][n])

    new_list.insert(0, names)
    save_machined_data(new_list)

    K=5
    # k에 대해 정확도가 제일 높은 인덱스2개를 통해 그래프로 그려줌(scatter)
    classify_and_plot_grid(K, new_list[len(new_list)-1][0], new_list[len(new_list)-1][1])
