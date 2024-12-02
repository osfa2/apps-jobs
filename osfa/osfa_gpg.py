import os
import gnupg 
import chardet
from dotenv import load_dotenv
from datetime import datetime
from common.singleton_base import SingletonBase

class OsfaGpg(SingletonBase):

    def __init__(self) -> None:
        load_dotenv()

        self.gnu_gpg_home: str = os.environ["GPG_HOME_PATH"]
        self.gnu_gpg_secure: str = os.environ["GPG_SECURE_PATH"]
        self.decrypt_path = os.environ["DECRYPT_PATH"]
        self.encrypt_path = os.environ["ENCRYPT_PATH"]
        self.PATH_TEMP = os.environ["PATH_TEMP"]

        self.decrypt_recipient = os.environ["DECRYPT_RECIPIENT"]
        self.passphrase: str = os.environ["PASSPHRASE"]

        #   INSTANTIATE GPG
        self.gpg = gnupg.GPG()
        self.gpg.homedir="C:/OSFA/GPG/keyring"
        #   self.gpg.homedir = self.gnu_gpg_home
        self.gpg.encoding = "utf-8"
        #   LOAD PRIVATE KEYS INTO GPG INSTANCE
        with open(os.environ["PRIVATE_KEY_PATH"]) as private_key_file:
            self.gpg.import_keys(private_key_file.read())

        self.encrypted_data: bytes

    def decrypt_file(self, file):
        # CREATE NEW FILE NAME
        today = datetime.today().strftime("%Y%m%d%H%M%S")
        file_name: str = (today + "-" + os.path.basename(file))[:-4] + '.TXT'
        #   GET BYTE STREAM OF ENCRYPTED DATE
        with open("c:/osfa/Reports/" + file, "rb") as f:
            self.encrypted_data: bytes = f.read()

        try:
            #   DECRYPT
            results = self.gpg.decrypt(self.encrypted_data, passphrase=self.passphrase)
            #   CHECK RESULTS OBJECT
            if results.ok:
                #   SAVE FILE TO DECRYPTED FILES FOLDER
                with open(self.decrypt_path + file_name, "wb") as file:
                    file.write(results.data)

                #   SET DECODE AND RETURN DECRYPTED DATA
                encoding = chardet.detect(results.data);
                return results.data.decode(encoding['encoding'])
            else:
                print(f"{results.stderr}")
                print(vars(results))
        except Exception:
            print(f"{results.stderr}")

        return None


    def encrypt_file(self, full_file_path, file, recipient):
        results = None   

        try:
            results = self.gpg.encrypt_file(file, recipients=[recipient], always_trust=True)

            if results.ok:
                with open(full_file_path + ".gpg", 'wb') as f:
                    f.write(results.data)
            else:
                print(f"{results.stderr}")
                print(vars(results))

        except Exception:
            print("bad things happened")

        return results