import pandas as pd
import psycopg2
from sqlalchemy import create_engine
def read_data(name,engine):
    try:
        return pd.read_sql_table(name,engine)
    except:
        return pd.DataFrame([])
if __name__ == '__main__':
    # Creating PostgreSQL engine
    engine = create_engine('postgresql://<username>:<password>@localhost:'
 '<port>/<database>')
    df = read_data('user_insights',engine)
    df.to_excel('C:/Users/.../user_insights.xlsx',index=False)
