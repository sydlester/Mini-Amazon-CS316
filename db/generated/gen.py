from werkzeug.security import generate_password_hash
import csv, random
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_orders = 4000 
num_carts = 1500
num_product_reviews = 500
num_seller_reviews = 500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    sellers = []
    with open('users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address() 
            balance = 0
            isSeller = fake.random_element(elements = ('true', 'false'))
            if isSeller == 'true':
                sellers.append(uid)
            writer.writerow([uid, email, password, firstname, lastname, address, balance, isSeller])
        print(f'{num_users} generated')
    return sellers


def gen_products(num_products, sellers):
    available_pids = []
    with open('products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            description = fake.sentence(nb_words =12)[:-1]
            category = fake.random_element(elements=('food', 'clothes', 'sports', 'appliances', 'random'))
            quantity = random.randint(1, 100)
            sellerId = fake.random_element(elements=sellers)
            writer.writerow([pid, name, price, available, category, description, quantity, sellerId])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_orders(num_orders, available_pids):
    with open('orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_orders):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            time_purchased = fake.date_time()
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, uid, fulfilled, time_purchased])
        print(f'{num_purchases} generated')   

    return

def gen_purchases(num_purchases, available_pids):
    with open('purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            orderId = fake.random_int(min=0, max=num_orders-1)
            userId = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=50)
            unit_price = fake.random_int(min=0, max=500)
            writer.writerow([id, orderId, userId, pid, quantity, unit_price])
        print(f'{num_purchases} generated')
    return

def gen_carts(num_carts, available_pids):
    with open('carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_carts):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            userId = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=50)
            writer.writerow([userId, pid, quantity])
        print(f'{num_purchases} generated')
    return 



def gen_product_reviews(num_product_reviews, available_pids):
    with open('productReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            userId = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            rating = fake.random_int(min=0, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            writer.writerow([userId, pid, rating, description, theDate])
        print(f'{num_purchases} generated')
    return 

def gen_seller_reviews(num_seller_reviews, sellers):
    with open('productReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            userId = fake.random_int(min=0, max=num_users-1)
            sellerId = fake.random_element(elements=sellers)
            rating = fake.random_int(min=0, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            writer.writerow([userId, sellerId, rating, description, theDate])
        print(f'{num_purchases} generated')
    return 


gen_users(num_users)
sellers = gen_users(num_users)
available_pids = gen_products(num_products, sellers)
gen_orders(num_orders, available_pids)
gen_purchases(num_purchases, available_pids)
gen_carts(num_carts, available_pids)
gen_product_reviews(num_product_reviews, available_pids)
gen_seller_reviews(num_seller_reviews, sellers)
