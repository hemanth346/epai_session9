from time import perf_counter

import datetime
from faker import Faker
from collections import namedtuple
from collections import Counter
import random
import re

fake = Faker()

# AGE_REFERENCE = datetime.datetime.strptime('09072021', "%d%m%Y").date()


def get_namedtuple_profiles(n=10_000):
    """
    Returns a list of namedtuples with profile details
    """
    Profile = namedtuple('Profile', fake.profile().keys())
    Profile.__doc__ = """Represents profile of a person using the attributes - 
    job, company, ssn, residence, current_location, blood_group, website, username, 
    name, sex, address, mail, birthdate
    """
    profiles_namedtuples_list = []

    for i in range(n):
        profiles_namedtuples_list.append(Profile(**fake.profile()))

    return profiles_namedtuples_list


def get_largest_blood_type_nt(profiles_namedtuples_list):
    """
    get_largest_blood_type from namedtuple 
    """
    # largest blood type
    blood_types = [profile.blood_group for profile in profiles_namedtuples_list]
    return Counter(blood_types).most_common()[0]


def get_mean_current_location_nt(profiles_namedtuples_list):
    """
    Get mean-current_location from named tuple
    """
    # mean-current_location
    current_locations = [profile.current_location for profile in profiles_namedtuples_list]
    return (
        sum(x[0] for x in current_locations)/len(current_locations), 
        sum(x[1] for x in current_locations)/len(current_locations)
        )


def get_oldest_person_age_nt(profiles_namedtuples_list):
    """
    oldest_person_age via namedtuple
    """
    ages_in_days = [(datetime.datetime.now().date() - profile.birthdate).days for profile in profiles_namedtuples_list]
    # oldest_person_age
    years, days = divmod(max(ages_in_days),365)
    print(f'Oldest person age is {years} years and {days} days')
    return max(ages_in_days)
    

def get_average_age_nt(profiles_namedtuples_list):
    """
    average_age via namedtuple
    """
    ages_in_days = [(datetime.datetime.now().date() - profile.birthdate).days for profile in profiles_namedtuples_list]
    # average_age
    avg_age = sum(ages_in_days) / len(ages_in_days)
    years, days = divmod(int(avg_age),365)
    print(f'Average age is {years} years and {days} days')
    return (int(avg_age))


# ### Using dicts


def get_dict_profiles(n=10_000):
    """
    Returns a list of dicts with profile details
    """
    profiles_dict_list = []

    for i in range(10_000):
        profiles_dict_list.append(fake.profile())

    return profiles_dict_list


def get_largest_blood_type_dt(profiles_dict_list):
    """
    get_largest_blood_type from dict 
    """
    # largest blood type
    blood_types = [profile['blood_group'] for profile in profiles_dict_list]
    return Counter(blood_types).most_common()[0]



def get_mean_current_location_dt(profiles_dict_list):
    """
    Get mean-current_location from dict
    """
    # mean-current_location
    current_locations = [profile['current_location'] for profile in profiles_dict_list]
    return (
        sum(x[0] for x in current_locations)/len(current_locations), 
        sum(x[1] for x in current_locations)/len(current_locations)
    )


def get_oldest_person_age_dt(profiles_dict_list):
    """
    oldest_person_age via namedtuple
    """
    ages_in_days = [(datetime.datetime.now().date() - profile['birthdate']).days for profile in profiles_dict_list]

    # oldest_person_age
    years, days = divmod(max(ages_in_days),365)
    print(f'Oldest person age is {years} years and {days} days')
    return max(ages_in_days)


def get_average_age_dt(profiles_dict_list):
    """
    average_age via namedtuple
    """
    ages_in_days = [(datetime.datetime.now().date() - profile['birthdate']).days for profile in profiles_dict_list]
    # average_age
    avg_age = sum(ages_in_days) / len(ages_in_days)
    years, days = divmod(int(avg_age),365)
    print(f'Average age is {years} years and {days} days')
    return (int(avg_age))



def get_tickers(n=100):
    Ticker = namedtuple('Ticker', 'name symbol open high close')
    tickers_list = []
    for i in range(n):
        company = fake.company()
        symbol = re.sub("[^a-zA-Z]+", "", company.upper())
        symbol = company[0] + ''.join(random.sample(symbol, k=2))
        open = random.randrange(100, 10000) * random.random()
        close = open + 100*random.uniform(1, -0.2)
        high = open if open > close else random.uniform(close, close+random.uniform(1,10))
        tickers_list.append(Ticker(company, symbol, round(open, 2), round(high, 2), round(close, 2)))
    return tickers_list


def get_stock_weights():
    # assigning weight - https://stackoverflow.com/a/2640067/7445772
    random_weights = [random.random() for _ in range(100)]
    total = sum(random_weights)
    random_weights = [100*(w/total) for w in random_weights]
    return random_weights


def get_day_values(tickers_list, stock_weights):
    start, day_high, end = 0, 0, 0
    for idx, ticker in enumerate(tickers_list):
        start += ticker.open * stock_weights[idx]
        day_high += ticker.high * stock_weights[idx]
        end += ticker.close * stock_weights[idx]

    start, day_high, end = [round(x, 2) for x in [start, day_high, end]]
    start, day_high, end = [x/100 for x in [start, day_high, end]]
    return start, day_high, end


# def average_time(structure, test_func):
#     time_measurements = []
#     for _ in range(10_000):
#         start = perf_counter()
#         test_func(structure)
#         end = perf_counter()
#         time_measurements.append(end - start)
#     return sum(time_measurements) / len(time_measurements) * int(1e9) # convert to nanoseconds



from functools import wraps
# decorator to calculate execution time of given funciton
def timeit(fn):
    """
    decorator to calculate execution time of given funciton
    """
    @wraps(fn)                   
    def wrapper(*args, **kwargs):
        start = perf_counter()                
        for _ in range(10_000): 
            fn(*args, **kwargs)                   
        end = perf_counter()                   
        print(f'{fn.__name__} took {end - start} seconds')                                      
    return wrapper


def timer():
    """
    Calculate execution time of input function call
    """
    
