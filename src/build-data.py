
from source.openf1 import OpenF1
from source.base.savecsv import save_data_to_csv
from source.generate.create_timeseries import create_timeseries
from source.generate.create_telemetry import create_telemetry

client = OpenF1()

sessions = client.session_list(2024, "Race")

driver_list = client.driver_list(9488)

save_data_to_csv(sessions, "sessions")
save_data_to_csv(driver_list, "driver_list")

"""
The following variables are set after you find the data in the generated csv files
built above. Find the Driver Number in the `driver_list.csv`. Find the Session and Meeting
keys in the `sessions.csv`. Update the following variables with the correct values, and two
files will be generated for analysis.
"""

driver_number = 14 # ALO
session_key = 9558 #Silverstone
meeting_key = 1240 #British GP

create_timeseries(session_key, meeting_key, driver_number)
create_telemetry(session_key, meeting_key, driver_number)