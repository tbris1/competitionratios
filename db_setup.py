from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, MetaData
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///feedback.db")

metadata = MetaData()

feedback_table = Table('feedback', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('timestamp', DateTime),
                       Column('training_stage', String),
                       Column('usefulness', Integer),
                       Column('specialty', String),
                       Column('confidence', Integer),
                       Column('feelings', String),
                       Column('suggestions', String))

metadata.create_all(engine)

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("✅ Database and feedback table created successfully.")
