# import pandas as pd

# # Assuming you have the two sets of data in Excel files named excel1.xlsx and excel2.xlsx
# df1 = pd.read_excel('C:/Users/tinky/OneDrive/Documents/households_excel.xlsx', usecols=['HH_Score_H_CD'])
# df2 = pd.read_excel("C:/Users/tinky/OneDrive/Documents/Health.xlsx", usecols=['HH_Score_H_CD'])

# # Compare the two dataframes
# # Find differing rows
# differing_rows = df1[df1.ne(df2).any(axis=1)]

# print("Differing rows:")
# print(differing_rows)

# # Display specific values in the 3rd row
# print("Values in the 3rd row:")
# print("Excel 1:", df1.iloc[3])
# print("Excel 2:", df2.iloc[3])


# print_households.py

from .models import Household

# Assuming your model is named Household

# Filter objects where size is 6
households_size_6 = Household.objects.filter(size=6)

# Print all fields for each object
for household in households_size_6:
    print("Household ID:", household.id)
    print("Tribe ID:", household.tribeID.id)  # Access the related Tribe ID
    print("Size:", household.size)
    print("CD_score:", household.CD_score)
    print("IM_score:", household.IM_score)
    print("MC_score:", household.MC_score)
    print("CM_score:", household.CM_score)
    print("FS_score:", household.FS_score)
    print("LE_score:", household.LE_score)
    print("DRO_score:", household.DRO_score)
    print("IC_score:", household.IC_score)
    print("OW_score:", household.OW_score)
    print("SANI_score:", household.SANI_score)
    print("FUEL_score:", household.FUEL_score)
    print("DRWA_score:", household.DRWA_score)
    print("ELECTR_score:", household.ELECTR_score)
    print("ASS_score:", household.ASS_score)
    print("LAN_score:", household.LAN_score)
    print("ARTS_score:", household.ARTS_score)
    print("EV_score:", household.EV_score)
    print("MEET_score:", household.MEET_score)

    # Add a separator for better readability
    print("-" * 20)
