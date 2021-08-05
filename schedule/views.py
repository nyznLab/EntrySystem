import time
from datetime import datetime

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render

from config.OptionsConfig import appointment_items_data
from config.PaginatorConfig import page_size, page_start
from patients.models import DPatientDetail
from schedule.impl.ScheduleServiceImpl import ScheduleServiceImpl
from schedule.models import TSchedule
from utils.AttrUtil import AttrUtil
from utils.JsonUtil import JsonUtil

# Create your views here.


# 待办列表视图
def index_schedule(request):
    # 载入视图
    return render(request, 'schedule/index.html', {

    })


# 预约列表数据
def list_schedule(request):
    # 载入service层
    service = ScheduleServiceImpl
    # 接收参数
    schedule_date = request.GET.get('date')
    status = request.GET.get('status')
    keywords = request.GET.get('keywords')
    is_urgent = request.GET.get('is_urgent')
    # 分页参数
    limit = request.GET.get('limit')
    page = request.GET.get('page')

    # 分页参数
    if not limit:
        limit = page_size
    if not page or page == '':
        page = page_start

    # 构造查询参数集合
    args = dict()
    # 日期
    if schedule_date:
        args['schedule_date'] = schedule_date
    # 状态
    if status:
        args['status'] = status
    # 关键词
    if keywords:
        args['keywords'] = keywords
    # 是否紧急
    if is_urgent:
        args['is_urgent'] = is_urgent

    # 获取列表
    schedule_data = service.list_schedule(args)
    schedule_list = []
    for i in schedule_data:
        schedule_list.append(i)
    print('----------------------------------------------------------------')
    # print(schedule_list)
    # 开启分页
    paginator = Paginator(schedule_list, limit)
    # 当前页的数据对象
    data = paginator.page(page)
    # 遍历数据对象，构造返回数据
    result = service.list_schedule_result(data)
    # print(list.count())
    print('----------------------------------------------------------------')
    print(result)
    return JsonUtil.success(result, schedule_data.count())


# 完成待办
@transaction.atomic
def done_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 数据
    schedule = service.get_schedule(schedule_id)
    if schedule is not None:
        if schedule.status == 1:
            # 已经完成，不能重复完成
            return JsonUtil.error({}, 0, '该待办已完成，操作失败')
        elif schedule.status == 2:
            # 已经取消，不能完成
            return JsonUtil.error({}, 0, '该待办已取消，操作失败')
        else:
            schedule.status = 1
            schedule.save()
            return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 取消预约
@transaction.atomic
def cancel_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 删除数据
    schedule = service.get_schedule(schedule_id)
    if schedule is not None:
        if schedule.status == 1:
            # 已经完成，不能取消
            return JsonUtil.error({}, 0, '该待办已完成，不能取消')
        elif schedule.status == 2:
            # 已经取消，不能重复取消
            return JsonUtil.error({}, 0, '该待办已取消，操作失败')
        else:
            schedule.status = 2
            schedule.save()
            return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 删除
@transaction.atomic
def delete_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 删除数据
    service.delete_schedule(schedule_id)
    return JsonUtil.success()


# 批量删除
@transaction.atomic
def delete_batch_schedule(request):
    # 载入service层
    service = ScheduleServiceImpl
    # 接收参数
    ids = request.POST.get('ids')
    if ids:
        if ids[-1] == ',':
            ids = ids[0:-1]
        ids_data = ids.split(',')
        # 删除
        service.delete_batch_schedule(ids_data)
    return JsonUtil.success()


# 检查是否存在预约
def check_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 删除数据
    schedule = service.get_schedule(schedule_id)
    if schedule is not None:
        return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 更新“字段”状态
def toggle_schedule(request):
    # 载入service层
    service = ScheduleServiceImpl
    # 接收参数
    schedule_id = request.GET.get('id')
    key = request.GET.get('key')
    value = request.GET.get('value')
    # 获取模型数据
    schedule = service.get_schedule(schedule_id)
    if schedule is None:
        return JsonUtil.error({}, 0, '未找到数据')
    if key == 'is_urgent':
        schedule.is_urgent = value
    # 保存数据
    schedule.save()
    return JsonUtil.success()


# 查询扫描列表
def list_patient_detail(request):
    # 载入service层
    service = ScheduleServiceImpl
    # 接收参数
    patient_id = request.POST.get('patient_id')
    # 患者信息
    patient = service.get_patient(patient_id)
    if patient is None:
        return JsonUtil.error({}, 0, '未找到数据')
    # 查询列表
    patient_detail_all = DPatientDetail.objects.all().select_related().filter(patient_id=patient_id).values('id',
                                                                                            'patient_id',
                                                                                            'session_id',
                                                                                            'standard_id',
                                                                                            'age',
                                                                                            'phone',
                                                                                            'scan_date').order_by('-id')
    patient_detail_list = []
    if patient_detail_all:
        for item in patient_detail_all:
            # 特殊字段处理
            item['scan_date'] = str(item['scan_date'])
            patient_detail_data = item
            patient_detail_list.append(patient_detail_data)
    return JsonUtil.success({'patient_name': patient.name,
                             'patient_code': patient.id,
                             'patient_detail_list': patient_detail_list})


# 编辑预约
def edit_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 预约
    schedule = service.get_schedule(schedule_id)
    print('--------------------------')
    print('~!~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(schedule)
    if request.method == 'GET':
        # 处理特殊数据
        schedule.start_date = str(schedule.start_date)
        schedule.end_date = str(schedule.end_date)
        # 载入视图
        return render(request, 'schedule/form.html', {
            'is_edit': 1,
            'schedule': schedule,
            'appointment_items_data': appointment_items_data,
        })
    else:
        # 更新
        schedule = AttrUtil.set_attr(request, schedule)
        service.update_schedule(schedule)
        return JsonUtil.success()


# 创建预约
def create_schedule(request):
    print("create_schedule")
    # 载入service层
    service = ScheduleServiceImpl
    if request.method == 'GET':
        date = request.GET.get('date')
        if date is None:
            date = ''
        # 载入视图
        return render(request, 'schedule/form.html', {
            'is_edit': 0,
            'schedule': {
                'schedule_id': 0,
            },
            'date': date,
            'appointment_items_data': appointment_items_data,
        })
    else:
        # 新增
        schedule = AttrUtil.set_attr(request, TSchedule())
        '''
        其他参数处理
        '''
        # 医生id：当前登录用户
        schedule.doctor_id = request.session.get('doctor_id')
        # 默认状态：未处理
        schedule.status = 0
        # 创建时间：当前时间戳
        schedule.create_time = int(time.time())
        # 更新时间：当前时间date数据
        schedule.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        service.create_schedule(schedule)
        return JsonUtil.success()


# 恢复
@transaction.atomic
def init_schedule(request, schedule_id):
    # 载入service层
    service = ScheduleServiceImpl
    # 删除数据
    schedule = service.get_schedule(schedule_id)
    if schedule is not None:
        if schedule.status == 1:
            # 已经完成，不能恢复
            return JsonUtil.error({}, 0, '该待办已完成，不能恢复')
        else:
            schedule.status = 0
            schedule.save()
            return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 待办页面（日历）
def calendar_schedule(request):
    # 当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    # 载入视图
    return render(request, 'schedule/calendar.html', {
        'today': today,
    })


# 待办列表（日历）：指定月份的
def calendar_list_schedule(request):
    # 载入service层
    service = ScheduleServiceImpl
    # 接收参数
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    # 构造查询参数集合
    args = dict()
    # 日期
    if start_date:
        args['start_date'] = start_date
    if end_date:
        args['end_date'] = end_date

    # 获取列表
    schedule_data = service.list_schedule(args)

    schedule_list = []
    for i in schedule_data:
        schedule_list.append(i)
    print('----------------------------------------------------------------')
    result = service.list_schedule_result(schedule_list)
    # print(list.count())
    print('----------------------------------------------------------------')
    print(result)
    return JsonUtil.success(result, schedule_data.count())
