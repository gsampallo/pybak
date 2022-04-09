import io,sys,os
import datetime
import zipfile
from Parameters import Parameters
from CompressFiles import CompressFiles
import BD
import Models


class Backup:

    def __init__(self,full_backup=False):
        self.parameters = Parameters()
        
        self.session = BD.get_session()

        job = self.create_new_job()

        os.makedirs(self.parameters.remote_path+job.get_foldername(), exist_ok=True)

        list_folders = self.list_file_in_folder(self.parameters.local_path)
        for folder in list_folders:
            
            filename_zip = self.get_filename(folder,job)
            print("Folder: "+folder+" -> "+filename_zip)

            all_files = self.list_all_files(folder)
            files_to_add = []
            for file in all_files:
                if full_backup:
                    files_to_add.append(file)
                elif not self.exist_in_database(file):
                    files_to_add.append(file)

            if len(files_to_add) > 0:
                self.process_files(filename_zip,files_to_add,job)



    def remove_path_from_filename(self,path, filename):
        if path in filename:
            filename = filename.replace(path, "")
        return filename

    def create_new_job(self):
        job = Models.Jobs(name="Job1",date_backup=datetime.datetime.now())
        self.session.add(job)
        self.session.commit()
        return job


    def process_files(self,filename_zip,files_to_add,job):
        zip_file = zipfile.ZipFile(filename_zip, 'w')
        for file in files_to_add:
            print("Adding {} to {}".format(file,filename_zip))
            zip_file.write(file)
            self.add_file_to_database(file,job)
        zip_file.close()

    def get_filename(self,filename,job):
        filename_with_path = self.parameters.remote_path + job.get_foldername() + "/" + self.remove_path_from_filename(self.parameters.local_path+"/",filename)
        #filename_with_path = self.remove_path_from_filename(self.parameters.local_path+"/",filename)
        now = datetime.datetime.now()
        return "{}_".format(filename_with_path)+f'{now:%Y%m%d_%H%M%S}'+".zip"

    def list_file_in_folder(self,folder):
        list_file = []
        for file in os.listdir(folder):
            list_file.append(folder+"/"+file)
        return list_file

    #get the list of all files on the local path recursively
    def list_all_files(self,folder):
        list_file = []
        for file in os.listdir(folder):
            if os.path.isdir(folder+"/"+file):
                list_file.extend(self.list_all_files(folder+"/"+file))
            else:
                list_file.append(folder+"/"+file)
        return list_file


    def exist_in_database(self,file):
        file_model = self.session.query(Models.FileModel).filter_by(filename=file).first()
        return (file_model is not None)

    def add_file_to_database(self,file,job):
        file_model = Models.FileModel(filename=file,job_id=job.id)
        self.session.add(file_model)
        self.session.commit()

if __name__ == "__main__":
    bkp = Backup()
