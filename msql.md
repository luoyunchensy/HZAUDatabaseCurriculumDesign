# 数据库课程设计代码

## mysql

```sql
create database youyiku;
use youyiku;
create table test(
    idx int primary key
);


create table Costume(
    CID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    CName VARCHAR(20) not null,
    CType VARCHAR(20) not null,
    CTag VARCHAR(20),
    UPrice decimal(8,2) not null check (UPrice > 0 and UPrice <= 1000000),
    Material varchar(20) not null,
    Color varchar(20) not null,
    Size ENUM('S','M','L','XL','XXL','均码') not null,
    AddDate DATETIME not null,
    Sales INT DEFAULT 0,
    Status varchar(10) DEFAULT '库存充足',
    PicPath varchar(255),
    Descrip varchar(255)
)AUTO_INCREMENT = 1001;

INSERT INTO Costume(CName, CType, CTag, UPrice, Material, Color, Size, AddDate, Sales, Status, PicPath, Descrip) VALUES ('高腰中長半身裙','裙子',null,'99.81','棉','珊瑚橙','S',now(),default,default,'https://static.zara.net/photos///2023/I/0/1/p/4088/250/615/12/w/1126/4088250615_1_1_1.jpg?ts=1697803373266','这是一条好裙子');




create table User(
    UID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Uname varchar(20) not null,
    UPass varchar(20) not null,
    UAdress varchar(255) not null,
    UTele varchar(20) not null

)Auto_Increment = 1000000;

INSERT into User (Uname, UPass, UAdress, UTele) values ('wjs','jj1cm','成都','13086395513');




Drop table Employee;
Create table Employee (
    EID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Ename varchar(20) not null,
    EPass varchar(20) not null,
    Level enum('仓库管理员','订单管理员','服装管理员','员工管理员') not null,
    Etele varchar(20) not null,
    EAdress varchar(255) not null
)AUTO_INCREMENT = 1;


INSERT into Employee(Ename, EPass, Level, Etele, EAdress) VALUES ('宋毅','123','员工管理员','19189011557','贵州贵阳');


CREATE table Inventory(
    IID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    CID int UNSIGNED,
    Stock int not null check(Stock>=0),
    WNO int not null check(WNO<=10),
    SNO int not null check(SNO<=100),
    FOREIGN KEY (CID) REFERENCES Costume(CID)
)AUTO_INCREMENT = 1;

Insert into Inventory(CID, Stock, WNO, SNO) values (1001,2,1,13);




Drop Table Orders;
CREATE TABLE Orders(
    OID varchar(20) PRIMARY KEY ,
    UID int UNSIGNED,
    CID int UNSIGNED,
    Quantity int,
    TPrice Decimal(10,2),
    Status ENUM('成功','失败'),
    Hour datetime,
    FOREIGN KEY(UID) REFERENCES User(UID),
    FOREIGN KEY(CID) REFERENCES Costume(CID)
);

insert into Orders(oid, uid, cid, quantity, tprice, status, hour)
VALUES (
        CONCAT(
        UNIX_TIMESTAMP(now()),
        LPAD(FLOOR(RAND() * 10000), 4, '0')
        ),
        1000000,
        1001,
        2,
        (SELECT UPrice from Costume WHERE CID = 1000000)*2,
        '成功',
        NOW()
                                                                       );
                                                                       
                                                                       
                                                                       
                                                     drop table ShopCart;
CREATE TABLE ShopCart(
    CartID int primary key auto_increment ,
    UID int unsigned,
    CID int unsigned,
    number int,
    foreign key (UID) references User(UID),
    foreign key (CID) references Costume(CID)

);
INSERT into ShopCart( UID, CID, number) VALUES (1000000,1001,2);
```





```sql
DELIMITER //
DROP TRIGGER update_inventory_status_1;
CREATE TRIGGER update_inventory_status_1
BEFORE UPDATE ON Inventory
FOR EACH ROW
BEGIN

    DECLARE existing_stock int;


    SELECT Stock INTO existing_stock
    FROM Inventory
    WHERE CID = NEW.CID;

            SET NEW.Stock = existing_stock + NEW.Stock;

            IF NEW.Stock>=0 AND NEW.Stock < 100 THEN
                UPDATE Costume
                SET Status = '库存紧张'
                WHERE CID = NEW.CID;
            end if;
            IF NEW.Stock>=100 THEN
                UPDATE Costume
                SET Status = '库存充足'
                WHERE CID = NEW.CID;
            end if;
            IF NEW.Stock<=0 THEN
                UPDATE Costume
                SET Status = '缺货'
                WHERE CID = NEW.CID;

            end if;

END//



DELIMITER //
```



```sql
DELIMITER //
CREATE TRIGGER insert_inventory_status_1
BEFORE INSERT ON Inventory
FOR EACH ROW
BEGIN

    DECLARE existing_cid varchar(20);
    SELECT CID into existing_cid
    FROM Costume
    WHERE CID = NEW.CID;

    IF existing_cid IS NOT NULL THEN
        SIGNAL SQLSTATE '45002' SET MESSAGE_TEXT = '已有库存记录，请选择进货';

    end if;


END//

DELIMITER //
```





```sql
DELIMITER //
CREATE TRIGGER insert_orders_status
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN

    DECLARE number int;

    DELETE FROM ShopCart
    WHERE ShopCart.CID = NEW.CID;

    SET number = -NEW.Quantity;

    UPDATE Inventory
    SET Stock = number
    WHERE CID = NEW.CID;

    UPDATE Costume
    SET Sales = Sales+NEW.Quantity
    WHERE CID = NEW.CID;



END//

DELIMITER //


```



