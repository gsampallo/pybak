from sqlalchemy import Column, Integer, String, Float, DateTime
import BD

class FileModel(BD.Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(360))
    job_id = Column(Integer)

class Jobs(BD.Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    name = Column(String(360))
    date_backup = Column(DateTime)

    def get_foldername(self):
        return "{}_{}_{}".format(self.id,self.name,self.date_backup.strftime("%Y%m%d_%H%M%S"))