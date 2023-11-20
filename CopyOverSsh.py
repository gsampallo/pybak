from Parameters import Parameters
import BD
import Models
import os
import logging
from datetime import datetime
import paramiko

from sqlalchemy import desc

class CopyOverSsh:
    
    def __init__(self):
        self.param = Parameters()
        self.session = BD.get_session()
        logfile = f"./log/{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info("Start backup files on server at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.get_env_parameters()

        #client = self.get_client()
        task = self.get_last_task()
        job = self.get_job_by_task(task)
        input_folder = self.get_input_folder(job, task,True)
        print(input_folder)

        self.get_list_of_files(input_folder)
        
        client = self.get_client()
        sftp = client.open_sftp()
        sftp.chdir("/root/bkp")
        
        output_folder = self.get_input_folder(job, task,False)
        
        dir_list = sftp.listdir()
        if output_folder not in dir_list:
            logging.info(f"{output_folder} created")
            sftp.mkdir(output_folder)

        self.upload_files(sftp, input_folder,output_folder)
        self.send_notification()
        sftp.close()
        client.close()
        
        logging.info("Finish at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        

    def upload_files(self, sftp, input_folder, output_folder):
        files_list = os.listdir(input_folder)
        total_files = len(files_list)
        logging.info(f"Total files to upload: {total_files}")
        file_count = 1
        for file in files_list:
            print(f"{input_folder}/{file}",f"/root/bkp/{output_folder}")
            sftp.put(f"{input_folder}/{file}",f"/root/bkp/{output_folder}/{file}")
            logging.info(f"Upload: {file_count}/{total_files} {file}")
            file_count += 1

    def get_last_task(self):
        return self.session.query(Models.Task).order_by(desc("id")).first()
        

    def get_job_by_task(self, task):
        return self.session.query(Models.Jobs).filter(Models.Jobs.id==task.job_id).order_by(desc("id")).first()

    def get_input_folder(self, job, task, withPath):
        if withPath:
            return self.param.remote_path + str(job.id)+"_"+str(task.number)+"_"+job.name
        else:
            return str(job.id)+"_"+str(task.number)+"_"+job.name

    def get_env_parameters(self):
        if not os.environ.get('BKP_HOSTNAME') or not os.environ.get('BKP_PORT') or not os.environ.get('BKP_USERNAME'):
            logging.error("Can't find environment variables. Please configure.")
            exit(1)
        
        self.hostname = os.environ.get('BKP_HOSTNAME')
        self.port = os.environ.get('BKP_PORT')
        self.username = os.environ.get('BKP_USERNAME')
        self.topic_notification = os.environ.get('BKP_TOPIC_NOTIF')

    def get_list_of_files(self, folder):
        for file in os.listdir(folder):
            print(file)

    def get_client(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy())
            client.connect(self.hostname, self.port, self.username, '')
            return client
        except Exception as e:
            logging.error("Can't connect to the server "+self.hostname)
            logging.error("*** Caught exception: %s: %s" % (e.__class__, e))
            exit(1)

    def send_notification(self):
        import requests
        requests.post(f"https://ntfy.sh/{self.topic_notification}", data=f"All files upload to {self.hostname}")
            

cos = CopyOverSsh()
