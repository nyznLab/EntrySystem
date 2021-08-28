#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：entry_system 
@File ：doc2pdf.py
@IDE  ：PyCharm 
@Author ：skj
@Date ：1/31/21 11:39 AM 
'''
import os
import tempfile
import subprocess
from django.conf import settings
from django.http import StreamingHttpResponse
from tools.exception import BussinessException
class StreamingConvertedPdf:

    def __init__(self, dock_obj, download=True):
        self.doc = dock_obj
        self.download = download
        self.tmp_path = settings.MEDIA_ROOT + 'tmp/'

    def validate_document(self):
        if not self.doc.name.split('.')[-1] in ('doc', 'docm', 'docx'):
            raise BussinessException('请校验文件格式,上传文件为word格式')

    def check_tmp_folder(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    def convert_to_pdf(self):
        self.validate_document()
        self.check_tmp_folder()

        with tempfile.NamedTemporaryFile(prefix=self.tmp_path, delete=False) as tmp:
            tmp.write(self.doc.read())
            tmp.close()
            cmd = 'soffice --headless'.split() + ['--convert-to pdf'] + [tmp.name] + ['--outdir'] + [self.tmp_path]
            print(cmd)
            p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            p.wait()
            stdout, stderr = p.communicate()
            if stderr:
                raise subprocess.SubprocessError(stderr.decode("gbk"))
            self.tmp_path = tmp.name + '.pdf'

    def get_file_name(self):
        return self.doc.name.split('.')[0] + '.pdf'

    def stream_content(self):
        self.convert_to_pdf()
        res = StreamingHttpResponse(open(self.tmp_path, 'rb'), content_type='application/pdf')
        if self.download:
            res['Content-Disposition'] = 'attachment; filename="{}"'.format(self.get_file_name())
        return res

    def __del__(self):
        try:
            if os.path.exists(self.tmp_path):
                os.remove(self.tmp_path)
        except IOError:
            print('Error deleting file')


class ConvertFileModelField(StreamingConvertedPdf):

    def get_content(self):
        self.convert_to_pdf()
        return {'path': self.tmp_path, 'name': self.get_file_name()}

    def stream_content(self):
        pass
