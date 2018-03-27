from peewee_async import PooledMySQLDatabase, MySQLDatabase

db = {
    'host': 'localhost',
    'port': 3306,
    'user': 'user',
    'passwd': 'password',
    'database': 'database',
    'max_connections': 5,
}


try:
    from . import config_my
    db.update(**config_my.db)
finally:
    database = MySQLDatabase(
        db.get('database'), 
        host=db.get('host'),
        port=db.get('port'),
        user=db.get('user'),
        password=db.get('passwd')
    )
    print(db)
    # pool = PooledMySQLDatabase(database, max_connections=db.get('max_connections'))
    # pool._connect()
