import os
import getopt
import logging
import sys
from xlsformpo.services import process_xform

#from pyfhirsdc.services.generateBundle import write_bundle
#from pyfhirsdc.services.processInputFile import process_input_file, process_data_dictionary_file, process_decision_support_logic_file
#from pyfhirsdc.services.processLibraries import process_libraries
#from pyfhirsdc.services.uploadFiles import upload_files
#from pyfhirsdc.services.processConf import updateBuildNumber

def print_help():
    print("XLFFormPo takes an XLSform as input, a gettext 'locales' folder is expected on the same directory")
    print('-i / --input config_file_path')
    print('-s source lang, default `en` (not implemented)')
    print('-h / --help to generate this message')
    
   
   
def setup_logger(logger_name,
                 log_file, 
                 level=logging.INFO, 
                 formatting  ='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'):
     
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(formatting)
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)
    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(file_handler)


setup_logger('default', "debug.log", logging.DEBUG)
logger = logging.getLogger('default')


if __name__ == "__main__":
    #anthro = False
    input_path = None
    source_lang = 'en'
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hsi:",["input=","help"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_path = arg
            if input_path.startswith('./'):
                cwd = os.getcwd()
                input_path = os.path.join(cwd, input_path[2:])
        elif opt in ("-s", "--source"):
            source_lang = arg
    #if anthro:
    #    generate_anthro_codesystems(conf)

    # thorw an error when conf file is not provided 
    # if conf file is provided update the conf file build number and library version
    logger.info("Process input file")
    process_xform(input_path, source_lang) # output is the default output directory
