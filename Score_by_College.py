import pandas as pd
import logging

kor_highest = 149#국어 표준점수 최고점
math_highest = 147#수학 표준점수 최고점

eng_seo = [0, 0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
eng_yon = [100, 95, 87.5, 75, 60, 40, 25, 12.5, 5]
eng_ko = [0, 3, 6, 9, 12, 15, 18, 21, 24]
eng_han = [100, 98, 94, 88, 80, 70, 58, 44, 28]
eng_han_in = [100, 96, 90, 82, 72, 60, 46, 30, 12]
eng_jung = [100, 98, 95, 92, 86, 75, 64, 58, 50]
eng_su = [100, 99, 98, 97, 96, 95, 94, 93, 92]
eng_keon = [200, 198, 196, 193, 188, 183, 180, 170, 160]
eng_keon_in = [200, 196, 193, 188, 183, 180, 170, 160, 150]

han_seo = [0, 0, 0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
han_yon = [10, 10, 10, 10, 9.8, 9.6, 9.4, 9.2, 9.0]
han_ko = [10, 10, 10, 10, 9.8, 9.6, 9.4, 9.2, 8.0]
han_ko_in = [10, 10, 10, 9.8, 9.6, 9.4, 9.2, 9, 8]
han_han = [0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
han_han_in = [0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
han_jung = [10, 10, 10, 10, 9.6, 9.2, 8.8, 8.4, 8.0]
han_su = [10, 10, 10, 10, 9.5, 9.0, 8.5, 8.0, 7.5]
han_keon = [200, 200, 200, 200, 196, 193, 188, 183, 180]

byun = pd.read_excel('./2022_변환표점.xls')
korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history =\
    map(int, input("1. 국어 표점 2. 수학 표점 3. 탐구 표점 합 4. 탐구1 백분위 5. 탐구2 백분위 6. 영어 등급 7. 한국사 등급 순으로 입력해주세요 >").split())

score_by_college = pd.Series(dtype=float)
def byun_finder(uni, type, inquiry1, inquiry2):
    if len(byun[byun['대학명']==uni]['계열코드'].unique()) == 2:
        return byun[ (byun['대학명']==uni) & (byun['계열코드'] == type) & (byun['백분위'] == inquiry1)]['변환점수'].values[0]\
                   + byun[ (byun['대학명']==uni) & (byun['계열코드'] == type) & (byun['백분위'] == inquiry2)]['변환점수'].values[0]

    elif len(byun[byun['대학명']==uni]['계열코드'].unique()) == 3:
        return byun[(byun['대학명'] == uni) & (byun['계열코드'] == '직탐') & (byun['백분위'] == inquiry1)]['변환점수'].values[0] \
               + byun[(byun['대학명'] == uni) & (byun['계열코드'] == '직탐') & (byun['백분위'] == inquiry2)]['변환점수'].values[0]

def cal_score(korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history, score_by_college):
    #서울대
    score_by_college['서울대'] = korean*1 + math*1.2 + inquiry_std*0.8 - eng_seo[english-1] - han_seo[history-1]

    #연세대
    yon_byun = byun_finder('연세대', '자연', inquiry_ba1, inquiry_ba2)
    yon_byun_in = byun_finder('연세대', '인문', inquiry_ba1, inquiry_ba2)
    score_by_college['연세대(자연)'] = (korean + math*1.5 + (yon_byun)*1.5 + eng_yon[english-1])*(10/9)+han_yon[history-1]
    score_by_college['연세대(인문)'] = (korean + math + yon_byun_in/2 +eng_yon[english-1])*(10/6)+han_yon[history-1]

    #고려대
    ko_byun = byun_finder('고려대', '자연', inquiry_ba1, inquiry_ba2)
    ko_byun_in = byun_finder('고려대', '인문', inquiry_ba1, inquiry_ba2)
    score_by_college['고려대(자연)'] = (korean + math*1.2 + (ko_byun)*1)/640*1000-eng_ko[english-1] + han_ko[history-1]
    score_by_college['고려대(인문)'] = (korean + math + ko_byun_in*0.8) / 560 * 1000 - eng_ko[english - 1] + han_ko_in[history - 1]

    #한양대
    han_byun = byun_finder('한양대', '자연', inquiry_ba1, inquiry_ba2)
    han_byun_in = byun_finder('한양대', '인문', inquiry_ba1, inquiry_ba2)
    inquiry_highest = byun_finder('한양대', '자연', 100, 100)
    inquiry_highest_in = byun_finder('한양대', '인문', 100, 100)
    score_by_college['한양대(자연)'] = korean/149*0.2*1000 + math/147*0.35*1000 + han_byun/inquiry_highest*0.35*1000+ eng_han[english-1] - han_han[history-1]
    score_by_college['한양대(인문)'] = korean/149*0.3*1000 + math/147*0.3*1000 + han_byun_in/inquiry_highest_in*0.3*1000 + eng_han_in[english-1] - han_han_in[history-1]
    score_by_college['한양대(상경)'] = korean/149*0.3*1000 + math/147*0.4*1000 + han_byun_in/110*0.2*1000 + eng_han_in[english - 1] - han_han_in[history - 1]
    #과목에 나눈 값들은 각 과목 최고 표점/변환표점

    #중앙대
    jung_byun = byun_finder('중앙대', '자연', inquiry_ba1, inquiry_ba2)
    jung_byun_in = byun_finder('중앙대', '인문', inquiry_ba1, inquiry_ba2)
    score_by_college['중앙대(자연)'] = korean*0.4*5 + math*0.4*5 + jung_byun*0.2*5 +eng_jung[english-1]+han_jung[history-1]
    score_by_college['중앙대(인문)'] = korean*0.4*5 + math*0.4*5 + jung_byun_in*0.2*5 + eng_jung[english-1] + han_jung[history-1]

    #서강대
    su_byun = byun_finder('서강대', '자연', inquiry_ba1, inquiry_ba2)
    su_byun_in = byun_finder('서강대', '인문', inquiry_ba1, inquiry_ba2)
    score_by_college['서강대(자연)'] = korean*1.1 + math*1.3 + su_byun*0.6 + eng_su[english-1] + han_su[history-1]
    score_by_college['서강대(인문)'] = korean * 1.1 + math * 1.3 + su_byun_in * 0.6 + eng_su[english - 1] + han_su[history - 1]

# # 로그 생성
# logger = logging.getLogger()
#
# # 로그의 출력 기준 설정
# logger.setLevel(logging.INFO)
#
# # log 출력 형식
# formatter = logging.Formatter('%(asctime)s \n%(message)s')
#
# # log를 파일에 출력
# file_handler = logging.FileHandler('my.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
#
# logger.info(cal_score(korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history, score_by_college))

cal_score(korean, math, inquiry_std, inquiry_ba1, inquiry_ba2, english, history, score_by_college)
print(score_by_college)