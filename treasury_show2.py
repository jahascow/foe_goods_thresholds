# -*- coding: utf-8 -*-
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
configuration = 0 # 0 for MDT, 1 for noremorse
run_type = 0 # 0 for self goods, 1 for guild
# get newest treasury file
if run_type != 0:
    files = glob.glob(dl_path+'/'+'guild-treasury-daily'+'*.csv')
else:
    files = glob.glob(dl_path+'/'+'your-treasure-daily'+'*.csv')
files.sort(key=os.path.getmtime, reverse=True)
market_file = files[0]
print(market_file)
# read treasury file into dataframe, print without index
df = pd.read_csv(market_file, sep=',', header = 0)# get only columns begininng with iron age
df = df.tail(1)# get last row of dataframe
t_df = df.iloc[:1 , df.columns.get_loc('Jewelry'):] #Jewelry is the first treasury good
t_df = t_df.T # Transpose rows / columns
t_df.reset_index(inplace=True)
t_df.rename(columns = {t_df.columns[0]:'good',t_df.columns[1]:'volume'}, inplace = True)


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

    Goods below 210k by era lowest -> greatest
------------------------------------------------

'''.format(length='multi-line', updated=strftime("%Y-%m-%d %I:%M %p"))

elif configuration == 1:
    for_clipboard_on = '''
    𝚃𝚛𝚎𝚊𝚜𝚞𝚛𝚢 𝚄𝚙𝚍𝚊𝚝𝚎/𝚁𝚎𝚙𝚘𝚛𝚝.  {updated}
    Let’s Get Ready For War!! ᗜಠ o ಠ)¤=[]:::::>
    ❗️= critically empty, less than 3k
    Empty =less 15k.      Good= 50-60k
    Very Low= 15-25k.     Very Good =60-70k
    Low =25-35k.            Excellent = 70-80
    Ok = 35k-50k

'''.format(length='multi-line', updated=strftime("%Y-%m-%d %I:%M %p"))

if configuration == 0:
    conditions = [
        (t_df['volume'] <= 150000),
        (t_df['volume'].between(150000, 151000)),
        (t_df['volume'].between(151000, 152000)),
        (t_df['volume'].between(152000, 153000)),
        (t_df['volume'].between(153000, 154000)),
        (t_df['volume'].between(154000, 155000)),
        (t_df['volume'].between(155000, 156000)),
        (t_df['volume'].between(156000, 210000)),
        (t_df['volume'] > 210000),
        ]
elif configuration == 1:
    conditions = [
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
        ' - ',
        ' - ',
        ' - ',
        ' - ',
        ' - ',
        ' - ',
        ' - ',
        ' - ',
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


########################################################################
# code for determining the three highest goods to trade from by erra
def get_market_exceptions():
    images_dict = {
        16: "Cloth", 17: "Ebony", 18: "Jewelry", 19: "Iron", 20: "Limestone",
        21: "Copper", 22: "Gold", 23: "Granite", 24: "Honey", 25: "Alabaster",
        26: "Brick", 27: "Glass", 28: "Dried Herbs", 29: "Ropes", 30: "Salt",
        31: "Basalt", 32: "Brass", 33: "Gunpowder", 34: "Silk", 35: "Talc Powder",
        36: "Coffee", 37: "Paper", 38: "Porcelain", 39: "Tar", 40: "Wire",
        41: "Coke", 42: "Fertilizer", 43: "Rubber", 44: "Textiles", 45: "Whale Oil",
        46: "Asbestos", 47: "Explosives", 48: "Machine Parts", 49: "Gasoline", 50: "Tinplate",
        51: "Convenience Food", 52: "Ferroconcrete", 53: "Flavorants", 54: "Luxury Materials", 55: "Packaging",
        56: "Genome Data", 57: "Industrial Filters", 58: "Renewable Resources", 59: "Semiconductors", 60: "Steel",
        61: "Bionics Data", 62: "Electromagnets", 63: "Gas", 64: "Plastics", 65: "Robots",
        66: "Nutrition Research", 67: "Papercrete", 68: "Preservatives", 69: "Smart Materials", 70: "Translucent Concrete",
        71: "Algae", 72: "Biogeochemical Data", 73: "Nanoparticles", 74: "Purified Water", 75: "Superconductors",
        76: "AI data", 77: "Bioplastics", 78: "Nanowire", 79: "Paper Batteries", 80: "Transester gas",
        81: "Artificial Scales", 82: "Biolight", 83: "Corals", 84: "Pearls", 85: "Plankton",
        86: "Cryptocash", 87: "Data Crystals", 88: "Golden Rice", 89: "Nanites", 90: "Tea Silk",
        91: "BioTech Crops", 92: "Fusion Reactors", 93: "Lubricants", 94: "Mars Microbes", 95: "Superalloys",
        96: "Bromine", 97: "Compound Fluid", 98: "Nickel", 99: "Platinum Crystal", 100: "Processed Material",
        101: "Glowing Seaweed", 102: "Herbal Snack", 103: "Microgreen Supplements", 104: "Soy Proteins", 105: "Sugar Crystals",
        }
    market_df = t_df.copy()
    images_df = pd.DataFrame(images_dict, index=['good',]).T
    images_df = images_df.rename_axis('good_keys').reset_index()
    market_df = pd.merge(market_df, images_df, how='left', on = 'good')
    market_df = market_df[market_df['good_keys'].notna()]
    market_list = ''
    market_list_verbose = []

    for i in range(len(age_dict)-1): # subtracting 1 as I have not included the next erra of goods
       market_erra_df = market_df[(i*5):((i*5)+5)]
       market_erra_df = market_erra_df.sort_values(by=['volume'], ascending=True)[:5]
       for i2 in range(2):
           market_list+= str(int(market_erra_df['good_keys'][i2:i2+1].values[0])) + ','
           market_list_verbose.append(age_dict[i] + ' ' + market_erra_df['good'][i2:i2+1].values[0])

    print(market_list_verbose,market_list)



if run_type == 0:
    get_market_exceptions()
########################################################################

t_df['status'] = np.select(condlist=conditions, choicelist=choices)
t3_df = pd.DataFrame()

t_df_list = []
for x in range(t_df.shape[0]):
    t_df_list.append(age_dict[math.floor(x/5)])

for x in range(t_df.shape[0]):
    t_df['age'] = t_df_list#age_dict[math.floor(x/5)]
    if x % 5 == 0:
        if configuration == 0:
            t2_df = t_df[x:(x+5)].sort_values(by=['volume'])[:5]
            t3_df = pd.concat([t3_df, t2_df])
        if configuration == 1:
            t2_df = t_df[x:(x+5)].sort_values(by=['volume'])[:2]
            t3_df = pd.concat([t3_df, t2_df])

# ^ confirmed above good

goods,status = '',''
if configuration == 0:
    t3_df = t3_df.loc[t3_df['status'] != 'Ready for War- ']
    for i in range(len(age_dict)):
        goods_df = t3_df.loc[t3_df['age'] == age_dict[i]].copy()

        if goods_df.empty == False:
            erra_goods = [val.strip() for sublist in goods_df.good.dropna().str.split(",").tolist() for val in sublist]
            erra_goods = ', '.join(erra_goods)
            for_clipboard += str(goods_df['age'].values[0]) + erra_goods + '\n'
elif configuration == 1:
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

for_clipboard += '\n------------------------------------------------\nThank you everyone for your donations!'
#pyclip.copy(for_clipboard)
if run_type != 0:
    print(for_clipboard)
