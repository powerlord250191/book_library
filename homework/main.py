from initial_db import insert_data
from routers import app

if __name__ == '__main__':
    insert_data()
    app.run()
