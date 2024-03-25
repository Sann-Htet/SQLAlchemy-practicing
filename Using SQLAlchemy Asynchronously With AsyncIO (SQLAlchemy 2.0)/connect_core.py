from sqlalchemy import Table, Column, Integer, MetaData, String, Text
from sqlalchemy import select



meta = MetaData()

users_table = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=True),
    Column('email', String, nullable=False),
    Column('bio', Text, nullable=False)    
)

