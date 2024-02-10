import pandas as pd
import numpy as np
from django.conf import settings

# def perform_calculations(base_data_df, user, year):


base_data_df = pd.read_excel("C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/TRI_base_data.xlsx")

base_data_df['Eligibility_CD'] = np.where(base_data_df['chronic_disease'].str.strip() == 'लागू नहीं', 0, 1)

    
            
base_data_df['CD_Cum_Score'] = np.where(base_data_df['chronic_disease'].str.strip() == "हां", 0, 1)

base_data_df['Age'] = pd.to_numeric(base_data_df['Age'], errors='coerce')

base_data_df['Eligibility_IMM'] = np.where(base_data_df['Age'] < 1, 0, 1)




conditions_IMM_Cum_Score = [
    (base_data_df['Age'] < 16),
    (base_data_df['basic_vaccination'].str.strip() == 'पूरी तरह')
]
values_IMM_Cum_Score = [np.nan, 1]
base_data_df['IMM_Cum_Score'] = np.select(conditions_IMM_Cum_Score, values_IMM_Cum_Score, default=0)


base_data_df['Eligibility_IND'] = np.where(base_data_df['Institutional_delivery'].str.strip() == 'लागू नहीं', 0, 1)



conditions_IND_Cum_Score = [
    (base_data_df['Institutional_delivery'].str.strip() == 'स्वास्थ्य केंद्र'),
    (base_data_df['Eligibility_IND'] == 0)
]
values_IND_Cum_Score = [1, np.nan]
base_data_df['IND_Cum_Score'] = np.select(conditions_IND_Cum_Score, values_IND_Cum_Score, default=0)



conditions_Eligibility_ANC = [
    (base_data_df['ANC'].str.strip() == 'लागू नहीं') | (16 > base_data_df['Age']) | (base_data_df['Age'] > 45) | (base_data_df['Gender'].str.strip() != 'महिला')
]
values_Eligibility_ANC = [0]
base_data_df['Eligibility_ANC'] = np.select(conditions_Eligibility_ANC, values_Eligibility_ANC, default=1)


conditions_ANC_Cum_Score = [
    (base_data_df['ANC'].str.strip().isin(['हाँ, सभी तिमाही', 'हाँ, 1 तिमाही', 'हाँ, 2 तिमाही'])),
    (base_data_df['Eligibility_ANC'] == 0)
]
values_ANC_Cum_Score = [1, np.nan]
base_data_df['ANC_Cum_Score'] = np.select(conditions_ANC_Cum_Score, values_ANC_Cum_Score, default=0)


condition_U5CM_Cum_Score = (base_data_df['Infant_mortality'].str.strip() == 'हां')
base_data_df['U5CM_Cum_Score'] = np.where(condition_U5CM_Cum_Score, 0, 1)

condition_2sq_Cum_Score = (base_data_df['2sqmeals'].str.strip() == 'हाँ, पर्याप्त')
base_data_df['2sq_Cum_Score'] = np.where(condition_2sq_Cum_Score, 1, 0)

keywords_Energy = ['चावल', 'रोटी', 'ज्वार', 'आलू', 'बाजरा', 'लिट्टी']
condition_Energy = base_data_df['food_diversity'].str.strip().apply(lambda x: any(keyword in x for keyword in keywords_Energy))
base_data_df['Energy'] = np.where(condition_Energy, 1, 0)

proteins_condition = (
    base_data_df['food_diversity'].str.contains('दाल|मछली|मांस|खुकड़ी|सत्तू', regex=True, na=False)
)
base_data_df['Proteins'] = np.where(proteins_condition, 1, 0)

condition_Vitamins = base_data_df['food_diversity'].apply(lambda x: 1 if 'साग' in x or 'अन्य' in x else 0)
base_data_df['Vitamins'] = condition_Vitamins

condition_FD_Cum_Score = (np.sum(base_data_df[['Energy', 'Proteins', 'Vitamins']], axis=1) == 3)
base_data_df['FD_Cum_Score'] = np.where(condition_FD_Cum_Score, 1, 0)

condition_eligibility_LE = (base_data_df['Age'] >= 10)
base_data_df['Eligibility LE'] = np.where(condition_eligibility_LE, 1, 0)

conditions = [
    (base_data_df['Ed'].isin(["6th कक्षा पूरा किया हुआ", "7th कक्षा पूरा किया हुआ", "8th कक्षा पूरा किया हुआ", "9th कक्षा पूरा किया हुआ", "10th कक्षा पूरा किया हुआ", "11th कक्षा पूरा किया हुआ", "12th कक्षा पूरा किया हुआ", "डिप्लोमा पूरा किया हुआ", "डिग्री पूरा किया हुआ", "पोस्ट ग्रेजुएशन पूरा किया हुआ"])),
    (base_data_df['Eligibility LE'] == 0)
]

choices = [1, np.nan]

base_data_df['cum_score_LE'] = np.select(conditions, choices, default=0)

condition_Eligibility_DRO = np.logical_or(base_data_df['Age'] < 15, base_data_df['Age'] > 64)
base_data_df['Eligibility DRO'] = np.where(condition_Eligibility_DRO, 0, 1)



conditions_cum_score_DRO = [
    (base_data_df['Ed'].str.strip().isin(['10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ', '12th कक्षा पूरा किया हुआ', 'डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ', 'पोस्ट ग्रेजुएशन पूरा किया हुआ'])),
    (base_data_df['Eligibility DRO'] == 0)
]

values_cum_score_DRO = [1, np.nan]
base_data_df['cum_score_DRO'] = np.select(conditions_cum_score_DRO, values_cum_score_DRO, default=0)




condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['Inst_Credit'].str.contains('आधार कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('बैंक खाता')) &
    (base_data_df['Inst_Credit'].str.contains('आयुष्मान कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('जच्चा बच्चा पात्रता'))
)
base_data_df['Aadhaar_bank_account_MCP_Aayushman'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)

condition_Ration = (base_data_df['ration_c_color'].str.strip() == 'लागू नहीं')
base_data_df['Ration'] = np.where(condition_Ration, 0, 1)


condition_job_labour_kisan_credit = base_data_df['Inst_Credit'].str.contains('जॉब कार्ड|श्रम कार्ड|किसान क्रेडिट कार्ड', case=False, na=False)
base_data_df['Job/ Labour/ Kisan credit'] = np.where(condition_job_labour_kisan_credit, 1, 0)


condition_CUM_SCORE_IC = ((base_data_df['Aadhaar_bank_account_MCP_Aayushman'] + base_data_df['Ration'] + base_data_df['Job/ Labour/ Kisan credit']) >= 1)

base_data_df['CUM_SCORE_IC'] = np.where(condition_CUM_SCORE_IC, 1, 0)


condition_CUM_SCORE_OWN = (base_data_df['agricultureland'].str.strip() == 'हां') | (base_data_df['home_ownership'].str.strip() == 'हां')
base_data_df['CUM_SCORE_OWN'] = np.where(condition_CUM_SCORE_OWN, 1, 0)


condition_CUM_SCORE_SANI = (base_data_df['defecation'].str.contains('घर के भीतर') | base_data_df['bath'].str.contains('घर के भीतर'))
base_data_df['CUM_SCORE_SANI'] = np.where(condition_CUM_SCORE_SANI, 1, 0)


condition_cum_score_Fuel = base_data_df['source_fuel'].str.contains("गैस")
base_data_df['cum_score_Fuel'] = np.where(condition_cum_score_Fuel, 1, 0)


condition_cum_score_SoDrWa = base_data_df['source_drinking_water'].str.contains("घर का नल")
base_data_df['cum_score_SoDrWa'] = np.where(condition_cum_score_SoDrWa, 1, 0)

base_data_df['cum_score_ELECTR'] = np.where(base_data_df['electricity'].str.strip() == 'हां', 1, 0)

condition_ASS_INFO = (
    (base_data_df['assets'].str.contains('इंटरनेट का उपयोग')) |
    (base_data_df['assets'].str.contains('सामान्य फोन')) |
    (base_data_df['assets'].str.contains('टेलीविजन')) |
    (base_data_df['assets'].str.contains('कंप्यूटर सिस्टम/लैपटॉप/टैबलेट'))|
    (base_data_df['smart_phone'].str.contains('हां'))
)
base_data_df['ASS_INFO'] = np.where(
    condition_ASS_INFO, 1, 0
)


condition_ASS_LIVE = (
    (base_data_df['assets'].str.contains('बिजली का पंखा')) |
    (base_data_df['assets'].str.contains('गैस - चूल्हा')) |
    (base_data_df['assets'].str.contains('हल')) |
    (base_data_df['assets'].str.contains('मिक्सी'))|
    (base_data_df['assets'].str.contains('सिचाई के लिए पम्पसेट'))|
    (base_data_df['assets'].str.contains('प्रेशर कुकर'))|
    (base_data_df['assets'].str.contains('तालाब'))
)
base_data_df['ASS_LIVE'] = np.where(
    condition_ASS_LIVE, 1, 0
)


condition_ASS_TRANS = (
    (base_data_df['assets'].str.contains('गाड़ी')) |
    (base_data_df['assets'].str.contains('साइकिल')) |
    (base_data_df['assets'].str.contains('दो पहिया')) |
    (base_data_df['assets'].str.contains('रिक्शा'))|
    (base_data_df['assets'].str.contains('ट्रैक्टर'))
)
base_data_df['ASS_TRANS'] = np.where(
    condition_ASS_TRANS, 1, 0
)


condition_ASS = ((base_data_df['ASS_TRANS'] + base_data_df['ASS_LIVE'] + base_data_df['ASS_INFO'])) == 3
base_data_df['ASS'] = np.where(condition_ASS, 1, 0)


columns_to_handle = ['no_hen_cock', 'no_goats', 'no_cows', 'no_buffaloes', 'no_oxan', 'no_pigs', 'no_ducks', 'no_swan']

for column in columns_to_handle:
        base_data_df[column] = pd.to_numeric(base_data_df[column], errors='coerce').fillna(0).astype(int)


condition_ANI = (
(base_data_df['no_hen_cock'] + base_data_df['no_goats'] + base_data_df['no_cows'] + base_data_df['no_buffaloes'] + base_data_df['no_oxan'] + base_data_df['no_pigs'] + base_data_df['no_ducks'] + base_data_df['no_swan']) > 0 | (base_data_df['Pond_Fish'] == 'हां'))


base_data_df['ANI'] = np.where(condition_ANI, 1, 0)




condition_CUM_SCORE_ASS = (base_data_df['ASS'] + base_data_df['ANI']== 2)
base_data_df['CUM_SCORE_ASS'] = np.where(condition_CUM_SCORE_ASS, 1, 0)


condition_cum_score_L = (
    (base_data_df['Language'].str.contains('कोरथा')) |
    (base_data_df['Language'].str.contains('मुंडारी')) |
    (base_data_df['Language'].str.contains('बिरहोर')) |
    (base_data_df['Language'].str.contains('बिरजिया'))|
    (base_data_df['Language'].str.contains('करमाली'))|
    (base_data_df['Language'].str.contains('हो')) |
    (base_data_df['Language'].str.contains('खरिया')) |
    (base_data_df['Language'].str.contains('खोंडी')) |
    (base_data_df['Language'].str.contains('संताली'))|
    (base_data_df['Language'].str.contains('कोरा'))|
    (base_data_df['Language'].str.contains('कोरवा')) |
    (base_data_df['Language'].str.contains('पहाड़िया')) |
    (base_data_df['Language'].str.contains('कुरुख/ओरांव')) |
    (base_data_df['Language'].str.contains('सावर'))
    
)
base_data_df['cum_score_L'] = np.where(
    condition_cum_score_L, 1, 0
)

base_data_df['cum_score_So'] = np.where(base_data_df['traditional_song'].str.strip() == "हां", 1, 0)



condition_cum_score_MuI = (
    (base_data_df['traditional_instrument'].str.strip() == "हां") |
    (base_data_df['Traditional_Instrument'].str.strip() != "कुछ नहीं")
)

base_data_df['cum_score_MuI'] = np.where(condition_cum_score_MuI, 1, 0)



condition_cum_score_Da = (base_data_df['traditional_dance'].str.strip() == "हां")
base_data_df['cum_score_Da'] = np.where(condition_cum_score_Da, 1, 0)


condition_cum_score_Arts = ((base_data_df['cum_score_Da'] + base_data_df['cum_score_MuI'] + base_data_df['cum_score_So'])) > 0
base_data_df['cum_score_Arts'] = np.where(condition_cum_score_Arts, 1, 0)


condition_Eligibility_voter = (base_data_df['Age'] >= 18)
base_data_df['Eligibility_voter'] = np.where(condition_Eligibility_voter, 1, 0)






conditions_cum_score_EV = [
    (base_data_df['Eligibility_voter'] == 0),
    ((base_data_df['voter'] > 0) | (base_data_df['voter'] == np.nan) | (base_data_df['voter'] == "") | base_data_df['voter'].isnull())
]


values_cum_score_EV = [np.nan, 1]
base_data_df['cum_score_EV'] = np.select(conditions_cum_score_EV, values_cum_score_EV, default=0)



condition_Cum_s_core_meetings = (
    (base_data_df['SHG'].str.contains("हां")) |
    (base_data_df['traditional_meeting'].str.contains("हां")) |
    (base_data_df['gram_sabha_meeting'].str.contains("हां")) |
    (base_data_df['Panchayat_meetings'].str.contains("हां"))
    
)
base_data_df['Cum_s core_meetings'] = np.where(
    condition_Cum_s_core_meetings, 1, 0
)


excel_writer = pd.ExcelWriter('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/base_data.xlsx', engine='xlsxwriter')
base_data_df.to_excel(excel_writer, sheet_name='Sheet1', na_rep='NA', index=False)
excel_writer._save()
print("Result Excel file saved successfully.")
# base_data_df.to_excel(settings.EXCEL_FILE_PATH, index=False)
# print("Result Excel file saved successfully.")

# base_data_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/base_data_df.xlsx', index=False)
# print("Result Excel file saved successfully.")

total_fid = base_data_df[['__fid__']].values.tolist()
tribes = np.array(base_data_df['Tribe_N']).flatten().tolist()
Block_name = np.array(base_data_df['Block_name']).flatten().tolist()
village_name = np.array(base_data_df['village_name']).flatten().tolist()
District_name = np.array(base_data_df['District_name']).flatten().tolist()



unique_fid = []
unique_tribes = []
unique_Block_name = []
unique_village_name = []
unique_District_name = []

for x in total_fid:
    if x not in unique_fid:
        unique_fid.append(x)

for x in tribes:
    if x not in unique_tribes:
        unique_tribes.append(x)

for x in Block_name:
    if x not in unique_Block_name:
        unique_Block_name.append(x)
for x in village_name:
    if x not in unique_village_name:
        unique_village_name.append(x)
for x in District_name:
    if x not in unique_District_name:
        unique_District_name.append(x)


score = [0] * len(unique_fid)
HH_size_list = [0] * len(unique_fid)
HH_tribe_list = [""] * len(unique_fid)
HH_village_name_list = [""] * len(unique_fid)
HH_District_name_list = [""] * len(unique_fid)
HH_Block_name_list = [""] * len(unique_fid)


for i in range(len(unique_fid)):
        for j in range(len(total_fid)):

            if unique_fid[i] == total_fid[j]:
                HH_size_list[i] += 1
                if HH_tribe_list[i] == "":
                    HH_tribe_list[i] = tribes[j]
                    HH_village_name_list[i]=village_name[j]
                    HH_District_name_list[i]=District_name[j]
                    HH_Block_name_list[i]=Block_name[j]




def calScore(list1,list2,score):
    for i in range(len(unique_fid)):
        score[i] = 0
        for j in range(len(list1)):

            if unique_fid[i] == list1[j]:
                if pd.isna(list2[j]) or list2[j] == np.nan:
                    continue  
                score[i] += int(list2[j])

# Rest of your code remains unchanged

# Rest of your code remains unchanged


# Rest of your code remains unchanged


score_columns = {}

for column in ['Eligibility_CD', 'CD_Cum_Score', 'Eligibility_IMM','IMM_Cum_Score','Eligibility_IND', 'IND_Cum_Score', 'Eligibility_ANC', 'ANC_Cum_Score', 'U5CM_Cum_Score', '2sq_Cum_Score', 'FD_Cum_Score', 'Eligibility LE', 'cum_score_LE', 'Eligibility DRO', 'cum_score_DRO', 'CUM_SCORE_IC', 'CUM_SCORE_OWN', 'CUM_SCORE_SANI', 'cum_score_Fuel', 'cum_score_SoDrWa', 'cum_score_ELECTR','CUM_SCORE_ASS', 'Cum_s core_meetings', 'cum_score_L', 'cum_score_Arts', 'Eligibility_voter', 'cum_score_EV']:
    # Initialize a list to store cumulative scores
    score_column = [0] * len(unique_fid)

    # Calculate the cumulative score
    calScore(total_fid, base_data_df[column], score_column)

    # Add the cumulative score to the dictionary
    score_columns[f'Sum of {column}'] = score_column

# Combine the cumulative scores into a DataFrame
cum_score_df = pd.DataFrame({
    '_fid_': unique_fid,
    **score_columns
})

cum_score_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/cum_scores.xlsx', index=False)
print("Result Excel file saved successfully.")


HH_score_df = pd.DataFrame({
    '_fid_': unique_fid,
    'Tribe_N' : HH_tribe_list,
    'Sum of HH_S' : HH_size_list,
    'HH_village_name_list':HH_village_name_list,
    'HH_Block_name_list':HH_Block_name_list,
    'HH_District_name_list':HH_District_name_list,

})

village_name_list = [""] * len(unique_tribes)
Block_name_list = [""] * len(unique_tribes)
District_name_list = [""] * len(unique_tribes)
for i in range(len(unique_tribes)):
    for j in range(len(tribes)):
        if tribes[j] == unique_tribes[i] and village_name_list[i].find(village_name[j]) == -1:
            village_name_list[i] += village_name[j] + ', '
        if tribes[j] == unique_tribes[i] and Block_name_list[i].find(Block_name[j]) == -1:
            Block_name_list[i] += Block_name[j] + ', '
        if tribes[j] == unique_tribes[i] and District_name_list[i].find(District_name[j]) == -1:
            District_name_list[i] += District_name[j] + ', '
        
# from .models import Tribe


# Assuming village_name_list has been created and populated




# # Conditions and value assigning for the new column 'HH_Score_H_CD'
HH_score_df['HH_Score_H_CD'] = np.where(cum_score_df['Sum of Eligibility_CD'] == cum_score_df['Sum of CD_Cum_Score'], 1, 0)
HH_score_df['HH_Score_H_IMM'] = np.where(cum_score_df['Sum of Eligibility_IMM'] == cum_score_df['Sum of IMM_Cum_Score'], 1, 0)

conditions = [
    (cum_score_df['Sum of Eligibility_IND'] == HH_score_df['Sum of HH_S']),
    (cum_score_df['Sum of Eligibility_IND'] != HH_score_df['Sum of HH_S'])
]

choices = [
    np.where(cum_score_df['Sum of IND_Cum_Score'] > 1, 1, 0),
    np.nan
]

HH_score_df['HH_Score_H_IND'] = np.select(conditions, choices, default=0).astype('object')


condition_HH_Score_H_ANC = (cum_score_df['Sum of Eligibility_ANC'] > 0) & (cum_score_df['Sum of ANC_Cum_Score'] > 1)
HH_score_df['HH_Score_H_ANC'] = np.where(condition_HH_Score_H_ANC, 1, np.where(cum_score_df['Sum of Eligibility_ANC'] > 0, 0, np.nan)).astype('object')



HH_score_df['HH_Score_H_IND'] = pd.to_numeric(HH_score_df['HH_Score_H_IND'], errors='coerce')
HH_score_df['HH_Score_H_ANC'] = pd.to_numeric(HH_score_df['HH_Score_H_ANC'], errors='coerce')

conditions_HH_Score_H_MC = [
    (HH_score_df['HH_Score_H_IND'].notna() & HH_score_df['HH_Score_H_ANC'].notna() & (HH_score_df['HH_Score_H_IND'] + HH_score_df['HH_Score_H_ANC'] == 2)),
    (HH_score_df['HH_Score_H_IND'].isna() | HH_score_df['HH_Score_H_ANC'].isna())
]
choices_HH_Score_H_MC = [1, np.nan]
HH_score_df['HH_Score_H_MC'] = np.select(conditions_HH_Score_H_MC, choices_HH_Score_H_MC, default=0)
HH_score_df['HH_Score_H_MC'] = pd.to_numeric(HH_score_df['HH_Score_H_MC'], errors='coerce')

HH_score_df['HH_Score_H_U5CM'] = np.where(cum_score_df['Sum of U5CM_Cum_Score'] < HH_score_df['Sum of HH_S'], 0, 1)
HH_score_df['HH_Score_H_FS'] = np.where((cum_score_df['Sum of 2sq_Cum_Score'] == HH_score_df['Sum of HH_S']) & (cum_score_df['Sum of FD_Cum_Score'] == HH_score_df['Sum of HH_S']), 1, 0)

HH_score_df['H_TOT_IND'] = HH_score_df[['HH_Score_H_CD', 'HH_Score_H_IMM', 'HH_Score_H_MC', 'HH_Score_H_U5CM', 'HH_Score_H_FS']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
HH_score_df['H_DEV_IND'] = HH_score_df[['HH_Score_H_CD', 'HH_Score_H_IMM', 'HH_Score_H_MC', 'HH_Score_H_U5CM', 'HH_Score_H_FS']].eq(1).sum(axis=1)
HH_score_df['H_weightage'] = round((0.2 / HH_score_df['H_TOT_IND']),4)
HH_score_df['H_DS'] = round((HH_score_df['H_weightage'] * HH_score_df['H_DEV_IND']),3)


HH_score_df['HH_Score_E_LE'] = np.where(cum_score_df['Sum of cum_score_LE'] >= 1, 1, 0)
HH_score_df['HH_Score_E_DRO'] = np.where(cum_score_df['Sum of cum_score_DRO'] == cum_score_df['Sum of Eligibility DRO'], 1, 0)

HH_score_df['E_TOT_IND'] = HH_score_df[['HH_Score_E_LE', 'HH_Score_E_DRO']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
HH_score_df['E_DEV_IND'] = HH_score_df[['HH_Score_E_LE', 'HH_Score_E_DRO']].eq(1).sum(axis=1)
HH_score_df['E_weightage'] = round((0.2 / HH_score_df['E_TOT_IND']),4)
HH_score_df['E_DS'] = round((HH_score_df['E_weightage'] * HH_score_df['E_DEV_IND']),3)


HH_score_df['HH_Score_S_IC'] = np.where(cum_score_df['Sum of CUM_SCORE_IC'] >= 1, 1, 0)


# Assuming 'cum_score_df' is your DataFrame

# Assigning values for the column "HH_Score_S_OWN"
HH_score_df['HH_Score_S_OWN'] = np.where(cum_score_df['Sum of CUM_SCORE_OWN'] >= 1, 1, 0)

# Assigning values for the column "HH_Score_S_SANI"
HH_score_df['HH_Score_S_SANI'] = np.where(cum_score_df['Sum of CUM_SCORE_SANI'] == HH_score_df['Sum of HH_S'], 1, 0)

# Assigning values for the column "HH_Score_S_Fuel"
HH_score_df['HH_Score_S_Fuel'] = np.where(cum_score_df['Sum of cum_score_Fuel'] >= 1, 1, 0)

# Assigning values for the column "HH_Score_S_SoDrWa"
HH_score_df['HH_Score_S_SoDrWa'] = np.where(cum_score_df['Sum of cum_score_SoDrWa'] >= 1, 1, 0)

# Assigning values for the column "HH_Score_S_ELECTR"
HH_score_df['HH_Score_S_ELECTR'] = np.where(cum_score_df['Sum of cum_score_ELECTR'] >= 1, 1, 0)

# Assigning values for the column "HH_Score_S_ASS"
HH_score_df['HH_Score_S_ASS'] = np.where(cum_score_df['Sum of CUM_SCORE_ASS'] >= 1, 1, 0)

HH_score_df['S_TOT_IND'] = HH_score_df[['HH_Score_S_IC', 'HH_Score_S_OWN', 'HH_Score_S_SANI', 'HH_Score_S_Fuel', 'HH_Score_S_SoDrWa', 'HH_Score_S_ELECTR', 'HH_Score_S_ASS']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
HH_score_df['S_DEV_IND'] = HH_score_df[['HH_Score_S_IC', 'HH_Score_S_OWN', 'HH_Score_S_SANI', 'HH_Score_S_Fuel', 'HH_Score_S_SoDrWa', 'HH_Score_S_ELECTR', 'HH_Score_S_ASS']].eq(1).sum(axis=1)
HH_score_df['S_weightage'] = round((0.2 / HH_score_df['S_TOT_IND']),4)
HH_score_df['S_DS'] = round((HH_score_df['S_weightage'] * HH_score_df['S_DEV_IND']),3)


HH_score_df['HH_Score_C_L'] = np.where(cum_score_df['Sum of cum_score_L'] >= 1, 1, 0)
HH_score_df['HH_Score_C_Arts'] = np.where(cum_score_df['Sum of cum_score_Arts'] >= 1, 1, 0)

HH_score_df['C_TOT_IND'] = HH_score_df[['HH_Score_C_L', 'HH_Score_C_Arts']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
HH_score_df['C_DEV_IND'] = HH_score_df[['HH_Score_C_L', 'HH_Score_C_Arts']].eq(1).sum(axis=1)
HH_score_df['C_weightage'] = round((0.2 / HH_score_df['C_TOT_IND']),4)
HH_score_df['C_DS'] = round((HH_score_df['C_weightage'] * HH_score_df['C_DEV_IND']),3)




conditions_HH_Score_G_EV = [
    (np.logical_and(cum_score_df['Sum of cum_score_EV'] > 0, cum_score_df['Sum of cum_score_EV'] == cum_score_df['Sum of Eligibility_voter'])),
    (cum_score_df['Sum of Eligibility_voter'] == 0)
]

choices_HH_Score_G_EV = [1, np.nan]

HH_score_df['HH_Score_G_EV'] = np.select(conditions_HH_Score_G_EV, choices_HH_Score_G_EV, default=0)
HH_score_df['HH_Score_G_EV'] = pd.to_numeric(HH_score_df['HH_Score_G_EV'], errors='coerce')

HH_score_df['HH_Score_G_meeting'] = np.where(cum_score_df['Sum of Cum_s core_meetings'] > 0, 1, 0)

HH_score_df['G_TOT_IND'] = HH_score_df[['HH_Score_G_EV', 'HH_Score_G_meeting']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
HH_score_df['G_DEV_IND'] = HH_score_df[['HH_Score_G_EV', 'HH_Score_G_meeting']].eq(1).sum(axis=1)
HH_score_df['G_weightage'] = round((0.2 / HH_score_df['G_TOT_IND']),4)
HH_score_df['G_DS'] = round((HH_score_df['G_weightage'] * HH_score_df['G_DEV_IND'] ),3)

HH_score_df['HH_DS'] = np.sum(HH_score_df[['H_DS', 'E_DS', 'S_DS', 'C_DS', 'G_DS']].values, axis=1)


HH_score_df['H_Is_the_HH_developed'] = np.where(HH_score_df['H_DS'] < 0.066, 0, 1)
HH_score_df['E_Is_the_HH_developed'] = np.where(HH_score_df['E_DS'] < 0.066, 0, 1)
HH_score_df['S_Is_the_HH_developed'] = np.where(HH_score_df['S_DS'] < 0.066, 0, 1)
HH_score_df['C_Is_the_HH_developed'] = np.where(HH_score_df['C_DS'] < 0.066, 0, 1)
HH_score_df['G_Is_the_HH_developed'] = np.where(HH_score_df['G_DS'] < 0.066, 0, 1)

HH_score_df['Is_the_HH_multidimensionally_developed'] = np.where(HH_score_df['HH_DS'] <= 0.33, 0, 1)

HH_score_df['H_HH_members_of_developed_HHs'] = np.where(HH_score_df['H_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
HH_score_df['E_HH_members_of_developed_HHs'] = np.where(HH_score_df['E_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
HH_score_df['S_HH_members_of_developed_HHs'] = np.where(HH_score_df['S_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
HH_score_df['C_HH_members_of_developed_HHs'] = np.where(HH_score_df['C_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
HH_score_df['G_HH_members_of_developed_HHs'] = np.where(HH_score_df['G_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)

HH_score_df['HH_members_of_developed_HHs'] = np.where(HH_score_df['Is_the_HH_multidimensionally_developed'] == 1, HH_score_df['Sum of HH_S'], 0)


    


Tribe_cum_score_df = pd.DataFrame({
    'Tribe_N' : unique_tribes,
})

Total_Sum_of_HH_S=[0]*len(unique_tribes)
Total_H_Is_the_HH_developed=[0]*len(unique_tribes)
Total_E_Is_the_HH_developed=[0]*len(unique_tribes)
Total_S_Is_the_HH_developed=[0]*len(unique_tribes)
Total_C_Is_the_HH_developed=[0]*len(unique_tribes)
Total_G_Is_the_HH_developed=[0]*len(unique_tribes)
Total_Is_the_HH_mulltidimensionally_developed=[0]*len(unique_tribes)
Total_H_HH_members_of_developed_HHs=[0]*len(unique_tribes)
Total_E_HH_members_of_developed_HHs=[0]*len(unique_tribes)
Total_S_HH_members_of_developed_HHs=[0]*len(unique_tribes)
Total_C_HH_members_of_developed_HHs=[0]*len(unique_tribes)
Total_G_HH_members_of_developed_HHs=[0]*len(unique_tribes)
Total_HH_members_of_developed_HHs=[0]*len(unique_tribes)


for i in range(len(unique_tribes)):
    for j in range(len(HH_tribe_list)):
        if HH_tribe_list[j] == unique_tribes[i]:
            Total_Sum_of_HH_S[i] += HH_size_list[j]
            Total_H_Is_the_HH_developed[i] += HH_score_df['H_Is_the_HH_developed'][j]
            Total_E_Is_the_HH_developed[i] += HH_score_df['E_Is_the_HH_developed'][j]
            Total_S_Is_the_HH_developed[i] += HH_score_df['S_Is_the_HH_developed'][j]
            Total_C_Is_the_HH_developed[i] += HH_score_df['C_Is_the_HH_developed'][j]
            Total_G_Is_the_HH_developed[i] += HH_score_df['G_Is_the_HH_developed'][j]
            Total_Is_the_HH_mulltidimensionally_developed[i] += HH_score_df['Is_the_HH_multidimensionally_developed'][j]
            Total_H_HH_members_of_developed_HHs[i] += HH_score_df['H_HH_members_of_developed_HHs'][j]
            Total_E_HH_members_of_developed_HHs[i] += HH_score_df['E_HH_members_of_developed_HHs'][j]
            Total_S_HH_members_of_developed_HHs[i] += HH_score_df['S_HH_members_of_developed_HHs'][j]
            Total_C_HH_members_of_developed_HHs[i] += HH_score_df['C_HH_members_of_developed_HHs'][j]
            Total_G_HH_members_of_developed_HHs[i] += HH_score_df['G_HH_members_of_developed_HHs'][j]
            Total_HH_members_of_developed_HHs[i] += HH_score_df['HH_members_of_developed_HHs'][j]

Tribe_cum_score_df['Total_Sum_of_HH_S'] = Total_Sum_of_HH_S
Tribe_cum_score_df['Total_H_Is_the_HH_developed'] = Total_H_Is_the_HH_developed
Tribe_cum_score_df['Total_E_Is_the_HH_developed'] = Total_E_Is_the_HH_developed
Tribe_cum_score_df['Total_S_Is_the_HH_developed'] = Total_S_Is_the_HH_developed
Tribe_cum_score_df['Total_C_Is_the_HH_developed'] = Total_C_Is_the_HH_developed
Tribe_cum_score_df['Total_G_Is_the_HH_developed'] = Total_G_Is_the_HH_developed
Tribe_cum_score_df['Total_Is_the_HH_mulltidimensionally_developed'] = Total_Is_the_HH_mulltidimensionally_developed
Tribe_cum_score_df['Total_H_HH_members_of_developed_HHs'] = Total_H_HH_members_of_developed_HHs
Tribe_cum_score_df['Total_E_HH_members_of_developed_HHs'] = Total_E_HH_members_of_developed_HHs
Tribe_cum_score_df['Total_S_HH_members_of_developed_HHs'] = Total_S_HH_members_of_developed_HHs
Tribe_cum_score_df['Total_C_HH_members_of_developed_HHs'] = Total_C_HH_members_of_developed_HHs
Tribe_cum_score_df['Total_G_HH_members_of_developed_HHs'] = Total_G_HH_members_of_developed_HHs
Tribe_cum_score_df['Total_HH_members_of_developed_HHs'] = Total_HH_members_of_developed_HHs




HH_score_df['H_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['E_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['S_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['C_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['G_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['H_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['E_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['S_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['C_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['G_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
HH_score_df['Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)



for i in range(len(unique_tribes)):
    total_sum_of_hh_s = Tribe_cum_score_df['Total_Sum_of_HH_S'][i]
    total_h_hh_members = Tribe_cum_score_df['Total_H_HH_members_of_developed_HHs'][i]
    total_e_hh_members = Tribe_cum_score_df['Total_E_HH_members_of_developed_HHs'][i]
    total_s_hh_members = Tribe_cum_score_df['Total_S_HH_members_of_developed_HHs'][i]
    total_c_hh_members = Tribe_cum_score_df['Total_C_HH_members_of_developed_HHs'][i]
    total_g_hh_members = Tribe_cum_score_df['Total_G_HH_members_of_developed_HHs'][i]
    total_hh_members = Tribe_cum_score_df['Total_HH_members_of_developed_HHs'][i]

    for j in range(len(HH_tribe_list)):
        if HH_tribe_list[j] == unique_tribes[i]:
            HH_score_df.loc[j,'H_Incidence_of_Tribal_development'] = round(float(HH_score_df['H_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            HH_score_df.loc[j,'E_Incidence_of_Tribal_development'] = round(float(HH_score_df['E_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            HH_score_df.loc[j,'S_Incidence_of_Tribal_development'] = round(float(HH_score_df['S_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            HH_score_df.loc[j,'C_Incidence_of_Tribal_development'] = round(float(HH_score_df['C_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            HH_score_df.loc[j,'G_Incidence_of_Tribal_development'] = round(float(HH_score_df['G_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            HH_score_df.loc[j,'Incidence_of_Tribal_development'] = round(float(HH_score_df['HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
            
            HH_score_df.loc[j,'H_Intensity_of_Tribal_development'] = round(float((HH_score_df['H_DS'][j] * HH_score_df['H_HH_members_of_developed_HHs'][j] * 5) / total_h_hh_members) if total_h_hh_members != 0 else 0, 5)
            HH_score_df.loc[j,'E_Intensity_of_Tribal_development'] = round(float((HH_score_df['E_DS'][j] * HH_score_df['E_HH_members_of_developed_HHs'][j] * 5) / total_e_hh_members) if total_e_hh_members != 0 else 0, 5)
            HH_score_df.loc[j,'S_Intensity_of_Tribal_development'] = round(float((HH_score_df['S_DS'][j] * HH_score_df['S_HH_members_of_developed_HHs'][j] * 5) / total_s_hh_members) if total_s_hh_members != 0 else 0, 5)
            HH_score_df.loc[j,'C_Intensity_of_Tribal_development'] = round(float((HH_score_df['C_DS'][j] * HH_score_df['C_HH_members_of_developed_HHs'][j] * 5) / total_c_hh_members) if total_c_hh_members != 0 else 0, 5)
            HH_score_df.loc[j,'G_Intensity_of_Tribal_development'] = round(float((HH_score_df['G_DS'][j] * HH_score_df['G_HH_members_of_developed_HHs'][j] * 5) / total_g_hh_members) if total_g_hh_members != 0 else 0, 5)
            HH_score_df.loc[j,'Intensity_of_Tribal_development'] = round(float((HH_score_df['HH_DS'][j] * HH_score_df['HH_members_of_developed_HHs'][j]) / total_hh_members) if total_hh_members != 0 else 0, 5)


Total_H_Incidence_of_Tribal_development=[0]*len(unique_tribes)
Total_E_Incidence_of_Tribal_development=[0]*len(unique_tribes)
Total_S_Incidence_of_Tribal_development=[0]*len(unique_tribes)
Total_C_Incidence_of_Tribal_development=[0]*len(unique_tribes)
Total_G_Incidence_of_Tribal_development=[0]*len(unique_tribes)
Total_Incidence_of_Tribal_development=[0]*len(unique_tribes)

Total_H_Intensity_of_Tribal_development=[0]*len(unique_tribes)
Total_E_Intensity_of_Tribal_development=[0]*len(unique_tribes)
Total_S_Intensity_of_Tribal_development=[0]*len(unique_tribes)
Total_C_Intensity_of_Tribal_development=[0]*len(unique_tribes)
Total_G_Intensity_of_Tribal_development=[0]*len(unique_tribes)
Total_Intensity_of_Tribal_development=[0]*len(unique_tribes)



for i in range(len(unique_tribes)):
    for j in range(len(HH_tribe_list)):
        if HH_tribe_list[j] == unique_tribes[i]:
            Total_H_Incidence_of_Tribal_development[i] += HH_score_df['H_Incidence_of_Tribal_development'][j]
            Total_E_Incidence_of_Tribal_development[i] += HH_score_df['E_Incidence_of_Tribal_development'][j]
            Total_S_Incidence_of_Tribal_development[i] += HH_score_df['S_Incidence_of_Tribal_development'][j]
            Total_C_Incidence_of_Tribal_development[i] += HH_score_df['C_Incidence_of_Tribal_development'][j]
            Total_G_Incidence_of_Tribal_development[i] += HH_score_df['G_Incidence_of_Tribal_development'][j]
            Total_Incidence_of_Tribal_development[i] += HH_score_df['Incidence_of_Tribal_development'][j]

            Total_H_Intensity_of_Tribal_development[i] += HH_score_df['H_Intensity_of_Tribal_development'][j]
            Total_E_Intensity_of_Tribal_development[i] += HH_score_df['E_Intensity_of_Tribal_development'][j]
            Total_S_Intensity_of_Tribal_development[i] += HH_score_df['S_Intensity_of_Tribal_development'][j]
            Total_C_Intensity_of_Tribal_development[i] += HH_score_df['C_Intensity_of_Tribal_development'][j]
            Total_G_Intensity_of_Tribal_development[i] += HH_score_df['G_Intensity_of_Tribal_development'][j]
            Total_Intensity_of_Tribal_development[i] += HH_score_df['Intensity_of_Tribal_development'][j]

    Total_H_Incidence_of_Tribal_development[i] = round(Total_H_Incidence_of_Tribal_development[i],3)
    Total_E_Incidence_of_Tribal_development[i] = round(Total_E_Incidence_of_Tribal_development[i],3)
    Total_S_Incidence_of_Tribal_development[i] = round(Total_S_Incidence_of_Tribal_development[i],3)
    Total_C_Incidence_of_Tribal_development[i] = round(Total_C_Incidence_of_Tribal_development[i],3)
    Total_G_Incidence_of_Tribal_development[i] = round(Total_G_Incidence_of_Tribal_development[i],3)
    Total_Incidence_of_Tribal_development[i] = round(Total_Incidence_of_Tribal_development[i],3)
    Total_H_Intensity_of_Tribal_development[i] = round(Total_H_Intensity_of_Tribal_development[i],3)
    Total_E_Intensity_of_Tribal_development[i] = round(Total_E_Intensity_of_Tribal_development[i],3)
    Total_S_Intensity_of_Tribal_development[i] = round(Total_S_Intensity_of_Tribal_development[i],3)
    Total_C_Intensity_of_Tribal_development[i] = round(Total_C_Intensity_of_Tribal_development[i],3)
    Total_G_Intensity_of_Tribal_development[i] = round(Total_G_Intensity_of_Tribal_development[i],3)
    Total_Intensity_of_Tribal_development[i] = round(Total_Intensity_of_Tribal_development[i],3)

Tribe_cum_score_df['Total_H_Incidence_of_Tribal_development'] = Total_H_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_E_Incidence_of_Tribal_development'] = Total_E_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_S_Incidence_of_Tribal_development'] = Total_S_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_C_Incidence_of_Tribal_development'] = Total_C_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_G_Incidence_of_Tribal_development'] = Total_G_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_Incidence_of_Tribal_development'] = Total_Incidence_of_Tribal_development
Tribe_cum_score_df['Total_H_Intensity_of_Tribal_development'] = Total_H_Intensity_of_Tribal_development
Tribe_cum_score_df['Total_E_Intensity_of_Tribal_development'] = Total_E_Intensity_of_Tribal_development
Tribe_cum_score_df['Total_S_Intensity_of_Tribal_development'] = Total_S_Intensity_of_Tribal_development
Tribe_cum_score_df['Total_C_Intensity_of_Tribal_development'] = Total_C_Intensity_of_Tribal_development
Tribe_cum_score_df['Total_G_Intensity_of_Tribal_development'] = Total_G_Intensity_of_Tribal_development
Tribe_cum_score_df['Total_Intensity_of_Tribal_development'] = Total_Intensity_of_Tribal_development

Tribe_cum_score_df['H_DI'] = round((Tribe_cum_score_df['Total_H_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_H_Intensity_of_Tribal_development']),2)
Tribe_cum_score_df['E_DI'] = round((Tribe_cum_score_df['Total_E_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_E_Intensity_of_Tribal_development']),2)
Tribe_cum_score_df['S_DI'] = round((Tribe_cum_score_df['Total_S_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_S_Intensity_of_Tribal_development']),2)
Tribe_cum_score_df['C_DI'] = round((Tribe_cum_score_df['Total_C_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_C_Intensity_of_Tribal_development']),2)
Tribe_cum_score_df['G_DI'] = round((Tribe_cum_score_df['Total_G_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_G_Intensity_of_Tribal_development']),2)
Tribe_cum_score_df['TDI'] = round((Tribe_cum_score_df['Total_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_Intensity_of_Tribal_development']),2)




HH_score_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/HH_scores.xlsx', index=False)
print("Result Excel file saved successfully.")

Tribe_cum_score_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/Tribe_cum_score_df.xlsx', index=False)
print("Result Excel file saved successfully.")

import math

censored_uncensored_df = pd.DataFrame({
    'Tribe_N' : unique_tribes,
    'Sum_of_HH_S' : Total_Sum_of_HH_S,
})


UNC_CD_score=[0]*len(unique_tribes)
UNC_IM_score=[0]*len(unique_tribes)
UNC_MC_score=[0]*len(unique_tribes)
UNC_CM_score=[0]*len(unique_tribes)
UNC_FS_score=[0]*len(unique_tribes)
UNC_LE_score=[0]*len(unique_tribes)
UNC_DRO_score=[0]*len(unique_tribes)
UNC_IC_score=[0]*len(unique_tribes)
UNC_OW_score=[0]*len(unique_tribes)
UNC_SANI_score=[0]*len(unique_tribes)
UNC_FUEL_score=[0]*len(unique_tribes)
UNC_DRWA_score=[0]*len(unique_tribes)
UNC_ELECTR_score=[0]*len(unique_tribes)
UNC_ASS_score=[0]*len(unique_tribes)
UNC_LAN_score=[0]*len(unique_tribes)
UNC_ARTS_score=[0]*len(unique_tribes)
UNC_EV_score=[0]*len(unique_tribes)
UNC_MEET_score=[0]*len(unique_tribes)

CEN_CD_score=[0]*len(unique_tribes)
CEN_IM_score=[0]*len(unique_tribes)
CEN_MC_score=[0]*len(unique_tribes)
CEN_CM_score=[0]*len(unique_tribes)
CEN_FS_score=[0]*len(unique_tribes)
CEN_LE_score=[0]*len(unique_tribes)
CEN_DRO_score=[0]*len(unique_tribes)
CEN_IC_score=[0]*len(unique_tribes)
CEN_OW_score=[0]*len(unique_tribes)
CEN_SANI_score=[0]*len(unique_tribes)
CEN_FUEL_score=[0]*len(unique_tribes)
CEN_DRWA_score=[0]*len(unique_tribes)
CEN_ELECTR_score=[0]*len(unique_tribes)
CEN_ASS_score=[0]*len(unique_tribes)
CEN_LAN_score=[0]*len(unique_tribes)
CEN_ARTS_score=[0]*len(unique_tribes)
CEN_EV_score=[0]*len(unique_tribes)
CEN_MEET_score=[0]*len(unique_tribes)

HH_DS = HH_score_df['HH_DS']

for i in range(len(unique_tribes)):

    Sum_of_HH_S = censored_uncensored_df['Sum_of_HH_S'][i]

    if Sum_of_HH_S > 0 :
        for j in range(len(HH_tribe_list)):
            if HH_tribe_list[j] == unique_tribes[i]:
            
                    
                HH_size = HH_score_df['Sum of HH_S'][j]


                CD_score_value = (HH_score_df['HH_Score_H_CD'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_CD'][j]) or HH_score_df['HH_Score_H_CD'][j] is None) else 0
                IM_score_value = (HH_score_df['HH_Score_H_IMM'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_IMM'][j]) or HH_score_df['HH_Score_H_IMM'][j] is None) else 0
                MC_score_value = (HH_score_df['HH_Score_H_MC'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_MC'][j]) or HH_score_df['HH_Score_H_MC'][j] is None) else 0
                CM_score_value = (HH_score_df['HH_Score_H_U5CM'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_U5CM'][j]) or HH_score_df['HH_Score_H_U5CM'][j] is None) else 0
                FS_score_value = (HH_score_df['HH_Score_H_FS'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_FS'][j]) or HH_score_df['HH_Score_H_FS'][j] is None) else 0
                LE_score_value = (HH_score_df['HH_Score_E_LE'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_E_LE'][j]) or HH_score_df['HH_Score_E_LE'][j] is None) else 0
                DRO_score_value = (HH_score_df['HH_Score_E_DRO'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_E_DRO'][j]) or HH_score_df['HH_Score_E_DRO'][j] is None) else 0
                IC_score_value = (HH_score_df['HH_Score_S_IC'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_IC'][j]) or HH_score_df['HH_Score_S_IC'][j] is None) else 0
                OW_score_value = (HH_score_df['HH_Score_S_OWN'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_OWN'][j]) or HH_score_df['HH_Score_S_OWN'][j] is None) else 0
                SANI_score_value = (HH_score_df['HH_Score_S_SANI'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_SANI'][j]) or HH_score_df['HH_Score_S_SANI'][j] is None) else 0
                FUEL_score_value = (HH_score_df['HH_Score_S_Fuel'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_Fuel'][j]) or HH_score_df['HH_Score_S_Fuel'][j] is None) else 0
                DRWA_score_value = (HH_score_df['HH_Score_S_SoDrWa'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_SoDrWa'][j]) or HH_score_df['HH_Score_S_SoDrWa'][j] is None) else 0
                ELECTR_score_value = (HH_score_df['HH_Score_S_ELECTR'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_ELECTR'][j]) or HH_score_df['HH_Score_S_ELECTR'][j] is None) else 0
                ASS_score_value = (HH_score_df['HH_Score_S_ASS'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_ASS'][j]) or HH_score_df['HH_Score_S_ASS'][j] is None) else 0
                LAN_score_value = (HH_score_df['HH_Score_C_L'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_C_L'][j]) or HH_score_df['HH_Score_C_L'][j] is None) else 0
                ARTS_score_value = (HH_score_df['HH_Score_C_Arts'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_C_Arts'][j]) or HH_score_df['HH_Score_C_Arts'][j] is None) else 0
                EV_score_value = (HH_score_df['HH_Score_G_EV'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_G_EV'][j]) or HH_score_df['HH_Score_G_EV'][j] is None) else 0
                MEET_score_value = (HH_score_df['HH_Score_G_meeting'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_G_meeting'][j]) or HH_score_df['HH_Score_G_meeting'][j] is None) else 0

                UNC_CD_score[i] += CD_score_value
                UNC_IM_score[i] += IM_score_value
                UNC_MC_score[i] += MC_score_value
                UNC_CM_score[i] += CM_score_value
                UNC_FS_score[i] += FS_score_value
                UNC_LE_score[i] += LE_score_value
                UNC_DRO_score[i] += DRO_score_value
                UNC_IC_score[i] += IC_score_value
                UNC_OW_score[i] += OW_score_value
                UNC_SANI_score[i] += SANI_score_value
                UNC_FUEL_score[i] += FUEL_score_value
                UNC_DRWA_score[i] += DRWA_score_value
                UNC_ELECTR_score[i] += ELECTR_score_value
                UNC_ASS_score[i] += ASS_score_value
                UNC_LAN_score[i] += LAN_score_value
                UNC_ARTS_score[i] += ARTS_score_value
                UNC_EV_score[i] += EV_score_value
                UNC_MEET_score[i] += MEET_score_value




                if HH_DS[j] > 0.33:
                    CEN_CD_score[i] +=     CD_score_value
                    CEN_IM_score[i] +=     IM_score_value
                    CEN_MC_score[i] +=     MC_score_value
                    CEN_CM_score[i] +=     CM_score_value
                    CEN_FS_score[i] +=     FS_score_value
                    CEN_LE_score[i] +=     LE_score_value
                    CEN_DRO_score[i] +=    DRO_score_value
                    CEN_IC_score[i] +=     IC_score_value
                    CEN_OW_score[i] +=     OW_score_value
                    CEN_SANI_score[i] +=   SANI_score_value
                    CEN_FUEL_score[i] +=   FUEL_score_value
                    CEN_DRWA_score[i] +=   DRWA_score_value
                    CEN_ELECTR_score[i] += ELECTR_score_value
                    CEN_ASS_score[i] +=    ASS_score_value
                    CEN_LAN_score[i] +=    LAN_score_value
                    CEN_ARTS_score[i] +=   ARTS_score_value 
                    CEN_EV_score[i] +=     EV_score_value
                    CEN_MEET_score[i] +=   MEET_score_value


        UNC_CD_score[i]= round(UNC_CD_score[i],2)*100
        UNC_IM_score[i]= round(UNC_IM_score[i],2)*100
        UNC_MC_score[i]= round(UNC_MC_score[i],2)*100
        UNC_CM_score[i]= round(UNC_CM_score[i],2)*100
        UNC_FS_score[i]= round(UNC_FS_score[i],2)*100
        UNC_LE_score[i]= round(UNC_LE_score[i],2)*100
        UNC_DRO_score[i]= round(UNC_DRO_score[i],2)*100
        UNC_IC_score[i]= round(UNC_IC_score[i],2)*100
        UNC_OW_score[i]= round(UNC_OW_score[i],2)*100
        UNC_SANI_score[i]= round(UNC_SANI_score[i],2)*100
        UNC_FUEL_score[i]= round(UNC_FUEL_score[i],2)*100
        UNC_DRWA_score[i]= round(UNC_DRWA_score[i],2)*100
        UNC_ELECTR_score[i]= round(UNC_ELECTR_score[i],2)*100
        UNC_ASS_score[i]= round(UNC_ASS_score[i],2)*100
        UNC_LAN_score[i]= round(UNC_LAN_score[i],2)*100
        UNC_ARTS_score[i]= round(UNC_ARTS_score[i],2)*100
        UNC_EV_score[i]= round(UNC_EV_score[i],2)*100
        UNC_MEET_score[i]= round(UNC_MEET_score[i],2)*100
        CEN_CD_score[i]= round(CEN_CD_score[i],2)*100
        CEN_IM_score[i]= round(CEN_IM_score[i],2)*100
        CEN_MC_score[i]= round(CEN_MC_score[i],2)*100
        CEN_CM_score[i]= round(CEN_CM_score[i],2)*100
        CEN_FS_score[i]= round(CEN_FS_score[i],2)*100
        CEN_LE_score[i]= round(CEN_LE_score[i],2)*100
        CEN_DRO_score[i]= round(CEN_DRO_score[i],2)*100
        CEN_IC_score[i]= round(CEN_IC_score[i],2)*100
        CEN_OW_score[i]= round(CEN_OW_score[i],2)*100
        CEN_SANI_score[i]= round(CEN_SANI_score[i],2)*100
        CEN_FUEL_score[i]= round(CEN_FUEL_score[i],2)*100
        CEN_DRWA_score[i]= round(CEN_DRWA_score[i],2)*100
        CEN_ELECTR_score[i]= round(CEN_ELECTR_score[i],2)*100
        CEN_ASS_score[i]= round(CEN_ASS_score[i],2)*100
        CEN_LAN_score[i]= round(CEN_LAN_score[i],2)*100
        CEN_ARTS_score[i]= round(CEN_ARTS_score[i],2)*100
        CEN_EV_score[i]= round(CEN_EV_score[i],2)*100
        CEN_MEET_score[i]= round(CEN_MEET_score[i],2)*100
        

        
    censored_uncensored_df['UNC_CD_score'] = UNC_CD_score
    censored_uncensored_df['UNC_IM_score'] = UNC_IM_score
    censored_uncensored_df['UNC_MC_score'] = UNC_MC_score
    censored_uncensored_df['UNC_CM_score'] = UNC_CM_score
    censored_uncensored_df['UNC_FS_score'] = UNC_FS_score
    censored_uncensored_df['UNC_LE_score'] = UNC_LE_score
    censored_uncensored_df['UNC_DRO_score'] = UNC_DRO_score
    censored_uncensored_df['UNC_IC_score'] = UNC_IC_score
    censored_uncensored_df['UNC_OW_score'] = UNC_OW_score
    censored_uncensored_df['UNC_SANI_score'] = UNC_SANI_score
    censored_uncensored_df['UNC_FUEL_score'] = UNC_FUEL_score
    censored_uncensored_df['UNC_DRWA_score'] = UNC_DRWA_score
    censored_uncensored_df['UNC_ELECTR_score'] = UNC_ELECTR_score
    censored_uncensored_df['UNC_ASS_score'] = UNC_ASS_score
    censored_uncensored_df['UNC_LAN_score'] = UNC_LAN_score
    censored_uncensored_df['UNC_ARTS_score'] = UNC_ARTS_score
    censored_uncensored_df['UNC_EV_score'] = UNC_EV_score
    censored_uncensored_df['UNC_MEET_score'] = UNC_MEET_score
    censored_uncensored_df['CEN_CD_score'] = CEN_CD_score
    censored_uncensored_df['CEN_IM_score'] = CEN_IM_score
    censored_uncensored_df['CEN_MC_score'] = CEN_MC_score
    censored_uncensored_df['CEN_CM_score'] = CEN_CM_score
    censored_uncensored_df['CEN_FS_score'] = CEN_FS_score
    censored_uncensored_df['CEN_LE_score'] = CEN_LE_score
    censored_uncensored_df['CEN_DRO_score'] = CEN_DRO_score
    censored_uncensored_df['CEN_IC_score'] = CEN_IC_score
    censored_uncensored_df['CEN_OW_score'] = CEN_OW_score
    censored_uncensored_df['CEN_SANI_score'] = CEN_SANI_score
    censored_uncensored_df['CEN_FUEL_score'] = CEN_FUEL_score
    censored_uncensored_df['CEN_DRWA_score'] = CEN_DRWA_score
    censored_uncensored_df['CEN_ELECTR_score'] = CEN_ELECTR_score
    censored_uncensored_df['CEN_ASS_score'] = CEN_ASS_score
    censored_uncensored_df['CEN_LAN_score'] = CEN_LAN_score
    censored_uncensored_df['CEN_ARTS_score'] = CEN_ARTS_score
    censored_uncensored_df['CEN_EV_score'] = CEN_EV_score
    censored_uncensored_df['CEN_MEET_score'] = CEN_MEET_score
        
                
censored_uncensored_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/censored_uncensored_df.xlsx', index=False)
print("Result Excel file saved successfully.")

        