import os
import pandas as pd
import html2text
from xlsformpo.models.lang import SingletonLangClass
from xlsformpo.serializers.xlsform import parse_sheets,read_input_file, export



# the soup.text strips off the html formatting also
def remove_html(string):
    text = html2text.html2text(string) # retrive pure text from html
    text = text.strip('\n') # get rid of empty lines at the end (and beginning)
    text = text.split('\n') # split string into a list at new lines
    text = '\n'.join([i.strip(' ') for i in text if i]) # in each element in that list strip empty space (at the end of line) 
    # and delete empty lines
    return text

def process_xform(source_path, source_lang = 'en'):
    #check inputs, ensure presence of 'locales' folder
    base, filename, langs = check_source(source_path)
    #loads langs

    #gettext.bindtextdomain('tricc', './locale/')
    #gettext.textdomain('tricc')
    trads = SingletonLangClass(base, filename, langs)
    #xlsform to pd
    input_file= read_input_file(source_path)
    dfs = parse_sheets(input_file)
    #inject trads
    out = inject_trad(dfs, trads)
    #print output
    if trads.languages:
        export(out, base)
    #print pot
    trads.to_po_file(os.path.join(base,f'{filename}.pot'))

def inject_trad(dfs, trads):
    dfs_out = {}
    dfs_out['survey'] = trad_df(dfs['survey'], trads)
    dfs_out['choices'] = trad_df(dfs['choices'], trads )
    dfs_out['settings'] = trad_df(dfs['settings'], trads)
    if 'entities' in dfs and dfs['entities']:
        dfs_out['entities'] = trad_df(dfs['entities'], trads)
    return dfs_out
    
def trad_df(df, trads):
    TRAD_MAP = ['label','constraint_message', 'required_message', 'hint', 'help', 'title']
    columns = my_list = df.columns.values.tolist()
    trad_columns = get_trad_columns(columns, TRAD_MAP, trads)
    df_out = pd.DataFrame(columns=trad_columns)
    for id, row in df.iterrows():
        values = []
        col_idx = 0
        for column in columns:
            if clean_column(column) in TRAD_MAP:
                trad_code = lang_column(column)
                values+=list(trads.get_trads(row[column], force_dict=True).values())
            else:
                values.append(row[column])
            col_idx
        df_out.loc[len(df_out)] = values
    return df_out

def clean_column(column):
    return column.split('::')[0]

def lang_column(column):
    return column.split('::')[-1]

def get_trad_columns(columns, TRAD_MAP, trads):
    trad_colunms = []
    for column in columns:
        clean_col = clean_column(column)
        if column.split('::')[0] in  TRAD_MAP:
           trad_colunms += trads.get_trads_map(clean_column(column)).keys()
        else:
            trad_colunms.append(column)
    return trad_colunms
#check the source
#expect this kind of files structure:
# - myxlsform.xlsx
# - locales/en/LC_MESSAGES/myxlsform.po
#@param source_path path to xlsform file
#@return source_path(path) , langs(array<str>)
def check_source(source_path):
    langs = []
    if os.path.isfile(source_path):
        base_dir = os.path.dirname(source_path)
        filename = "".join(os.path.splitext(os.path.basename(source_path))[:-1])
        lang_dir = os.path.join(base_dir, 'locales')
        if (os.path.isdir(lang_dir)):
            for f in os.listdir(lang_dir):
                tmp_path = os.path.join(lang_dir, f, 'LC_MESSAGES')
                if os.path.isdir(tmp_path):
                    if f'{filename}.mo' in os.listdir(tmp_path) or  f'{f}.mo' in os.listdir(tmp_path) :
                        langs.append(f)
        return base_dir , filename, langs
    else:
        raise Exception(f"Source file `{source_path}` is not a file")


# the soup.text strips off the html formatting also
def remove_html(string):
    text = html2text.html2text(string) # retrive pure text from html
    text = text.strip('\n') # get rid of empty lines at the end (and beginning)
    text = text.split('\n') # split string into a list at new lines
    text = '\n'.join([i.strip(' ') for i in text if i]) # in each element in that list strip empty space (at the end of line) 
    # and delete empty lines
    return text