from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import Http404
import requests, xmltodict
from .models import Staff, Check, Course, Sub_Course, Course_Pretest, Staff_Score, Staff_Vdolog , Feedback, Evaluate_t, Closed_class, Hub_test, Bu_test
import string
from django.db.models import Avg
from datetime import datetime
from itertools import zip_longest
import re
from django.db.models import Count, Sum,Q,F
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
import json
from django.db.models import Count, Sum,Q,F
#Export to Excel
import itertools
import xlwt
from datetime import date
from django.http import HttpResponse
from django.contrib.auth.models import User


def login(request):
    mgs = {
                    'massage' : ' '
                }
    if request.method == 'POST':
        Emp_id = request.POST.get('userID')
        Emp_pass = str(request.POST.get('passwordID'))

        # print(Emp_id,Emp_pass)
        check = Check.objects.filter(StaffID=Emp_id).count()

        if check == 1:
            reposeMge = 'true'
        # if Emp_id == '300109' or Emp_id == '498433' or Emp_id == '505397' or Emp_id == '495186' or  Emp_id =='510117' or Emp_id == '504636' or Emp_id == '499700' or Emp_id == '499691' or Emp_id == '499734' or Emp_id == '498610' :
        #     reposeMge = 'true'
            #มีปัญหากับการเช็คpassword ผ่านidm
        elif Emp_id == '502979' or Emp_id == '509024' or Emp_id == '505330' or Emp_id == '509805' or Emp_id == '505321' or Emp_id == '501103' or Emp_id == '502041' :
             reposeMge = 'true'
        else:
            check_ID = idm_login(Emp_id,Emp_pass)
            # print(check_ID)
            reposeMge = check_ID
        
        if reposeMge == 'true':
                nameget = idm(Emp_id)
                # print(nameget)
                Fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                Position = nameget['PositionDescShort']
                LevelCode = nameget['LevelCode']
                Dept = nameget['DepartmentShort']
                Dept_code = nameget['NewOrganizationalCode']
                RegionCode = nameget['RegionCode']
                Gender = nameget['Gender']
                request.session['Emp_id'] = Emp_id
                request.session['Fullname'] = Fullname
                request.session['Position'] = Position
                request.session['LevelCode'] = LevelCode
                request.session['Department'] = Dept
                request.session['Dept_code'] = Dept_code
                request.session['RegionCode'] = RegionCode 
                request.session['Gender'] = Gender
                # 9900
                check_user = Staff.objects.filter(StaffID=Emp_id).count()
                if check_user == 0 :
                    Staff_save = Staff(
                        StaffID = Emp_id,
                        StaffName = Fullname,
                        StaffPosition = Position,
                        StaffLevelcode = LevelCode,
                        StaffDepshort = Dept,
                        DeptCode = Dept_code,
                        Organization = RegionCode,
                    )
                    Staff_save.save()

                    return redirect('home')
                else:
                    Staff_score = Staff.objects.get(StaffID = Emp_id)
                    print(Staff_score)
                return redirect('home')
        else:
                mgs = {
                    'massage' : 'รหัสพนักงานหรือรหัสผ่านไม่ถูกต้อง....'
                }
                # return redirect('login',{'mgs':mgs})

    return render(request,'login.html',{'mgs':mgs})

def menu(request):
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    
    return render(request,'menu.html',{'Profile':Profile})

def home(request):
    Emp_id = request.session['Emp_id']
    Fullname = request.session['Fullname']
    Position = request.session['Position']
    LevelCode = request.session['LevelCode']
    Dept = request.session['Department']
    RegionCode = request.session['RegionCode']
    # Score = Staff_Score.objects.get(StaffID = Emp_id)
    close_check = len(Closed_class.objects.filter(StaffID = Emp_id, Status = True))
    # Course_all = Closed_class.objects.select_related('Link_course').filter(StaffID = Emp_id, Status = True)
    print(close_check)
    if close_check == 1 or close_check == '1':
        Course_all = Course.objects.filter(id = 18)
        Count_view = len(Staff_Vdolog.objects.filter(Link_course= 18))
        print(Count_view)
    elif close_check > 1 : 
        Course_all = Course.objects.all().order_by('id')
        # Count_view = len(Staff_Vdolog.objects.select_related('Link_course').order_by('Link_course'))
    else :
        Course_all = Course.objects.all().order_by('id').exclude(id = 11)
        Count_view = Staff_Vdolog.objects.select_related('Link_course').exclude(id = 11).annotate(Count('id'))
        # print(Count_view)

    # print(Course_all)
    Name_Course = []
    Count_view_label = []
    Count_view_values = []

    Count_view = Staff_Vdolog.objects.values('Link_course__CourseName','Link_course__CourseStatus','Link_course__id','Link_course__Cover_img','Link_course__CourseBy','Link_course__Course_Pass_Score').filter(Link_course__CourseStatus = 'ON').annotate(Count('Link_course__id')).order_by('Link_course')
    for j in Count_view :
        #print(j['Link_course__CourseName'],j['Link_course__id__count'],j['Link_course__Course_Pass_Score'],j['Link_course__id'])

                # Count_view_label.append(j['Link_course__'])
                # Count_view_values.append(j['Link_course__Count'])
        # Staff_Score.objects.select_related('Staff').filter(Link_course_id=1).filter(Post_Score__gte=9).order_by('Staff__DeptCode')
        compare_total_test = Staff_Score.objects.filter(Link_course_id=j['Link_course__id']).filter(Post_Score__gte=j['Link_course__Course_Pass_Score']).values('Link_course__id','Link_course__Course_Pass_Score').annotate(Count('Link_course__id')).order_by('Link_course')
        for k in compare_total_test:
            #print(j['Link_course__CourseName'],j['Link_course__id__count'],k['Link_course__id__count'])
            Name_Course.append(j['Link_course__CourseName'])
            Count_view_label.append(j['Link_course__id__count'])
            Count_view_values.append(k['Link_course__id__count'])
    total ={
        'Name_Course' : Name_Course,
        'Count_view_label' : Count_view_label,
        'Count_view_values': Count_view_values
    }
    #print(total['Name_Course'])
    Course_score = Staff_Score.objects.select_related('Link_course').filter(Staff = Staff.objects.get(StaffID = Emp_id)).order_by('Link_course')
    combined_results = list(zip_longest(Course_all ,Course_score))
    # print(combined_results)
    # Course_name = list(zip_longest(Course_all, Course_score))
    
    Profile= {
        'Emp_id' : Emp_id,
        'Fullname' : Fullname,
        'Position' : Position,
        'LevelCode' : LevelCode,
        'Dept' : Dept,
        'RegionCode':RegionCode,
        }
    return render(request, 'home.html',{'Profile':Profile, 'Course_all': Course_all ,'combined_results':combined_results,'Course_score':Course_score,'Count_view':Count_view})

def idm_login(Emp_id, Emp_pass):
    # Emp_passc = str(Emp_pass)
    print('--------------------')
    
    url="https://idm.pea.co.th/webservices/idmservices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <IsValidUsernameAndPassword_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <Username>{1}</Username>
                        <Password>{2}</Password>
                        </IsValidUsernameAndPassword_SI>
                    </soap:Body>
                </soap:Envelope>'''
    wskey = '07d75910-3365-42c9-9365-9433b51177c6'
    body = xmltext.format(wskey,Emp_id,Emp_pass)
    response = requests.post(url,data=body,headers=headers)
    # print(response.status_code)
    o = xmltodict.parse(response.text)
    jsonconvert=dict(o)
    # print(o)
    authen_response = jsonconvert["soap:Envelope"]["soap:Body"]["IsValidUsernameAndPassword_SIResponse"]["IsValidUsernameAndPassword_SIResult"]["ResultObject"]
    return authen_response

def idm(Emp_id):
    url="https://idm.pea.co.th/webservices/EmployeeServices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <GetEmployeeInfoByEmployeeId_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <EmployeeId>{1}</EmployeeId>
                        </GetEmployeeInfoByEmployeeId_SI>
                </soap:Body>
                </soap:Envelope>'''
    wsauth = 'e7040c1f-cace-430b-9bc0-f477c44016c3'
    body = xmltext.format(wsauth,Emp_id)
    response = requests.post(url,data=body,headers=headers)
    o = xmltodict.parse(response.text)

    # print(o)
    jsonconvert=o["soap:Envelope"]['soap:Body']['GetEmployeeInfoByEmployeeId_SIResponse']['GetEmployeeInfoByEmployeeId_SIResult']['ResultObject']
    employeedata = dict(jsonconvert)
    # print(employeedata['FirstName'])
    return employeedata

def Course_main(request, PK_Course_D):
    Emp_id = request.session['Emp_id']

    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    
    Course_detail = Course.objects.get(id=PK_Course_D)
    Staff_score_check = Staff_Score.objects.filter(Staff = Staff.objects.get(StaffID = Emp_id), Link_course = Course.objects.get(id = PK_Course_D)).count
    print(Staff_score_check)
    if Staff_score_check() > 0:
        if PK_Course_D != 18:
            Staff_score = Staff_Score.objects.get(Staff = Staff.objects.get(StaffID = Emp_id), Link_course = Course.objects.get(id = PK_Course_D))
            pre = Staff_score.Pre_Score
            post = Staff_score.Post_Score
        else :
            print(PK_Course_D)
            pre = "0"
            post = "0"
    else:
        Staff_prescore_create = Staff_Score(
                    Pre_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    Pre_Score = 0,
                    Post_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    Post_Score = 0,
                    Staff = Staff.objects.get(StaffID = Emp_id),
                    Link_course = Course.objects.get(id = PK_Course_D)
                    )
        Staff_prescore_create.save()
        Staff_score = Staff_Score.objects.get(Staff = Staff.objects.get(StaffID = Emp_id), Link_course = Course.objects.get(id = PK_Course_D))
        pre = Staff_score.Pre_Score
        post = Staff_score.Post_Score
        

    Sub_course = Sub_Course.objects.filter(Link_Course = Course.objects.get(id=PK_Course_D)).order_by('id')
    # Sub_course_check = Sub_Course.objects.all().prefetch_related('SubCourse_Vdo').filter(Link_Course = Course.objects.get(id=PK_Course_D)).values()

    Sub_course_check = Staff_Vdolog.objects.all().filter(Link_course = Course.objects.get(id=PK_Course_D),Staff = Staff.objects.get(StaffID = Emp_id)).order_by('Link_SubCourse')
    # Sub_course_check_personal = Staff_Vdolog.objects.all().filter(Link_course = Course.objects.get(id=PK_Course_D),Staff = Staff.objects.get(StaffID = Emp_id)).order_by('Link_SubCourse')
    combined_results = list(zip_longest(Sub_course, Sub_course_check))
    # print(combined_results)
    # queryset = Staff_Vdolog.objects.all().select_related('Link_course').filter(Link_course = Course.objects.get(id=PK_Course_D),Staff = Staff.objects.get(StaffID = Emp_id))
    # print(queryset.query)
    # sub = queryset[0]
    # all attendances for the student
    # attendances = sub.Link_SubCourse.all()
    # print(attendances)
    # select_pass_label = []
    # subcourse_check = Sub_Course.objects.filter(Link_Course = Course.objects.get(id=PK_Course_D))
    # Sub_course_test = Sub_Course.objects.filter(Link_Course = Course.objects.get(id=PK_Course_D)).order_by('id')
    # for t in Sub_course_test:
    #     vdolog = Staff_Vdolog.objects.all().filter(Link_course = Course.objects.get(id=PK_Course_D),Staff = Staff.objects.get(StaffID = Emp_id)).order_by('Link_SubCourse')
    #     for v in vdolog :
    #         if t.id == v.Link_SubCourse.id:
    #          print('pass',v.Staff)
    #         else:
    #          print('join',t.id,v.Link_SubCourse.id)

    
    vdo = Staff_Vdolog.objects.filter(Status = 'Done',Staff = Staff.objects.get(StaffID = Emp_id),Link_course = Course.objects.get(id=PK_Course_D)).count()
    B_colour = check(Course_detail.Couse_Sub_Total,vdo)
    
    Evaluate = Evaluate_t.objects.filter(Staff = Staff.objects.get(StaffID = Emp_id),Link_course = Course.objects.get(id=PK_Course_D)).count()
    if Evaluate >=1:
        Evaluate = 1
    else:
        Evaluate = 0
    
    if PK_Course_D == 9 :
        check_Test = len(Hub_test.objects.filter(StaffID=Emp_id))
        if check_Test == 1:
            hub_score = Hub_test.objects.get(StaffID=Emp_id)
            Hub_status_test = hub_score.Status
            print('Hub_status_test',Hub_status_test)
        else :
            Hub_status_test = 0
    else :
        Hub_status_test = 0
    
    return render(request, 'Course_main.html',{'Profile':Profile,'Course_detail': Course_detail, 'Sub_course': Sub_course,'Sub_course_check':Sub_course_check, 'pre':pre, 'post':post, 'vdo': vdo, 'B_colour': B_colour, 'combined_results':combined_results, 'Evaluate':Evaluate,'Hub_status_test':Hub_status_test})

def eva_chart(request,PK_Course_D): #, PK_Course_D
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }

    avg_eva = {}
    for num in range(9):
        a='No_'
        num+=1
        avg_eva.update(Evaluate_t.objects.filter(Link_course = Course.objects.get(id = PK_Course_D)).aggregate(Avg(a+str(num))))
    print(avg_eva)
    no_1 = float(avg_eva['No_1__avg'])
    no_1 = round(no_1,2)
    no_2 = float(avg_eva['No_2__avg'])
    no_2 = round(no_2,2)
    no_3 = float(avg_eva['No_3__avg'])
    no_3 = round(no_3,2)
    no_4 = float(avg_eva['No_4__avg'])
    no_4 = round(no_4,2)
    no_5 = float(avg_eva['No_5__avg'])
    no_5 = round(no_5,2)
    no_6 = float(avg_eva['No_6__avg'])
    no_6 = round(no_6,2)
    no_7 = float(avg_eva['No_7__avg'])
    no_7 = round(no_7,2)
    no_8 = float(avg_eva['No_8__avg'])
    no_8 = round(no_8,2)
    no_9 = float(avg_eva['No_9__avg'])
    no_9 = round(no_9,2)
    total_eva = (no_1+no_2+no_3+no_4+no_5+no_6+no_7+no_8+no_9)/9
    total_eva = round(total_eva,2)
    data = []
    data.extend((no_1,no_2,no_3,no_4,no_5,no_6,no_7,no_8,no_9,total_eva))
    json.dumps(data)
    send_data ={
        'data':data
    }
    return render(request,'eva_chart.html',send_data)
    
def VDO(request, PK_Title):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Sub_course = Sub_Course.objects.select_related('Link_Course').get(id = PK_Title )
    print(Sub_course.Link_Course.id)
    if request.method == 'POST':
        check = Staff_Vdolog.objects.filter(Staff=Emp_id, Link_SubCourse = PK_Title).count()
        if check == 0:
            Staff_vdo_save = Staff_Vdolog(
                            Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            Status = 'Done',
                            Link_SubCourse = Sub_Course.objects.get(id = PK_Title),
                            Link_course = Course.objects.get(id = Sub_course.Link_Course.id),
                            Staff = Staff.objects.get(StaffID = Emp_id)
                        )
            Staff_vdo_save.save()
        else:
            Staff_vdo_update = Staff_Vdolog.objects.get(Staff=Emp_id, Link_SubCourse = PK_Title)
            Staff_vdo_update.Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Staff_vdo_update.Status = 'Done'
            Staff_vdo_update.save()
        
        return redirect('Course_main',PK_Course_D=Sub_course.Link_Course.id)
    
    return render(request, 'VDO.html',{'Profile':Profile,'Sub_course': Sub_course})

def check(Couse_Sub_Total,vdo):
    if Couse_Sub_Total == vdo:
        colour = 'Done'
    else:
        colour = 'False'
    return colour

def pretest(request, PK_Course_D):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Course_item = Course.objects.get(id = PK_Course_D)
    Question = Course_Pretest.objects.select_related('Test_Course').filter(Test_Course = Course.objects.get(id = PK_Course_D)).order_by('?')
    # print(Question)
    if request.method == 'POST':
        sum =0
        for key, value in request.POST.items():
                # print(key)
                # print(text_num_split(key))
                value = request.POST[key]
                # print(value)
                if value == '1' :
                    value = int(value)
                    sum += value
        # print('total',sum)
        
        check_StaffID = Staff_Score.objects.filter(Staff = Emp_id, Link_course = Course.objects.get(id = PK_Course_D)).count
        if check_StaffID == 0:
                Staff_prescore_create = Staff_Score(
                                                Pre_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                Pre_Score = sum,
                                                Staff = Staff.objects.get(StaffID = Emp_id),
                                                Link_course = Course.objects.get(id = PK_Course_D)
                                                    )
                Staff_prescore_create.save()
        else : 
            Staff_prescore_update = Staff_Score.objects.get(Staff = Emp_id, Link_course = PK_Course_D)
            Staff_prescore_update.Pre_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Staff_prescore_update.Pre_Score = sum
            Staff_prescore_update.save()

        return redirect('Course_main',PK_Course_D)

    return render(request, 'Pretest.html',{'Profile':Profile, 'Question': Question, 'Course_item':Course_item })

def posttest(request, PK_Course_D):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Course_item = Course.objects.get(id = PK_Course_D)
    Question = Course_Pretest.objects.select_related('Test_Course').filter(Test_Course = Course.objects.get(id = PK_Course_D)).order_by('?')
    # print(Question)
    if request.method == 'POST':
        sum =0
        for key, value in request.POST.items():
                # print(key)
                # print(text_num_split(key))
                value = request.POST[key]
                # print(value)
                if value == '1' :
                    value = int(value)
                    sum += value
        # print('total',sum)
         
        Staff_postscore_update = Staff_Score.objects.get(Staff = Emp_id, Link_course = PK_Course_D)
        Staff_postscore_update.Post_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Staff_postscore_update.Post_Score = sum
        Staff_postscore_update.save()

        return redirect('evaluate',PK_Course_D)
    return render(request, 'Posttest.html',{'Profile':Profile, 'Question': Question, 'Course_item':Course_item })

def check_ans(key,value):
    key_cut = key.split("dio")[1]
    # print(key_cut)
    return key_cut

def text_num_split(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return [item[:index]]

def errorstage(request):
    mgs = {
                    'massage' : ' '
                }
    if request.method == 'POST':
        Emp_id = request.POST.get('Emp_ID')
        detail = request.POST.get('detail')
        Staff_error_create = Check(
                            Date_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            StaffID = Emp_id,
                            Error_Detail = detail
                            )
        Staff_error_create.save()
        return redirect('login')
    
    return render(request,'errorstage.html',{'mgs':mgs})

def virtualclass(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    
    return render(request,'virtualclass.html',{'Profile':Profile})

def feedback(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        feedback_staff_create = Feedback(
                            Title = title,
                            Detail = detail,
                            Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            Staff = Staff.objects.get(StaffID = Emp_id)
                            )
        feedback_staff_create.save()
        return redirect('home')
    
    return render(request,'feedback.html',{'Profile':Profile})

def evaluate(request, PK_Course_D):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Course_item = Course.objects.get(id = PK_Course_D)
    Sub_Course_item = Sub_Course.objects.values('ConstructorName').filter(Link_Course = Course.objects.get(id = PK_Course_D)).annotate(dcount=Count('ConstructorName'))

    if request.method == 'POST':
        optradio1 = request.POST.get('optradio1')
        print(optradio1)
        optradio2 = request.POST.get('optradio2')
        print(optradio2)
        optradio3 = request.POST.get('optradio3')
        print(optradio3)
        optradio4 = request.POST.get('optradio4')
        print(optradio4)
        optradio5 = request.POST.get('optradio5')
        print(optradio5)
        optradio6 = request.POST.get('optradio6')
        print(optradio6)
        optradio7 = request.POST.get('optradio7')
        print(optradio7)
        optradio8 = request.POST.get('optradio8')
        print(optradio8)
        optradio9 = request.POST.get('optradio9')
        print(optradio9)
        if PK_Course_D == 17 :
            Eva_update  = Evaluate_t.objects.filter(Link_course = Course.objects.get(id = PK_Course_D), Staff =Staff.objects.get(StaffID = Emp_id))
            Usability = request.POST.get('Usability')
            Future_Subject = request.POST.get('Future_Subject')
            Suggestion = request.POST.get('Suggestion')
            eve_staff_create = Evaluate_t(
                                No_1 = optradio1,
                                No_2 = optradio2,
                                No_3 = optradio3,
                                No_4 = optradio4,
                                No_5 = optradio5,
                                No_6 = optradio6,
                                No_7 = optradio7,
                                No_8 = optradio8,
                                No_9 = optradio9,
                                Status = 1,
                                Usability = Usability,
                                Future_Subject = Future_Subject,
                                Suggestion = Suggestion,
                                Link_course = Course.objects.get(id = PK_Course_D),
                                Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                Staff = Staff.objects.get(StaffID = Emp_id)
                                )
            eve_staff_create.save()

        else :
            eve_staff_create = Evaluate_t(
                                No_1 = optradio1,
                                No_2 = optradio2,
                                No_3 = optradio3,
                                No_4 = optradio4,
                                No_5 = optradio5,
                                No_6 = optradio6,
                                No_7 = optradio7,
                                No_8 = optradio8,
                                No_9 = optradio9,
                                Status = 1,
                                Link_course = Course.objects.get(id = PK_Course_D),
                                Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                Staff = Staff.objects.get(StaffID = Emp_id)
                                )
            eve_staff_create.save()
        return redirect('Course_main',PK_Course_D)

    return render(request, 'evaluate.html',{'Profile':Profile, 'Course_item':Course_item, 'Sub_Course_item':Sub_Course_item })

def evaluate_audit(request, PK_Course_D):
    Emp_id = request.session['Emp_id']
    # Gender = request.session['Gender']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Course_item = Course.objects.get(id = PK_Course_D)
    Sub_Course_item = Sub_Course.objects.values('ConstructorName').filter(Link_Course = Course.objects.get(id = PK_Course_D)).annotate(dcount=Count('ConstructorName'))

    if request.method == 'POST':
        check_eve = len(Evaluate_t.objects.filter(Staff = Staff.objects.get(StaffID=Emp_id),Link_course= Course.objects.get(id = PK_Course_D)))
        # print(Gender)
        KM_Gender = request.POST.get('radioG')
        KM_Generation = request.POST.get('radioGen')
        print(KM_Generation)
        KM_B1 = request.POST.get('optradioA_1')
        KM_Day = request.POST.get('KM_Day')
        print(KM_Day)
        KM_Training = request.POST.get('KM_Training')
        print(KM_Training)
        KM_Meeting = request.POST.get('KM_Meeting')
        print(KM_Meeting)
        KM_DDoc = request.POST.get('KM_DDoc')
        KM_Leaflets = request.POST.get('KM_Leaflets')
        KM_email = request.POST.get('KM_email')
        KM_Vdo = request.POST.get('KM_Vdo')
        KM_Social = request.POST.get('KM_Social')
        KM_B3 = request.POST.get('optradioA_3')
        KM_B4 = request.POST.get('radioA_4')
        KM_B5 = request.POST.get('A_5')
        optradio1 = request.POST.get('optradio1')
        print(optradio1)
        optradio2 = request.POST.get('optradio2')
        print(optradio2)
        optradio3 = request.POST.get('optradio3')
        print(optradio3)
        optradio4 = request.POST.get('optradio4')
        print(optradio4)
        optradio5 = request.POST.get('optradio5')
        print(optradio5)
        optradio6 = request.POST.get('optradio6')
        print(optradio6)
        optradio7 = request.POST.get('optradio7')
        print(optradio7)
        optradio8 = request.POST.get('optradio8')
        print(optradio8)
        Suggestion = request.POST.get('Suggestion')
        print(Suggestion)
        
        if check_eve == 0 :
            eve_staff_create = Evaluate_t(
                            KM_Gender =KM_Gender,
                            KM_Generation=KM_Generation,
                            KM_B1 =KM_B1,
                            KM_Day = KM_Day,
                            KM_Training =KM_Training,
                            KM_Meeting=KM_Meeting,
                            KM_DDoc = KM_DDoc,
                            KM_Leaflets = KM_Leaflets,
                            KM_email = KM_email,
                            KM_Vdo = KM_Vdo,
                            KM_Social = KM_Social,
                            KM_B3 = KM_B3,
                            KM_B4 = KM_B4,
                            KM_B5 = KM_B5,
                            No_1 = optradio1,
                            No_2 = optradio2,
                            No_3 = optradio3,
                            No_4 = optradio4,
                            No_5 = optradio5,
                            No_6 = optradio6,
                            No_7 = optradio7,
                            No_8 = optradio8,
                            Suggestion = Suggestion,
                            Status = 1,
                            Link_course = Course.objects.get(id = PK_Course_D),
                            Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            Staff = Staff.objects.get(StaffID = Emp_id)
                            )
            eve_staff_create.save()
            return redirect('Course_main',PK_Course_D)
        else:
            print('done')
        return redirect('Course_main',PK_Course_D)

    return render(request, 'evaluate_audit.html',{'Profile':Profile, 'Course_item':Course_item, 'Sub_Course_item':Sub_Course_item })

def ihub_test(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    PK_Course_D = 9
    Course_item = Course.objects.get(id = PK_Course_D)
    Question = Course_Pretest.objects.select_related('Test_Course').filter(Test_Course = Course.objects.get(id = PK_Course_D)).order_by('?')
    # print(Question)
    check_test = len(Hub_test.objects.filter(StaffID = Emp_id))
    if request.method == 'POST':
        no1 = request.POST.get('no1')
        no2_1 = request.POST.get('no2_1_ans')
        no2_2 = request.POST.get('no2_2_ans')
        no2_3 = request.POST.get('no2_3_ans')
        no2_4 = request.POST.get('no2_4_ans')
        no2_5 = request.POST.get('no2_5_ans')
        no3 = request.POST.get('no3')
        no4 = request.POST.get('no4')
        no5 = request.POST.get('no5')
        no6 = request.POST.get('no6')
        no7 = request.POST.get('no7')
        no8 = request.POST.get('no8')
        no9 = request.POST.get('no9')
        no10 = request.POST.get('no10')
        if check_test == 0 :
            Hub_test_create = Hub_test(
                                no1 = no1,
                                no2_1 = no2_1,
                                no2_2 = no2_2,
                                no2_3 = no2_3,
                                no2_4 = no2_4,
                                no2_5 = no2_5,
                                no3 = no3,
                                no4 = no4,
                                no5 = no5,
                                no6 = no6,
                                no7 = no7,
                                no8 = no8,
                                no9 = no9,
                                no10 = no10,
                                Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                StaffID = Staff.objects.get(StaffID = Emp_id),
                                Status = '1'
                                )
            Hub_test_create.save()
            return redirect('evaluate',PK_Course_D)
        else:
            test = Hub_test.objects.get(StaffID = Emp_id)
            test.no1 = no1
            test.no2_1 = no2_1
            test.no2_2 = no2_2
            test.no2_3 = no2_3
            test.no2_4 = no2_4
            test.no2_5 = no2_5
            test.no3 = no3
            test.no4 = no4
            test.no5 = no5
            test.no6 = no6
            test.no7 = no7
            test.no8 = no8
            test.no9 = no9
            test.no10 = no10
            test.Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test.Status = '1'
            test.save()
            return redirect('Course_main',PK_Course_D)
        
    return render(request, 'ihub_test.html',{'Profile':Profile, 'Question': Question, 'Course_item':Course_item })

def BU_test(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    PK_Course_D = 4
    Course_item = Course.objects.get(id = PK_Course_D)
    if request.method == 'POST':
        no1 = request.POST.get('no1')
        BU_test_ans = Bu_test(
            no1 = no1,
            Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            StaffID = Emp_id,
            Status = '1'
        )
        BU_test_ans.save()

        Staff_postscore_update = Staff_Score.objects.get(Staff = Staff.objects.get(StaffID = Emp_id), Link_course = Course.objects.get(id = PK_Course_D))
        Staff_postscore_update.Post_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Staff_postscore_update.Post_Score = '10'
        Staff_postscore_update.save()

        return redirect('evaluate',PK_Course_D)
    return render(request, 'BU_test.html',{'Profile':Profile, 'Course_item':Course_item })

def ihub_score(request, Staff_ID):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    PK_Course_D = 9
    Course_item = Course.objects.get(id = PK_Course_D)
    # Question = Course_Pretest.objects.select_related('Test_Course').filter(Test_Course = Course.objects.get(id = PK_Course_D)).order_by('?')
    # print(Question)
    nameget = idm(Staff_ID)
    # print(nameget)
    User = {
        'Fullname' : nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName'],
        'Position' : nameget['PositionDescShort'],
        'LevelCode' : nameget['LevelCode'],
        'Dept' : nameget['DepartmentShort']
    }
    
    Answer_ihub = Hub_test.objects.get(StaffID = Staff_ID)
    if request.method == 'POST':
        no1_Score = request.POST.get('no1_Score')
        no2_1_Score = request.POST.get('no2_1_Score')
        no2_2_Score = request.POST.get('no2_2_Score')
        no2_3_Score = request.POST.get('no2_3_Score')
        no2_4_Score = request.POST.get('no2_4_Score')
        no2_5_Score = request.POST.get('no2_5_Score')
        no3_Score = request.POST.get('no3_Score')
        no4_Score = request.POST.get('no4_Score')
        no5_Score = request.POST.get('no5_Score')
        no6_Score = request.POST.get('no6_Score')
        no7_Score = request.POST.get('no7_Score')
        no8_Score = request.POST.get('no8_Score')
        no9_Score = request.POST.get('no9_Score')
        no10_Score = request.POST.get('no10_Score')
        feedback = request.POST.get('feedback')
        total = 0
        total = (int(no1_Score) + int(no2_1_Score) + int(no2_2_Score) + int(no2_3_Score) + int(no2_4_Score) + int(no2_5_Score) + int(no3_Score) + int(no4_Score) + int(no5_Score) + int(no6_Score) + int(no7_Score) + int(no8_Score) + int(no9_Score) + int(no10_Score))
        print(total)
        if total >= 70 :
            Status = '2'
        else:
            Status = '3'
        test = Hub_test.objects.get(StaffID = Staff_ID)
        test.no1_Score = no1_Score
        test.no2_1_Score = no2_1_Score
        test.no2_2_Score = no2_2_Score
        test.no2_3_Score = no2_3_Score
        test.no2_4_Score = no2_4_Score
        test.no2_5_Score = no2_5_Score
        test.no3_Score = no3_Score
        test.no4_Score = no4_Score
        test.no5_Score = no5_Score
        test.no6_Score = no6_Score
        test.no7_Score = no7_Score
        test.no8_Score = no8_Score
        test.no9_Score = no9_Score
        test.no10_Score = no10_Score
        test.total = total
        test.feedback = feedback
        test.Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test.Status = Status
        test.save()

        Staff_postscore_update = Staff_Score.objects.get(Staff = Staff.objects.get(StaffID = Staff_ID), Link_course = Course.objects.get(id = PK_Course_D))
        Staff_postscore_update.Post_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Staff_postscore_update.Post_Score = total
        Staff_postscore_update.save()
        return redirect('ihub_test_summary')

    return render(request, 'ihub_score.html',{'Profile':Profile, 'Course_item':Course_item ,'Answer_ihub':Answer_ihub, 'User' : User})

def ihub_test_summary(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    hub_score = Hub_test.objects.select_related('StaffID').filter(Status__in=['1', '4']).order_by('Date_Created')
    # summary = []
    # for i in hub_score:
    #     idm(i.StaffID)

    return render(request, 'ihub_test_summary.html',{'Profile':Profile, 'hub_score':hub_score })

def ihub_test_alter(request):
    Emp_id = request.session['Emp_id']
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    PK_Course_D = 9
    Course_item = Course.objects.get(id = PK_Course_D)
    # Question = Course_Pretest.objects.select_related('Test_Course').filter(Test_Course = Course.objects.get(id = PK_Course_D)).order_by('?')
    # print(Question)
    
    Answer_ihub = Hub_test.objects.get(StaffID = Emp_id)
    Sum_2 = (Answer_ihub.no2_1_Score)+(Answer_ihub.no2_2_Score)+(Answer_ihub.no2_3_Score)+(Answer_ihub.no2_4_Score)+(Answer_ihub.no2_5_Score)
    print(Sum_2)
    if request.method == 'POST':
        no1 = request.POST.get('no1')
        no2_1 = request.POST.get('no2_1_ans')
        no2_2 = request.POST.get('no2_2_ans')
        no2_3 = request.POST.get('no2_3_ans')
        no2_4 = request.POST.get('no2_4_ans')
        no2_5 = request.POST.get('no2_5_ans')
        no3 = request.POST.get('no3')
        no4 = request.POST.get('no4')
        no5 = request.POST.get('no5')
        no6 = request.POST.get('no6')
        no7 = request.POST.get('no7')
        no8 = request.POST.get('no8')
        no9 = request.POST.get('no9')
        no10 = request.POST.get('no10')
        test = Hub_test.objects.get(StaffID = Emp_id)
        test.no1 = no1
        test.no2_1 = no2_1
        test.no2_2 = no2_2
        test.no2_3 = no2_3
        test.no2_4 = no2_4
        test.no2_5 = no2_5
        test.no3 = no3
        test.no4 = no4
        test.no5 = no5
        test.no6 = no6
        test.no7 = no7
        test.no8 = no8
        test.no9 = no9
        test.no10 = no10
        test.Date_Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test.Status = '4'
        test.save()
        return redirect('Course_main',PK_Course_D)
    return render(request, 'ihub_test_alter.html',{'Profile':Profile, 'Answer_ihub': Answer_ihub, 'Course_item':Course_item ,'Sum_2':Sum_2})

def admin_list_report(request):
    Emp_id = request.session['Emp_id']
    Fullname = request.session['Fullname']
    Position = request.session['Position']
    LevelCode = request.session['LevelCode']
    Dept = request.session['Department']
    RegionCode = request.session['RegionCode']

    NameCourse_values = []
    Count_view_values = []
    Count_view_values1 = []
    Course_view_values_id = []
    Count_view = Staff_Vdolog.objects.values('Link_course__CourseName','Link_course__CourseStatus','Link_course__id','Link_course__Cover_img','Link_course__CourseBy','Link_course__Course_Pass_Score').exclude(Link_course__id = 11).annotate(Count('Link_course__id')).order_by('Link_course')
    for j in Count_view :
        #print(j['Link_course__CourseName'],j['Link_course__id__count'],j['Link_course__Course_Pass_Score'],j['Link_course__id'])
                # Count_view_label.append(j['Link_course__'])
                # Count_view_values.append(j['Link_course__Count'])
        # Staff_Score.objects.select_related('Staff').filter(Link_course_id=1).filter(Post_Score__gte=9).order_by('Staff__DeptCode')
        compare_total_test = Staff_Score.objects.filter(Link_course_id=j['Link_course__id']).filter(Post_Score__gte=j['Link_course__Course_Pass_Score']).values('Link_course__id','Link_course__Course_Pass_Score').annotate(Count('Link_course__id')).order_by('Link_course')
        for k in compare_total_test:
            #print(j['Link_course__id__count'],k['Link_course__id__count'])
            NameCourse_values.append(j['Link_course__CourseName'])
            Count_view_values.append(j['Link_course__id__count'])
            Count_view_values1.append(k['Link_course__id__count'])
            Course_view_values_id.append(j['Link_course__id'])
    Count_pass = list(zip_longest(NameCourse_values, Count_view_values,Count_view_values1,Course_view_values_id))

    Profile= {
        'Emp_id' : Emp_id,
        'Fullname' : Fullname,
        'Position' : Position,
        'LevelCode' : LevelCode,
        'Dept' : Dept,
        'RegionCode':RegionCode,
        }
    # พี่ส้มทำต่อ

    # for i in Count_pass :
    #     print(i['Link_course__CourseName'],i['Post_Score'])

    return render(request, 'admin_list_report.html', { 'Profile':Profile, 'Count_view': Count_view,'Count_pass': Count_pass})

def export_users_xls(request,input_course):
    # Course_id = Course.objects.get(id=input_course)
    pass_Score = Course.objects.get(id=input_course)
    #datetime--now
    
    #-----------------------
    #namecourse = Course.objects.get(id = CourseName)
    today = str(date.today())
    courseid = str(pass_Score.id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename="Export :"'+str(courseid)+ "[" +str(today) + "]"'".xls"'

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Course'+today)
    col_width = 256 * 20 # 20 characters wide

    try:
        for i in itertools.count():
            sheet.col(i).width = col_width
    except ValueError:
        pass

    default_book_style = book.default_style
    default_book_style.font.height = 20 * 36 # 36pt

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True    #  bold 
    font.name = 'TH Sarabun New'   #  select the font 
    font.height = 300   #  the font size 
    font.colour_index = 0  #  the font color 
    aligment = xlwt.Alignment()
    aligment.horz = aligment.HORZ_CENTER    #  horizontal alignment 
    aligment.vert = aligment.VERT_BOTTOM    #  perpendicular to its way 
    font_style.alignment = aligment
    font_style.font = font

    columns = ['รหัสพนักงาน', 'ชื่อ-นามสกุล', 'สังกัด', 'ตำแหน่ง','คะแนนสอบ','รหัสวิชา','ชื่อวิชา']

    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'TH Sarabun New'   #  select the font 
    font.height = 300   #  the font size 
    font.colour_index = 0  #  the font color 
    font_style.font = font      
                                                        # .filter(Link_course_id=input_course).filter(Post_Score__gte=pass_Score.Course_Pass_Score)
    query_re = Staff_Score.objects.select_related('Staff').filter(Q(Link_course_id=input_course) & Q(Post_Score__gte=pass_Score.Course_Pass_Score)).order_by('Staff__DeptCode')

    rows = query_re.values_list('Staff__StaffID', 
                                'Staff__StaffName', 
                                'Staff__StaffDepshort',
                                'Staff__StaffPosition',
                                'Post_Score',
                                'Link_course',
                                'Link_course__CourseName')
                                
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            sheet.write(row_num, col_num, row[col_num], font_style)

    book.save(response)
    return response 
 
def summary(request):
    # Profile ={
    #     'Emp_id' : request.session['Emp_id'],
    #     'Fullname' : request.session['Fullname'],
    #     'Position' : request.session['Position'],
    #     'LevelCode' : request.session['LevelCode'],
    #     'Dept' : request.session['Department'],
    #     'RegionCode' : request.session['RegionCode']
    # }
    total_record = Staff_Score.objects.select_related('Staff').values('Staff__StaffName', 'Staff__StaffPosition','Staff__StaffLevelcode','Staff__StaffDepshort').exclude(Link_course=11).annotate(Count('Staff_id')).order_by('Staff__DeptCode')
    print(total_record.query)

    return render(request, 'summary_admin.html',{ 'total_record':total_record })

def summary_healthy(request):
    # Profile ={
    #     'Emp_id' : request.session['Emp_id'],
    #     'Fullname' : request.session['Fullname'],
    #     'Position' : request.session['Position'],
    #     'LevelCode' : request.session['LevelCode'],
    #     'Dept' : request.session['Department'],
    #     'RegionCode' : request.session['RegionCode']
    # }
    total_record = Staff_Score.objects.select_related('Staff').values('Staff__StaffName', 'Staff__StaffPosition','Staff__StaffLevelcode','Staff__StaffDepshort').filter(Link_course=11).annotate(Count('Staff_id')).order_by('Staff__DeptCode')
    print(total_record.query)

    return render(request, 'summary_healthy.html',{ 'total_record':total_record })

def select(request):
    Profile ={
        'Emp_id' : request.session['Emp_id'],
        'Fullname' : request.session['Fullname'],
        'Position' : request.session['Position'],
        'LevelCode' : request.session['LevelCode'],
        'Dept' : request.session['Department'],
        'RegionCode' : request.session['RegionCode']
    }
    Course_all = Course.objects.filter(Course_Type = 2)

    return render(request, 'select.html',{ 'Profile':Profile ,'Course_all':Course_all })