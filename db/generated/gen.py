from werkzeug.security import generate_password_hash
import csv, random
from faker import Faker
from itertools import product


num_users = 100
num_products = 100
num_purchases = 100
num_orders = 100 
num_carts = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    sellers = []
    users = [] 
    with open('db/data/users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            users.append(uid)
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
        print(f'{len(users)} is length of users')
    return sellers, users


def gen_products(num_products, sellers):
    available_pids = []
    with open('db/data/products.csv', 'w') as f:
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
    with open('db/data/orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for id in range(num_orders):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            time_purchased = fake.date_time()
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, uid, fulfilled, time_purchased])
        print(f'{num_orders} generated')   

    return

def gen_purchases(num_purchases, available_pids):
    with open('db/data/purchases.csv', 'w') as f:
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

def gen_carts(num_carts, available_pids, users):
    with open('db/data/carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        tempUsers = users.copy()
        for id in range(num_carts):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            userId = fake.random_element(elements = tempUsers)
            tempUsers.remove(userId)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=50)
            writer.writerow([userId, pid, quantity])
        print(f'{num_carts} generated')
    return 


def gen_product_reviews(num_product_reviews, available_pids, users):
    with open('db/data/productReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        temp = []
        for x in users:
            for y in available_pids:
                temp.append([x, y])

        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            
            selected = fake.random_element(elements=temp)
            userId = selected[0]
            pid = selected[1]
            temp.remove(selected)
            rating = fake.random_int(min=0, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            writer.writerow([userId, pid, rating, description, theDate])
        print(f'{num_product_reviews} generated')
    return 

def gen_seller_reviews(num_seller_reviews, sellers, users):
    with open('db/data/sellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        
        temp = []
        for x in users:
            for y in available_pids:
                temp.append([x, y])

        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
        
        
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            
            selected = fake.random_element(elements=temp)
            userId = selected[0]
            sellerId = selected[1]
            temp.remove(selected)
            rating = fake.random_int(min=0, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            writer.writerow([userId, sellerId, rating, description, theDate])
        print(f'{num_seller_reviews} generated')
    return 


sellers, users = gen_users(num_users)
available_pids = gen_products(num_products, sellers)
gen_orders(num_orders, available_pids)
gen_purchases(num_purchases, available_pids)
gen_carts(num_carts, available_pids, users)

num_product_reviews = len(available_pids)*len(users)
num_seller_reviews = len(sellers)*len(users)

gen_product_reviews(num_product_reviews, available_pids, users)
gen_seller_reviews(num_seller_reviews, sellers, users)
