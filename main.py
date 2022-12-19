# write your code here!
import requests
import json

actual_currency = ""
new_currency = ""
actual_money = 0.00
exchanged_money = 0.00
program_cache = dict()
currencies_processed = 0
n_currencies = 0


# function to save item in a cache and update it
# this json_request is a dict with its values as dicts
def save_to_cache(json_request, cache, currency):
    for key, value in json_request.items():
        if key == currency:
            for inner_key, inner_value in value.items():
                if inner_key == "rate":
                    cache[key] = inner_value
                    return cache
    # if we do not find the currency in the request, we save it with the exchange rate of 1
    cache[currency] = 1
    return cache


# function to check if a currency is in the cache
# returns the exchange rate if the currency exists
def check_cache(cache, currency):
    for key, value in cache.items():
        if key == currency:
            # Is in the cache
            print("Oh! It is in the cache!")
            return value
    # In case it does not have the currency in cache
    print("Sorry, but it is not in the cache!")
    return False


# Still have to count the number of keys in the request to check if we should still be searching or not

# First Input
actual_currency = input().lower()
actual_currency_request = requests.get(f"http://www.floatrates.com/daily/{actual_currency}.json")
actual_currency_json = json.loads(actual_currency_request.text)


# the + 1 is to save the actual currency as well
n_currencies = len(actual_currency_json) + 1

# save actual currency if not usd or eur
if actual_currency != "usd" and actual_currency != "eur":
    program_cache = save_to_cache(actual_currency_json, program_cache, actual_currency)
    currencies_processed += 1

# save usd and eur to cache
program_cache = save_to_cache(actual_currency_json, program_cache, "usd")
program_cache = save_to_cache(actual_currency_json, program_cache, "eur")
currencies_processed += 2

while currencies_processed < n_currencies:
    new_currency = input().lower()
    if new_currency == "":
        break
    actual_money = float(input())
    # Checking cache
    print("Checking the cache...")
    cache_checker = check_cache(program_cache, new_currency)
    if not cache_checker:
        program_cache = save_to_cache(actual_currency_json, program_cache, new_currency)
        currencies_processed += 1
        # access the last rate saved to cache
        exchanged_money = round(actual_money * program_cache[new_currency], 2)
    else:
        exchanged_money = round(actual_money * cache_checker, 2)
    # Exchange known
    print(f"You received {exchanged_money} {new_currency}.")
