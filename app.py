import time
import redis
from flask import Flask
from math import sqrt; from itertools import count, islice

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! Here I have been seen {} times.\n'.format(count)


@app.route('/isPrime/<int:number>')
def is_it_prime_number(number):
    if number > 1 and all(number%i for i in islice(count(2), int(sqrt(number)-1))):
        cache.rpush('primes', number)
        return str(number) + " is prime"
    else:
        return str(number) + " is not prime"

@app.route('/primesStored')
def get_stored_prime():
    primes = cache.lrange('primes', 0, -1)
    message = ''
    for prime in primes:
        message += str(int(prime)) + '\n'
    return message
