import os
from dotenv import load_dotenv
load_dotenv()

IS_PRODUCTION = os.getenv('IS_PRODUCTION')

if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *
