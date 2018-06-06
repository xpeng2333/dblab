create table Book(
	ID char(8) primary key,
	name varchar2(10) not null,
	author varchar2(10),
	price float, 
	status int default 0 check(status in(1,0))
);

create table Reader(
	ID char(8) primary key,
	name varchar2(10),
	age int,
	address varchar2(20)
);

create table borrow(
    book_id				char(8),
    reader_id			char(8),
    borrow_date			date,
    return_date			date,
    constraint PK_BR primary key (book_id, reader_id),
    constraint bookkey foreign key (book_id) references book(id),
    constraint readerkey foreign key (reader_id) references reader(id)
);

insert into book values ('B#001', 'Oracle', 'Ullman', '10', '1');
insert into book values ('B#002', 'SQL', 'xiepeng', '100', '0');
insert into book values ('B#003', 'GoOut', 'Ullman', '50', '0');
insert into book values ('B#004', 'book4', 'author1', '11', '0');
insert into book values ('B#005', 'book5', 'author2', '12', '1');
insert into book values ('B#006', 'book6', 'author3', '13', '0');
insert into book values ('B#007', 'book7', 'author4', '14', '1');
insert into book values ('B#008', 'Oracle123', 'Ullman', '10', '0');
insert into book values ('B#009', '123Oracle', 'Ullman', '0.2', '1');
insert into book values ('B#010', '23Oracle32', 'Ullman', '10.3', '1');

insert into reader values ('R#001', 'Rose', '18', 'address1');
insert into reader values ('R#002', '李林', '18', 'address2');
insert into reader values ('R#003', 'author3', '19', 'address1');
insert into reader values ('R#004', 'author4', '19', 'address1');
insert into reader values ('R#005', 'author5', '19', 'address1');		# not borrow books

insert into borrow values ('B#001', 'R#001', to_date('12/08/2017', 'dd-mm-yyyy'), NULL);
insert into borrow values ('B#002', 'R#002', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('13/09/2017','dd-mm-yyyy'));
insert into borrow values ('B#003', 'R#001', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('12/09/2017','dd-mm-yyyy'));
insert into borrow values ('B#004', 'R#003', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('20/09/2017','dd-mm-yyyy'));
insert into borrow values ('B#005', 'R#002', to_date('11/08/2015', 'dd-mm-yyyy'), NULL);
insert into borrow values ('B#005', 'R#003', to_date('11/08/2016', 'dd-mm-yyyy'), to_date('12/08/2017','dd-mm-yyyy'));
insert into borrow values ('B#006', 'R#003', to_date('11/08/2014', 'dd-mm-yyyy'), to_date('19/09/2017','dd-mm-yyyy'));
insert into borrow values ('B#007', 'R#003', to_date('11/08/2017', 'dd-mm-yyyy'), NULL);
insert into borrow values ('B#008', 'R#004', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('18/09/2017','dd-mm-yyyy'));
insert into borrow values ('B#009', 'R#002', to_date('11/08/2012', 'dd-mm-yyyy'), NULL);
insert into borrow values ('B#010', 'R#003', to_date('11/08/2017', 'dd-mm-yyyy'), NULL);

insert into book values (NULL, 'Oracle', 'Ullman', '10', '1');
insert into borrow values ('B#011', 'R#001', to_date('12/08/2017', 'dd-mm-yyyy'), NULL);
insert into book values ('B#001', NULL, 'Ullman', '10', '1');

select ID, address from Reader 
where name = 'Rose';

select Book.name, borrow.borrow_date 
from Book, Reader, borrow 
where Reader.ID = borrow.READER_ID 
and Book.ID = borrow.BOOK_ID 
and Reader.name = 'Rose';

select ID from Reader
where ID not in 
(select reader_id from borrow);

select name, price from Book
where author = 'Ullman';

select Book.ID, Book.name
from Book, Reader, borrow
where book.id = borrow.BOOK_ID
and reader.id = borrow.READER_ID
and reader.name = '李林'
and borrow.RETURN_DATE is NULL;

select reader.name
from reader, borrow
where reader.ID = borrow.READER_ID
group by reader.name
having COUNT(*) > 3;

select reader.id, reader.name
from reader, borrow
where borrow.READER_ID = reader.ID
and borrow.BOOK_ID not in
(select borrow.BOOK_ID
from borrow, reader
where borrow.READER_ID = reader.ID
and reader.NAME = '李林'
);

select id, name
from book
where name like '%Oracle%';

Create View libview (rid, rname, bid, bname, bdate)
As Select reader.id,reader.name,book.id,book.name,BORROW.BORROW_DATE
From book, reader, borrow
Where book.id = borrow.book_id
and reader.id = borrow.reader_id
With Read Only;

select rid, count(distinct bname) as num
from libview 
where bdate < to_date('01/04/2017', 'dd-mm-yyyy')
group by rid;


Create or Replace Procedure updateBookID(oldID IN char, newID IN char)
AS
type tempbook is record(
	ID char(8), 
	name varchar2(10),
	author varchar2(10),
	price float, 
	status int 
);
tmp tempbook;
BEGIN
select * into tmp from book where id = oldID;
insert into book values (newID, tmp.name , tmp.author, tmp.price, tmp.status);

Update borrow
Set book_id = newID
Where book_id = oldID;

Delete From book
Where ID = oldID;
END;

Execute updateBookID('B#011','B#010');

Create or Replace Trigger borrowtri
After Insert On borrow for each row
Begin
Update book Set book.status=1
where book.id = :new.book_id;
End;

Create or Replace Trigger returntri
After update On borrow for each row
Begin
Update book Set book.status=0
where book.id = :new.book_id
and :new.return_date is not NULL;
End;
