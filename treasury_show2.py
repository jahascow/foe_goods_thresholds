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
import re
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
print(market_file)
# read treasury file into dataframe, print without index
df = pd.read_csv(market_file, sep=',', header = 0)# get only columns begininng with iron age
df = df.tail(1)# get last row of dataframe
#print(df.to_string(index=False)) 

# drop Requested amount & Rate & 
t_df = df.iloc[:1 , df.columns.get_loc('Jewelry'):] #Jewelry is the first treasury good
#print(t_df)

#print(m_df.iloc[:, 0])
#print(m_df.to_string(index=False)) 

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
    0: "IA:------ ",
    1: "EMA:---- ",
    2: "HMA:---- ",
    3: "LMA:---- ",
    4: "CA:------ ",
    5: "Indy:---- ",
    6: "PE:------ ",
    7: "ME:------ ",
    8: "PME:---- ",
    9: "CE:------ ",
    10: "TE:------ ",
    11: "TF:------ ",
    12: "AF:------ ",
    13: "OF:------ ",
    14: "VF:------ ",
    15: "SAM:----- ",
    16: "SAAB:---- ",
    17: "SAV:----- ",
}

"""
for_clipboard = '''\
Goods criteria index (in thousands)
a: Critical = less than 3k!
b: Empty =less 15.      f: Good= 51-60
c: Very Low= 16-25.     g: Very Good =61-70
d: Low =26-35.            h: Excellent = 71-80
e: Okay = 36-50.          Ready for War +81
updated - {updated}\n
'''.format(length='multi-line', updated=date.today())
"""
for_clipboard = 'Updated: ' + str(date.today()) + '\n'
# gives a tuple of column name and series
# for each column in the dataframe
age = age_dict[0]
goods = ""
a = 0 # set to 4 as index starts at 0
g = 0
age_status = ""
age_status2 = [0]
#needed_good = "Need: "
needed_good = ""
print(list(t_df))
for (columnName, columnData) in t_df.iteritems():
    if a % 5 == 0 and a != 0: # modulus 4 if 0 then we are on a new age
        age_index = int((g/5)-1)
        age = age_dict[age_index]
        if age_status != "Ready for War -- ": 
            needed_good = sorted(needed_good.split(','))
            print(needed_good)
            if len(needed_good) > 2:
                needed_good = needed_good[1] + needed_good[2] # str split with sort will bring in an empty value into the beginning of the list
                needed_good = re.sub("[a-g]:", lambda x: ', ', needed_good)[2:]
            else:
                needed_good = needed_good[1]
                needed_good = re.sub("[a-g]:", lambda x: ',', needed_good)[1:]
            for_clipboard+= age + age_status + needed_good + str('\n')
        needed_good = ""
        age_status = ""
        age_status2 = [0]
        a = 0
        #goods = "" 
    #goods+=columnName
    if int(columnData.values) <= goods_criteria_dict["Empty"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('a:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('b:') + columnName + str(', ')
        age_status2.append(8)
        age_status="Empty ---------- "
    elif goods_criteria_dict["Empty"] <= int(columnData.values) <= goods_criteria_dict["Very Low"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('c:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('c:') + columnName + str(', ')
        if bool(set([8])&set(age_status2)) == False:
            age_status2.append(7)
            age_status="Very Low ------- "
    elif goods_criteria_dict["Very Low"] <= int(columnData.values) <= goods_criteria_dict["Low"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('d:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('d:') + columnName + str(', ')
        if bool(set([8,7])&set(age_status2)) == False:
            age_status2.append(6)
            age_status="Low ------------- "
    elif goods_criteria_dict["Low"] <= int(columnData.values) <= goods_criteria_dict["Okay"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('e:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('e:') + columnName + str(', ')
        if bool(set([8,7,6])&set(age_status2)) == False:
            age_status2.append(5)
            age_status="Okay ------------ "
    elif goods_criteria_dict["Okay"] <= int(columnData.values) <= goods_criteria_dict["Good"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('f:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('f:') + columnName + str(', ')
        if bool(set([8,7,6,5])&set(age_status2)) == False:
            age_status2.append(4)
            age_status="Good ----------- "
    elif goods_criteria_dict["Good"] <= int(columnData.values) <= goods_criteria_dict["Very Good"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('g:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('g:') + columnName + str(', ')
        if bool(set([8,7,6,5,4])&set(age_status2)) == False:
            age_status2.append(3)
            age_status="Very Good ------ "
    elif goods_criteria_dict["Very Good"] <= int(columnData.values) <= goods_criteria_dict["Excellent"]:
        if int(columnData.values) <= 3000:
            needed_good+=str('h:') + '❗' + columnName + str(', ')
        else:
            needed_good+=str('h:') + columnName + str(', ')
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
