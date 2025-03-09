import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')