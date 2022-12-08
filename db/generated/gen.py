from werkzeug.security import generate_password_hash
import csv, random
from faker import Faker
from itertools import product

num_users = 100
num_products = 100
num_purchases = 100
num_carts = 100

Faker.seed(0)
fake = Faker()

images = ['apple.png', 'banana.png', 'detergent.png', 'gloves.png', 'keurig.png', 'legos.png', 'soccer.png', 'sweater.png', 'sweatshirt.png', 'tennis.png']

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
    names = []
    with open('db/data/products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for x in range(int(num_products/4)):
            names.append(fake.sentence(nb_words=4)[:-1])
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.random_element(elements=names)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            description = fake.sentence(nb_words =12)[:-1]
            category = fake.random_element(elements=('Food', 'Clothes', 'Sports', 'Appliances', 'Random'))
            quantity = random.randint(1, 100)
            sellerId = fake.random_element(elements=sellers)
            theImage = fake.random_element(elements=images)
            writer.writerow([pid, name, price, available, category, description, quantity, sellerId, theImage])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_purchases(num_purcahses, available_pids):
    with open('db/data/purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purcahses):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=50)
            unit_price=  fake.random_int(min=0, max=500)
            time_ordered= fake.date_time()
            fulfilled = fake.random_element(elements=('true', 'false'))
            if fulfilled: 
                time_fulfilled = fake.date_time()
            else:
                time_fulfilled = None
            writer.writerow([id, uid, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled])
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
            rating = fake.random_int(min=1, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            theImage = fake.random_element(elements=images)
            upvotes = fake.random_int(min=0, max=num_users)
            writer.writerow([userId, pid, rating, description, theDate, theImage, upvotes])
        print(f'{num_product_reviews} generated')
    return 

def gen_seller_reviews(num_seller_reviews, sellers, users):
    with open('db/data/sellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        
        temp2 = []
        for x in users:
            for y in sellers:
                temp2.append([x, y])

        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
        
        
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            
            selected = fake.random_element(elements=temp2)
            userId = selected[0]
            sellerId = selected[1]
            temp2.remove(selected)
            rating = fake.random_int(min=1, max=5)
            description = fake.sentence(nb_words =12)[:-1]
            theDate = fake.date_time()
            theImage = fake.random_element(elements=images)
            upvotes = fake.random_int(min=0, max=num_users)
            writer.writerow([userId, sellerId, rating, description, theDate, theImage, upvotes])
        print(f'{num_seller_reviews} generated')
    return 


def coupons():
    with open('db/data/coupons.csv', 'w') as f:
        writer = get_csv_writer(f)
        writer.writerow(["123456", .1])
    return 


sellers, users = gen_users(num_users)
available_pids = gen_products(num_products, sellers)
gen_purchases(num_purchases, available_pids)
gen_carts(num_carts, available_pids, users)

num_product_reviews = len(available_pids)*len(users)
num_seller_reviews = len(sellers)*len(users)

gen_product_reviews(num_product_reviews, available_pids, users)
gen_seller_reviews(num_seller_reviews, sellers, users)
coupons()