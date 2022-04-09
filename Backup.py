import io,sys,os
import datetime
import zipfile
from Parameters import Parameters
from CompressFiles import CompressFiles
import BD
import Models


class Backup:

    def __init__(self,job_name,full_backup=False):
        self.parameters = Parameters()
        self.total_files = 0
        self.total_process_files = 0
        self.session = BD.get_session()

        #self.job = self.find_job_by_name(job_name)
        if full_backup:
            task = self.set_full_backup(job_name)
        else:
            task = self.get_task(job_name,full_backup)

        os.makedirs(self.get_output_folder(self.job,task),exist_ok=True)
        #os.makedirs(self.parameters.remote_path+self.job.get_foldername(), exist_ok=True)

        list_folders = self.list_file_in_folder(self.parameters.local_path)
        for folder in list_folders:
            filename_zip = self.get_filename(folder,self.job,task)
            if os.path.isdir(folder):

                all_files = self.list_all_files(folder)
                files_to_add = []
                for file in all_files:
                    self.total_files += 1
                    if task.isFull() or not self.exist_in_database(file):
                        files_to_add.append(file)

                if len(files_to_add) > 0:
                    print("Folder: "+folder+" -> "+filename_zip)
                    self.process_files(filename_zip,files_to_add,self.job)
                else:
                    self.process_files(filename_zip,[folder],self.job)
            else:
                print("File: "+folder+" -> "+filename_zip)
                self.process_files(filename_zip,[folder],self.job)
            
        self.final_report()

    def remove_path_from_filename(self,path, filename):
        if path in filename:
            filename = filename.replace(path, "")
        return filename

    def find_job_by_name(self,job_name):
        job = self.session.query(Models.Jobs).filter_by(name=job_name,active=1).first()
        return job

    def create_new_job(self,job_name):
        job = Models.Jobs(name=job_name,date_backup=datetime.datetime.now(),active=1)
        self.session.add(job)
        self.session.commit()
        return job

    def create_new_task(self,job_id,number,type):
        task = Models.Task(job_id=job_id,number=number,type=type,date_backup=datetime.datetime.now())
        self.session.add(task)
        self.session.commit()
        return task

    def get_last_task_by_job(self,job):
        task = self.session.query(Models.Task).filter_by(job_id=job.id).order_by(Models.Task.id.desc()).first()
        return task

    def set_full_backup(self,job_name):
        self.job = self.find_job_by_name(job_name)
        self.job.active = 0
        self.session.commit()
        self.job = self.create_new_job(job_name)
        return self.create_new_task(self.job.id,0,"full")


    def get_task(self,job_name,full_backup=False):
        self.job = self.find_job_by_name(job_name)
        if self.job is None:
            self.job = self.create_new_job(job_name)
            return self.create_new_task(self.job.id,0,"full")
        else:
            task = self.get_last_task_by_job(self.job)
            if task is None:
                return self.create_new_task(self.job.id,0,"full")
            else:
                if task.number <= self.parameters.number_incrementals:
                    return self.create_new_task(self.job.id,task.number+1,"incremental")
                else:
                    self.job.active = 0
                    self.session.commit()
                    self.job = self.create_new_job(job_name)
                    return self.create_new_task(self.job.id,0,"full")
        
    

    def process_files(self,filename_zip,files_to_add,task):
        zip_file = zipfile.ZipFile(filename_zip, 'w')
        for file in files_to_add:
            self.total_process_files += 1
            print("Adding {} to {}".format(file,filename_zip))
            zip_file.write(file)
            self.add_file_to_database(file,task)
        zip_file.close()


    def get_output_folder(self,job,task):
        return self.parameters.remote_path + str(job.id)+"_"+str(task.number)+"_"+job.name

    def get_filename(self,filename,job,task):
        filename_with_path = self.get_output_folder(job,task) + "/"+ str(job.id)+"_"+str(task.number)+"_"+task.type +"_"+self.remove_path_from_filename(self.parameters.local_path+"/",filename)
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

    def add_file_to_database(self,file,task):
        file_model = Models.FileModel(filename=file,job_id=self.job.id,task_id=task.id)
        self.session.add(file_model)
        self.session.commit()

    def final_report(self):
        print("Total files: {}".format(self.total_files))
        print("Total process files: {}".format(self.total_process_files))

if __name__ == "__main__":
    job_name = "mail"
    bkp = Backup(job_name)
