from entity import organizations as o
from util import public_tools as tool
from util import io_tools as io
import datetime
import calendar

#加载数据
def load_emp_data():
    io.checking_data_files()#文件自检
    io.load_users()#载入管理员账号
    io.load_lock_record()#载入打卡记录
    io.load_employee_info()#载入员工信息
    io.load_employee_pic()#载入员工照片

#添加新员工
def add_new_employee(name):
    code=tool.randomCode()#生成随机特征码
    newEmp=o.Employee(o.get_new_id(),name,code)#创建员工对象
    o.add(newEmp)#在组织结构中添加新员工
    io.save_employee_all()#保存最新的员工信息
    return code

#删除某个员工
def remove_employee(id):
    io.remove_pics(id)#删除员工的所有图片
    o.remove(id)#从组织结构中删除员工
    io.save_employee_all()#保存最新的员工信息
    io.save_lock_record()#保存最新的打卡记录

#未指定员工添加打卡记录
def add_lock_record(name):
    record=o.LOCK_RECORD#所有打卡记录
    now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#当前时间
    if name in record.keys():#如果该员工有打卡记录
        r_list=record[name]#获取打卡时间
        if len(r_list)==0:#如果记录为空
            r_list=list()#创建新列表
        r_list.append(now_time)#记录当前时间
    else:#如果该员工没有打卡记录
        r_list=list()#创建新列表
        r_list.append(now_time)#记录当前时间
        record[name]=r_list#将记录保存在字典中
    io.save_lock_record()#保存所有的打卡记录

#所有员工信息报表
def get_employee_report():
    #report=list()#员工信息列表
    report='####################################\n'
    report+='员工姓名如下：\n'
    i=0#换行计数器
    for emp in o.EMPLOYEES:#历遍所有员工
        report+='('+str(emp.id)+')'+emp.name+'\t'
        i+=1#计数器自增
        if i==4:#每四个员工换一行
            report+='\n'
            i=0#计数器归零
    report=report.strip()#清楚报表末尾可能出现的换行符
    report+='\n#####################################'
    return report

#检查id是否存在
def check_id(id):
    for emp in o.EMPLOYEES:
        if str(id)==str(emp.id):
            return True
    return False

#通过特征码获取员工姓名
def get_name_with_code(code):
    for emp in o.EMPLOYEES:
        if str(code)==str(emp.code):
            return emp.name

#通过id获取员工特征码
def get_code_with_id(id):
    for emp in o.EMPLOYEES:
        if str(id)==str(emp.id):
            return emp.code

#验证管理员账号和密码
def vaild_user(user_name,password):
    if user_name in o.USERS.keys():#如果有这个账号
        if o.USERS.get(user_name)==password:#如果账号和密码匹配
            return True#验证成功
    return False#验证失败

#保存上下班时间
def save_work_time(work_time,close_time):
    o.WORK_TIME=work_time
    o.CLOSING_TIME=close_time
    io.save_work_time_config()#上下班时间保存到文件中

#打印指定日期的打卡日报
def get_day_report(date):
    io.load_work_time_config()#读取上下班时间
    #当天0点
    earliest_time=datetime.datetime.strptime(date+" 00:00:00",'%Y-%m-%d %H:%M:%S')
    #当天中午12点
    noon_time=datetime.datetime.strptime(date+" 12:00:00",'%Y-%m-%d %H:%M:%S')
    #今晚0点
    latest_time=datetime.datetime.strptime(date+" 23:59:59",'%Y-%m-%d %H:%M:%S')
    #上班时间
    work_time=datetime.datetime.strptime(date+''+o.WORK_TIME,'%Y-%m-%d %H:%M:%S')
    #下班时间
    closing_time=datetime.datetime.strptime(date+''+o.CLOSING_TIME,'%Y-%m-%d %H:%M:%S')

    late_list=[]#迟到名单
    left_early=[]#早退名单
    absent_list=[]#缺席名单

    for emp in o.EMPLOYEES:
        if emp.name in o.LOCK_RECORD.keys():
            emp_lock_list=o.LOCK_RECORD.get(emp.name)
            is_absent=True
            for lock_time_str in emp_lock_list:
                lock_time=datetime.datetime.strptime(lock_time_str,'%Y-%m-%d %H:%M:%S')
                if earliest_time<lock_time<latest_time:
                    is_absent=False
                    if work_time<lock_time<noon_time:
                        late_list.append(emp.name)
                    if noon_time<lock_time<closing_time:
                        left_early.append(emp.name)
            if is_absent:
                absent_list.append(emp.name)
        else:
            absent_list.append(emp.name)

    emp_count=len(o.EMPLOYEES)
    print('--------'+date+'----------')
    print('应到人数：'+str(emp_count))
    print('缺席人数：'+str(len(absent_list)))
    absent_name=''
    if len(absent_list)==0:
        absent_name='(空)'
    else:
        for name in absent_list:
            absent_name+=name+''
    print('缺席名单：'+absent_name)
    print('迟到人数：'+str(len(late_list)))
    late_name=''
    if len(late_list)==0:
        late_name='(空)'
    else:
        for name in late_list:
            late_name+=name+''
    print('迟到名单：'+str(late_name))
    print('早退人数：'+str(len(left_early)))
    early_name=''
    if len(left_early)==0:
        early_name='(空)'
    else:
        for name in left_early:
            early_name+=name+''
    print('早退名单：'+early_name)

#打印当天打卡日报
def get_today_report():
    date=datetime.datetime.now().strftime('%Y-%m-%d')#当天日期
    get_day_report(str(date))#打印当天日报

#创建指定月份的打卡记录月报
def get_month_report(month):
    io.load_work_time_config()#读取上下班时间
    date=datetime.datetime.strptime(month,'%Y-%m')
    monthRange=calendar.monthrange(date.year,date.month)[1]#该月最后一天的天数
    month_first_day=datetime.date(date.year,date.month,1)
    month_last_day=datetime.date(date.year,date.month,monthRange)

    clock_in='I'
    clock_out='O'
    late='L'
    left_early='E'
    absent='A'

    lock_report=dict()#键为员工名，值为员工打卡情况的字典

    for emp in o.EMPLOYEES:
        emp_lock_date=[]
        if emp.name in o.LOCK_RECORD.get(emp.name):
            emp_lock_list=o.LOCK_RECORD.get(emp.name)
            index_day=month_first_day
            while index_day<=month_last_day:
                is_absent=True
                #当天零点
                earliest_time=datetime.datetime.strptime(str(index_day)+' 00:00:00','%Y-%m-%d %H:%M:%S')
                # 当天中午12点
                noon_time = datetime.datetime.strptime(str(index_day) + ' 12:00:00', '%Y-%m-%d %H:%M:%S')
                # 今晚0点
                latest_time = datetime.datetime.strptime(str(index_day) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
                # 上班时间
                work_time = datetime.datetime.strptime(str(index_day) + '' + o.WORK_TIME, '%Y-%m-%d %H:%M:%S')
                # 下班时间
                closing_time = datetime.datetime.strptime(str(index_day) + '' + o.CLOSING_TIME, '%Y-%m-%d %H:%M:%S')

                emp_today_data=''

                for lock_time_str in emp_lock_list:
                    lock_time=datetime.datetime.strptime(lock_time_str,'%Y-%m-%d %H:%M:%S')#打卡记录转为日期格式

                    #如果当前日期有打卡记录
                    if earliest_time<lock_time<latest_time:
                        is_absent=False
                        if lock_time<work_time:
                            emp_today_data+=clock_in
                        elif lock_time>=closing_time:
                            emp_today_data += clock_out
                        #上班时间后中午时间前打卡
                        elif work_time<lock_time<=noon_time:
                            emp_today_data+=late
                        elif noon_time<lock_time<closing_time:
                            emp_today_data+=left_early
                if is_absent:
                    emp_today_data=absent
                emp_lock_date.append(emp_today_data)
                index_day=index_day+datetime.timedelta(days=1)
        else:
            index_day=month_first_day
            while index_day<=month_last_day:
                emp_lock_date.append(absent)
                index_day=index_day+datetime.timedelta(days=1)
        lock_report[emp.name]=emp_lock_date

    report="\"姓名/日期\""
    index_day=month_first_day
    while index_day<=month_last_day:
        report+=",\""+str(index_day)+"\""
        index_day=index_day+datetime.timedelta(days=1)
    report+="\n"

    for emp in lock_report.keys():
        report+="\""+emp+"\""
        date_list=lock_report.get(emp)
        for data in date_list:
            text=""
            if absent==data:
                text="【缺席】"
            elif clock_in in data and clock_out in data:
                text=""
            else:
                if late in data and clock_in not in data:
                    text+="【迟到】"
                if left_early in data and clock_out not in data:
                    text+="【早退】"
                if clock_out not in data and left_early not in data:
                    text+="【下班未打卡】"
                if clock_in not in data and late not in data:
                    text+="【上班未打卡】"
            report+=",\""+text+"\""
        report+="\n"

    #cvs文件标题日期
    title_date=month_first_day.strftime('%Y{y}%m{m}').format(y='年',m='月')
    file_name=title_date+'考勤月报'
    io.create_CSV(file_name,report)

#创建上一个月打卡记录月报
def get_pre_month_report():
    today=datetime.date.today()
    #获取上一个月的第一天的日期
    pre_month_first_day=datetime.date(today.year,today.month-1,1)
    pre_month=pre_month_first_day.strftime('%Y-%m')
    get_month_report(pre_month)
