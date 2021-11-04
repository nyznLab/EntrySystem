#coding=utf-8
from django.conf import settings
import subprocess
import os
from tools.exception import BussinessException
from django.http import StreamingHttpResponse

try:
    from comtypes import client
    import pythoncom
except ImportError:
    client = None

try:
    from win32com.client import constants, gencache
except ImportError:
    constants = None
    gencache = None

def create_pdf(wordPath, pdfPath, linuxPdfPath):
    """
    word转pdf,如果目录中有该文件则更新
    :param wordPath: word文件路径
    :param pdfPath:  生成pdf文件路径
    :param linuxPdfPath:  linux系统生成pdf文件路径
    三个参数是因为Linux和windows的文件存储方式不同，存储路径的输入格式应该也不同。
    因此，windows存储pdf的路径为pdfPath；Linux存储pdf的路径为linuxPdfPath
    """

    if client is None:  # 判断环境，linux环境这里肯定为None
        return doc2pdf_linux(wordPath, linuxPdfPath)

    pythoncom.CoInitialize()
    word = gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(wordPath)
    doc.ExportAsFixedFormat(pdfPath,
                            constants.wdExportFormatPDF,
                            Item=constants.wdExportDocumentWithMarkup,
                            CreateBookmarks=constants.wdExportCreateHeadingBookmarks)

    word.Quit(constants.wdDoNotSaveChanges)


def doc2pdf_linux(docPath, pdfPath):
    """
    convert a doc/docx document to pdf format (linux only, requires libreoffice)
    :param doc: path to document
    """
    cmd = 'libreoffice --headless --convert-to pdf'.split() + [docPath] + ['--outdir'] + [pdfPath]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=30)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)


class StreamingConvertedPdfTest:
    def __init__(self, dock_obj, word_path, download=True):
        self.doc = dock_obj
        self.download = download
        self.tmp_path = settings.MEDIA_ROOT + 'tmp/'
        self.pdf_path = settings.MEDIA_ROOT + 'tmp/' + self.doc.name.split('.')[-2]
        self.word_path = word_path


    def validate_document(self):
        if not self.doc.name.split('.')[-1] in ('doc', 'docm', 'docx'):
            raise BussinessException('请校验文件格式,上传文件为word格式')

    def check_tmp_folder(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)


    def convert_to_pdf(self):
        self.validate_document()
        self.check_tmp_folder()
        create_pdf(self.word_path, self.pdf_path, self.tmp_path)

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

    def get_content(self):
        self.convert_to_pdf()
        return {'path': self.tmp_path + self.doc.name.split('.')[-2] + '.pdf', 'name': self.get_file_name()}

    def stream_content(self):
        pass