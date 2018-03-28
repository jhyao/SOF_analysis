import peewee_async
import peewee
from playhouse.pool import PooledMySQLDatabase

db = {
    'host': 'localhost',
    'port': 3306,
    'user': 'user',
    'passwd': 'password',
    'database': 'database',
    'max_connections': 10,
}


try:
    from . import config_my
    db.update(**config_my.db)
finally:
    database = peewee.MySQLDatabase(
        db.get('database'), 
        host=db.get('host'),
        port=db.get('port', 3306),
        user=db.get('user'),
        passwd=db.get('passwd')
    )
    database_async = peewee_async.MySQLDatabase(
        db.get('database'), 
        host=db.get('host'),
        port=db.get('port', 3306),
        user=db.get('user'),
        password=db.get('passwd')
    )
    pool = PooledMySQLDatabase(
        db.get('database'), 
        host=db.get('host'),
        port=db.get('port', 3306),
        user=db.get('user'),
        passwd=db.get('passwd'),
        max_connections=db.get('max_connections', 10)
    )
    pool_async = peewee_async.PooledMySQLDatabase(database_async, max_connections=db.get('max_connections'))
    # pool._connect()
