import pandas as pd 

def calculate(df):
    down_timestamp = None
    down_duration = 0

    for index, row in df.iterrows():
        timestamp = row["Epoch Time"]
        status = row["Value"]

        if status == 1 and down_timestamp is None:
            down_timestamp = timestamp
        elif status == 0 and down_timestamp is not None:
            down_duration += timestamp - down_timestamp
            down_timestamp = None 

    if down_timestamp is not None:
        down_duration += df.iloc[-1]["Epoch Time"] - down_timestamp


    down_duration_seconds = down_duration / 1000
    return down_duration_seconds


if __name__ == "__main__":
    #read file
    df = pd.read_csv("device_network_data.csv", na_values=["Null",""])

    #replace null values with previous non null value
    df["Value"] = df["Value"].ffill()

    #calculate total down time
    down_duration = calculate(df)

    print("Total down time is {} seconds".format(down_duration))