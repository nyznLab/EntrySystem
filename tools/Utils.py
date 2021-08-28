from datetime import date
from datetime import datetime
# from patients.models import DPatientDetail
# 分页
class Paginator:
    def __init__(self,obj_count=1,obj_perpage=1,pagetag_current=1,pagetag_dsp_count=1):
        '''
        :param obj_count: 获得 条目总数
        :param obj_perpage: 定义 每页显示条目数
        :param pagetag_current: 获得 当前页码
        :param pagetag_dsp_count: 定义 显示多少个页码
        '''
        self.obj_count=obj_count
        self.obj_perpage=obj_perpage

        try:
            pagetag_current=int(pagetag_current)
            if pagetag_current < 1:
                pagetag_current=1
            self.pagetag_current=pagetag_current
        except Exception as e:
            self.pagetag_current=1

        self.pagetag_dsp_count=pagetag_dsp_count
        self.pagetag_all_count=self.last_page

    @property
    def obj_slice_start(self):
        return (self.pagetag_current-1)*self.obj_perpage

    @property
    def obj_slice_end(self):
        return self.pagetag_current* self.obj_perpage

    @property
    def has_prev_page(self):
        return False if self.pagetag_current <= self.first_page else True

    @property
    def has_next_page(self):
        return False if self.pagetag_current >= self.last_page else True

    @property
    def prev_page(self):
        if self.pagetag_current==1:
            return 1
        elif self.pagetag_current > self.pagetag_all_count:
            return self.pagetag_all_count
        else:
            return self.pagetag_current-1

    @property
    def next_page(self):
        if self.pagetag_current >= self.pagetag_all_count:
            return self.pagetag_all_count
        else:
            return self.pagetag_current+1

    @property
    def first_page(self):
        return 1

    @property
    def last_page(self):
        if self.obj_count % self.obj_perpage == 0:
            pagecount=int(self.obj_count / self.obj_perpage)
        else:
            pagecount = int(self.obj_count / self.obj_perpage)+1
        return pagecount

    @property
    def pagetag_range(self):
        '''页码列表'''
        start=1
        end=1
        #pagetag页码数 奇数偶数情况下，前后多少个不同。
        if self.pagetag_dsp_count%2==1:
            before=int(self.pagetag_dsp_count/2)
            after=before
        else:
            before=int(self.pagetag_dsp_count/2)
            after=before-1

        if self.pagetag_all_count < self.pagetag_dsp_count:
            start=1
            end=self.pagetag_all_count+1
        elif self.pagetag_current <= before:  #当前页码过小时
            start=1
            end=self.pagetag_dsp_count+1
        elif self.pagetag_current >= self.pagetag_all_count - after: #当前页码过大时
            start=self.pagetag_all_count - self.pagetag_dsp_count +1
            end=self.pagetag_all_count+1
        else:
            start=self.pagetag_current - before
            end=self.pagetag_current + after +1
            # print("logging %s %s %s"%(self.pagetag_current,self.pagetag_dsp_count,self.pagetag_dsp_count))

        return range(start, end)
# 计算年龄
def calculate_age(born):
    year = born.split('-')[0]
    month = born.split('-')[1]
    day = born.split('-')[2]
    birth = date(int(year), int(month), int(day))
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def calculate_age_by_scandate(born, scan_date):
    born_year = int(born.split('-')[0])
    born_month = int(born.split('-')[1])
    born_day = int(born.split('-')[2])
    scan_year = int(scan_date.split('-')[0])
    scan_month = int(scan_date.split('-')[1])
    scan_day = int(scan_date.split('-')[2])
    return scan_year - born_year - ((scan_month, scan_day) < (born_month, born_day))


# 空值判断
def object_judgment(object_flag):
    if object_flag:
        return None




# 获取患者病程记录存储路径
def get_patient_progress_note_direct(instance, filename):
    return '病程记录/{}/{}'.format(str(instance.patient_id), filename)

# 获取患者长期医嘱记录存储路径
def get_patient_medical_advice_direct(instance, filename):
    return '医嘱记录/{}/{}'.format(str(instance.patient_id), filename)




# 获取住院患者病程记录存储路径
def get_progress_note_direct(instance,filename):
    return '病程记录/{}/{}'.format(str(instance.id),filename)

# 获取住院患者出院记录存储路径
def get_out_record_direct(instance,filename):
    return '出院记录/{}/{}'.format(str(instance.id),filename)

# 获取住院患者长期医嘱记录存储路径
def get_medical_advice_direct(instance,filename):
    return '医嘱记录/{}/{}'.format(str(instance.id),filename)

def insert_medical_dict():
    from docx import Document  # 导入库
    from inpatients.models import DMedicalAdvice
    type_dict = {'常规护理':1,'常规治疗':2,'常规量表':3,'电休克组套':4,'物理治疗':5,'团体生物反馈治疗':6,'VR治疗':7}
    dmedicaladvice_list = []
    path = "/home/zxz/Downloads/qq-files/1162520680/file_recv/1_医嘱说明.docx"  # 文件路径
    document = Document(path)  # 读入文件
    tables = document.tables  # 获取文件中的表格集
    table = tables[0]  # 获取文件中的第一个表格
    for i in range(1, len(table.rows)):  # 从表格第二行开始循环读取表格数据
        dmedicaladvice = DMedicalAdvice(medical_name=table.cell(i, 1).text.strip(),type=type_dict[table.cell(i, 2).text.strip()])
        dmedicaladvice_list.append(dmedicaladvice)

    table = tables[1]  # 获取文件中的第一个表格
    for i in range(0, len(table.rows)):  # 从表格第二行开始循环读取表格数据
        dmedicaladvice = DMedicalAdvice(medical_name=table.cell(i, 1).text.strip(), type=type_dict[table.cell(i, 2).text.strip()])
        dmedicaladvice_list.append(dmedicaladvice)
    DMedicalAdvice.objects.bulk_create(dmedicaladvice_list)
def convert_to_pdf():
    import docx2pdf
    docx2pdf.convert()
