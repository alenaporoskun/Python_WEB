import aiohttp
import asyncio
import argparse
from datetime import date, timedelta
import json
import os  # Додалимо бібліотеку os для роботи з операційною системою

API_URL = "https://api.privatbank.ua/p24api/exchange_rates"


async def fetch_exchange_rates(session, date_str):
    # Функція для виконання HTTP-запиту до API та отримання курсів валют на обрану дату
    params = {
        'json': 'true',
        'date': date_str,
    }

    async with session.get(API_URL, params=params) as response:
        data = await response.json()
        return data


async def get_currency_rates_for_days(days):
    # Функція для отримання курсів валют для кількох днів
    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(days):
            current_date = date.today() - timedelta(days=i)
            date_str = current_date.strftime("%d.%m.%Y")

            task = fetch_exchange_rates(session, date_str)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        return results


def save_to_json(data, days):
    # Функція для збереження результатів у файл JSON
    current_date = date.today().strftime("%Y-%m-%d")
    filename = f"exchange_rates_{current_date}_{days}days.json"
    filepath = os.path.join("results", filename)  # Використовуємо os.path.join для побудови шляху

    os.makedirs("results", exist_ok=True)  # Створюємо папку results, якщо вона ще не існує

    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Results saved to {filepath}")


def parse_args():
    # Функція для обробки введених аргументів з командного рядка
    parser = argparse.ArgumentParser(description='Get currency exchange rates from PrivatBank API.')
    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates for (up to 10 days)')

    return parser.parse_args()


def main():
    args = parse_args()

    if args.days > 10:
        print("Error: Number of days should not exceed 10.")
        return

    loop = asyncio.get_event_loop()
    exchange_rates = loop.run_until_complete(get_currency_rates_for_days(args.days))

    formatted_results = []

    for i, rates in enumerate(exchange_rates):
        current_date = date.today() - timedelta(days=i)
        date_str = current_date.strftime("%d.%m.%Y")

        formatted_result = {
            date_str: {
                'EUR': {
                    'sale': rates['exchangeRate'][0]['saleRateNB'],
                    'purchase': rates['exchangeRate'][0]['purchaseRateNB']
                },
                'USD': {
                    'sale': rates['exchangeRate'][1]['saleRateNB'],
                    'purchase': rates['exchangeRate'][1]['purchaseRateNB']
                }
            }
        }

        formatted_results.append(formatted_result)

    save_to_json(formatted_results, args.days)
    print(formatted_results)


if __name__ == "__main__":
    main()