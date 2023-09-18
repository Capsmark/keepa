import requests
import json


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


def main():
    fetch_keepa_data(
        "160gfpn5t9g8sqt0m239kdpg1fcutu85q667od7q96b8csvgaeqc8ktndl8ial9r", 1, "283155", 0)


if __name__ == "__main__":
    main()
