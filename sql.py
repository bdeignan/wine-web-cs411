
import pymysql
import re
import sys


def exec_sql_file(cursor, sql_file):
    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                print (statement)
                cursor.execute(statement)
                print(cursor.fetchall())
            except Exception, e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""

if (len(sys.argv) >= 2):
    name = str(sys.argv[1])
    conn = pymysql.connect(
        local_infile=True,
        host="localhost",
        user="root",
        database="wine_web",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    exec_sql_file(cursor,name)
    conn.commit()
    print (cursor.rowcount)

else:
    print ("No filename given")