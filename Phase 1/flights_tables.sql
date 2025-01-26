create table flights.airlines
(
    airline_id   integer not null
        constraint airlines_pk
            primary key,
    airline_name varchar,
    alias        varchar,
    "IATA_code"  varchar not null,
    "ICAO_code"  varchar not null,
    callsign     varchar,
    country      varchar,
    active       varchar
);



create table flights."Airport"
(
    airport_id   integer not null
        constraint airport
            primary key,
    airline_name varchar,
    city         varchar,
    country      varchar,
    "IATA_code"  varchar not null,
    "ICAO_code"  varchar not null,
    latitude     integer,
    longitude    integer,
    altitude     integer,
    timezone     integer,
    "DST_zone"   varchar
);


create table flights.countries
(
    country_name integer,
    iso_code     varchar not null,
    country_id   integer not null
        constraint countries_pk
            primary key
);


create table flights.planes
(
    aircraft_name varchar,
    "IATA_code"   varchar,
    "ICAO_code"   varchar,
    plane_id      integer not null
        constraint planes_pk
            primary key
);


create table flights.routes
(
    airline        integer,
    id             integer
        constraint routes_airlines_airline_id_fk
            references flights.airlines,
    source         integer,
    source_id      integer,
    destination_id integer,
    codeshare      integer,
    stops          integer,
    equipment      integer
);


create table flights.airlines_aircrafts
(
    airlines_id integer
        constraint airlines_aircrafts_airlines_airline_id_fk
            references flights.airlines,
    plane_id    integer
        constraint airlines_aircrafts_planes_plane_id_fk
            references flights.planes
);


create table flights.countries_airport
(
    airport_id integer
        constraint countries_airport_fk
            references flights."Airport",
    country_id integer
        constraint country_id_fk
            references flights.countries
);
