import time
from datetime import datetime

from django.core.paginator import Paginator
from django.db import transaction, DatabaseError, connection
from django.shortcuts import render

from appointment.models import TAppointment
from config.OptionsConfig import appointment_time_data, appointment_items_data
from config.PaginatorConfig import page_size, page_start
from appointment.impl.AppointmentServiceImpl import AppointmentServiceImpl
from schedule.models import TSchedule
from utils.AttrUtil import AttrUtil
from utils.JsonUtil import JsonUtil
import patients.models as patients_models
import tools.idAssignments as tools_idAssignments
import tools.Utils as tools_utils


# Create your views here.


# 预约列表视图
def index_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
    # 医生列表
    doctor_list = service.list_doctor()
    # 载入视图
    return render(request, 'appointment/index.html', {
        'doctor_list': doctor_list,
        'appointment_time_data': appointment_time_data
    })


# 预约列表数据
def list_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
    # 接收参数
    doctor_id = request.GET.get('doctor_id')
    appointment_date = request.GET.get('date')
    appointment_time = request.GET.get('time')
    status = request.GET.get('status')
    keywords = request.GET.get('keywords')
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
    # 医生id
    if doctor_id:
        args['doctor_id'] = doctor_id
    # 预约日期
    if appointment_date:
        args['appointment_date'] = appointment_date
    # 预约时间
    if appointment_time:
        args['appointment_time'] = appointment_time
    # 状态
    if status:
        args['status'] = status
    # 关键词
    if keywords:
        args['keywords'] = keywords

    # 获取列表
    appointment_data = service.list_appointment(args)
    appointment_list = []
    for i in appointment_data:
        appointment_list.append(i)
    print('----------------------------------------------------------------')
    # print(appointment_list)
    # 开启分页
    paginator = Paginator(appointment_list, limit)
    # 当前页的数据对象
    data = paginator.page(page)
    # 遍历数据对象，构造返回数据
    result = service.list_appointment_result(data)
    # print(list.count())
    print('----------------------------------------------------------------')
    print(result)
    return JsonUtil.success(result, appointment_data.count())


# 删除
@transaction.atomic
def delete_appointment(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 删除数据
    service.delete_appointment(appointment_id)
    return JsonUtil.success()


# 批量删除
@transaction.atomic
def delete_batch_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
    # 接收参数
    ids = request.POST.get('ids')
    if ids:
        if ids[-1] == ',':
            ids = ids[0:-1]
        ids_data = ids.split(',')
        # 删除
        service.delete_batch_appointment(ids_data)
    return JsonUtil.success()


# 取消预约
@transaction.atomic
def cancel_appointment(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 删除数据
    appointment = service.get_appointment(appointment_id)
    if appointment is not None:
        if appointment.status == 1:
            # 已经报到，不能取消
            return JsonUtil.error({}, 0, '该预约已报到，不能取消')
        elif appointment.status == 2:
            # 已经取消，不能重复取消
            return JsonUtil.error({}, 0, '该预约已取消，操作失败')
        else:
            appointment.status = 2
            appointment.save()
            return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 检查是否是已存在患者
def check_patient(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 删除数据
    appointment = service.get_appointment(appointment_id)
    if appointment is not None:
        if appointment.status == 1 or appointment.status == 2:
            # 已经报到，不能取消
            return JsonUtil.error({}, 0, '该预约不能执行【报到】操作')
        else:
            patient_id = 0
            # 查询是新患者还是老患者
            cursor = connection.cursor()
            sql = "SELECT `pb`.`id`, `pb`.`name` AS `patient_id` " \
                  "FROM `b_patient_base_info` AS `pb` " \
                  "LEFT JOIN `d_patient_detail` AS `pd` " \
                  "ON pb.`id` = pd.`patient_id` " \
                  "WHERE `pb`.`name` = %s AND `pd`.`phone` = %s" \
                  " ORDER BY `pb`.`id` DESC LIMIT 1"
            cursor.execute(sql, [appointment.name, appointment.phone])
            patient_info = cursor.fetchone()
            print('患者信息----------------------------------------------------')
            print(patient_info)
            print('患者信息----------------------------------------------------')
            if patient_info is not None:
                # 老患者，传递参数操作业务逻辑
                patient_id = patient_info[0]
            return JsonUtil.success({'patient_id': patient_id})
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 预约报到
# @transaction.atomic
def check_in_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
    appointment_id = int(request.POST.get('appointment_id'))
    patient_id = int(request.POST.get('patient_id'))
    is_new = int(request.POST.get('is_new'))
    # 删除数据
    appointment = service.get_appointment(appointment_id)
    if appointment is not None:
        if appointment.status == 1 or appointment.status == 2:
            # 已经报到，不能取消
            return JsonUtil.error({}, 0, '该预约不能执行【报到】操作')
        else:
            '''
            报到逻辑：
            1.更新预约的状态为“已报到”
            2.查询是新患者还是老患者
            3.新患者需要创建患者基本信息
            4.创建初扫/复扫记录
            5.根据患者ID和初扫/复扫ID等参数，创建待办
            '''
            try:
                with transaction.atomic():
                    # 当前时间
                    now_date = datetime.now().strftime("%Y-%m-%d")
                    # 1.更新预约的状态为“已报到”
                    appointment.status = 1
                    appointment.save()
                    # 2.查询是新患者还是老患者
                    # 3.新患者需要创建患者基本信息
                    if not patient_id <= 0:
                        # 新患者
                        if is_new == 1:
                            # 1.创建基本信息表
                            patient_base_info = patients_models.BPatientBaseInfo(id=patient_id,
                                                                                 name=appointment.name,
                                                                                 sex=appointment.sex,
                                                                                 birth_date=appointment.birth_date,
                                                                                 nation="",
                                                                                 doctor_id=appointment.doctor_id)
                            patient_base_info.save()
                        # 2.创建患者详情表 = 4.创建初扫/复扫记录
                        [patient_id, session_id,
                         standard_id] = tools_idAssignments.patient_session_id_assignment(patient_id)
                        # 计算年龄
                        age = tools_utils.calculate_age_by_scandate(str(appointment.birth_date), str(now_date))
                        # 创建详情表
                        patient_detail = patients_models.DPatientDetail(patient_id=patient_id,
                                                                        session_id=session_id,
                                                                        standard_id=standard_id,
                                                                        phone=appointment.phone,
                                                                        age=age,
                                                                        doctor_id=appointment.doctor_id,
                                                                        scan_date=now_date,
                                                                        tms=None)
                        patient_detail.save()
                    # 4.创建初扫/复扫记录
                    # 5.根据患者ID和初扫/复扫ID等参数，创建待办
                    if appointment.items != '':
                        items_data = appointment.items.split(',')
                        create_schedule_list = []
                        for item_type in items_data:
                            # 转为整型
                            item_type = int(item_type)
                            # 批量添加待办事项记录
                            create_schedule_list.append(TSchedule(patient_id=patient_id,
                                                                  patient_session_id=patient_detail.id,
                                                                  item_type=item_type,
                                                                  name=appointment.name,
                                                                  phone=appointment.phone,
                                                                  standard_id=standard_id,
                                                                  title=appointment_items_data[item_type]['title'],
                                                                  content=appointment_items_data[item_type]['title'],
                                                                  is_urgent=0,
                                                                  start_date=now_date, # appointment.appointment_date,
                                                                  end_date=now_date, # appointment.appointment_date,
                                                                  status=0,
                                                                  doctor_id=appointment.doctor_id,
                                                                  remark="",
                                                                  create_time=int(time.time()),
                                                                  update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        # 批量写入数据
                        TSchedule.objects.bulk_create(create_schedule_list)
                    done = True
            except DatabaseError:
                done = False
            # 是否完成操作
            if done is True:
                return JsonUtil.success()
            else:
                return JsonUtil.error()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 检查是否存在预约
def check_appointment(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 删除数据
    appointment = service.get_appointment(appointment_id)
    if appointment is not None:
        return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 编辑预约
def edit_appointment(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 预约
    appointment = service.get_appointment(appointment_id)
    print('--------------------------')
    if request.method == 'GET':
        # 处理特殊数据
        appointment.birth_date = str(appointment.birth_date)
        appointment.appointment_date = str(appointment.appointment_date)
        # 已存在的预约项目
        had_items_data = []
        if appointment.items is not None:
            had_items_data = appointment.items.split(',')
        print(had_items_data)
        # 医生列表
        doctor_list = service.list_doctor()
        # 载入视图
        return render(request, 'appointment/form.html', {
            'is_edit': 1,
            'appointment': appointment,
            'doctor_list': doctor_list,
            'appointment_time_data': appointment_time_data,
            'appointment_items_data': appointment_items_data,
            'had_items_data': had_items_data,
        })
    else:
        # 更新
        appointment = AttrUtil.set_attr(request, appointment)
        service.update_appointment(appointment)
        return JsonUtil.success()


# 恢复
@transaction.atomic
def init_appointment(request, appointment_id):
    # 载入service层
    service = AppointmentServiceImpl
    # 删除数据
    appointment = service.get_appointment(appointment_id)
    if appointment is not None:
        if appointment.status == 1:
            # 已经完成，不能恢复
            return JsonUtil.error({}, 0, '该预约已报到，操作失败')
        else:
            appointment.status = 0
            appointment.save()
            return JsonUtil.success()
    else:
        return JsonUtil.error({}, 0, '未找到数据')


# 创建预约
def create_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
    if request.method == 'GET':
        # 医生列表
        doctor_list = service.list_doctor()
        # 载入视图
        return render(request, 'appointment/form.html', {
            'is_edit': 0,
            'appointment': {
                'appointment_id': 0,
            },
            'doctor_list': doctor_list,
            'appointment_time_data': appointment_time_data,
            'appointment_items_data': appointment_items_data,
            'had_items_data': [],
        })
    else:
        # 新增
        appointment = AttrUtil.set_attr(request, TAppointment())
        '''
        其他参数处理
        '''
        # 医生id：当前登录用户
        appointment.doctor_id = request.session.get('doctor_id')
        # 默认状态：未报到
        appointment.status = 0
        # 创建时间：当前时间戳
        appointment.create_time = int(time.time())
        # 更新时间：当前时间date数据
        appointment.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        service.create_appointment(appointment)
        return JsonUtil.success()


# 待办页面（日历）
def calendar_appointment(request):
    # 当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    # 载入视图
    return render(request, 'appointment/calendar.html', {
        'today': today,
    })


# 待办列表（日历）：指定月份的
def calendar_list_appointment(request):
    # 载入service层
    service = AppointmentServiceImpl
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
    appointment_data = service.list_appointment(args)

    appointment_list = []
    for i in appointment_data:
        appointment_list.append(i)
    print('----------------------------------------------------------------')
    result = service.list_appointment_result(appointment_list)
    # print(list.count())
    print('----------------------------------------------------------------')
    print(result)
    return JsonUtil.success(result, appointment_data.count())
