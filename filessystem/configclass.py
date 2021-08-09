# 预处理各个文件对应文件
class preprocessDict(object):
    REHO = 'ReHo_FunImgARWDCF'
    ALFF = 'ALFF_FunImgARWSD'
    fALFF = 'fALFF_FunImgARWSD'
    FC = 'FC_FunImgARWSDCF'
    ROI_FC = 'ROISignals_FunImgARWSDCF'

    ReHo_Types = ['ReHo','smReHo','sReHo','mReHo','szReHo','zReHo']
    ALFF_Types = ['ALFF','mALFF','zALFF']

    fALFF_Types = ['fALFF','mfALFF','zfALFF']
    FC_Types = ['FC','zFC','ROI_Orderkey_FC','ROI_FC']
    ROI_FC_Types = ['ROI_OrderKey','ROICorrelation_FisherZ','ROICorrelation','ROISignals']