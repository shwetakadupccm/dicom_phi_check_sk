import pydicom
import os
import pandas as pd

dicom_folder = 'D:\\Shweta\\radiology_dicom\\dicom_image_folder\\86_18_Indu_Sangle\\1.3.12.2.1107.5.12.7.3430.30000018021208400300000001212'
file_name = '1.3.12.2.1107.5.12.7.3430.30000018021208400300000001104.dic'
file_path = os.path.join(dicom_folder, file_name)

##
file = pydicom.read_file(file_path)
file.dir('loc')

# def get_dicom_file_data(file):
#     patient_name = file.PatientName
#     patient_age = file.PatientAge
#     file_uid = file.SOPInstanceUID
#     institute_name = file.InstitutionName
#     file_description = file.StudyDescription
#     return patient_name, patient_age, file_uid, institute_name, file_description
#
# patient_name, patient_age, file_uid, institute_name, file_description = get_dicom_file_data(file)

def get_dicom_file_data(dicom_folder_path):
    file_names = []
    dir_paths = []
    patient_names = []
    patient_ages = []
    uids = []
    series_description = []
    series_number = []
    file_description_lst = []
    for root, dirs, files in os.walk(dicom_folder_path):
        for file in files:
            if file.endswith('.dic'):
                file_names.append(file)
                file_path = os.path.join(root, file)
                dir_path = os.path.dirname(file_path)
                dir_paths.append(dir_path)
                file_txt = pydicom.read_file(file_path)
                patient_name = file_txt.PatientName
                patient_names.append(patient_name)
                patient_age = file_txt.PatientAge
                patient_ages.append(patient_age)
                file_uid = file_txt.SOPInstanceUID
                uids.append(file_uid)
                sr_des = file_txt.SeriesDescription
                series_description.append(sr_des)
                sr_num = file_txt.SeriesNumber
                series_number.append(sr_num)
                file_description = file_txt.StudyDescription
                file_description_lst.append(file_description)
    output_df = pd.DataFrame(file_names, columns=['file_name'])
    output_df['file_path'] = dir_paths
    output_df['patient_name'] = patient_names
    output_df['patient_age'] = patient_ages
    output_df['file_uid'] = uids
    output_df['series_description'] = series_description
    output_df['series_number'] = series_number
    output_df['file_description'] = file_description_lst
    return output_df

output_df = get_dicom_file_data('D:\\Shweta\\radiology_dicom\\dicom_image_folder')
output_df.to_excel('D:\\Shweta\\radiology_dicom\\dicom_image_folder\\output_df\\2021_08_25_dicom_file_series_data_sk.xlsx', index=False)
