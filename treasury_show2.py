"""
FOE Automation
by : jahascow
git_hub : https://github.com/jahascow
about : This is a simple script for the game forge of empires "FOE" which
    takes the csv output download from foe_tools for guild daily treasury with
    all options selected and determines good needs by established thresholds.
    I wrote this to help the guild NoRemorse, and added an edit to expand for another
    Guild thresholds in the us world Angkor.
"""
from pathlib import Path
import pandas as pd
import os
import glob
import numpy as np
import pyclip #pyperclip
import math
from time import strftime

# set directory for downloads folder
dl_path = str(Path.home())+'/Downloads'
configuration = 0 # 0 for MDT, 1 for noremorse, carthage
# get newest treasury file
files = glob.glob(dl_path+'/'+'guild-treasury-daily'+'*.csv')
files.sort(key=os.path.getmtime, reverse=True)
market_file = files[0]
print(market_file)
# read treasury file into dataframe, print without index
df = pd.read_csv(market_file, sep=',', header = 0)# get only columns begininng with iron age
df = df.tail(1)# get last row of dataframe
t_df = df.iloc[:1 , df.columns.get_loc('Jewelry'):] #Jewelry is the first treasury good


# Create a dictionary to set value uper bound thresholds
if configuration == 0:
    goods_criteria_dict = {
      "Critical------ ": 150000,
      "Empty--------- ": 200000,
      "Very Low------ ": 250000,
      "Low----------- ": 300000,
      "Okay---------- ": 350000,
      "Good---------- ": 400000,
      "Very Good----- ": 450000,
      "Excellent----- ": 500000,
      "Ready for War- ": 5500000
    }
elif configuration == 1:
    goods_criteria_dict = {
      "Critical------ ": 3000,
      "Empty--------- ": 15000,
      "Very Low------ ": 25000,
      "Low----------- ": 35000,
      "Okay---------- ": 50000,
      "Good---------- ": 60000,
      "Very Good----- ": 70000,
      "Excellent----- ": 80000,
      "Ready for War- ": 9000000
    }
age_dict = {
    0: "IA:------ ",
    1: "EMA:----- ",
    2: "HMA:----- ",
    3: "LMA:----- ",
    4: "CA:------ ",
    5: "Indy:---- ",
    6: "PE:------ ",
    7: "ME:------ ",
    8: "PME:----- ",
    9: "CE:------ ",
    10: "TE:------ ",
    11: "TF:------ ",
    12: "AF:------ ",
    13: "OF:------ ",
    14: "VF:------ ",
    15: "SAM:----- ",
    16: "SAAB:---- ",
    17: "SAV:----- ",
    18: "SAJM:----- ",
}


if configuration == 0:
    for_clipboard = '''
    𝚃𝚛𝚎𝚊𝚜𝚞𝚛𝚢 𝚄𝚙𝚍𝚊𝚝𝚎/𝚁𝚎𝚙𝚘𝚛𝚝.  {updated}
    Let’s Get Ready For War!! ᗜಠ o ಠ)¤=[]:::::>
    ❗️= critically empty, less than 150k
    Empty =less 200k.      Good= 400-450k
    Very Low= 200-250k.     Very Good =450-500k
    Low =250-300k.            Excellent = 500+
    Ok = 300k-350k\n
    '''.format(length='multi-line', updated=strftime("%Y-%m-%d %I:%M %p"))
elif configuration == 1:
    for_clipboard_on = '''
    𝚃𝚛𝚎𝚊𝚜𝚞𝚛𝚢 𝚄𝚙𝚍𝚊𝚝𝚎/𝚁𝚎𝚙𝚘𝚛𝚝.  {updated}
    Let’s Get Ready For War!! ᗜಠ o ಠ)¤=[]:::::>
    ❗️= critically empty, less than 3k
    Empty =less 15k.      Good= 50-60k
    Very Low= 15-25k.     Very Good =60-70k
    Low =25-35k.            Excellent = 70-80
    Ok = 35k-50k\n
    '''.format(length='multi-line', updated=strftime("%Y-%m-%d %I:%M %p"))


t_df = t_df.T # Transpose rows / columns
t_df.reset_index(inplace=True)
t_df.rename(columns = {t_df.columns[0]:'good',t_df.columns[1]:'volume'}, inplace = True)
if configuration == 0:
    conditions = [
        (t_df['volume'] <= 150000),
        (t_df['volume'].between(150000, 200000)),
        (t_df['volume'].between(200000, 250000)),
        (t_df['volume'].between(250000, 300000)),
        (t_df['volume'].between(300000, 350000)),
        (t_df['volume'].between(350000, 400000)),
        (t_df['volume'].between(400000, 450000)),
        (t_df['volume'].between(450000, 500000)),
        (t_df['volume'] >= 500000),
        ]
elif configuration == 1:
    conditions_no = [
        (t_df['volume'] <= 3000),
        (t_df['volume'].between(3000, 15000)),
        (t_df['volume'].between(15000, 25000)),
        (t_df['volume'].between(25000, 35000)),
        (t_df['volume'].between(35000, 50000)),
        (t_df['volume'].between(50000, 60000)),
        (t_df['volume'].between(60000, 70000)),
        (t_df['volume'].between(70000, 80000)),
        (t_df['volume'] >= 80000),
        ]
if configuration == 0:
    choices = [
        'Critical------ ',
        'Empty--------- ',
        'Very Low------ ',
        'Low----------- ',
        'Okay---------- ',
        'Good---------- ',
        'Very Good----- ',
        'Excellent----- ',
        'Ready for War- '
        ]
elif configuration == 1:
    choices = [
        'Critical------ ',
        'Empty--------- ',
        'Very Low------ ',
        'Low----------- ',
        'Okay---------- ',
        'Good---------- ',
        'Very Good----- ',
        'Excellent----- ',
        'Ready for War- '
        ]

t_df['status'] = np.select(condlist=conditions, choicelist=choices)

t3_df = pd.DataFrame()
for x in range(t_df.shape[0]):
    t_df['age'] = age_dict[math.floor(x/5)]
    if x % 5 == 0:
        t2_df = t_df[x:(x+4)].sort_values(by=['volume'])[:2]
        t3_df = pd.concat([t3_df, t2_df])
goods,status = '',''
for x in range(t3_df.shape[0]):
    if t3_df['status'].values[x] == 'Critical------ ':
        goods += '❗ ' + t3_df['good'].values[x] + ', '
    else:
        goods += t3_df['good'].values[x] + ', '
    if x % 2 == 0:
        status = str(t3_df['status'].values[x])
    if x % 2 == 1:
        if status != 'Ready for War- ':
            for_clipboard += str(t3_df['age'].values[x]) + status + goods.rsplit(',', 1)[0] + '\n'
        goods = ''

for_clipboard += '\nThank you everyone for your donations!'
#pyclip.copy(for_clipboard)
print(for_clipboard)
