from sqlite3 import Connection


def SetupMigration(conn: Connection):
    cur = conn.cursor()
    try:
        cur.execute("""
                create table measurement_data
        (
            ID         integer
                constraint measurement_data_pk
                    primary key,
            timestamp  integer not null,
            dimmFactor float not null,
            voltage    float not null,
            angle      float not null
        );
        """)
        cur.close()
    except:
        pass
