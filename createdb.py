import sqlite3
#makes sure the local sqlite database and tables are created

def createdb():
    con = sqlite3.connect('trips.db')
    cur = con.cursor()

    con.execute("CREATE TABLE IF NOT EXISTS trips (region text, origin_coord text, destination_coord text, datetime text, datasource text)")
    con.execute("DELETE FROM trips")
    con.commit()
    con.close()

Returns: None
