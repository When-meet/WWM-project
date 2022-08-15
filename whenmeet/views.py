from django.shortcuts import render
from wwmgroup.models import WwmGroup
from accounts.models import User
from datetime import timedelta
# 1-1. 그룹타임 테이블 뿌리는 view -> group_id를 받아야됨
def post_group_timetable(request,pk):
    if request.method == 'GET':
        date = []
        group = WwmGroup.objects.get(id = pk)
        start_date = group.startdate
        end_date = group.enddate
        day_count = (end_date - start_date).days + 1
        for single_date in (start_date + timedelta(n) for n in range(day_count)):
            date.append(str(single_date))
        user_count = len([user for user in group.user.all()])
        timetable = create_group_timetable(pk,start_date,end_date)
        result = get_result(timetable,user_count)
        context = {
            'groupname': group.groupname,
            'timetable' : timetable, #리스트 형이며 리스트의 요소는 안되는사람의 이름들의 리스트임
            'startdate' : str(start_date), 
            'enddate' : str(end_date),
            'date' : date, 
            'result_list' : result,
            'result_count' : user_count - len(timetable[result[0]]),
            'user_count' : user_count,
        }
        return render(request,'index.html',context)
# 1-2. 개인타임 테이블 뿌리는 view -> 시작일을 name = startdate 로 받아야됨
def post_personal_timetable(request):
    user = User.objects.get(id = '1')
    start = get_weekday(request.POST.get('startdate'))
    timetable = user.avaliablity_days_time
    timetable = timetable[start*24:]+timetable[:start*24]

    context = {
            'timetable' : timetable, #string 형으로 반환
            'startdate' : start, # index
    }
    return render(request,'test.html',context)
# 2-1. 그룹원들 타임 테이블 취합하는 view 
# - wwmgroup modeld의 avaliablity_cal_length 속성 사용 
# - 유저의 avaliablity_days_time가 일주일 기준으로 월요일부터 총 24글자씩이라고 가정
# - 유저의 avaliablity_days_time을 24씩 분리해서 wwmGroup의 시작요일과 매칭해서 24시간씩 비교 
def create_group_timetable(group_id,start_date,end_date):
    timetable = []
    start = get_weekday(start_date)
    end = get_weekday(end_date)
    day_count = (end_date - start_date).days + 1

    group = WwmGroup.objects.get(id = group_id)
    users_timetables = [[user.name,user.avaliablity_days_time] for user in group.user.all()]
    users = [data[0] for data in users_timetables]
    availity_times = [data[1] for data in users_timetables]
    timetables = []
    for availity_time in availity_times:
        formatted_time = ''
        for i in range(start,start+day_count):
            if (i+1)%7==0:
                formatted_time += availity_time[24*(i%7):]

            else:
                formatted_time += availity_time[24*(i%7):24*((i+1)%7)]
        timetables.append(formatted_time)
    binds = list(map(list,zip(*timetables)))
    for bind in binds:
        timetable.append([users[i] for i in range(len(bind)) if bind[i]=='0'])
    return timetable
# 2-2. 시작 요일 구하는 view
# - 숫자 return 0(월), 1(화), 2(수) …  
# [python에서 datetime  불러와서 요일 구하는 로직] : https://ddolcat.tistory.com/688
def get_weekday(date):
    return date.weekday()



def get_result(timetable,count):
    min_len = count
    result = []
    for i in range(len(timetable)):
        if(min_len>len(timetable[i])):
            result = []
            result.append(i)
            min_len = len(timetable[i])
        elif min_len == len(timetable[i]):
            result.append(i)
    return result
