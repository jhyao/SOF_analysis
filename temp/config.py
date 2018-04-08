import data.config.config as config
from data.models.sof_models import User
import logging

logging.basicConfig(level=logging.DEBUG)
database = config.database
database.drop_tables([User])
database.create_tables([User])