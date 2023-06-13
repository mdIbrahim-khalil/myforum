import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv('ENV')
print('ENV: ', ENV)

if ENV == 'production':
    from .conf.production.settings import *
else:
    from .conf.development.settings import *
