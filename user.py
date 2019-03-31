import pandas as pd
import sqlite3
import sqlalchemy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = sqlite3.connect('database.sqlite')
cur = data.cursor()
query = cur.execute(
    'select ascent.year, ascent.user_id, grade.fra_routes, user.sex, user.height, user.weight, user.started\
        from ascent, grade, user where ascent.grade_id = grade.id and ascent.user_id = user.id'
    )
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data=query.fetchall(), columns = cols)
print(df)