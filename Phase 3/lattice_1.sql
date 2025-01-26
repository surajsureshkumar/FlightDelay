SELECT flight_number as flight_number_1, COUNT(*) as delay_count
INTO flights.L1
FROM flights.major_airlines
GROUP BY flight_number
HAVING COUNT(*) > 9;
