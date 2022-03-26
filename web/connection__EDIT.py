# EDIT THIS CODE WITH YOUR CREDENTIALS AND
# RENAME IT TO connection.py
def conn():
    from sqlalchemy import create_engine
    return create_engine('postgresql://USERNAME:PASSWORD@SERVER_ADDRESS:5432/postgres')

if __name__ == '__main__':
    pass