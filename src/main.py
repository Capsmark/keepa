import requests
import json
import csv


def fetch_keepa_data(api_key, domain_id, category_id, range_value):
    try:
        # Construct the API endpoint URL
        url = "https://api.keepa.com/bestsellers"
        params = {
            "key": api_key,
            "domain": domain_id,
            "category": category_id,
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
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


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

        with open('./out/product_keepa_response.json', 'w') as file:
            json.dump(response_data, file, indent=4)

        # Step 2: Access the specified type of data from the response data
        if 'csv' in response_data:
            specified_data = response_data['products'][0]['csv']

            # Step 3: Save the data to a CSV file
            with open(f'{product_asin}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Price"])
                for record in specified_data:
                    writer.writerow(record)
            print(f'Data has been saved to {product_asin}_data.csv')
        else:
            print('CSV data not found in the response data.')
    except Exception as e:
        print(f'An error occurred: {e}')


def main():
    fetch_keepa_data(
        "160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r", 1, "283155", 0)
    # fetch_keepa_product_data(
    #     '160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r', 'B075ZX9G4H')


if __name__ == "__main__":
    main()
