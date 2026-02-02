from sqlalchemy import Column,Integer,Double,DateTime,String,Float,ForeignKey
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__= "client"

    id_client = Column(Integer, primary_key=True, index=True, autoincrement=True)

    seniorcitizen = Column(String)
    partner = Column(String)
    dependents = Column(String)
    phoneservice =Column(String)
    paperlessbilling =Column(String)
    multiplelines = Column (String)
    internetservice = Column(String)
    onlinesecurity = Column(String)
    onlinebackup =Column(String)
    deviceprotection=Column(String)
    techsupport=Column(String)
    streamingtv=Column(String)
    streamingmovies=Column(String)
    contract=Column(String)
    paymentmethod = Column (String)
    monthlycharges = Column(Float)
    tenure = Column(Integer)
    totalcharges = Column(Float)

class Prediction(Base):
    __tablename__="prediction"

    id_prediction = Column(Integer, primary_key=True,index=True, autoincrement=True)
    
    id_client = Column(Integer,ForeignKey("client.id_client"),nullable=False)

    option_model = Column(String)
    score = Column(Double)
    label = Column(String)
    time_stamp =  Column(DateTime,default=datetime.now())

#print(datetime.now().strftime("%Y-%m-%d , %H:%M:%S"))



    