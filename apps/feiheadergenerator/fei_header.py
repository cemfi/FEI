import json
import easygui

fei = {
    "fei": {
        "fhead": {
            "titlestmt": {},
            "editionstmt":{},
            "prodstmt":{},
            "genrestmt":{},
            "crewlist":{},
        }
    }
}

fhead = fei['fei']['fhead']
titlestmt = fei['fei']['fhead']['titlestmt']
editionstmt = fei['fei']['fhead']['editionstmt']
prodstmt = fei['fei']['fhead']['prodstmt']
genrestmt = fei['fei']['fhead']['genrestmt']
crewlist = fei['fei']['fhead']['crewlist']

msg = "Fill in the blanks"
title = "Basic FEI Head Generator V.0.5"
names = ["title","date","duration","source","company","producer","distributor","genre","director","assistent","composer","leading actor","leading actress","supporting actor","supporting actress","technical direction","sound mixing","sound editing" ]
values = []  
values = easygui.multenterbox(msg, title, names)

if values:
    titlestmt['title'] = values[0]
    editionstmt['date'] = values[1]
    editionstmt['duration'] = values[2]
    editionstmt['source'] = values[3]
    prodstmt['company'] = values[4]
    prodstmt['producer'] = values[5]
    prodstmt['distributor'] = values[6]
    genrestmt['genre'] = values[7]
    crewlist['director'] = values[8]
    crewlist['assistent'] = values[9]
    crewlist['composer'] = values[10]
    crewlist['leading actor'] = values[11]
    crewlist['leading actress'] = values[12]
    crewlist['supporting actor'] = values[13]
    crewlist['supporting actress'] = values[14]
    crewlist['technical direction'] = values[15]
    crewlist['sound mixing'] = values[16]
    crewlist['sound editing'] = values[17]

    with open('myfei.json', 'w') as f:
        json.dump(fei, f, indent=2)