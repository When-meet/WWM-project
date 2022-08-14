from concurrent.futures import ProcessPoolExecutor
from msvcrt import kbhit
from django.shortcuts import render

# 1. 프론트엔드에서 그룹원별 위치 정보(위도, 경도) 받는 함수  
import requests
import json
def post(request):
    if request.method =='POST':
        latitude = request.get.GET('latitude')
        longitude = request.get.GET('longtitude')
    return latitude, longitude

# 2. 중간 지점 및 가장 가까운 지하철 역 뿌리는 view 

# 2-1. 그룹원별 위치 정보(위도, 경도)의 평균 계산 함수
def locate(request):
    global result1, result2   # 전역 변수 => result1 위도 총 합 / result2 경도 총 합 
    global people             # 전역 변수 => 총 인원수

    if request.method =='POST':
        people+=1       #인원수 증가
        x = request.get.GET('x')    # 위도 값 받기
        y = request.get.GET('y')    # 경도 값 받기
        result1 += x     #위도 값들의 합
        result2 += y     #경도 값들의 합
    return    

#만약 위의 전체 인원 입력 끝나면 average 함수 호출
def average(x, y):      #전체 인원 평균 함수
    x = result1/people  #위도 평균 값
    y = result2/people  #경도 평균 값
    return x,y          # 중간 지점의 위도 경도 값

# 2-2. 서울시 역사마스터 정보.csv dataframe 형태로 저장
# - 컬럼: 역사_ID, 역사명, 호선, 위도, 경도 
import pandas as pd 
df = pd.read_csv ('/서울시 역사마스터 정보.csv',encoding='EUC-KR')

# 2-3. 행별로 돌리면서 두 점(중간 지점의 위도 경도, 역 위도 경도) 사이의 거리 계산 및 최솟값 구하기 
from haversine import haversine
def find(x,y):  #중간지점 (위도, 경도) 
    num= float(500)     #초기에 비교하기 위해 1회성으로 임의로 넣은 값

    for i in range(764): # 전체 행 개수 만큼 비교
    #중간지점 위도, 경도
        average_palce= (x, y)
    #지하철역 위도, 경도
        station = (df.loc[i, '위도'], df.loc[i, '경도'] ) 
    # 거리 계산
        num1 = haversine(average_palce, station, unit = 'km')   #중간지점과 역 사이의 거리 값(km)

        if num >num1:
            num = num1
        else:
            num = num   
    return num     #초기에 비교하기 위해 임의로 넣은 값 반환

