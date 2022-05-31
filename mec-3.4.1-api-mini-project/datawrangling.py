import os
from dotenv import load_dotenv  # if missing this module, simply run `pip install python-dotenv`
import requests
import pandas as pd



def get_api_key():
    load_dotenv()
    api_key = os.getenv('NASDAQ_API_KEY')
    # print(api_key)
    return api_key


def get_data(api_url, api_params):
    try:
        response = requests.get(api_url, params=api_params)
        if response.ok:
            print(response.json())
            return response.json()
        else:
            print("Failed to call dataset api.  Error = ", response)
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        raise SystemExit(e)


def process_response_using_pandas(response):
    print("*** Processing with Pandas")

    # create dataframe from dictionary
    df = pd.DataFrame(response["dataset_data"]["data"], columns=response["dataset_data"]["column_names"])
    print(df)

    # Calculate what the highest and lowest opening prices were for the stock in this period.
    highest_opening = df["Open"].max()
    lowest_opening = df["Open"].min()
    print("Highest Opening = ", highest_opening, " Lowest Opening = ", lowest_opening)

    # What was the largest change in any one day (based on High and Low price)?
    largest_change = (df["High"] - df["Low"]).max()
    print("Largest Change = ", largest_change)

    # What was the largest change between any two days (based on Closing Price)?
    largest_two_day_change = df["Close"].diff().max()
    print("Largest two day change = ", largest_two_day_change)

    # What was the average daily trading volume during this year?
    average_traded_volume = df["Traded Volume"].mean()
    print("Average Traded Volume = ", average_traded_volume)

    # (Optional) What was the median trading volume during this year. (Note: you may need to implement your own
    # function for calculating the median.)
    median_traded_volume = df["Traded Volume"].median()
    print("Median Traded Volume = ", median_traded_volume)


def process_response_without_pandas(response):
    print("**** Processing without pandas")

    data = response["dataset_data"]["data"]
    # this is a list of lists so let's try and iterate
    highest_opening = 0.0
    lowest_opening = 0.0
    largest_change = 0.0
    largest_two_day_change = 0.0
    prev_close = 0.0
    average_traded_volume = 0.0
    number_of_traded_days = 0.0
    median_traded_days_list = []
    median_traded_volume = 0.0
    for data_item in data:
        # print(data_item)
        # calculate highest and lowest opening

        if data_item[1] is not None:
            if highest_opening == 0.0:
                highest_opening = data_item[1]
            else:
                if highest_opening < data_item[1]:
                    highest_opening = data_item[1]
            if lowest_opening == 0.0:
                lowest_opening = data_item[1]
            else:
                if lowest_opening > data_item[1]:
                    lowest_opening = data_item[1]

            # calculate largest intraday change
            if data_item[2] is not None and data_item[3] is not None:
                if largest_change == 0.0:
                    largest_change = data_item[2] - data_item[3]
                else:
                    if largest_change < data_item[2] - data_item[3]:
                        largest_change = data_item[2] - data_item[3]

            # calculate the largest two day change
            if data_item[4] is not None:
                if prev_close != 0.0:
                    if largest_two_day_change == 0.0:
                        largest_two_day_change = data_item[4] - prev_close
                    elif largest_two_day_change < data_item[4] - prev_close:
                        largest_two_day_change = data_item[4] - prev_close
                prev_close = data_item[4]

            # calculate average traded volume
            if data_item[6] is not None:
                average_traded_volume += data_item[6]
                number_of_traded_days += 1
                # accumulate new list for median
                median_traded_days_list.append(data_item[6])

    # let's try and calculate median now
    median_traded_days_list.sort()
    if len(median_traded_days_list) % 2 != 0:
        # odd number of items in the list
        median_index = int((len(median_traded_days_list) + 1) / 2 - 1)
        median_traded_volume = median_traded_days_list[median_index]
    else:
        median_index1 = int(len(median_traded_days_list) / 2 - 1)
        median_index2 = int(len(median_traded_days_list) / 2)
        median_traded_volume = (median_traded_days_list[median_index1] + \
                                median_traded_days_list[median_index2]) / 2.0

    print("highest opening = ", highest_opening, "lowest opening = ", lowest_opening)
    print("largest change = ", largest_change)
    print("largest two day change = ", largest_two_day_change)
    print("*** Not sure why it does not match pandas output --> average traded volume = ",
          average_traded_volume / number_of_traded_days, "avg with len = ", average_traded_volume / len(data))
    print("*** Not sure why it does not match pandas output --> median = ", median_traded_volume)


def main():
    print("main")

    # setup parameters to API
    api_parameters = {'api_key': get_api_key(), 'start_date': '2017-01-01', 'end_date': '2017-12-31'}
    api_url = "https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X/data.json";

    # Collect data from the Frankfurt Stock Exchange, for the ticker AFX_X, for the whole year
    # 2017 (keep in mind that the date format is YYYY-MM-DD).

    response = get_data(api_url, api_parameters)
    # Convert the returned JSON object into a Python dictionary.
    print(type(response))

    process_response_using_pandas(response)
    process_response_without_pandas(response)


if __name__ == "__main__":
    main()
