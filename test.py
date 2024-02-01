import pandas as pd
import numpy as np

#create dataframe of base_data
base_data_df = pd.read_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/base_data_excel.xlsx')

print(base_data_df)

print(base_data_df.columns)


#create required columns after applying conditions
base_data_df['Eligibility_CD'] = np.where(base_data_df['chronic_disease'] == 'लागू नहीं', 0, 1)
base_data_df['CD_Cum_Score'] = np.where(base_data_df['chronic_disease'] == "हां", 0, 1)
base_data_df['Eligibility_IMM'] = np.where(base_data_df['Age'] < 1, 0, 1)


conditions_IMM_Cum_Score = [
    (base_data_df['Age'] < 16),
    (base_data_df['basic_vaccination'] == 'पूरी तरह ')
]
values_IMM_Cum_Score = ['NA', 1]
base_data_df['IMM_Cum_Score'] = np.select(conditions_IMM_Cum_Score, values_IMM_Cum_Score, default=0)

base_data_df['Eligibility_IND'] = np.where(base_data_df['Institutional_delivery'] == 'लागू नहीं', 0, 1)


conditions_IND_Cum_Score = [
    (base_data_df['Institutional_delivery'] == 'स्वास्थ्य केंद्र '),
    (base_data_df['Eligibility_IND'] == 0)
]
values_IND_Cum_Score = [1, 'NA']
base_data_df['IND_Cum_Score'] = np.select(conditions_IND_Cum_Score, values_IND_Cum_Score, default=0)


conditions_Eligibility_ANC = [
    (base_data_df['ANC'] == 'लागू नहीं') | (16 > base_data_df['Age']) | (base_data_df['Age'] > 45) | (base_data_df['Gender'] != 'महिला')
]
values_Eligibility_ANC = [0]
base_data_df['Eligibility_ANC'] = np.select(conditions_Eligibility_ANC, values_Eligibility_ANC, default=1)


conditions_ANC_Cum_Score = [
    (base_data_df['ANC'].isin(['हाँ, सभी तिमाही ', 'हाँ, 1 तिमाही ', 'हाँ, 2 तिमाही '])),
    (base_data_df['Eligibility_ANC'] == 0)
]
values_ANC_Cum_Score = [1, 'NA']
base_data_df['ANC_Cum_Score'] = np.select(conditions_ANC_Cum_Score, values_ANC_Cum_Score, default=0)

condition_U5CM_Cum_Score = (base_data_df['Infant_mortality'] == 'हां')
base_data_df['U5CM_Cum_Score'] = np.where(condition_U5CM_Cum_Score, 0, 1)

condition_2sq_Cum_Score = (base_data_df['2sqmeals'] == 'हाँ, पर्याप्त')
base_data_df['2sq_Cum_Score'] = np.where(condition_2sq_Cum_Score, 1, 0)

keywords_Energy = ['चावल', 'रोटी', 'ज्वार', 'आलू', 'बाजरा', 'लिट्टी']
condition_Energy = base_data_df['food_diversity'].apply(lambda x: any(keyword in x for keyword in keywords_Energy))
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

condition_cum_score_LE = base_data_df['Ed'].isin([
    '6th कक्षा पूरा किया हुआ', '7th कक्षा पूरा किया हुआ', '8th कक्षा पूरा किया हुआ',
    '9th कक्षा पूरा किया हुआ', '10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ',
    '12th कक्षा पूरा किया हुआ', 'डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ',
    'पोस्ट ग्रेजुएशन पूरा किया हुआ'
])
base_data_df['cum_score_LE'] = np.where(condition_cum_score_LE | (base_data_df['Eligibility LE'] == 0), 1, 0)

condition_Eligibility_DRO = np.logical_or(base_data_df['Age'] < 15, base_data_df['Age'] > 64)
base_data_df['Eligibility DRO'] = np.where(condition_Eligibility_DRO, 0, 1)


condition_cum_score_DRO = base_data_df['Ed'].isin(['10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ', '12th कक्षा पूरा किया हुआ','डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ', 'पोस्ट ग्रेजुएशन पूरा किया हुआ'])
base_data_df['cum_score_DRO'] = np.where(condition_cum_score_DRO | (base_data_df['Eligibility DRO'] == 0), 0, 'NA')


condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['Inst_Credit'].str.contains('आधार कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('बैंक खाता')) &
    (base_data_df['Inst_Credit'].str.contains('आयुष्मान कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('जच्चा बच्चा पात्रता'))
)
base_data_df['Aadhaar_bank_account_MCP_Aayushman'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)

condition_Ration = (base_data_df['ration_c_color'] == 'लागू नहीं')
base_data_df['Ration'] = np.where(condition_Ration, 0, 1)

condition_job_labour_kisan_credit = base_data_df['Inst_Credit'].str.contains('जॉब कार्ड|श्रम कार्ड|किसान क्रेडिट कार्ड', case=False, na=False)
base_data_df['Job/ Labour/ Kisan credit'] = np.where(condition_job_labour_kisan_credit, 1, 0)

condition_CUM_SCORE_IC = (base_data_df[['Aadhaar, bank account, MCP, Aayushman', 'Ration', 'Job/ Labour/ Kisan credit']].sum(axis=1) >= 1)
base_data_df['CUM_SCORE_IC'] = np.where(condition_CUM_SCORE_IC, 1, 0)

condition_CUM_SCORE_OWN = (base_data_df['agricultureland'] == 'हां') | (base_data_df['home_ownership'] == 'हां')
base_data_df['CUM_SCORE_OWN'] = np.where(condition_CUM_SCORE_OWN, 1, 0)

condition_CUM_SCORE_SANI = (base_data_df['defecation'].str.contains('घर के भीतर') | base_data_df['bath'].str.contains('घर के भीतर'))
base_data_df['CUM_SCORE_SANI'] = np.where(condition_CUM_SCORE_SANI, 1, 0)

condition_cum_score_Fuel = base_data_df['AY2'].str.contains("गैस")
base_data_df['cum_score_Fuel'] = np.where(condition_cum_score_Fuel, 1, 0)

print(base_data_df)
