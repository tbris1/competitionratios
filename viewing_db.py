import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///feedback.db")
df = pd.read_sql("SELECT * FROM feedback", engine)

print(df[['specialty', 'usefulness']])
