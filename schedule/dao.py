#!/usr/bin/env python
# *_*coding:utf-8 *_*
# 待办dao层
from django.db.models import Q

import schedule.models as schedule_model

'''
待办模块dao层
'''


class ScheduleDao:

    # 保存
    @staticmethod
    def save_schedule(schedule):
        schedule.save()
        return True

    # 根据主键获取预约记录
    @staticmethod
    def get_schedule(schedule_id):
        schedule = schedule_model.TSchedule.objects.filter(schedule_id=schedule_id)
        if schedule.count() == 0:
            return None
        else:
            return schedule[0]

    @staticmethod
    def delete_schedule(schedule_id):
        schedule = ScheduleDao.get_schedule(schedule_id)
        if schedule is not None:
            schedule.delete()
        return True

    @staticmethod
    def delete_batch_schedule(schedule_id_data):
        if schedule_id_data is not None:
            schedule_model.TSchedule.objects.filter(schedule_id__in=schedule_id_data).delete()
        return True

    # 获取预约记录列表
    @staticmethod
    def list_schedule(args):
        # print('医生的id======================')
        # print(args.get('doctor_id', 0))
        # print(args.get('date', ''))
        # print(args.get('status', 0))
        # print('医生的id======================' . str(args.get('doctor_id', 0)))
        filter_args = ScheduleDao.args_handler(args)
        print('查询参数filter_args111111111======================')
        print(filter_args)
        keywords = ''
        if 'keywords' in filter_args:
            keywords = filter_args['keywords']
            del filter_args['keywords']
        schedule_date = ''
        if 'schedule_date' in filter_args:
            schedule_date = filter_args['schedule_date']
            del filter_args['schedule_date']
        start_date = ''
        if 'start_date' in filter_args:
            start_date = filter_args['start_date']
            del filter_args['start_date']
        end_date = ''
        if 'end_date' in filter_args:
            end_date = filter_args['end_date']
            del filter_args['end_date']
        print('查询参数filter_args222222222======================')
        print(filter_args)
        print('查询参数filter_args33333333======================')
        # 关联查询
        list_schedule = schedule_model.TSchedule.objects.filter(**filter_args)  # .select_related('patient')
        # 关键词查询：包含标题、内容、病人姓名、电话、扫描ID匹配查询
        if keywords != '':
            list_schedule = list_schedule.filter(Q(title__contains=keywords) | Q(content__contains=keywords) | Q(name__contains=keywords) | Q(phone__contains=keywords) | Q(standard_id__contains=keywords))
        # 时间
        if schedule_date != '':
            list_schedule = list_schedule.filter(Q(start_date__lte=schedule_date) & Q(end_date__gte=schedule_date))
        if start_date != '' and end_date != '':
            list_schedule = list_schedule.filter(((Q(start_date__gte=start_date) & Q(start_date__lte=end_date)) | Q(end_date__gte=start_date) & Q(end_date__lte=end_date)))
        # 排序
        list_schedule = list_schedule.order_by("-schedule_id")
        return list_schedule

    # 处理请求参数
    @staticmethod
    def args_handler(args):
        filter_args = {}
        if args:
            # 患者id
            patient_id = int(args.get('patient_id', 0))
            # print(patient_id)
            if patient_id > 0:
                filter_args['patient_id'] = patient_id
            # 预约日期
            schedule_date = args.get('schedule_date', '')
            # print(date)
            if schedule_date != '':
                filter_args['schedule_date'] = schedule_date
            # 起始日期
            start_date = args.get('start_date', '')
            if start_date != '':
                filter_args['start_date'] = start_date
            # 截止日期
            end_date = args.get('end_date', '')
            if end_date != '':
                filter_args['end_date'] = end_date
            # 状态
            status = int(args.get('status', 0))
            if status == 0:
                pass
            elif status == 1:
                filter_args['status'] = 1  # 已处理
            elif status == 2:
                filter_args['status'] = 2  # 取消
            elif status == 10:
                filter_args['status'] = 0  # 未处理
            # 是否紧急
            is_urgent = int(args.get('is_urgent', 0))
            if is_urgent == 0:
                pass
            elif is_urgent == 1:
                filter_args['is_urgent'] = 1  # 紧急
            elif is_urgent == 10:
                filter_args['is_urgent'] = 0  # 默认

            # 关键词
            keywords = args.get('keywords', '')
            # print(keywords)
            if keywords != '':
                filter_args['keywords'] = keywords
        return filter_args
