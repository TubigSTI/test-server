from dotenv import load_dotenv
import os
load_dotenv()
class ApplicationConfig: 
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATION = False
    # Echo Sql, everytime it runs a sql function it echo
    SQLALCHEMY_ECHO = True
    # setting the database uri 
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    