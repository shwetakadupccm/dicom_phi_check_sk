import re
import pydicom
import os
import pandas as pd

# dicom_folder = 'D:\\Shweta\\radiology_dicom\\dicom_image_folder\\86_18_Indu_Sangle\\1.3.12.2.1107.5.12.7.3430.30000018021208400300000001212'
# file_name = '1.3.12.2.1107.5.12.7.3430.30000018021208400300000001104.dic'
# file_path = os.path.join(dicom_folder, file_name)

##
# file = pydicom.read_file(file_path)
# file.dir('img')

# def get_dicom_file_data(file):
#     patient_name = file.PatientName
#     patient_age = file.PatientAge
#     file_uid = file.SOPInstanceUID
#     institute_name = file.InstitutionName
#     file_description = file.StudyDescription
#     return patient_name, patient_age, file_uid, institute_name, file_description
#
# patient_name, patient_age, file_uid, institute_name, file_description = get_dicom_file_data(file)


varsha_chitre_folder = 'D:/Shweta/radiology_dicom/dicom_image_folder/43_18_Varsha_Chitre/1.3.12.2.1107.5.12.7.3430.30000018011607462201500000117'
file_name1 = '1.3.12.2.1107.5.12.7.3430.30000018011607462201500000009.dic'
file_path = os.path.join(varsha_chitre_folder, file_name1)

file_info = pydicom.read_file(file_path)
file_info.dir('pat')

# code_id = file_info[0x0054, 0x0220][0]
# code_value = code_id.values
# code_meaning = code_id['CodeMeaning'].value

def clean_img_laterality(img_laterality):
    if img_laterality == 'R':
        return 'Right'
    elif img_laterality == 'L':
        return 'Left'
    else:
        return None

def get_code_type_from_meaning(code_meaning):
    if code_meaning == 'cranio-caudal':
        return 'CC'
    elif code_meaning == 'medio-lateral oblique':
        return 'MLO'
    else:
        return None

def get_image_type(series_description):
    if 'Segmentation' in series_description:
        return 'tomo'
    elif 'Diagnosis' in series_description:
        return 'mammogram'
    else:
        return None

def get_dicom_file_data(dicom_folder_path, path_to_replace = 'D:\\Shweta\\radiology_dicom\\dicom_image_folder\\'):
    dicom_file_data = []
    for root, dirs, files in os.walk(dicom_folder_path):
        for file in files:
            if file.endswith('.dic'):
                file_path = os.path.join(root, file)
                print(file_path)
                dir_path = os.path.dirname(file_path)
                # print(dir_path)
                cleaned_dir_path = dir_path.replace(path_to_replace, '')
                file_txt = pydicom.read_file(file_path)
                patient_name = file_txt.PatientName
                patient_age = file_txt.PatientAge
                file_uid = file_txt.SOPInstanceUID
                img_laterality = file_txt.ImageLaterality
                img_laterality_cleaned = clean_img_laterality(img_laterality)
                sr_des = file_txt.SeriesDescription
                file_description = file_txt.StudyDescription
                code_id = file_txt[0x0054, 0x0220][0]
                code_meaning = code_id['CodeMeaning'].value
                code_type = get_code_type_from_meaning(code_meaning)
                image_type = get_image_type(sr_des)
                slice_lst = file_txt.dir('slice')
                if 'SliceLocation' in slice_lst:
                    slice_loc = file_txt.SliceLocation
                    new_file_name = img_laterality_cleaned + '_' + code_type + '_' + image_type + '_' + str(slice_loc)
                else:
                    slice_loc = None
                    new_file_name = img_laterality_cleaned + '_' + code_type + '_' + image_type
                output_lst = [file, cleaned_dir_path, patient_name, patient_age, file_uid, img_laterality_cleaned, slice_loc,
                                  code_meaning, code_type, sr_des, file_description, image_type, new_file_name]
                dicom_file_data.append(output_lst)
    colnames = ['file_name', 'file_path', 'patient_name', 'patient_age', 'file_uid', 'image_laterality',
                'slice_location', 'code_meaning', 'code_type', 'series_description', 'file_description', 'image_type',
                'new_file_name']
    output_df = pd.DataFrame(dicom_file_data, columns=colnames)
    return output_df

output_df = get_dicom_file_data('D:\\Shweta\\radiology_dicom\\dicom_image_folder')
output_df.to_excel('D:\\Shweta\\radiology_dicom\\dicom_image_folder\\output_df\\2021_08_31_dicom_file_data_with_new_names_sk.xlsx', index=False)

