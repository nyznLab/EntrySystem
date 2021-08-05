#!/usr/bin/env python
# *_*coding:utf-8 *_*
from appointment.dao import AppointmentDao
from appointment.service import AppointmentService
from config.OptionsConfig import appointment_items_data, gender_data, appointment_time_data, appointment_status_data
from users.models import SUser

'''
预约模块服务层实现类
'''


class AppointmentServiceImpl(AppointmentService):

    # 创建
    @classmethod
    def create_appointment(self, appointment):
        dao = AppointmentDao()
        return dao.save_appointment(appointment)

    # 更新
    @classmethod
    def update_appointment(self, appointment):
        dao = AppointmentDao()
        return dao.save_appointment(appointment)

    # 删除
    @classmethod
    def delete_appointment(self, appointment_id):
        dao = AppointmentDao()
        return dao.delete_appointment(appointment_id)

    # 批量删除
    @classmethod
    def delete_batch_appointment(self, appointment_id_data):
        dao = AppointmentDao()
        return dao.delete_batch_appointment(appointment_id_data)

    # 医生列表
    @classmethod
    def list_doctor(self):
        return SUser.objects.all()

    # 获取医生
    @classmethod
    def get_doctor(self, doctor_id):
        return SUser.objects.filter(id=doctor_id).first()

    # 根据主键获取预约记录
    @classmethod
    def get_appointment(self, appointment_id):
        dao = AppointmentDao()
        appointment = dao.get_appointment(appointment_id)
        return appointment

    # 获取预约记录列表
    @classmethod
    def list_appointment(self, args):
        dao = AppointmentDao
        list = dao.list_appointment(args)
        return list

    # 处理预约列表 Tabular data for the list
    @classmethod
    def list_appointment_result(self, data):
        result = []
        for item in data:
            appointment_dict = {}
            appointment_dict['appointment_id'] = item.appointment_id
            appointment_dict['name'] = item.name
            appointment_dict['sex'] = item.sex
            # 性别
            if item.sex in gender_data:
                appointment_dict['sex_label'] = gender_data[item.sex]
            else:
                appointment_dict['sex_label'] = ''
            appointment_dict['birth_date'] = str(item.birth_date)
            appointment_dict['phone'] = item.phone
            appointment_dict['items'] = item.items
            appointment_dict['appointment_date'] = str(item.appointment_date)
            # 预约时间
            if item.appointment_time in appointment_time_data:
                appointment_dict['appointment_time'] = appointment_time_data[item.appointment_time]
            else:
                appointment_dict['appointment_time'] = ''
            # 状态
            appointment_dict['status'] = item.status
            if item.status in appointment_status_data:
                appointment_dict['status_label'] = appointment_status_data[item.status]
            else:
                appointment_dict['status_label'] = ''
            # 医生
            doctor = self.get_doctor(item.doctor_id)
            if doctor == None:
                appointment_dict['doctor'] = ''
                appointment_dict['doctor_id'] = 0
            else:
                appointment_dict['doctor'] = doctor.name
                appointment_dict['doctor_id'] = doctor.id

            # 预约项目
            if item.items is not None and item.items != '':
                # 处理预约项目
                items_array = item.items.split(',')
                items_label = ''
                for i in items_array:
                    i = int(i)
                    if i in appointment_items_data:
                        items_label += appointment_items_data[i]['title'] + '、'
                appointment_dict['items_label'] = items_label[0:-1]  # 去掉末尾的符号
            result.append(appointment_dict)
        return result
