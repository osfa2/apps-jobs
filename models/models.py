from dateutil import parser
from datetime import datetime
from .database import Database 

class Form_132:
    def __init__(self):
        self.db = Database()
    
    def parse_line(self, line):
        if line:
            #   SPLIT THE LINE BY THE COMMAS
            values = line.split(',')

            self.form_132_term = values[0].upper()
            #   LINE HAS QUOTES AROUND SCHOOL
            self.form_132_school = values[1].replace('\t', '').replace('"', '').strip().upper()
            self.form_132_abroad = values[2][:1]
            self.form_132_hours_enrolling = values[3]
            self.form_132_ssn = '999999999'
            self.form_132_phone = ''
            self.form_132_export_dt = ''
            self.form_132_fafsa = ''
            if(values[10]):
                self.form_132_usession = values[10].strip()
            else:
                self.form_132_usession = '999999'

            if(values[11]):
                self.form_132_submit_dt = parser.parse(values[11]).strftime('%Y-%m-%d').strip()
            else:
                self.form_132_submit_dt = datetime.now().strftime('%Y-%m-%d')

            if(not(values[15])):
                self.form_132_can = values[7].replace('"', '').strip()[-9:]
                self.form_132_name = values[5].replace("'", "''").replace('"', '').strip().upper() + ", " + values[6].replace('"', '').strip().upper()
                self.form_132_email = values[8].strip()
            else:
                self.form_132_can = values[14].replace('"', '').strip()[-9:]
                self.form_132_name = values[13].replace("'", "''").replace('"', '').strip().upper() + ", " + values[12].replace('"', '').strip().upper()
                self.form_132_email = values[15].strip() + '@uga.edu'

            return self

    def get_form_132_usesession(self):
        q = "Select form_132_usession from forms.form_132 where form_132_usession is not null order by form_132_id desc"
        records = self.db.select(query=q)

        return records
    
    def insert_form_132(
        self,
        form_132_can,
        form_132_ssn,
        form_132_name,
        form_132_phone,
        form_132_email,
        form_132_submit_dt,
        form_132_export_dt,
        form_132_usession,
        form_132_abroad,
        form_132_school,
        form_132_term,
        form_132_hours_enrolling,
        form_132_fafsa
    ):
        
        query = f"""INSERT INTO forms.form_132
            (form_132_can,
            form_132_ssn,
            form_132_name,
            form_132_phone,
            form_132_email,
            form_132_submit_dt,
            form_132_usession,
            form_132_abroad,
            form_132_school,
            form_132_term,
            form_132_hours_enrolling,
            form_132_fafsa)
            SELECT
            '{form_132_can}',
            '{form_132_ssn}',
            '{form_132_name}',
            '{form_132_phone}',
            '{form_132_email}',
            '{form_132_submit_dt}',
            '{form_132_usession}',
            '{form_132_abroad}',
            '{form_132_school}',
            '{form_132_term}',
            '{form_132_hours_enrolling}',
            '{form_132_fafsa}';"""
        
        new_id = self.db.insert_data(query=query)

        return new_id
    
    def insert_tracking_record(self, form_132_id):

        query = f"""INSERT INTO forms.form_132_tracking
            (form_132_tracking_id,
            form_132_tracking_ineligible,
            form_132_tracking_ineligible_reason,
            form_132_tracking_level,
            form_132_tracking_hours_attempted,
            form_132_tracking_hours_enrolled,
            form_132_tracking_hours_surfer,
            form_132_tracking_transcript,
            form_132_tracking_surfer,
            form_132_tracking_pell,
            form_132_tracking_fafsa,
            form_132_tracking_comments,
            form_132_tracking_scholarship,
            form_132_tracking_hours_cap,
            form_132_tracking_by,
            form_132_tracking_dt)
            VALUES
            ({form_132_id},
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL);"""

        new_id = self.db.insert_data(query=query)

        return new_id


class Form_116:
    
    def __init__(self, line):
        self.db = Database
        #   SPLIT THE LINE BY THE COMMAS
        values = line.split(',')

        self.form_116_term = values[1].strip().upper()
        #   LINE HAS QUOTES AROUND SCHOOL        
        self.form_116_school = values[2].replace('\t', '').replace('"', '').strip().upper()
        self.form_116_abroad = values[3].strip()
        self.form_116_hours_enrolling = ''
        self.form_116_ssn = '999999999'
        self.form_116_phone = ''
        self.form_116_export_dt = ''
        self.form_116_fafsa = ''
        self.form_116_usession = values[8].strip()

        if(values[7]):
            self.form_116_submit_dt = parser.parse(values[7]).strftime('%Y-%m-%d').strip()
        else:
            self.form_116_submit_dt = datetime.now().strftime('%Y-%m-%d')

        if(values[11]):
            if(len(values[11]) > 9):
                can_len = len(values[11])
                remainder  = can_len - 9
                self.form_116_can = values[11].replace('"', '').strip()[remainder:can_len]
            else:    
                self.form_116_can = values[11].replace('"', '').strip()
            
            self.form_116_name = values[10].replace("'", "''").replace('"', '').strip().upper() + ", " + values[9].replace('"', '').strip().upper()
        else:
            if(len(values[6]) > 9):
                can_len = len(values[11])
                remainder  = can_len - 9
                self.form_116_can = values[6].replace('"', '').strip()[remainder:can_len]
            else:
                self.form_116_can = values[6].replace('"', '').strip()
            
            self.form_116_name = values[4].replace("'", "''").replace('"', '').strip().upper() + ", " + values[5].replace('"', '').strip().upper()

    def get_form_116_usesession(self):
        q = "Select form_116_usession from forms.form_116 where form_116_usession is not null order by form_116_id desc"
        records = self.db.select(query=q)

        return records
    
    def insert_form_116(
        self,
        form_116_can,
        form_116_ssn,
        form_116_name,
        form_116_phone,
        form_116_submit_dt,
        form_116_usession,
        form_116_term,
        form_116_school
    ):

        query = f"""
            INSERT INTO `forms`.`form_116`
            (
            `form_116_can`,
            `form_116_ssn`,
            `form_116_name`,
            `form_116_phone`,
            `form_116_submit_dt`,
            `form_116_usession`,
            `form_116_term`,
            `form_116_school`)
            VALUES
            (
            '{form_116_can}',
            '{form_116_ssn}',
            '{form_116_name}',
            '{form_116_phone}',
            '{form_116_submit_dt}',
            '{form_116_usession}',
            '{form_116_term}',
            '{form_116_school}');"""
            
        new_id = self.db.insert_data(query=query)

        return new_id