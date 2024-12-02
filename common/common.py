import os
import re
import shutil

from common.singleton_base import SingletonBase

class Common(SingletonBase):
    '''
        GET ALL FILE MATCHING A REGEX PATTERN
        @directory - the directory to be searched
        @pattern - the regex pattern as a string
    '''
    @staticmethod
    def get_files_by_regex(directory, pattern):
        regex = re.compile(pattern)
        
        # List to store matched files
        matched_files = []
        
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if regex.match(file):
                    matched_files.append(os.path.join(root, file))

            break
        
        return matched_files
    
    @staticmethod
    def contains_value(arr, value):
        return value in arr
    
    @staticmethod
    def copy_and_rename(src_path, dest_path, new_name):
        # Copy the file
        shutil.copy(src_path, dest_path)
        file_name = Common.get_filename_from_path(src_path)
        # Rename the copied file
        new_path = f"{dest_path}/{new_name}"
        shutil.move(f"{dest_path}/{file_name}", new_path)
        
        return new_path

    @staticmethod
    def get_filename_from_path( path):
        return os.path.basename(path)
    
    @staticmethod
    def filter_objects(objects, key, value):
        return [obj for obj in objects if obj[key] == value]