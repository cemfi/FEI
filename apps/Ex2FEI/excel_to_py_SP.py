import argparse
import json
import xlrd

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="An Excel file that contains a sequence protocol.")
args = parser.parse_args()

fei = xlrd.open_workbook(args.input_file)
fp = fei.sheet_by_index(0)


def get_sequence_info(sheet):
    """navigates navigates through sheet, gets values from record's sequences."""
    result = {
        "summary": str(sheet.cell_value(rowx=1, colx=1)),
        "timecodestart": str(sheet.cell(rowx=1, colx=2)),
        "sceneStmt": {
            "scenes": get_scenes_info(sheet),
        }
    }
    return result


def get_scenes_info(sheet):
    """navigates navigates through sheet, gets values from the scenes sequences."""
    result = []
    for row_idx in range(1, sheet.nrows):
        d = {
            "summary": str(sheet.cell_value(row_idx, colx=4)),
            "timecodestart": str(sheet.cell_value(row_idx, colx=9)),
            "reference_frame": str(sheet.cell_value(row_idx, colx=5)),
            "annotations": [
                {
                    "type": "text",
                    "about": "content",
                    "text": str(sheet.cell_value(row_idx, colx=6)),
                },
                {
                    "type": "contains_shot",
                    "number": str(sheet.cell_value(row_idx, colx=8)),
                },
                {
                    "type": "text",
                    "about": "objects",
                    "text": str(sheet.cell_value(row_idx, colx=7)),
                },
            ],

        }
        result.append(d)
    return result


def get_all_sequences(fei):
    """navigates the workbooks, gets information from all sheets of the workbook"""
    result = []
    for idx in range(fei.nsheets):
        fp = fei.sheet_by_index(idx)
        d = get_sequence_info(fp)
        result.append(d)
    return result


fei_dic = {
    "fbody": {
        "protocolStmt": {
            "content": get_all_sequences(fei),
        }
    }

}

file_name = str(args.input_file[:-4] + "json")


with open(str(args.input_file[:-4] + "json"), 'w') as file_out:
    json.dump(fei_dic, file_out, indent=2)
