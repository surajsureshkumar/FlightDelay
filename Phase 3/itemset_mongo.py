import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['project']
ma = pd.DataFrame(list(db["major_airlines"].find({})))
ma.drop(columns=["_id"], inplace=True)
ma.rename(columns={'flight_number': 'flight_number_1'}, inplace=True)
lattice_count = 2
while True:
    temp = []
    l1 = pd.DataFrame(list(db["l1"].find({})))
    l1.drop(columns=['count', '_id'], inplace=True)
    for i in range(0, lattice_count):
        temp.append(pd.merge(l1, ma, how='inner', on='flight_number_1'))
    for i in range(1, lattice_count):
        new = pd.merge(temp[i - 1], temp[i], how='inner',
                       on=['flight_date', 'origin', 'destination'])
        new.rename(columns={'flight_number_1_x': 'flight_number_1',
                            'flight_number_1_y': f'flight_number_{i + 1}'},
                   inplace=True)
        new = new[new[f'flight_number_{i}'] < new[f'flight_number_{i + 1}']]
        temp[i] = new
    new_lattice = temp[-1]
    columns = [f'flight_number_{i}' for i in range(1, lattice_count + 1)]
    final_lattice = new_lattice.groupby(columns)['flight_date'].aggregate(
        'count').reset_index()
    final_lattice.rename(columns={'flight_date': 'count'}, inplace=True)
    final_lattice = final_lattice[final_lattice['count'] > 9]
    if len(final_lattice) == 0:
        break
    db.create_collection(f'l{lattice_count}')
    db[f'l{lattice_count}'].insert_many(final_lattice.to_dict('records'))
    print(f'l{lattice_count}', 'done', 'No of rows:', len(final_lattice))
    lattice_count += 1
