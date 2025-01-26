import pandas as pd

routes = pd.read_csv("op.csv")
delays = pd.read_csv(r"Data\delays.csv", header=0,
                     names=['index', 'flight_date', 'airline_code',
                            'flight_number', 'source',
                            'destination', 'scheduled_departure',
                            'actual_departure', 'departure_delay',
                            'TAXI_OUT', 'WHEELS_OFF', 'WHEELS_ON', 'TAXI_IN',
                            'scheduled_arrival', 'actual_arrival',
                            'arrival_delay', 'CANCELLED',
                            'CANCELLATION_CODE', 'DIVERTED',
                            'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME',
                            'AIR_TIME', 'DISTANCE', 'CARRIER_DELAY',
                            'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY',
                            'LATE_AIRCRAFT_DELAY', 'Unnamed: 27'],
                     usecols=['airline_code', 'flight_number', 'source',
                              'destination'])

routes_delay = pd.merge(routes, delays,
                        how="inner",
                        left_on=["src_airport", "dest_airport", "airline"],
                        right_on=["source", "destination", "airline_code"],
                        left_index=False, right_index=False)

routes_delay.drop(columns=["src_airport", "dest_airport", "airline",
                           'airline_code', 'source', 'destination'],
                  inplace=True)
routes_delay.drop_duplicates(inplace=True)
routes_delay.to_csv('final.csv', index=False)
