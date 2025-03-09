import pandas as pd

from source.openf1 import OpenF1
from source.base.savecsv import save_data_to_csv

client = OpenF1()
output_file = "./data/timeseries_telemetry.csv"

def create_telemetry(session_key, meeting_key, driver_number):

    """ driver_number = 14 # ALO
    session_key = 9558 #Silverstone
    meeting_key = 1240 #British GP """

    params = {
        "driver_number": driver_number,
        "session_key": session_key,
        "meeting_key": meeting_key
    }

    DRS_MAPPING = {
        0: "DRS off",
        1: "DRS off",
        2: "?",
        3: "?",
        8: "Detected, eligible",
        9: "?",
        10: "DRS on",
        12: "DRS on",
        14: "DRS on"
    }

    session_info = client.get("sessions", {"session_key": session_key})
    car_data = client.get("car_data", params)
    laps_data = client.get("laps", params)

    df_car = pd.DataFrame(car_data)
    df_laps = pd.DataFrame(laps_data)

    session_start_time = None
    if session_info and isinstance(session_info, list) and len(session_info) > 0:
        session_start_time = pd.to_datetime(session_info[0].get("date_start"))
        session_data = session_info[0]
        session_year = pd.to_datetime(session_data.get("date_start")).year
        country_code = session_data.get("country_code", "unknown")
        session_name = session_data.get("session_name", "session").replace(" ", "_")
        output_file = f"./data/{session_year}_{country_code}_{session_name}_{driver_number}_telemetry.csv"

    if not df_car.empty:
        df_car["timestamp"] = pd.to_datetime(df_car["date"])  # Convert timestamp
        df_car["drs_status"] = df_car["drs"].map(DRS_MAPPING)  # Map DRS values

    if not df_laps.empty:
        df_laps["timestamp"] = pd.to_datetime(df_laps["date_start"])
        df_laps["timestamp"] = df_laps["timestamp"].fillna(session_start_time)
        df_laps = df_laps.sort_values("timestamp")

    df_car = pd.merge_asof(
        df_car.sort_values("timestamp"),
        df_laps[["timestamp", "lap_number"]],
            on="timestamp", direction="backward", suffixes=("", "_lap"))

    df_car["lap_number"] = df_car["lap_number"].astype("Int64")

    df_car["sector"] = None
    for index, lap in df_laps.iterrows():
        mask = df_car["lap_number"] == lap["lap_number"]
        lap_start_time = lap["timestamp"]

        if "duration_sector_1" in lap and "duration_sector_2" in lap:
            sec_1_end = lap_start_time + pd.to_timedelta(lap["duration_sector_1"], unit="s")
            sec_2_end = sec_1_end + pd.to_timedelta(lap["duration_sector_2"], unit="s")

            df_car.loc[mask & (df_car["timestamp"] < sec_1_end), "sector"] = 1
            df_car.loc[mask & (df_car["timestamp"] >= sec_1_end) & (df_car["timestamp"] < sec_2_end), "sector"] = 2
            df_car.loc[mask & (df_car["timestamp"] >= sec_2_end), "sector"] = 3


    # Save Processed Data
    df_car.to_csv(output_file, index=False)
    print(f"Telemetry dataset saved as: {output_file}")