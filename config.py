from dotenv import dotenv_values

config = dotenv_values('.env')
PASSWORD = config['SECRET_CODE']
STATION_CONNECTION = config['STATION_CONNECTION']
DRONE_CONNECTION = config['DRONE_CONNECTION']