from flask import Flask, render_template, request
import omdb
import copy
import json

# Set OMDb API Key
omdb.set_default('apikey', '')  # Enter your API Key as the second argument.

with open('omdb_fei_dict.json', 'r') as f:
    o_f_dict = json.load(f)

template = {}  # fhead template
fei_elements = []  # list of added fei elements in template


def search_by_title(t):
    """OMDb API search request by title"""
    req = omdb.get(title=t)
    return req


def convert_timecode(dur):
    """converts OMDb runtime (minutes) to TC hh:mm:ss"""
    dur_info = ''
    for char in dur:
        if char.isdigit():
            dur_info += char
    hours = int(dur_info) // 60
    minutes = int(dur_info) % 60
    new_dur = str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':00'
    return new_dur


def get_f_elements(d, k):
    """This function extracts the FEI element for each OMDb key (k) from the omdb_fei_dict.json (d)."""
    x = d[k]  # associated FEI element
    x_key = list(x.keys()).pop(0)  # top FEI element (dict)
    try:
        x_val = list(x[x_key]).pop(0)  # 1st FEI sub element (str)
    except IndexError:
        x_val = ''
    y = x[x_key]  # 2nd FEI sub element (dict)
    try:
        y_key = list(y.keys()).pop(0)  # 3rd FEI sub element (str)
    except AttributeError:
        y_key = {}
    try:
        z = o_f_dict[k][x_key][y_key]
    except TypeError:
        z = []
    try:
        z_dict = z[0]
    except (IndexError, KeyError):
        z_dict = {}
    try:
        z_key = list(z_dict.keys())
    except AttributeError:
        z_key = []
    i = len(z_key) - 1
    try:
        z_key = z_key.pop(0)
    except IndexError:
        pass
    return x, x_key, x_val, y_key, z, z_dict, i, z_key


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/output", methods=["POST"])
def output():
    omdb_dict = search_by_title(request.form.get("title"))
    for key in omdb_dict.keys():
        if omdb_dict[key] != 'N/A' and key in o_f_dict:
            x, x_key, x_val, y_key, z, z_dict, i, z_key = get_f_elements(o_f_dict, key)
            if x_key in fei_elements:  # fei element already exists in template
                if 'crew' in x_val:
                    name_list = omdb_dict[key].split(', ')
                    for n in name_list:
                        if '(' in n:
                            subpers = n.split(' (')
                            subpers_name = subpers[0]
                            if subpers_name in str(template[x_key][x_val]):
                                counter = 0
                                while counter < len(template[x_key][x_val]):
                                    if subpers_name in str(template[x_key][x_val][counter]):
                                        if key not in template[x_key][x_val][counter]['role']:
                                            template[x_key][x_val][counter]['role'].append('writer')
                                            break
                                        else:
                                            counter += 1
                                    else:
                                        break
                            else:
                                add_subpers = {'role': ['writer'], 'persname': subpers_name}
                                template[x_key][x_val].append(add_subpers)
                        else:
                            z_dict['persname'] = n
                            template[x_key][x_val].append(z_dict)
                else:
                    if 'desc' in z_key:
                        add_z = copy.deepcopy(z)
                        template[x_key][y_key].extend(add_z)
                        template[x_key][y_key][i][z_key] = omdb_dict[key]
                    elif 'duration' in z_key:
                        template[x_key][y_key][0][z_key] = convert_timecode(omdb_dict[key])
                    elif 'lang' in z_key:
                        z_dict = omdb_dict[key].split(', ')
                        template[x_key][y_key][0][z_key] = z_dict
                    else:
                        template[x_key][y_key][0][z_key] = omdb_dict[key]
            else:  # jumps here if new element has to be added to template
                fei_elements.append(x_key)
                add_x = copy.deepcopy(x)
                template.update(add_x)  # new element is added to template
                if template[x_key] == '':
                    template[x_key] = omdb_dict[key]
                else:
                    if type(template[x_key][x_val]) == list:
                        if type(x[x_key][x_val][0]) == dict:
                            if 'persname' in x[x_key][x_val][0].keys():
                                name_list = omdb_dict[key].split(', ')
                                name_index = 0
                                while name_index < len(name_list):
                                    if '(' in name_list[name_index]:
                                        subpers = name_list[name_index].split('(')
                                        subpers_name = subpers[0]
                                        subpers_role = subpers[1][:-1]
                                        add_subpers = {'role': [subpers_role], 'persname': subpers_name}
                                        template[x_key][x_val].append(add_subpers)
                                    else:
                                        add_list = copy.deepcopy(add_x[x_key][x_val])
                                        add_list[0]['persname'] = name_list[name_index]
                                        if name_index == 0:
                                            template[x_key][x_val][0]['persname'] = name_list[0]
                                        else:
                                            template[x_key][x_val].append(add_list[0])
                                    name_index += 1
                            else:
                                list_item = x[x_key][x_val][0]
                                list_key = list(list_item.keys())
                                template[x_key][x_val][0][list_key[0]] = omdb_dict[key]
                        elif ', ' in omdb_dict[key]:
                            omdb_item_val = omdb_dict[key].split(', ')
                            template[x_key][x_val] = omdb_item_val
                        else:
                            template[x_key][x_val] = omdb_dict[key]
                    elif type(template[x_key][x_val]) == dict:
                        y_key = list(x[x_key][x_val].keys()).pop(0)
                        template[x_key][x_val][y_key] = omdb_dict[key]
                    else:
                        template[x_key][x_val] = omdb_dict[key]
    fei_output = json.dumps({"fhead": template}, sort_keys=False, ensure_ascii=False, indent=2)
    return render_template("output.html", input=request.form.get("title"), success=omdb_dict, output=fei_output)
