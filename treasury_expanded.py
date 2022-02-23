# -*- coding: utf-8 -*-
"""
FOE Automation
by : jahascow
git_hub : https://github.com/jahascow
about : This is a simple script for the game forge of empires "FOE" which
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
    0: "IA:",
    1: "EMA:",
    2: "HMA:",
    3: "LMA:",
    4: "CA:",
    5: "Indy:",
    6: "PE:",
    7: "ME:",
    8: "PME:",
    9: "CE:",
    10: "TE:",
    11: "TF:",
    12: "AF:",
    13: "OF:",
    14: "VF:",
    15: "SAM:",
    16: "SAAB:",
    17: "SAV:",
}


for_clipboard = '''\
Goods criteria (in thousands)
Empty < 15 ; Good 51-60 ; Very Low 16-25 ; Very Good 61-70 ; Low 26-35 ; Excellent 71-80 ; Okay 36-50 
/n updated - {updated}\n
'''.format(length='multi-line', updated=date.today())
# gives a tuple of column name and series
# for each column in the dataframe
age = age_dict[0]
goods = ""
a = 0 # set to 4 as index starts at 0
g = 1
age_status = 0
age_status2 = [0]
needed_good = "Need:  "
for_clipboard+="IA\n"
for (columnName, columnData) in t_df.iteritems():
    if a % 4 == 0 and a != 0: # modulus 4 if 0 then we are on a new age
        age_index = int((g/5))
        age = age_dict[age_index]
        if age_status == 1:
            for_clipboard+= age + str('\n')
        age_status2 = [0]
        a = 0
        age_status = 0
        #goods = "" 
    #goods+=columnName
    if int(columnData.values) <= goods_criteria_dict["Empty"]:
        age_status2.append(8)
        age_status="Empty ----- "
        for_clipboard+= age_status + columnName + str('\n')
        age_status = 1
    elif goods_criteria_dict["Empty"] > int(columnData.values) <= goods_criteria_dict["Very Low"]:
        if bool(set([8])&set(age_status2)) == False:
            age_status2.append(7)
            age_status="Very Low -- "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    elif goods_criteria_dict["Very Low"] > int(columnData.values) <= goods_criteria_dict["Low"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7])&set(age_status2)) == False:
            age_status2.append(6)
            age_status="Low ------- "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    elif goods_criteria_dict["Low"] > int(columnData.values) <= goods_criteria_dict["Okay"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6])&set(age_status2)) == False:
            age_status2.append(5)
            age_status="Okay ------ "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    elif goods_criteria_dict["Okay"] > int(columnData.values) <= goods_criteria_dict["Good"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5])&set(age_status2)) == False:
            age_status2.append(4)
            age_status="Good ------ "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    elif goods_criteria_dict["Good"] > int(columnData.values) <= goods_criteria_dict["Very Good"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5,4])&set(age_status2)) == False:
            age_status2.append(3)
            age_status="Very Good - "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    elif goods_criteria_dict["Very Good"] > int(columnData.values) <= goods_criteria_dict["Excellent"]:
        needed_good+=columnName + str(', ')
        if bool(set([8,7,6,5,4,3])&set(age_status2)) == False:
            age_status2.append(2)
            age_status="Excellent - "
            for_clipboard+= age_status + columnName + str('\n')
            age_status = 1
    else:
        if bool(set([8,7,6,5,4,3,2])&set(age_status2)) == False:
            age_status2.append(1)
            #age_status="Ready for War -- "

    
    #print('Column Name : ', columnName)
    #print('Column Contents : ', columnData.values)
    g+=1
    a+=1




pyperclip.copy(for_clipboard)#[:-12]) # remove last erra