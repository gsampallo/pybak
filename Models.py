from sqlalchemy import Column, Integer, String, Float, DateTime
import BD

class FileModel(BD.Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(360))
    job_id = Column(Integer)
    task_id = Column(Integer)

class Jobs(BD.Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    name = Column(String(360))
    date_backup = Column(DateTime)
    active = Column(Integer)


    def get_foldername(self):
        return "{}_{}_".format(self.id,self.name)
    
class Task(BD.Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer)
    number = Column(Integer)
    type = Column(String(20))
    date_backup = Column(DateTime)

    def isFull(self):
        return self.type == 'full'

    def get_foldername(self):
        return "{}_{}_{}".format(self.job_id,self.name,self.date_backup.strftime("%Y%m%d_%H%M%S"))