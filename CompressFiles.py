import zipfile
import datetime

class CompressFiles:

    def __init(self,zip_filename):
        self.filename = zip_filename
        self.zip_file = zipfile.ZipFile(zip_filename, 'w')

    def add_file_to_zip(self,file):
        self.zip_file.write(file)
