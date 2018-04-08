import peewee_async
import peewee
from playhouse.pool import PooledMySQLDatabase
import redis
import logging

CONFIG = {
    'env': {
        'env': 'prod'
    },
    'db': {
        'host': 'localhost',
        'port': 3306,
        'user': 'user',
        'passwd': 'password',
        'database': 'database',
        'max_connections': 10,
        'charset': 'utf8'
    },
    'db_test': {
        'host': 'localhost',
        'port': 3306,
        'user': 'user',
        'passwd': 'password',
        'database': 'database',
        'max_connections': 10,
        'charset': 'utf8'
    },
    'db_root': {
        'host': 'localhost',
        'port': 3306,
        'user': 'user',
        'passwd': 'password',
        'database': 'database',
        'max_connections': 10,
        'charset': 'utf8'
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'minsize': 5,
        'maxsize': 10
    },
    'logging': {
        'format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
        'level': logging.INFO
    }
}

try:
    from . import config_my
    for key in CONFIG:
        CONFIG[key].update(**config_my.config.get(key, {}))
except ImportError:
    raise Exception('No config found')

logging.basicConfig(format=CONFIG['logging']['format'], level=CONFIG['logging']['level'])
logger = logging.getLogger(__name__)


class Config(object):
    def __init__(self, env=None):
        if not env:
            env = CONFIG.get('env', {}).get('env', None)
        if env == 'root':
            self.db = CONFIG.get('db_root')
        elif env == 'test':
            self.db = CONFIG.get('db_test')
        else:
            self.db = CONFIG.get('db')
        self.redis_config = CONFIG.get('redis')

        logger.debug('db setting: ' + str(self.db))

        self.database = peewee.MySQLDatabase(
            self.db.get('database'),
            host=self.db.get('host'),
            port=self.db.get('port', 3306),
            user=self.db.get('user'),
            passwd=self.db.get('passwd'),
            charset=self.db.get('charset')
        )
        self.database_async = peewee_async.MySQLDatabase(
            'sof_basic',
            host=self.db.get('host'),
            port=self.db.get('port', 3306),
            user=self.db.get('user'),
            password=self.db.get('passwd'),
            charset=self.db.get('charset')
        )
        self.pool = PooledMySQLDatabase(
            'sof_basic',
            host=self.db.get('host'),
            port=self.db.get('port', 3306),
            user=self.db.get('user'),
            passwd=self.db.get('passwd'),
            max_connections=self.db.get('max_connections', 10)
        )
        self.pool_async = peewee_async.PooledMySQLDatabase(
            'sof_basic',
            host=self.db.get('host'),
            port=self.db.get('port', 3306),
            user=self.db.get('user'),
            password=self.db.get('passwd'),
            charset=self.db.get('charset'),
            max_connections=self.db.get('max_connections', 10)
        )

        # redis_pool_async = aioredis.create_redis_pool(
        #     (config['redis']['host'], config['redis']['port']),
        #     minsize=config['redis']['minsize'],
        #     maxsize=config['redis']['maxsize'],
        #     loop=asyncio.get_event_loop()
        # )

        self.redis_pool = redis.ConnectionPool(
            self.redis_config['host'],
            port=self.redis_config['port'],
            decode_responses=True
        )

config = Config()
