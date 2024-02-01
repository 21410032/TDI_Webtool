import pandas as pd
import numpy as np

#create dataframe of base_data
base_data_df = pd.read_excel('C:/Users/tinky/OneDrive/Documents/ho.xlsx')

print(base_data_df)

print(base_data_df.columns)


base_data_df['Eligibility_CD'] = np.where(base_data_df['chronic_disease'] == 'लागू नहीं', 0, 1)

            ##print('Eligibility_CD')
            
base_data_df['CD_Cum_Score'] = np.where(base_data_df['chronic_disease'] == "हां", 0, 1)

            ##print("CD_Cum_Score")
            ##print(base_data_df['Age'])
            #print(base_data_df['Age'].dtype)
base_data_df['Age'] = pd.to_numeric(base_data_df['Age'], errors='coerce')

base_data_df['Eligibility_IMM'] = np.where(base_data_df['Age'] < 1, 0, 1)
#print(base_data_df['Eligibility_IMM'])

#print("Eligibility_IMM")

conditions_IMM_Cum_Score = [
    (base_data_df['Age'] < 16),
    (base_data_df['basic_vaccination'] == 'पूरी तरह ')
]
values_IMM_Cum_Score = ['NA', 1]
base_data_df['IMM_Cum_Score'] = np.select(conditions_IMM_Cum_Score, values_IMM_Cum_Score, default=0)
#print("IMM_Cum_Score")

base_data_df['Eligibility_IND'] = np.where(base_data_df['Institutional_delivery'] == 'लागू नहीं', 0, 1)
#print("Eligibility_IND")


conditions_IND_Cum_Score = [
    (base_data_df['Institutional_delivery'] == 'स्वास्थ्य केंद्र '),
    (base_data_df['Eligibility_IND'] == 0)
]
values_IND_Cum_Score = [1, 'NA']
base_data_df['IND_Cum_Score'] = np.select(conditions_IND_Cum_Score, values_IND_Cum_Score, default=0)
#print("IND_Cum_Score")


conditions_Eligibility_ANC = [
    (base_data_df['ANC'] == 'लागू नहीं') | (16 > base_data_df['Age']) | (base_data_df['Age'] > 45) | (base_data_df['Gender'] != 'महिला')
]
values_Eligibility_ANC = [0]
base_data_df['Eligibility_ANC'] = np.select(conditions_Eligibility_ANC, values_Eligibility_ANC, default=1)
#print("Eligibility_ANC")

conditions_ANC_Cum_Score = [
    (base_data_df['ANC'].isin(['हाँ, सभी तिमाही ', 'हाँ, 1 तिमाही ', 'हाँ, 2 तिमाही '])),
    (base_data_df['Eligibility_ANC'] == 0)
]
values_ANC_Cum_Score = [1, 'NA']
base_data_df['ANC_Cum_Score'] = np.select(conditions_ANC_Cum_Score, values_ANC_Cum_Score, default=0)
#print("ANC_Cum_Score")

condition_U5CM_Cum_Score = (base_data_df['Infant_mortality'] == 'हां')
base_data_df['U5CM_Cum_Score'] = np.where(condition_U5CM_Cum_Score, 0, 1)
#print("U5CM_Cum_Score")
condition_2sq_Cum_Score = (base_data_df['2sqmeals'] == 'हाँ, पर्याप्त')
base_data_df['2sq_Cum_Score'] = np.where(condition_2sq_Cum_Score, 1, 0)
#print("2sq_Cum_Score")
keywords_Energy = ['चावल', 'रोटी', 'ज्वार', 'आलू', 'बाजरा', 'लिट्टी']
condition_Energy = base_data_df['food_diversity'].apply(lambda x: any(keyword in x for keyword in keywords_Energy))
base_data_df['Energy'] = np.where(condition_Energy, 1, 0)
#print("Energy")
proteins_condition = (
    base_data_df['food_diversity'].str.contains('दाल|मछली|मांस|खुकड़ी|सत्तू', regex=True, na=False)
)
base_data_df['Proteins'] = np.where(proteins_condition, 1, 0)
#print("Proteins")
condition_Vitamins = base_data_df['food_diversity'].apply(lambda x: 1 if 'साग' in x or 'अन्य' in x else 0)
base_data_df['Vitamins'] = condition_Vitamins
#print("Vitamins")
condition_FD_Cum_Score = (np.sum(base_data_df[['Energy', 'Proteins', 'Vitamins']], axis=1) == 3)
base_data_df['FD_Cum_Score'] = np.where(condition_FD_Cum_Score, 1, 0)
#print("FD_Cum_Score")
condition_eligibility_LE = (base_data_df['Age'] >= 10)
base_data_df['Eligibility LE'] = np.where(condition_eligibility_LE, 1, 0)
#print("Eligibility LE")
condition_cum_score_LE = base_data_df['Ed'].isin([
    '6th कक्षा पूरा किया हुआ', '7th कक्षा पूरा किया हुआ', '8th कक्षा पूरा किया हुआ',
    '9th कक्षा पूरा किया हुआ', '10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ',
    '12th कक्षा पूरा किया हुआ', 'डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ',
    'पोस्ट ग्रेजुएशन पूरा किया हुआ'
])
base_data_df['cum_score_LE'] = np.where(condition_cum_score_LE | (base_data_df['Eligibility LE'] == 0), 1, 0)
#print("cum_score_LE")
condition_Eligibility_DRO = np.logical_or(base_data_df['Age'] < 15, base_data_df['Age'] > 64)
base_data_df['Eligibility DRO'] = np.where(condition_Eligibility_DRO, 0, 1)
#print("Eligibility DRO")

condition_cum_score_DRO = base_data_df['Ed'].isin(['10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ', '12th कक्षा पूरा किया हुआ','डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ', 'पोस्ट ग्रेजुएशन पूरा किया हुआ'])
base_data_df['cum_score_DRO'] = np.where(condition_cum_score_DRO | (base_data_df['Eligibility DRO'] == 0), 0, 'NA')
#print("cum_score_DRO")

condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['Inst_Credit'].str.contains('आधार कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('बैंक खाता')) &
    (base_data_df['Inst_Credit'].str.contains('आयुष्मान कार्ड')) &
    (base_data_df['Inst_Credit'].str.contains('जच्चा बच्चा पात्रता'))
)
base_data_df['Aadhaar_bank_account_MCP_Aayushman'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("Aadhaar_bank_account_MCP_Aayushman")
condition_Ration = (base_data_df['ration_c_color'] == 'लागू नहीं')
base_data_df['Ration'] = np.where(condition_Ration, 0, 1)
#print("Ration")

condition_job_labour_kisan_credit = base_data_df['Inst_Credit'].str.contains('जॉब कार्ड|श्रम कार्ड|किसान क्रेडिट कार्ड', case=False, na=False)
base_data_df['Job/ Labour/ Kisan credit'] = np.where(condition_job_labour_kisan_credit, 1, 0)
#print("ob/ Labour/ Kisan credit")

condition_CUM_SCORE_IC = ((base_data_df['Aadhaar_bank_account_MCP_Aayushman'] + base_data_df['Ration'] + base_data_df['Job/ Labour/ Kisan credit']) >= 1)

base_data_df['CUM_SCORE_IC'] = np.where(condition_CUM_SCORE_IC, 1, 0)
#print("CUM_SCORE_IC")

condition_CUM_SCORE_OWN = (base_data_df['agricultureland'] == 'हां') | (base_data_df['home_ownership'] == 'हां')
base_data_df['CUM_SCORE_OWN'] = np.where(condition_CUM_SCORE_OWN, 1, 0)
#print("CUM_SCORE_OWN")

condition_CUM_SCORE_SANI = (base_data_df['defecation'].str.contains('घर के भीतर') | base_data_df['bath'].str.contains('घर के भीतर'))
base_data_df['CUM_SCORE_SANI'] = np.where(condition_CUM_SCORE_SANI, 1, 0)
#print("CUM_SCORE_SANI")

condition_cum_score_Fuel = base_data_df['source_fuel'].str.contains("गैस")
base_data_df['cum_score_Fuel'] = np.where(condition_cum_score_Fuel, 1, 0)
#print("cum_score_Fuel")

condition_cum_score_SoDrWa = base_data_df['source_drinking_water'].str.contains("घर का नल")
base_data_df['cum_score_SoDrWa'] = np.where(condition_cum_score_SoDrWa, 1, 0)
#print("cum_score_SoDrWa")

condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['assets'].str.contains('इंटरनेट का उपयोग')) |
    (base_data_df['assets'].str.contains('सामान्य फोन')) |
    (base_data_df['assets'].str.contains('टेलीविजन')) |
    (base_data_df['assets'].str.contains('कंप्यूटर सिस्टम/लैपटॉप/टैबलेट'))|
    (base_data_df['smart_phone'].str.contains('हां'))
)
base_data_df['ASS_INFO'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("ASS_INFO")

condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['assets'].str.contains('बिजली का पंखा')) |
    (base_data_df['assets'].str.contains('गैस - चूल्हा')) |
    (base_data_df['assets'].str.contains('हल')) |
    (base_data_df['assets'].str.contains('मिक्सी'))|
    (base_data_df['assets'].str.contains('सिचाई के लिए पम्पसेट'))|
    (base_data_df['assets'].str.contains('प्रेशर कुकर'))|
    (base_data_df['assets'].str.contains('तालाब'))
)
base_data_df['ASS_LIVE'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("ASS_LIVE")

condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['assets'].str.contains('गाड़ी')) |
    (base_data_df['assets'].str.contains('साइकिल')) |
    (base_data_df['assets'].str.contains('दो पहिया')) |
    (base_data_df['assets'].str.contains('रिक्शा'))|
    (base_data_df['assets'].str.contains('ट्रैक्टर'))
)
base_data_df['ASS_TRANS'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("ASS_TRANS")

condition_cum_score_Fuel = ((base_data_df['ASS_TRANS'] + base_data_df['ASS_LIVE'] + base_data_df['ASS_INFO'])) == 3
base_data_df['ASS'] = np.where(condition_cum_score_Fuel, 1, 0)
#print("ASS")
#print(base_data_df['no_hen_cock'])
#print(base_data_df['no_cows'])
#print( base_data_df['no_buffaloes'])
#print(base_data_df['no_oxan'])
#print(base_data_df['no_pigs'])
#print( base_data_df['no_ducks'])
#print(base_data_df['no_swan'])

columns_to_handle = ['no_hen_cock', 'no_goats', 'no_cows', 'no_buffaloes', 'no_oxan', 'no_pigs', 'no_ducks', 'no_swan']

# Iterate through each column and replace string values and NaN with 0
for column in columns_to_handle:
        base_data_df[column] = pd.to_numeric(base_data_df[column], errors='coerce').fillna(0).astype(int)

#print(base_data_df['no_hen_cock'])
#print(base_data_df['no_cows'])
#print( base_data_df['no_buffaloes'])
#print(base_data_df['no_oxan'])
#print(base_data_df['no_pigs'])
#print( base_data_df['no_ducks'])
#print(base_data_df['no_swan'])
condition_cum_score_Fuel = (
(base_data_df['no_hen_cock'] + base_data_df['no_goats'] + base_data_df['no_cows'] + base_data_df['no_buffaloes'] + base_data_df['no_oxan'] + base_data_df['no_pigs'] + base_data_df['no_ducks'] + base_data_df['no_swan']) > 0 | (base_data_df['Pond_Fish'] == 'हां'))


base_data_df['ANI'] = np.where(condition_cum_score_Fuel, 1, 0)
#print("ANI")



condition_cum_score_Fuel = (base_data_df['ASS'] + base_data_df['ASS']== 2)
base_data_df['CUM_SCORE_ASS'] = np.where(condition_cum_score_Fuel, 1, 0)
#print("CUM_SCORE_ASS")

condition_Aadhaar_bank_account_MCP_Aayushman = (
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
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("cum_score_L")

condition_Ration = (base_data_df['traditional_song'] == "हां")
base_data_df['cum_score_So'] = np.where(condition_Ration, 1, 0)
#print("cum_score_So")

condition_Ration = (
    (base_data_df['traditional_instrument'] == "हां") |
    (base_data_df['Traditional_Instrument'] != "कुछ नहीं")
)

base_data_df['cum_score_MuI'] = np.where(condition_Ration, 1, 0)
#print("cum_score_MuI")


condition_Ration = (base_data_df['traditional_dance'] == "हां")
base_data_df['cum_score_Da'] = np.where(condition_Ration, 1, 0)
#print("cum_score_Da")

condition_cum_score_Fuel = ((base_data_df['cum_score_Da'] + base_data_df['cum_score_MuI'] + base_data_df['cum_score_So'])) > 0
base_data_df['cum_score_Arts'] = np.where(condition_cum_score_Fuel, 1, 0)
#print("cum_score_Arts")

condition_Ration = (base_data_df['Age'] >= 18)
base_data_df['Eligibility_voter'] = np.where(condition_Ration, 1, 0)
#print("Eligibility_voter")

base_data_df['voter'] = pd.to_numeric(base_data_df['voter'], errors='coerce').fillna(0)

condition_Ration = (base_data_df['Eligibility_voter'] == 0)
condition_voter = (base_data_df['voter'] > 0)

#print("Before updating cum_score_EV")

base_data_df['cum_score_EV'] = 0  # Initialize the column with 0
base_data_df.loc[condition_Ration, 'cum_score_EV'] = 'NA'
base_data_df.loc[condition_voter & ~condition_Ration, 'cum_score_EV'] = 1

#print("After updating cum_score_EV")
#print("cum_score_EV:", base_data_df['cum_score_EV'])

# Check if the flow reaches this point
#print("Reached the end of the code block")




condition_Aadhaar_bank_account_MCP_Aayushman = (
    (base_data_df['SHG'].str.contains("हां")) |
    (base_data_df['traditional_meeting'].str.contains("हां")) |
    (base_data_df['gram_sabha_meeting'].str.contains("हां")) |
    (base_data_df['Panchayat_meetings'].str.contains("हां"))
    
)
base_data_df['Cum_s core_meetings'] = np.where(
    condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
)
#print("core_meetings")

df2 = base_data_df[['__fid__']].values.tolist()
#print(df2)

unique_list = []

def unique(list1):

# initialize a null list

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
unique(df2)
#print(unique_list)
print(base_data_df['CD_Cum_Score'].size)
score = [0] * len(unique_list)

def calScore(list1,list2,score):
    for i in range(len(unique_list)):
        for j in range(len(list1)):
            if unique_list[i] == list1[j]:
                if pd.isna(list2[j]) or list2[j] == 'NA':
                    score[i] = 0
                    break  # Break out of the inner loop if NA is encountered
                score[i] += int(list2[j])

# Rest of your code remains unchanged


# Rest of your code remains unchanged


# Rest of your code remains unchanged


score_columns = {}

for column in ['Eligibility_CD', 'CD_Cum_Score', 'Eligibility_IMM','IMM_Cum_Score','Eligibility_IND', 'IND_Cum_Score', 'ANC_Cum_Score', 'U5CM_Cum_Score', '2sq_Cum_Score', 'FD_Cum_Score', 'cum_score_LE', 'cum_score_DRO', 'CUM_SCORE_IC', 'CUM_SCORE_OWN', 'CUM_SCORE_SANI', 'cum_score_Fuel', 'cum_score_SoDrWa', 'CUM_SCORE_ASS', 'ASS', 'ANI', 'Cum_s core_meetings', 'cum_score_L', 'cum_score_So', 'cum_score_MuI', 'cum_score_Da', 'cum_score_Arts', 'Eligibility_voter', 'cum_score_EV']:
    # Initialize a list to store cumulative scores
    score_column = [0] * len(unique_list)

    # Calculate the cumulative score
    calScore(df2, base_data_df[column], score_column)

    # Add the cumulative score to the dictionary
    score_columns[f'Cum_Score_{column}'] = score_column

# Combine the cumulative scores into a DataFrame
result_df = pd.DataFrame({
    '__fid__': unique_list,
    **score_columns
})

    # Add the cumulative score to the DataFrame
    # base_data_df[f'Cum_Score_{column}'] = score_column

# Save the DataFrame to a new Excel file


# Save the DataFrame to a new Excel file
result_df.to_excel('C:/Users/tinky/OneDrive/Documents/households_excel.xlsx', index=False)
print("Result Excel file saved successfully.")



# try:
#     base_data_df.to_excel('C:/Users/tinky/OneDrive/Documents/households_excel.xlsx')
# ##print("Excel file saved successfully.")
# except Exception as e:
#     print(f"Error saving Excel file: {e}")