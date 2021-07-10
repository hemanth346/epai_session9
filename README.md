# [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)

## Challenges:

- Use the Faker library to get 10000 random profiles. Using namedtuple, calculate the largest blood type, mean-current_location, oldest_person_age, and average age 


Created a Profile object using namedtuple as `Profile = namedtuple('Profile', fake.profile().keys())` which represents profile of a person using the attributes - job, company, ssn, residence, current_location, blood_group, website, username, name, sex, address, mail, birthdate

Created a list of namedtuple profiles (`Profile(**fake.profile())`)and calculated requested as below

### largest blood type
```
blood_types = [profile.blood_group for profile in profiles_namedtuples_list]
Counter(blood_types).most_common()[0]
```

### mean-current_location
```
current_locations = [profile.current_location for profile in profiles_namedtuples_list]
(
    sum(x[0] for x in current_locations)/len(current_locations), 
    sum(x[1] for x in current_locations)/len(current_locations)
)
```

### oldest_person_age
```
ages_in_days = [(datetime.datetime.now().date() - profile.birthdate).days for profile in profiles_namedtuples_list]

years, days = divmod(max(ages_in_days),365)
print(f'Oldest person age is {years} years and {days} days')
```


### average_age
```
avg_age = sum(ages_in_days) / len(ages_in_days)
years, days = divmod(int(avg_age),365)
print(f'Average age is {years} years and {days} days')
```
---

- Do the same thing above using a dictionary. Prove that namedtuple is faster.

Created a list of dict profiles (`fake.profile()`) and calculated in similar manner as above

Calculated the execution time using custom defined function for 10000 iterations. Refer module_run notebook

```
from functools import partial
def time_it(fn, *args, **kwargs):
    start = perf_counter()                
    for _ in range(10_000): 
        partial(fn, *args, **kwargs)            
    end = perf_counter()                   
    print(f'{fn.__name__} took {(end - start)*1e6} micro seconds for 10000 iterations')                                      
    return (end - start)*1e6
```

---

- Create fake data (you can use Faker for company names) for imaginary stock exchange for top 100 companies (name, symbol, open, high, close). Assign a random weight to all the companies. Calculate and show what value the stock market started at, what was the highest value during the day, and where did it end. Make sure your open, high, close are not totally random. You can only use namedtuple.


Fetched company name using `fake.company()` and symbol using below snippet to make it unique and relatable to company name. 
```
symbol = re.sub("[^a-zA-Z]+", "", company.upper())
symbol = company[0] + ''.join(random.sample(symbol, k=2))
```

Calculated open, high and close values using randm but in a way that the values are not totally random and adhere to the law
```
    open = random.randrange(100, 10000) * random.random()
    close = open + 100*random.uniform(1, -0.2)
    high = open if open > close else random.uniform(close, close+random.uniform(1,10))
```

Weights for each stock is calculated as below
```
# assigning weight - https://stackoverflow.com/a/2640067/7445772

random_weights = [random.random() for _ in range(100)]
total = sum(random_weights)
random_weights = [100*(w/total) for w in random_weights]
```

Finally calculated the stock market vaule as below 
```
start, day_high, end = 0, 0, 0
for idx, ticker in enumerate(tickers_list):
    start += ticker.open * random_weights[idx]
    day_high += ticker.high * random_weights[idx]
    end += ticker.close * random_weights[idx]

start, day_high, end = [round(x, 2) for x in [start, day_high, end]]
start, day_high, end = [x/100 for x in [start, day_high, end]]
```


