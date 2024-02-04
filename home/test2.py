import pandas as pd
import numpy as np


def perform_calculations(base_data_df, user, year):
   

    # base_data_df = pd.read_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/TRI_base_data.xlsx')

    # print(base_data_df)

    # print(base_data_df.columns)


    base_data_df['Eligibility_CD'] = np.where(base_data_df['chronic_disease'].str.strip() == 'लागू नहीं', 0, 1)

        
                
    base_data_df['CD_Cum_Score'] = np.where(base_data_df['chronic_disease'].str.strip() == "हां", 0, 1)

    base_data_df['Age'] = pd.to_numeric(base_data_df['Age'], errors='coerce')

    base_data_df['Eligibility_IMM'] = np.where(base_data_df['Age'] < 1, 0, 1)




    conditions_IMM_Cum_Score = [
        (base_data_df['Age'] < 16),
        (base_data_df['basic_vaccination'].str.strip() == 'पूरी तरह')
    ]
    values_IMM_Cum_Score = ['NA', 1]
    base_data_df['IMM_Cum_Score'] = np.select(conditions_IMM_Cum_Score, values_IMM_Cum_Score, default=0)


    base_data_df['Eligibility_IND'] = np.where(base_data_df['Institutional_delivery'].str.strip() == 'लागू नहीं', 0, 1)



    conditions_IND_Cum_Score = [
        (base_data_df['Institutional_delivery'].str.strip() == 'स्वास्थ्य केंद्र'),
        (base_data_df['Eligibility_IND'] == 0)
    ]
    values_IND_Cum_Score = [1, 'NA']
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
    values_ANC_Cum_Score = [1, 'NA']
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

    choices = [1, "NA"]

    base_data_df['cum_score_LE'] = np.select(conditions, choices, default=0)

    condition_Eligibility_DRO = np.logical_or(base_data_df['Age'] < 15, base_data_df['Age'] > 64)
    base_data_df['Eligibility DRO'] = np.where(condition_Eligibility_DRO, 0, 1)



    conditions_cum_score_DRO = [
        (base_data_df['Ed'].str.strip().isin(['10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ', '12th कक्षा पूरा किया हुआ', 'डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ', 'पोस्ट ग्रेजुएशन पूरा किया हुआ'])),
        (base_data_df['Eligibility DRO'] == 0)
    ]

    values_cum_score_DRO = [1, 'NA']
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


    base_data_df['voter'] = pd.to_numeric(base_data_df['voter'], errors='coerce').fillna(0)



    conditions_cum_score_EV = [
        (base_data_df['Eligibility_voter'] == 0),
        (base_data_df['voter'] > 0)
    ]

    values_cum_score_EV = ['NA', 1]
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


    base_data_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/base_data_df.xlsx', index=False)
    print("Result Excel file saved successfully.")

    total_fid = base_data_df[['__fid__']].values.tolist()
    tribes = np.array(base_data_df['Tribe_N']).flatten().tolist()

    unique_fid = []
    unique_tribes = []

    for x in total_fid:
        if x not in unique_fid:
            unique_fid.append(x)

    for x in tribes:
        if x not in unique_tribes:
            unique_tribes.append(x)


    score = [0] * len(unique_fid)
    HH_size_list = [0] * len(unique_fid)
    HH_tribe_list = [""] * len(unique_fid)


    for i in range(len(unique_fid)):
            for j in range(len(total_fid)):

                if unique_fid[i] == total_fid[j]:
                    HH_size_list[i] += 1
                    if HH_tribe_list[i] == "":
                        HH_tribe_list[i] = tribes[j]

    # print(tribes)
    # print(HH_tribe_list)



    # print(len(HH_size_list))
    # print(len(unique_fid))

    def calScore(list1,list2,score):
        for i in range(len(unique_fid)):
            score[i] = 0
            for j in range(len(list1)):

                if unique_fid[i] == list1[j]:
                    if pd.isna(list2[j]) or list2[j] == 'NA':
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

    cum_score_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/cum_data_df.xlsx', index=False)
    print("Result Excel file saved successfully.")

    HH_score_df = pd.DataFrame({
        '_fid_': unique_fid,
        'Tribe_N' : HH_tribe_list,
        'Sum of HH_S' : HH_size_list,

    })




    # # Conditions and value assigning for the new column 'HH_Score_H_CD'
    HH_score_df['HH_Score_H_CD'] = np.where(cum_score_df['Sum of Eligibility_CD'] == cum_score_df['Sum of CD_Cum_Score'], 1, 0)
    HH_score_df['HH_Score_H_IMM'] = np.where(cum_score_df['Sum of Eligibility_IMM'] == cum_score_df['Sum of IMM_Cum_Score'], 1, 0)

    conditions = [
        (cum_score_df['Sum of Eligibility_IND'] == HH_score_df['Sum of HH_S']),
        (cum_score_df['Sum of Eligibility_IND'] != HH_score_df['Sum of HH_S'])
    ]

    choices = [
        np.where(cum_score_df['Sum of IND_Cum_Score'] > 1, 1, 0),
        "NA"
    ]

    HH_score_df['HH_Score_H_IND'] = np.select(conditions, choices, default=0).astype('object')


    condition_HH_Score_H_ANC = (cum_score_df['Sum of Eligibility_ANC'] > 0) & (cum_score_df['Sum of ANC_Cum_Score'] > 1)
    HH_score_df['HH_Score_H_ANC'] = np.where(condition_HH_Score_H_ANC, 1, np.where(cum_score_df['Sum of Eligibility_ANC'] > 0, 0, 'NA')).astype('object')



    HH_score_df['HH_Score_H_IND'] = pd.to_numeric(HH_score_df['HH_Score_H_IND'], errors='coerce')
    HH_score_df['HH_Score_H_ANC'] = pd.to_numeric(HH_score_df['HH_Score_H_ANC'], errors='coerce')

    conditions_HH_Score_H_MC = [
        (HH_score_df['HH_Score_H_IND'].notna() & HH_score_df['HH_Score_H_ANC'].notna() & (HH_score_df['HH_Score_H_IND'] + HH_score_df['HH_Score_H_ANC'] == 2)),
        (HH_score_df['HH_Score_H_IND'].isna() | HH_score_df['HH_Score_H_ANC'].isna())
    ]
    choices_HH_Score_H_MC = [1, "NA"]
    HH_score_df['HH_Score_H_MC'] = np.select(conditions_HH_Score_H_MC, choices_HH_Score_H_MC, default=0)
    HH_score_df['HH_Score_H_MC'] = pd.to_numeric(HH_score_df['HH_Score_H_MC'], errors='coerce')

    HH_score_df['HH_Score_H_U5CM'] = np.where(cum_score_df['Sum of U5CM_Cum_Score'] < HH_score_df['Sum of HH_S'], 0, 1)
    HH_score_df['HH_Score_H_FS'] = np.where((cum_score_df['Sum of 2sq_Cum_Score'] == HH_score_df['Sum of HH_S']) & (cum_score_df['Sum of FD_Cum_Score'] == HH_score_df['Sum of HH_S']), 1, 0)

    HH_score_df['HH_Score_E_LE'] = np.where(cum_score_df['Sum of cum_score_LE'] >= 1, 1, 0)
    HH_score_df['HH_Score_E_DRO'] = np.where(cum_score_df['Sum of cum_score_DRO'] == cum_score_df['Sum of Eligibility DRO'], 1, 0)

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

    HH_score_df['HH_Score_C_L'] = np.where(cum_score_df['Sum of cum_score_L'] >= 1, 1, 0)
    HH_score_df['HH_Score_C_Arts'] = np.where(cum_score_df['Sum of cum_score_Arts'] >= 1, 1, 0)




    conditions_HH_Score_G_EV = [
        (np.logical_and(cum_score_df['Sum of cum_score_EV'] > 0, cum_score_df['Sum of cum_score_EV'] == cum_score_df['Sum of Eligibility_voter'])),
        (cum_score_df['Sum of Eligibility_voter'] == 0)
    ]

    choices_HH_Score_G_EV = [1, "NA"]

    HH_score_df['HH_Score_G_EV'] = np.select(conditions_HH_Score_G_EV, choices_HH_Score_G_EV, default=0)
    HH_score_df['HH_Score_G_EV'] = pd.to_numeric(HH_score_df['HH_Score_G_EV'], errors='coerce')

    HH_score_df['HH_Score_G_meeting'] = np.where(cum_score_df['Sum of Cum_s core_meetings'] > 0, 1, 0)

    # print(HH_score_df)

    HH_score_df.to_excel('C:/SARTHAK/NOTES/SEM5/Web TDI/pandas/HH_scores.xlsx', index=False)
    print("Result Excel file saved successfully.")

    from .models import Tribe
    from django.http import HttpResponse
    from .forms import HouseholdForm
    from django.db import IntegrityError

    for index, row in HH_score_df.iterrows():
        slug = row.at['Tribe_N'].strip()

        
        if not slug in unique_tribes:
            print( HttpResponse(f'Tribe with slug "{slug}" not found. Check your Excel for valid tribe name.'))
        
        # print(slug)
        # # print(user)
        # print(year)
        try:
            tribe, created = Tribe.objects.get_or_create(user=user, year=year, name=slug)
        except IntegrityError:
            # Handle the case where the record already exists
            tribe = Tribe.objects.get(user=user, year=year, name=slug)

        

        household_data = {
        'size': row['Sum of HH_S'],
        'CD_score': row['HH_Score_H_CD'],
        'IM_score': row['HH_Score_H_IMM'],
        'MC_score': row['HH_Score_H_MC'],
        'CM_score': row['HH_Score_H_U5CM'],
        'FS_score': row['HH_Score_H_FS'],
        'LE_score': row['HH_Score_E_LE'],
        'DRO_score': row['HH_Score_E_DRO'],
        'IC_score': row['HH_Score_S_IC'],
        'OW_score': row['HH_Score_S_OWN'],
        'SANI_score': row['HH_Score_S_SANI'],
        'FUEL_score': row['HH_Score_S_Fuel'],
        'DRWA_score': row['HH_Score_S_SoDrWa'],
        'ELECTR_score': row['HH_Score_S_ELECTR'],
        'ASS_score': row['HH_Score_S_ASS'],
        'LAN_score': row['HH_Score_C_L'],
        'ARTS_score': row['HH_Score_C_Arts'],
        'EV_score': row['HH_Score_G_EV'],
        'MEET_score': row['HH_Score_G_meeting']
        }


        household_form = HouseholdForm(household_data)
        if household_form.is_valid():
            household = household_form.save(commit=False)
            household.tribeID = tribe
            household.save()

        else:
            print(household_form.errors)

        

