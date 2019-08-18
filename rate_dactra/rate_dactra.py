import os

from rate_dactra import create_app, db
from .models import User, Teacher, Review, Comment

app = create_app(configuration=os.getenv('FLASK_CONFIG') or 'default')                                                            
                                                                                                                                  
                                                                                                                                  
@app.shell_context_processor                                                                                                      
def make_shell_context():                                                                                                         
    return dict(db=db, User=User, Teacher=Teacher, Review=Review, Comment=Comment)
