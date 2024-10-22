-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Finds the crime scene report to get clues on where to start
SELECT description FROM crime_scene_reports
WHERE street = 'Humphrey Street' AND month = 7 AND day = 28;
-- Key details:
-- Time: 10:15am
-- Place: Bakery
-- Witnesses: 3

-- Gets a list of interviews from witnesses
SELECT transcript FROM interviews
WHERE month = 7 AND day = 28;
-- Key details:
-- Thief drove off within 10 minutes of the theft (10:15am - 10:25am)
-- Thief was withdrawing money from an ATM on Leggett Street, witness claimed thief was recognised
-- Thief called someone for less than a minute as he was leaving the bakery
-- Thief said they planned to take the earliest flight out of 50Ville on the 29th of July
-- Thief asked the person they were calling to purchase the flight ticket

-- Gets a list bank accounts that had atm transactions from the ATM at Leggett Street on the day of the theft
WITH leggett_street_bank_accounts AS (
    SELECT account_number, transaction_type, amount FROM atm_transactions
    WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street'
),
-- Gets a list of cars that exited the bakery between the suspected times of 10:15am - 10:25am
bakery_cars AS (
    SELECT activity, license_plate, minute FROM bakery_security_logs
    WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute <= 25
),
-- Gets a list of phone calls that are less than one minute in duration on the day of the theft
short_phone_calls AS (
    SELECT caller, receiver, duration FROM phone_calls
    WHERE month = 7 AND day = 28 AND duration <= 60
),
-- Gets the earliest flight out from Fiftyville airport on the 29th of July
earliest_flight_out AS (
    SELECT flights.id, origin_airport_id, destination_airport_id FROM flights
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE day = 29 AND month = 7 AND airports.city = "Fiftyville"
    ORDER BY hour ASC, minute ASC
    LIMIT 1
),
-- Gets the thief and his details
thief_details AS (
    SELECT people.name, people.license_plate, people.passport_number, people.phone_number
    FROM bank_accounts
    JOIN people ON people.id = bank_accounts.person_id
    JOIN bakery_cars ON people.license_plate = bakery_cars.license_plate
    JOIN short_phone_calls ON people.phone_number = short_phone_calls.caller
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN earliest_flight_out ON passengers.flight_id = earliest_flight_out.id
    WHERE account_number IN (SELECT account_number FROM leggett_street_bank_accounts)
)

-- Gets the thief's destination
SELECT destination.city FROM earliest_flight_out
JOIN airports AS destination ON destination.id = earliest_flight_out.destination_airport_id;

-- Gets the accomplice, the person the thief was calling
SELECT people.name, people.license_plate, people.passport_number, people.phone_number FROM thief_details
JOIN short_phone_calls ON thief_details.phone_number = short_phone_calls.caller
JOIN people ON people.phone_number = short_phone_calls.receiver;
