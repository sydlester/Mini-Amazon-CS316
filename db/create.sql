-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address varchar(255) NOT NULL,
    balance FLOAT NOT NULL DEFAULT 0,
    isSeller BOOLEAN DEFAULT FALSE
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    category varchar(255),
    theDescription varchar(255),
    quantity INT NOT NULL,
    sellerId INT NOT NULL REFERENCES USERS(id),
    theImage VARCHAR(2048) NOT NULL


);

CREATE TABLE Orders (
    orderId INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    userId INT NOT NULL REFERENCES Users(id),
    fulfilled BOOLEAN NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    orderId INT NOT NULL REFERENCES Orders(orderid),
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    unit_price FLOAT NOT NULL
);

CREATE TABLE Carts (
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (userId, pid)
);

CREATE TABLE ProductReviews(
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    rating FLOAT NOT NULL CHECK(rating>=0 AND rating <= 5),
    theDescription varchar(512),
    theDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    primary key (userId, pid)
);

CREATE TABLE SellerReviews(
    userId INT NOT NULL REFERENCES Users(id),
    sellerId INT NOT NULL REFERENCES Users(id),
    rating FLOAT NOT NULL CHECK(rating>=0 AND rating <= 5),
    theDescription varchar(512),
    theDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    primary key (userId, sellerId)
)