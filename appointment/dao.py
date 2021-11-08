#!/usr/bin/env python
# *_*coding:utf-8 *_*
# 预约dao层
from django.db.models import Q

import appointment.models as appointment_model

'''
预约模块dao层
'''


class AppointmentDao:

    # 保存
    @staticmethod
    def save_appointment(appointment):
        appointment.save()
        return True

    # 根据主键获取预约记录
    @staticmethod
    def get_appointment(appointment_id):
        appointment = appointment_model.TAppointment.objects.filter(appointment_id=appointment_id)
        if appointment.count() == 0:
            return None
        else:
            return appointment[0]

    @staticmethod
    def delete_appointment(appointment_id):
        appointment = AppointmentDao.get_appointment(appointment_id)
        if appointment is not None:
            appointment.delete()
        return True

    @staticmethod
    def delete_batch_appointment(appointment_id_data):
        if appointment_id_data is not None:
            appointment_model.TAppointment.objects.filter(appointment_id__in=appointment_id_data).delete()
        return True

    # 获取预约记录列表
    @staticmethod
    def list_appointment(args):
        # print('医生的id======================')
        # print(args.get('doctor_id', 0))
        # print(args.get('date', ''))
        # print(args.get('status', 0))
        # print('医生的id======================' . str(args.get('doctor_id', 0)))
        filter_args = AppointmentDao.args_handler(args)
        print('查询参数filter_args111111111======================')
        print(filter_args)
        keywords = ''
        if 'keywords' in filter_args:
            keywords = filter_args['keywords']
            del filter_args['keywords']
        start_date = ''
        if 'start_date' in filter_args:
            start_date = filter_args['start_date']
            del filter_args['start_date']
        end_date = ''
        if 'end_date' in filter_args:
            end_date = filter_args['end_date']
            del filter_args['end_date']

        is_appointment_date = ''
        if 'is_appointment_date' in filter_args:
            is_appointment_date = filter_args['is_appointment_date']
            del filter_args['is_appointment_date']

        print('查询参数filter_args222222222======================')
        print(filter_args)
        print('查询参数filter_args33333333======================')
        list_appointment = appointment_model.TAppointment.objects.filter(**filter_args).order_by("-appointment_id")
        # 关键词查询
        if keywords != '':
            list_appointment = list_appointment.filter(Q(name__contains=keywords) | Q(phone__contains=keywords))
        # 日期范围查询
        if start_date != '' and end_date != '':
            list_appointment = list_appointment.filter(Q(appointment_date__gte=start_date) & Q(appointment_date__lte=end_date))
        # 待定
        if is_appointment_date != '':
            if is_appointment_date == 0:
                list_appointment = list_appointment.filter(Q(appointment_date=None))
            elif is_appointment_date == 1:
                list_appointment = list_appointment.filter(~Q(appointment_date=None))
        # 排序
        list_appointment = list_appointment.order_by("-appointment_id")
        return list_appointment

    # 处理请求参数
    @staticmethod
    def args_handler(args):
        filter_args = {}
        if args:
            # 医生id
            doctor_id = int(args.get('doctor_id', 0))
            # print(doctor_id)
            if doctor_id > 0:
                filter_args['doctor_id'] = doctor_id
            # 预约日期
            appointment_date = args.get('appointment_date', '')
            # print(date)
            if appointment_date != '':
                filter_args['appointment_date'] = appointment_date
            # 预约时间
            appointment_time = int(args.get('appointment_time', 0))
            # print(time)
            if appointment_time > 0:
                filter_args['appointment_time'] = appointment_time
            # 状态
            status = int(args.get('status', 0))
            # print(status)
            if status == 0:
                pass
            elif status == 1:
                filter_args['status'] = 1  # 已报到
            elif status == 2:
                filter_args['status'] = 2  # 取消
            elif status == 10:
                filter_args['status'] = 0  # 未报到

            is_appointment_date = int(args.get('is_appointment_date', 0))
            if is_appointment_date == 0:
                pass
            elif is_appointment_date == 1:
                filter_args['is_appointment_date'] = 1
            elif is_appointment_date == 10:
                filter_args['is_appointment_date'] = 0

            # 关键词
            keywords = args.get('keywords', '')
            # print(keywords)
            if keywords != '':
                filter_args['keywords'] = keywords
            # 起始日期
            start_date = args.get('start_date', '')
            if start_date != '':
                filter_args['start_date'] = start_date
            # 截止日期
            end_date = args.get('end_date', '')
            if end_date != '':
                filter_args['end_date'] = end_date
        return filter_args
