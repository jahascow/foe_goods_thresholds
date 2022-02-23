# -*- coding: utf-8 -*-
"""
FOE Automation
by : jahascow
git_hub : https://github.com/jahascow
about : this is a simple script for the game forge of empires "FOE" which
    takes the csv output download from foe_tools for guild daily treasury with 
    all options selected and determines good needs by established thresholds.
    I wrote this to help the guild NoRemorse in the us world Angkor.
"""
import csv
from pathlib import Path
import pandas as pd
import os
import glob
import numpy as np
import pyperclip
# Import date class from datetime module
from datetime import date
  
# dataframes defined
# df = raw goods dataframe
# t_df = working dataframe with un-needed columns removed



# set directory for downloads folder
dl_path = str(Path.home())+'/Downloads'

# get newest treasury file
files = glob.glob(dl_path+'/'+'guild-treasury-daily'+'*.csv')
files.sort(key=os.path.getmtime, reverse=True)
market_file = files[0]
"""
[row_start:row_end , column_start, column_end]

where,

row_start refers start row with 0 position as index
row_end refers last row with n th  position as index
column_start refers start column with 0 position as index
column_end refers last column with n th position as index
"""
# read treasury file into dataframe, print without index
df = pd.read_csv(market_file, sep=',', header = 0)
#print(df.to_string(index=False)) 

# drop Requested amount & Rate & 
t_df = df.iloc[:1 , df.columns.get_loc('Jewelry'):] #Jewelry is the first treasury good
#print(t_df)

#print(m_df.iloc[:, 0])
#print(m_df.to_string(index=False)) 
"""
Goods criteria
Empty =less 15.      Good= 51-60
Very Low= 16-25.     Very Good =61-70
Low =26-35.            Excellent = 71-80
Okay = 36-50.          Ready for War +81

RFW= Ready For War!! ᗜಠ o ಠ)¤=[]:::::>-updated -02/14/22
IA -----------  Good -------------- jewelry, ebony 
EMA -------Empty--------------- Alabaster, Granite
HMA -------Low -------------- Rope, Brick
LMA -------- Okay --------------- Brass, silk 
CA ---------- Excellent ------------- Wire, Porcelain
Indy -------- Empty -------------- Coke, Rubber 
PE ------ RFW ------------ Tinplate , Explosives 
ME --------- Low -------------- convenience food, flavorants
PME ------ Empty ------------ Steel, genome data 
CE ---------- Okay ------------— Electromagnets, Robotics
TE ---------- Very Low --------------- Smart Materials, Translucent concrete 
FE ---------- Very Low -------------- Biodata, superconductors  
AF ---------- RFW -------------- Paper Batteries, Bioplastic
OF ---------- RFW ------------- Coral, Plankton
VF ---------- RFW -----------— CryptoCash, Golden Rice
SAM -------- RFW -------------- Fusion Reactors, Lubricants 
SAAB ------ RFW -------------- Bromine, Compound 
SAV --------- RFW ------------- Seaweed, MicroSupplement
"""
# Create a dictionary to set value uper bound thresholds
goods_criteria_dict = {
  "Empty": 15000,
  "Very Low": 25000,
  "Low": 35000,
  "Okay": 50000,
  "Good": 60000,
  "Very Good": 70000,
  "Excellent": 80000,
  "Ready for War": 9000000
}
age_dict = {
    0: "\nIA:------ ",
    1: "\nEMA:----- ",
    2: "\nHMA:----- ",
    3: "\nLMA:----- ",
    4: "\nCA:------ ",
    5: "\nIndy:---- ",
    6: "\nPE:------ ",
    7: "\nME:------ ",
    8: "\nPME:----- ",
    9: "\nCE:------ ",
    10: "\nTE:------ ",
    11: "\nTF:------ ",
    12: "\nAF:------ ",
    13: "\nOF:------ ",
    14: "\nVF:------ ",
    15: "\nSAM:----- ",
    16: "\nSAAB:---- ",
    17: "\nSAV:----- ",
}


for_clipboard = '''\
Goods criteria (in thousands)
Empty =less 15.      Good= 51-60
Very Low= 16-25.     Very Good =61-70
Low =26-35.            Excellent = 71-80
Okay = 36-50.          Ready for War +81

RFW= Ready For War!! :::::>-updated - {updated}\n
'''.format(length='multi-line', updated=date.today())
# gives a tuple of column name and series
# for each column in the dataframe
age = age_dict[0]
goods = ""
a = 0 # set to 4 as index starts at 0
g = 0
age_status = ""
age_status2 = [0]
needed_good = "Need:  "
print(list(t_df))
for (columnName, columnData) in t_df.iteritems():
    if a % 4 == 0 and a != 0: # modulus 4 if 0 then we are on a new age
        age_index = int((g/5))
        age = age_dict[age_index]
        if age_status != "Ready for War -- ": 
            for_clipboard+= age + age_status + needed_good + str('\n')
        needed_good = "Goods Needed: "
        age_status = ""
        age_status2 = [0]
        a = 0
        #goods = "" 
    #goods+=columnName
    if int(columnData.values) <= goods_criteria_dict["Empty"]:
        needed_good+=columnName + str(', ')
        age_status2.append(8)
        age_status="Empty ---------- "
    elif goods_criteria_dict["Empty"] > int(columnData.values) <= goods_criteria_dict["Very Low"]:
        needed_good+=columnName + str(', ')
        if bool(set([8])&set(age_status2)) == False:
            age_status2.append(7)
            age_status="Very Low ------- "
    elif goods_criteria_dict["Very Low"] > int(columnData.values) <= goods_criteria_dict["Low"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7])&set(age_status2)) == False:
            age_status2.append(6)
            age_status="Low ------------ "
    elif goods_criteria_dict["Low"] > int(columnData.values) <= goods_criteria_dict["Okay"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6])&set(age_status2)) == False:
            age_status2.append(5)
            age_status="Okay ----------- "
    elif goods_criteria_dict["Okay"] > int(columnData.values) <= goods_criteria_dict["Good"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5])&set(age_status2)) == False:
            age_status2.append(4)
            age_status="Good ----------- "
    elif goods_criteria_dict["Good"] > int(columnData.values) <= goods_criteria_dict["Very Good"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5,4])&set(age_status2)) == False:
            age_status2.append(3)
            age_status="Very Good ------ "
    elif goods_criteria_dict["Very Good"] > int(columnData.values) <= goods_criteria_dict["Excellent"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5,4,3])&set(age_status2)) == False:
            age_status2.append(2)
            age_status="Excellent ------ "
    else:
        if bool(set([8,7,6,5,4,3,2])&set(age_status2)) == False:
            age_status2.append(1)
            age_status="Ready for War -- "

    
    #print('Column Name : ', columnName)
    #print('Column Contents : ', columnData.values)
    g+=1
    a+=1


pyperclip.copy(for_clipboard)
