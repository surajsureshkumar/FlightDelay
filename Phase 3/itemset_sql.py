db = pg.connect(database='Project',
                user='postgres',
                password='your_password',
                host='localhost',
                port=5432)
cursor = db.cursor()
query = ''
cursor.execute('select * from flights.l1')
rows = cursor.fetchall()
lattice_level = 2
while rows and lattice_level < 11:
    query = "select "
    for i in range(1, lattice_level):
        query += "p.flight_number_" + str(i) + " as flight_number_" + str(i) + ','
    query += "q.flight_number_" + str(lattice_level - 1) + " as flight_number_" + str(
        lattice_level) + ", count(*) into flights.l" + str(lattice_level) + " "
    query += "from flights.l" + str(lattice_level - 1) + " p, flights.l" + str(lattice_level - 1) + " q, "
    for i in range(1, lattice_level + 1):
        query += "flights.major_airlines ma" + str(i) + ","
    query = query[:-1] + " where "
    for i in range(1, lattice_level - 1):
        query += "p.flight_number_" + str(i) + " = q.flight_number_" + str(i) + " and "
    query += "p.flight_number_" + str(lattice_level - 1) + "< q.flight_number_" + str(lattice_level - 1) + " and "
    for i in range(1, lattice_level):
        query += 'p.flight_number_' + str(i) + "= ma" + str(i) + ".flight_number and "
    query += 'q.flight_number_' + str(lattice_level - 1) + ' = ma' + str(lattice_level) + '.flight_number and '
    for i in range(1, lattice_level + 1):
        for j in range(i + 1, lattice_level + 1):
            query += "ma" + str(i) + ".flight_date = ma" + str(j) + ".flight_date and "
    for i in range(1, lattice_level + 1):
        for j in range(i + 1, lattice_level + 1):
            query += "ma" + str(i) + ".source = ma" + str(j) + ".source and "
    for i in range(1, lattice_level + 1):
        for j in range(i + 1, lattice_level + 1):
            query += "ma" + str(i) + ".destination = ma" + str(j) + ".destination and "

    query = query[:-4] + 'group by ('
    for i in range(1, lattice_level):
        query += 'p.flight_number_' + str(i) + ','
    query += 'q.flight_number_' + str(lattice_level - 1) + ") having count(*)>9"
    print('query', query)
    cursor.execute(query)
    db.commit()
    cursor.execute('select * from flights.l' + str(lattice_level))
    rows = cursor.fetchall()
    print('Number of rows in the lattice ', lattice_level, ": ", len(rows))
    lattice_level += 1
