#!/usr/bin/env python
# *_*coding:utf-8 *_*
from abc import ABCMeta, abstractmethod

'''
预约模块服务层抽象类
'''


class ScheduleService(metaclass=ABCMeta):
    @abstractmethod
    def get_schedule(self, schedule_id):
        pass

    @abstractmethod
    def list_schedule(self, args):
        pass

    @abstractmethod
    def list_schedule_result(self, data):
        pass

    @abstractmethod
    def delete_schedule(self, schedule_id):
        pass

    @abstractmethod
    def delete_batch_schedule(self, schedule_id_data):
        pass

    @abstractmethod
    def get_patient(self):
        pass

    @abstractmethod
    def get_patient_detail(self):
        pass

    @abstractmethod
    def create_schedule(self, data):
        pass

    @abstractmethod
    def update_schedule(self, data):
        pass
