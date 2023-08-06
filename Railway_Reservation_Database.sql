CREATE TABLE users (
    username  VARCHAR(10) primary key ,
    password VARCHAR(20),
    name VARCHAR(50),
    gender VARCHAR(8),
    age INT,
    mobile BIGINT,
    email VARCHAR(75),
    address VARCHAR(150)
);
CREATE TABLE tickets (
    pnr VARCHAR(12) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    selected_quota VARCHAR(20),
    date_of_journey DATE,
    boarding VARCHAR(50),
    destination VARCHAR(50),
    email_id VARCHAR(100) DEFAULT NULL,
    total_fare DECIMAL(10, 2) DEFAULT NULL,
    p1_name VARCHAR(50),
    p1_gender CHAR(5),
    p1_age INT,
    p1_phone VARCHAR(20),
    p1_address VARCHAR(100),
    p2_name VARCHAR(50) DEFAULT NULL,
    p2_gender CHAR(5) DEFAULT NULL,
    p2_age INT DEFAULT NULL,
    p3_name VARCHAR(50) DEFAULT NULL,
    p3_gender CHAR(5) DEFAULT NULL,
    p3_age INT DEFAULT NULL,
    p4_name VARCHAR(50) DEFAULT NULL,
    p4_gender CHAR(5) DEFAULT NULL,
    p4_age INT DEFAULT NULL,
    p5_name VARCHAR(50) DEFAULT NULL,
    p5_gender CHAR(5) DEFAULT NULL,
    p5_age INT DEFAULT NULL,
    p6_name VARCHAR(50) DEFAULT NULL,
    p6_gender CHAR(5) DEFAULT NULL,
    p6_age INT DEFAULT NULL,
    p1_seat VARCHAR(10) DEFAULT NULL,
    p2_seat VARCHAR(10) DEFAULT NULL,
    p3_seat VARCHAR(10) DEFAULT NULL,
    p4_seat VARCHAR(10) DEFAULT NULL,
    p5_seat VARCHAR(10) DEFAULT NULL,
    p6_seat VARCHAR(10) DEFAULT NULL
    
);
alter table tickets
add column p1_status varchar (5) default null ,
add column p2_status varchar (5) default null ,
add column p3_status varchar (5) default null ,
add column p4_status varchar (5) default null ,
add column p5_status varchar (5) default null ,
add column p6_status varchar (5) default null ;

alter table tickets
add column tob datetime;

drop table tickets;

select * from tickets
order by tob DESC;



