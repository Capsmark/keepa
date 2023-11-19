import json


def get_asin_numbers():
    with open('../out/results_7141123011.json', 'r') as file:
        data = json.load(file)

    return data


def main():
    print(len(get_asin_numbers()))


main()
