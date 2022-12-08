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
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    category varchar(255),
    theDescription varchar(255),
    quantity INT NOT NULL,
    sellerId INT NOT NULL REFERENCES USERS(id),
    theImage VARCHAR(2048) 
);

CREATE TABLE Purchases (
    id INT NOT NULL,
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL,
    quantity INT NOT NULL,
    unit_price FLOAT NOT NULL,
    time_ordered timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    fulfilled BOOLEAN NOT NULL,
    time_fulfilled timestamp without time zone DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (id, userId, pid)
);

CREATE TABLE Carts (
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (userId, pid)
);

CREATE TABLE Saved (
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    PRIMARY KEY (userId, pid)
);

CREATE TABLE ProductReviews(
    userId INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    rating FLOAT NOT NULL CHECK(rating>0 AND rating <= 5),
    theDescription varchar(512),
    theDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    theImage VARCHAR(2048),
    upvotes INT NOT NULL,
    primary key (userId, pid)
);

CREATE TABLE SellerReviews(
    userId INT NOT NULL REFERENCES Users(id),
    sellerId INT NOT NULL REFERENCES Users(id),
    rating FLOAT NOT NULL CHECK(rating>0 AND rating <= 5),
    theDescription varchar(512),
    theDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    theImage VARCHAR(2048),
    upvotes INT NOT NULL,
    primary key (userId, sellerId)
);

CREATE TABLE Messages(
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    sender INT NOT NULL REFERENCES Users(id),
    recipient INT NOT NULL REFERENCES Users(id),
    content varchar(512),
    theTime timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE FulFilledPurchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    purchaseId INT NOT NULL
);