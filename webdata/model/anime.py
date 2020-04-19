from sqlalchemy import Column,String,Float
from . import Base

class Anime(Base):
    __tablename__= 'anime'
    id = Column(String(50),primary_key=True,nullable=False)
    title = Column(String(50),nullable=True)
    link = Column(String(255), nullable=True)
    process = Column(String(20), nullable=True)
    cover = Column(String(255), nullable=True)
    play_count = Column(String(20), nullable=True)
    source = Column(String(20), nullable=True)
    trend = Column(Float)

    def __init__(self,id,title,link,process,cover,play_count,source):
        self.id=id
        self.title=title
        self.link=link
        self.process=process
        self.cover=cover
        self.play_count=play_count
        self.source=source
        self.trend=0
