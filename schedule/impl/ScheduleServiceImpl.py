#!/usr/bin/env python
# *_*coding:utf-8 *_*
from datetime import datetime

from config.OptionsConfig import schedule_status_data
from patients.models import BPatientBaseInfo, DPatientDetail
from schedule.dao import ScheduleDao
from schedule.service import ScheduleService

'''
待办模块服务层实现类
'''


class ScheduleServiceImpl(ScheduleService):

    # 创建
    @classmethod
    def create_schedule(self, schedule):
        dao = ScheduleDao()
        return dao.save_schedule(schedule)

    # 更新
    @classmethod
    def update_schedule(self, schedule):
        dao = ScheduleDao()
        # 更新时间：当前时间date数据
        schedule.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dao.save_schedule(schedule)

    # 删除
    @classmethod
    def delete_schedule(self, schedule_id):
        dao = ScheduleDao()
        return dao.delete_schedule(schedule_id)

    # 批量删除
    @classmethod
    def delete_batch_schedule(self, schedule_id_data):
        dao = ScheduleDao()
        return dao.delete_batch_schedule(schedule_id_data)

    # 获取患者
    @classmethod
    def get_patient(self, patient_id):
        return BPatientBaseInfo.objects.filter(id=patient_id).first()

    # 获取扫描记录
    @classmethod
    def get_patient_detail(self, patient_session_id):
        return DPatientDetail.objects.filter(id=patient_session_id).first()

    # 根据主键获取预约记录
    @classmethod
    def get_schedule(self, schedule_id):
        dao = ScheduleDao()
        schedule = dao.get_schedule(schedule_id)
        return schedule

    # 获取预约记录列表
    @classmethod
    def list_schedule(self, args):
        dao = ScheduleDao
        list = dao.list_schedule(args)
        return list

    # 处理预约列表 Tabular data for the list
    @classmethod
    def list_schedule_result(self, data):
        result = []
        for item in data:
            schedule_dict = {}
            schedule_dict['schedule_id'] = item.schedule_id
            schedule_dict['title'] = item.title
            schedule_dict['content'] = item.content
            schedule_dict['is_urgent'] = item.is_urgent # 是否紧急
            schedule_dict['start_date'] = str(item.start_date)
            schedule_dict['end_date'] = str(item.end_date)
            # 状态
            schedule_dict['status'] = item.status
            if item.status in schedule_status_data:
                schedule_dict['status_label'] = schedule_status_data[item.status]
            else:
                schedule_dict['status_label'] = ''
            # 患者信息
            if item.name == '':
                # 患者
                patient = self.get_patient(item.patient_id)
                if patient == None:
                    schedule_dict['patient'] = ''
                    schedule_dict['patient_id'] = 0
                else:
                    schedule_dict['patient'] = patient.name
                    schedule_dict['patient_id'] = patient.id
            else:
                schedule_dict['patient'] = item.name
                schedule_dict['phone'] = item.phone
            # 扫描ID
            if item.standard_id == '':
                # 患者扫描记录
                patient_detail = self.get_patient_detail(item.patient_session_id)
                if patient_detail == None:
                    schedule_dict['patient_standard_id'] = ''
                else:
                    schedule_dict['patient_standard_id'] = patient_detail.standard_id
            else:
                schedule_dict['patient_standard_id'] = item.standard_id

            result.append(schedule_dict)
        return result
