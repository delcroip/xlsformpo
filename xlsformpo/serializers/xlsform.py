
import os
import logging
import re
import datetime
import pandas as pd


logger = logging.getLogger("default")


def read_input_file(input_file_path):
    try:
        file = pd.ExcelFile(input_file_path)
    except Exception as e:
        logger.error("while opening the from the file {0} with error {1}".format(input_file_path, e) )
        return None
    return file


def parse_excel_sheets(data_dictionary_file, excludedWorksheets):
    worksheets = data_dictionary_file.sheet_names
    filtered_sheets = []
    for worksheet in worksheets:
        logger.info("loading sheet {0}".format(worksheet).replace("\u2265", " "))
        if worksheet.lower() not in excludedWorksheets:
            filtereddatetime_sheets.append(worksheet)
    return filtered_sheets

def parse_sheets(input_file, excudedWorksheets=None):
    worksheets = input_file.sheet_names
    df_survey = None
    df_choices = None
    df_settings = None
    df_entities = None

    for worksheet in worksheets:
        logger.info("loading sheet {0}".format( worksheet))
        if excudedWorksheets is None or worksheet not in excudedWorksheets:
            df = input_file.parse(worksheet)

            worksheet= worksheet.replace("_", ".")
            # strip space
            df = df.dropna(how='all').applymap(lambda x: x.strip() if type(x)==str else x)
            if worksheet == "choices":
                if validate_choices_sheet(df):
                    df_choices = df
                else:
                    break
            elif worksheet == "settings":
                if validate_settings_sheet(df):
                    df_settings = df
                else:
                    break
            elif worksheet == "survey":
                if validate_survey_sheet(df):
                    df_survey = df
                else: 
                    break
            elif worksheet == "entities":
                if validate_entities_sheet(df):
                    df_entities = df
                else: 
                    break
            
            else:
                logger.warning(f" worksheet {worksheet} not parsed, need to be change, valueset or start with r., l., q., r.")


    return {
        "choices" : df_choices,
        "survey" : df_survey,
        "settings" : df_settings,
        "entities" : df_entities
    }
BASIC_CHOICES_COLUMN = {'list_name','value','label'}
BASIC_SURVEY_COLUMN={'type','name','label'}
BASIC_SETTINGS_COLUMN = {'form_id'}
BASIC_ENTITIES_COLUMN = {'entity'}

def validate_choices_sheet(df):
    if BASIC_CHOICES_COLUMN.issubset(df.columns):
        return True
    else:
        logger.warning(f"sheet {worksheet} does not have the mandatory column: {','.join(BASIC_COLUMN).values()}")
        return False

def validate_survey_sheet(df):
    if BASIC_SURVEY_COLUMN.issubset(df.columns):
        return True
    else:
        logger.warning(f"sheet {worksheet} does not have the mandatory column: {','.join(BASIC_LIBRARY_COLUMN).values()}")
        return False
def validate_settings_sheet(df):
    if BASIC_SETTINGS_COLUMN.issubset(df.columns):
        return True
    else:
        logger.warning(f"sheet {worksheet} does not have the mandatory column: {','.join(BASIC_LIBRARY_COLUMN).values()}")
        return False

def validate_entities_sheet(df): 
    if BASIC_ENTITIES_COLUMN.issubset(df.columns):
        return True
    else:
        logger.warning(f"sheet {worksheet} does not have the mandatory column: {','.join(BASIC_CHANGE_COLUMN).values()}")
        return False
    
    
    
def export(dfs, base, filename= None):
    #settings={'form_title':title,'form_id':form_id,'version':version,'default_language':'English (en)','style':'pages'} 
    if not filename:
        filename = f"{dfs['settings']['form_id'].iloc[0]}_translated.xlsx"    
    # update-version
    now = datetime.datetime.now()
    version_date=now.strftime('%Y%m%d%H%M')
    #TODO avoid adding datetime to a version already using it
    current_version = dfs['settings']['version'].iloc[0]
    dfs['settings']['version'].iloc[0] = f"{current_version}_{version_date}"
    output_path = os.path.join(base, filename)
    #create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    dfs['survey'].to_excel(writer, sheet_name='survey', index=False)
    dfs['choices'].to_excel(writer, sheet_name='choices', index=False)
    dfs['settings'].to_excel(writer, sheet_name='settings', index=False)
    if 'entities' in dfs and dfs['entities']>0:
        dfs['entities'].to_excel(writer, sheet_name='settings', index=False)

    writer.close()