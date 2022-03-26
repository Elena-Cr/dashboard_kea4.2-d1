
def conn():
    from sqlalchemy import create_engine
    return create_engine('postgresql://dissingjan:Mengao22@jgfd-postgresql-db.postgres.database.azure.com:5432/postgres')

if __name__ == '__main__':
    pass