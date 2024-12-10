from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Kullanıcı-PDF tablosu
class UserPDF(Base):
    __tablename__ = 'user_pdfs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    pdf_name = Column(String)
    pdf_path = Column(String)

# Veritabanı bağlantısı
from config import DATABASE_URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()