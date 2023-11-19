from datetime import datetime
import requests
import json
import csv
import os


def get_asin_numbers():
    with open('./out/results_7141123011.json', 'r') as file:
        data = json.load(file)

    return data


def check_file_exists(directory, filename):
    filepath = os.path.join(directory, filename)
    return os.path.exists(filepath)


def fetch_keepa_data(api_key, domain_id, category_id, range_value):
    try:
        # Construct the API endpoint URL
        url = "https://api.keepa.com/bestsellers"
        params = {
            "key": api_key,
            "domain": domain_id,
            "category": category_id,
            "range": range_value
        }

        # Make the request to the Keepa API
        response = requests.get(url, params=params)

        # Raise exception for HTTP errors
        response.raise_for_status()

        # Get the JSON data from the response
        data = response.json()

        # Save the data to a JSON file
        with open('./out/keepa_response.json', 'w') as file:
            json.dump(data, file, indent=4)

        print("Data saved to keepa_response.json")

        return data['bestSellersList']['asinList']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Function to convert Keepa time to human-readable date


def convert_to_human_readable(keepa_time):
    uncompressed_time = (keepa_time + 21564000) * 60
    return datetime.utcfromtimestamp(uncompressed_time).strftime('%Y-%m-%d %H:%M:%S')


# Convert human-readable date to Keepa Time


def convert_to_keepa_time(date_string):
    human_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    keepa_time = (human_time.timestamp() // 60) - 21564000
    return int(keepa_time)


def save_rank_data_to_csv(salesRanks):
    for category_id, data in salesRanks.items():
        if data:
            with open(f'{category_id}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Value"])
                for i in range(0, len(data), 2):
                    if i + 1 < len(data):
                        timestamp = convert_to_human_readable(data[i])
                        value = data[i + 1]
                        writer.writerow([timestamp, value])
            print(f'Data has been saved to {category_id}_data.csv')


def save_data_to_csv(product_asin, specified_data):
    index_names = [
        "AMAZON", "NEW", "USED", "SALES", "LISTPRICE", "COLLECTIBLE",
        "REFURBISHED", "NEW_FBM_SHIPPING", "LIGHTNING_DEAL", "WAREHOUSE",
        "NEW_FBA", "COUNT_NEW", "COUNT_USED", "COUNT_REFURBISHED", "COUNT_COLLECTIBLE",
        "EXTRA_INFO_UPDATES", "RATING", "COUNT_REVIEWS", "BUY_BOX_SHIPPING",
        "USED_NEW_SHIPPING", "USED_VERY_GOOD_SHIPPING", "USED_GOOD_SHIPPING",
        "USED_ACCEPTABLE_SHIPPING", "COLLECTIBLE_NEW_SHIPPING", "COLLECTIBLE_VERY_GOOD_SHIPPING",
        "COLLECTIBLE_GOOD_SHIPPING", "COLLECTIBLE_ACCEPTABLE_SHIPPING", "REFURBISHED_SHIPPING",
        "EBAY_NEW_SHIPPING", "EBAY_USED_SHIPPING", "TRADE_IN", "RENTAL", "BUY_BOX_USED_SHIPPING",
        "PRIME_EXCL"
    ]

    # Save the data to multiple CSV files based on the index
    for index, data in enumerate(specified_data):
        if data is not None:
            with open(f'./csv/{product_asin}_{index_names[index]}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Value"])
                for i in range(0, len(data), 2):
                    if i + 1 < len(data):
                        timestamp = convert_to_human_readable(data[i])
                        value = data[i + 1]
                        writer.writerow([timestamp, value])
    print(
        f'Data has been saved to multiple CSV files with prefix {product_asin}')


def fetch_keepa_product_data(api_key, product_asin, data_type=0):
    """
    Fetches product data from Keepa API and saves the specified type of data to a CSV file.

    Args:
    api_key (str): Your Keepa API key
    product_asin (str): ASIN of the product
    data_type (int): The type of data to fetch. Default is 0 (Amazon price history).

    Returns:
    None
    """

    try:
        # Step 1: Make an API call to Keepa API with necessary parameters
        response = requests.get(
            f'https://api.keepa.com/product?key={api_key}&domain=1&asin={product_asin}')
        response_data = response.json()

        with open(f'./out/products/{product_asin}.json', 'w') as file:
            json.dump(response_data, file, indent=4)

        # # Step 2: Access the specified type of data from the response data
        # specified_data = response_data['products'][0]['csv']
        #
        # # Step 3: Calling function to save data to CSV
        # save_data_to_csv(product_asin, specified_data)
        #
        # specified_rank_data = response_data['products'][0]['salesRanks']
        #
        # save_rank_data_to_csv(specified_rank_data)

    except Exception as e:
        print(f'An error occurred: {e}')


def fetch_products(rootCategory, trackingSince_lte_date, access_key, domain_id):
    base_url = "https://api.keepa.com/query?domain={}&key={}"

    # Convert human-readable date to Keepa Time
    trackingSince_lte = convert_to_keepa_time(trackingSince_lte_date)

    results = []
    page = 0
    per_page = 1000

    while True:
        query_json = {
            "rootCategory": rootCategory,
            # "categories_include": [3741181],
            "current_COUNT_REVIEWS_gte": 1000,
            "current_AMAZON_gte": 10,
            "trackingSince_lte": trackingSince_lte,
            "perPage": per_page,
            "page": page
        }

        response = requests.post(base_url.format(
            domain_id, access_key), json=query_json)
        data = response.json()

        try:
            results.extend(data['asinList'])

            if len(data["asinList"]) < per_page:
                print(f"Total Results : {data['totalResults']}")
                break
        except KeyError:
            # Handle the case when "asinList" key is missing
            print("No More Data Available")
            break
        page += 1

    # Save to JSON file
    with open(f'./out/results_{rootCategory}.json', 'w') as f:
        json.dump(results, f)

    print(f"Results saved in results_{rootCategory}.json")
    print("Total results:", len(results))


def main():
    asins = get_asin_numbers()

    for id in asins:
        directory_path = './out/products'
        file_name_to_check = f'{id}.json'

        if check_file_exists(directory_path, file_name_to_check):
            print(f"The file '{file_name_to_check}' exists in the directory.")
            continue
        print(f"Fetching: '{file_name_to_check}'")
        fetch_keepa_product_data('160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r', id)


# access_key = "160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r"
# domain_id = 1
# rootCategory = 228013
# trackingSince_lte_date = "2014-01-01 00:00:00"
# fetch_products(rootCategory, trackingSince_lte_date, access_key, domain_id)


# asnList = fetch_keepa_data(
#     "160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r", 1, "1055398", 180)

# fetch_keepa_product_data(
#     '160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r', 'B00OHUQN3M')
# fetch_keepa_data(
#     "160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r", 1, "283155", 0)
# fetch_keepa_product_data(
#     '160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r', '150118315X')


if __name__ == "__main__":
    main()
