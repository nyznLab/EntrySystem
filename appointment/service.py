#!/usr/bin/env python
# *_*coding:utf-8 *_*
from abc import ABCMeta, abstractmethod

'''
预约模块服务层抽象类
'''


class AppointmentService(metaclass=ABCMeta):
    @abstractmethod
    def get_appointment(self, appointment_id):
        pass

    @abstractmethod
    def list_appointment(self, args):
        pass

    @abstractmethod
    def list_appointment_result(self, data):
        pass

    @abstractmethod
    def get_doctor(self):
        pass

    @abstractmethod
    def list_doctor(self):
        pass

    @abstractmethod
    def delete_appointment(self, appointment_id):
        pass

    @abstractmethod
    def delete_batch_appointment(self, appointment_id_data):
        pass

    @abstractmethod
    def create_appointment(self, data):
        pass

    @abstractmethod
    def update_appointment(self, data):
        pass
