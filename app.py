import time
import redis
from flask import Flask

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

def isPrime(number):
    if number > 1:
        for i in range(2, number//2):
            if(number%i)==0:
                print(number, "is not a prime")
                return False
                break
        else:
            print(number, "is prime")
            return True
    else:
         print(number, "is not prime")
         return False;

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! Here I have been seen {} times.\n'.format(count)


@app.route('/isPrime/<int:number>')
def isitPrime(number):
    if(isPrime(number)):
        cache.rpush('primes', number)
    else:
        return;

@app.route('/primesStored')
def getStoredPrime():
    return str(cache.lrange('primes', 0, cache.llen('primes')))

