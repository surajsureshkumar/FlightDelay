import pandas as pd

routes = pd.read_csv(r"Data\routes.dat",
                     names=['airline', 'airline_id', 'src_airport',
                            'src_airport_id', 'dest_airport',
                            'dest_airport_id', 'codeshare', 'stops',
                            'equipment'])
airlines = pd.read_csv(r"Data\airlines.dat",
                       names=['airline_id', 'airline.name', 'airline.alias',
                              'airline.iata_code', 'airline.icao_code',
                              'airline.callsign', 'airline.country',
                              'airline.active'])

src_airport = pd.read_csv(r"Data\airports.dat",
                          names=['source_airport.airport_id',
                                 'source_airport.name',
                                 'source_airport.city',
                                 'source_airport.country',
                                 'source_airport.iata_code',
                                 'source_airport.icao_code',
                                 'source_airport.latitude',
                                 'source_airport.longitude',
                                 'source_airport.altitude',
                                 'source_airport.timezone',
                                 'source_airport.DST_zone',
                                 'source_airport.tz', 'source_airport.type',
                                 'source_airport.source'])

dest_airport = pd.read_csv(r"Data\airports.dat",
                           names=['destination_airport.airport_id',
                                  'destination_airport.name',
                                  'destination_airport.city',
                                  'destination_airport.country',
                                  'destination_airport.iata_code',
                                  'destination_airport.icao_code',
                                  'destination_airport.latitude',
                                  'destination_airport.longitude',
                                  'destination_airport.altitude',
                                  'destination_airport.timezone',
                                  'destination_airport.DST_zone',
                                  'destination_airport.tz',
                                  'destination_airport.type',
                                  'destination_airport.source'])

planes = pd.read_csv(r"Data\planes.dat",
                     names=['aircraft.name', 'aircraft.iata_code',
                            'aircraft.icao_code'])

temp1 = pd.merge(routes, airlines, how="inner", left_on="airline",
                 right_on="airline.iata_code",
                 left_index=False, right_index=False)
temp2 = pd.merge(routes, airlines, how="inner", left_on="airline",
                 right_on="airline.icao_code",
                 left_index=False, right_index=False)
routes_airline = pd.concat([temp1, temp2], ignore_index=True)
routes_airline.drop_duplicates(inplace=True, keep='first')
temp1 = pd.merge(routes_airline, src_airport, how="inner",
                 left_on='src_airport',
                 right_on='source_airport.iata_code',
                 left_index=False, right_index=False)
temp2 = pd.merge(routes_airline, src_airport, how="inner",
                 left_on='src_airport',
                 right_on='source_airport.icao_code',
                 left_index=False, right_index=False)

routes_airline_src = pd.concat([temp1, temp2], ignore_index=True)
routes_airline_src.drop_duplicates(inplace=True, keep='first')


temp1 = pd.merge(routes_airline_src, dest_airport, how="inner",
                 left_on='dest_airport',
                 right_on='destination_airport.iata_code',
                 left_index=False, right_index=False)
temp2 = pd.merge(routes_airline, dest_airport, how="inner",
                 left_on='dest_airport',
                 right_on='destination_airport.icao_code',
                 left_index=False, right_index=False)

routes_airline_src_dest = pd.concat([temp1, temp2], ignore_index=True)
routes_airline_src_dest.drop_duplicates(inplace=True, keep='first')

routes_airline_src_dest['equipment'] = \
        routes_airline_src_dest['equipment'].apply(
            lambda x: x.split(' ') if type(x) == str else x)
routes_airline_src_dest = routes_airline_src_dest.explode('equipment',
                                                          ignore_index=True)


r_a_s_d_a = pd.merge(routes_airline_src_dest, planes,
                     how="inner", left_on='equipment',
                     right_on='aircraft.iata_code',
                     left_index=False, right_index=False)
r_a_s_d_a.drop(columns=['airline_id_x', 'src_airport_id',
                        'dest_airport_id', 'equipment',
                        'airline_id_y', 'airline.active',
                        'source_airport.airport_id', 'source_airport.tz',
                        'source_airport.type', 'source_airport.source',
                        'destination_airport.airport_id',
                        'destination_airport.tz',
                        'destination_airport.type',
                        'destination_airport.source'],
               inplace=True)
r_a_s_d_a.to_csv('op.csv', index=False)
