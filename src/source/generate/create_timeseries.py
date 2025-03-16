import pandas as pd

from source.openf1 import OpenF1
from source.base.savecsv import save_data_to_csv

client = OpenF1()
output_file = "./data/timeseries_sample.csv"

def create_timeseries(session_key, meeting_key, driver_number):
    """ driver_number = 14 # ALO
    session_key = 9558 #Silverstone
    meeting_key = 1240 #British GP """

    params = {
        "driver_number": driver_number,
        "session_key": session_key,
        "meeting_key": meeting_key
    }

    session_info = client.get("sessions", {"session_key": session_key})
    laps_data = client.get("laps", params)
    pits_data = client.get("pit", params)
    stints_data = client.get("stints", params)

    params.pop("driver_number", None)
    weather_data = client.get("weather", params)

    session_start_time = None
    if session_info and isinstance(session_info, list) and len(session_info) > 0:
        session_start_time = pd.to_datetime(session_info[0].get("date_start"))
        session_data = session_info[0]
        session_year = pd.to_datetime(session_data.get("date_start")).year
        country_code = session_data.get("country_code", "unknown")
        session_name = session_data.get("session_name", "session").replace(" ", "_")
        output_file = f"./data/{session_year}_{country_code}_{session_name}_{driver_number}_lap.csv"

    df_laps = pd.DataFrame(laps_data)
    df_pits = pd.DataFrame(pits_data)
    df_stints = pd.DataFrame(stints_data)
    df_weather = pd.DataFrame(weather_data)
    print(f"Weather: {len(df_weather)}")

    if not df_laps.empty:
        df_laps["timestamp"] = pd.to_datetime(df_laps["date_start"])
        df_laps["timestamp"] = df_laps["timestamp"].fillna(session_start_time)

    if df_weather.empty:
        print("No weather data found for this session!")
    else:
        df_weather["timestamp"] = pd.to_datetime(df_weather["date"])  # Convert 'date' to datetime

    if not df_weather.empty:
        df_laps = pd.merge_asof(
            df_laps.sort_values("timestamp"),
            df_weather.sort_values("timestamp"),
            on="timestamp", direction="nearest", suffixes=("", "_weather")
        )

    if not df_stints.empty:
        df_laps["stint_number"] = None
        df_laps["tyre_compound"] = None
        df_laps["tyre_age_at_start"] = None

        for index, stint in df_stints.iterrows():
            mask = (df_laps["lap_number"] >= stint["lap_start"]) & (df_laps["lap_number"] <= stint["lap_end"])
            df_laps.loc[mask, "stint_number"] = stint["stint_number"]
            df_laps.loc[mask, "tyre_compound"] = stint["compound"]
            df_laps.loc[mask, "tyre_age_at_start"] = stint["tyre_age_at_start"]

    if not df_pits.empty:
        df_pits["timestamp"] = pd.to_datetime(df_pits["date"])
        df_pits = df_pits.rename(columns={"pit_duration": "pit_stop_duration"})
        df_laps = df_laps.merge(df_pits[["lap_number", "pit_stop_duration"]],
            on="lap_number", how="left")


    for df in [df_laps, df_pits, df_weather]:
        if "date_start" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Save the dataset as CSV
    df_laps.to_csv(output_file, index=False)
    print(f"Time-series race dataset saved as: {output_file}")