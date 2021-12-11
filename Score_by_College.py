import pandas as pd

list = ['서울대', '연세대', '고려대', '한양대', '중앙대']

kor_highest = 149#국어 표준점수 최고점
math_highest = 147#수학 표준점수 최고점

eng_seo = [0, 0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
eng_yon = [0, 0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
eng_ko = [0, 3, 6, 9, 12, 15, 18, 21, 24]
eng_han = [100, 98, 94, 88, 80, 70, 58, 44, 28]
eng_jung = [100, 98, 94, 88, 80, 70, 58, 44, 28]

han_seo = [0, 0, 0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
han_yon = [10, 10, 10, 10, 9.8, 9.6, 9.4, 9.2, 9.0]
han_ko = [10, 10, 10, 10, 9.8, 9.6, 9.4, 9.2, 8.0]
han_han = [0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
han_jung = [10, 10, 10, 10, 10, 9.6, 9.2, 8.8, 8.4]

byun = pd.read_excel('./2022_변환표점.xls')
korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history =\
    map(int, input("1. 국어 표점 2. 수학 표점 3. 탐구 표점 합 4. 탐구1 백분위 5. 탐구2 백분위 6. 영어 등급 7. 한국사 등급 순으로 입력해주세요 >").split())

def byun_finder(uni, inquiry1, inquiry2):
    if len(byun[byun['대학명']==uni]['계열코드'].unique()) == 2:
        return byun[ (byun['대학명']==uni) & (byun['계열코드'] == '자연') & (byun['백분위'] == inquiry1)]['변환점수'].values[0]\
                   + byun[ (byun['대학명']==uni) & (byun['계열코드'] == '자연') & (byun['백분위'] == inquiry2)]['변환점수'].values[0]

    elif len(byun[byun['대학명']==uni]['계열코드'].unique()) == 3:
        return byun[(byun['대학명'] == uni) & (byun['계열코드'] == '직탐') & (byun['백분위'] == inquiry1)]['변환점수'].values[0] \
               + byun[(byun['대학명'] == uni) & (byun['계열코드'] == '직탐') & (byun['백분위'] == inquiry2)]['변환점수'].values[0]

def cal_score(korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history, score_by_college):
    #서울대
    score_by_college['서울대'] = korean*1 + math*1.2 + inquiry_std*0.8 - eng_seo[english-1] - han_seo[history-1]

    #연세대
    yon_byun = byun_finder('연세대', inquiry_ba1, inquiry_ba2)
    score_by_college['연세대'] = (korean + math*1.5 + (yon_byun)*1.5 + (100 - eng_yon[english-1]))*(10/9)+han_yon[history-1]

    #고려대
    ko_byun = byun_finder('고려대', inquiry_ba1, inquiry_ba2)
    score_by_college['고려대'] = (korean + math*1.2 + (ko_byun)*1)/640*1000-eng_ko[english-1] + han_ko[history-1]

    #한양대
    han_byun = byun_finder('한양대', inquiry_ba1, inquiry_ba2)
    score_by_college['한양대'] = korean/149*0.2*1000 + math/147*0.35*1000 + han_byun/(66.75*2)*0.35*1000+ eng_han[english-1] - han_han[history-1]\
    #과목에 나눈 값들은 각 과목 최고 표점/변환표점

    #중앙대
    jung_byun = byun_finder('중앙대', inquiry_ba1, inquiry_ba2)
    score_by_college['중앙대'] = korean*0.4*5 + math*0.4*5 + jung_byun*0.2*5 +eng_jung[english-1]+han_jung[history-1]
    return score_by_college
    # score_by_college['한양대'] = #

score_by_college = pd.Series(dtype=float)

print(cal_score(korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history, score_by_college))