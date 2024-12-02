import os

from models.models import Form_116
from common.common import Common
from osfa.osfa_gpg import OsfaGpg
from dotenv import load_dotenv


def process_files():
    #   LOAD ENV VARS
    load_dotenv()
    #   SET DIRECTORY VARIABLES
    working_dir = os.environ['HT_WORKING_DIR']
    new_folder = os.environ['HT_NEW_FOLDER']

    #   GET MATCHING FILES
    files = Common.get_files_by_regex(working_dir, "^HOPE_Zell\\+Miller.*\\.csv$")
    #   GET ALL OF THE USER SESSIONS FROM FORM_116 - THIS IS USED TO MAKE SURE NO DUPLICATES
    use_sessions = Form_116.get_form_116_usesession()

    number_of_files = 0
    number_of_records = 0
    number_inserted = 0

    #   LOOP THROUGH EACH FILE
    for f in files:
        #   OPEN THE FILE
        with open(f, 'r') as file:
            #   READ THE FILE INTO MEMORY
            file_content: str = file.read()
            #   SKIP THE FIRST 7 LINES - THEY ARE GARBAGE
            lines: list[str] = file_content.splitlines()[7:]
            #   NUMBER OF RECORDS IN THE FILE
            number_of_records += len(lines)
            #   LOOP THROUGH THE LINES OF THE FILES
            for line in lines:
                #   CREATE FORM 115
                form_116 = Form_116(line)
                #   MAKE SURE THE USER SESSION IS UNIQUE
                if not(Common.contains_value(use_sessions, (int(form_116.form_116_usession),))):
                    Form_116.insert_form_116(
                        form_116.form_116_can,
                        form_116.form_116_ssn,
                        form_116.form_116_name,
                        form_116.form_116_phone,
                        form_116.form_116_submit_dt,
                        form_116.form_116_usession,
                        form_116.form_116_term,
                        form_116.                            
                        form_116_school                            
                    )
                    #   NUMBER OF ROWS INSERTED
                    number_of_records += 1

        #   COPY FILE TO PROCESSED FOLDER
        new_file_path = Common.copy_and_rename(f, new_folder, "PROCESSED_-_" + Common.get_filename_from_path(f))
        osfa_gpg = OsfaGpg()
        #   ENCRYPT PROCESSED FILE
        osfa_gpg.encrypt_file(new_file_path, f, 'osfaweb@uga.edu')
        #   CLEAN UP FILES
        os.remove(new_file_path)
        os.remove(f)
        #   COUNT OF FILES
        number_of_files += 1

    return f"NON ENROLLMENT: Number of files processed: {number_of_files} -- Total number of records: {number_of_records} -- Number of records inserted: {number_inserted}"

if __name__ == '__main__': 
    print(process_files())