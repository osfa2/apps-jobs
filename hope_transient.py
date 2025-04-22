import os

from common.common import Common
from osfa.osfa_gpg import OsfaGpg
from models.models import Form_132
from dotenv import load_dotenv


def process_files():
    #   LOAD ENV VARS
    load_dotenv()
    #   SET DIRECTORY VARIABLES
    working_dir = os.environ['HT_WORKING_DIR']
    new_folder = os.environ['HT_NEW_FOLDER']
    _form_132 = Form_132()

    #   GET MATCHING FILES
    # files = Common.get_files_by_regex(working_dir, "^HOPE\\+Transient.*\\.csv$")
    files = Common.get_files_by_regex(working_dir, "new 2.csv")

    #   GET ALL OF THE USER SESSIONS FROM FORM_132 - THIS IS USED TO MAKE SURE NO DUPLICATES
    use_sessions = _form_132.get_form_132_usesession()

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
                #   CREATE FORM 132
                form_132 = _form_132.parse_line(line)
                #   MAKE SURE THE USER SESSION IS UNIQUE
                if not(Common.contains_value(use_sessions, (int(form_132.form_132_usession),))):
                    new_id = _form_132.insert_form_132(
                        form_132.form_132_can,
                        form_132.form_132_ssn,
                        form_132.form_132_name,
                        form_132.form_132_phone,
                        form_132.form_132_email,
                        form_132.form_132_submit_dt,
                        form_132.form_132_export_dt,
                        form_132.form_132_usession,
                        form_132.form_132_abroad,
                        form_132.form_132_school,
                        form_132.form_132_term,
                        form_132.form_132_hours_enrolling,
                        form_132.form_132_fafsa
                    )
                    #   NUMBER OF ROWS INSERTED
                    number_inserted += 1
                    _form_132.insert_tracking_record(new_id)

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

    return f"HOPE TRANSIENT: Number of files processed: {number_of_files} -- Total number of records: {number_of_records} -- Number of records inserted: {number_inserted}"

if __name__ == '__main__': 
    print(process_files()) 