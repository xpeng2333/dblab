create table Book
(
	ID char(8) primary key,
	name varchar2(10) not null,
	author varchar2(10),
	price float,
	status int default 0 check(status in(1,0))
);

create table Reader
(
	ID char(8) primary key,
	name varchar2(10),
	age int,
	address varchar2(20)
);

create table borrow
(
	book_id char(8),
	reader_id char(8),
	borrow_date date,
	return_date date,
	constraint PK_BR primary key (book_id, reader_id),
	constraint bookkey foreign key (book_id) references book(id),
	constraint readerkey foreign key (reader_id) references reader(id)
);

insert into book
values
    ('001', 'Oracle', 'Ullman', '10', '1');
insert into book
values
	('002', 'SQL', 'xiepeng', '100', '0');
insert into book
values
	('003', 'balabal', 'Ullman', '50', '0');
insert into book
values
	('004', 'book4', 'author1', '11', '0');
insert into book
values
	('005', 'book5', 'author2', '12', '1');
insert into book
values
	('006', 'book6', 'author3', '13', '0');
insert into book
values
	('007', 'book7', 'author4', '14', '1');
insert into book
values
	('008', 'Oracle123', 'Ullman', '10', '0');
insert into book
values
	('009', '123Oracle', 'Ullman', '0.2', '1');
insert into book
values
	('010', '23Oracle32', 'Ullman', '10.3', '0');

insert into reader
values
	('001', 'Rose', '18', 'address1');
insert into reader
values
	('002', '¿Ó¡÷', '18', 'address2');
insert into reader
values
	('003', 'author3', '19', 'address1');
insert into reader
values
	('004', 'author4', '19', 'address1');
insert into reader
values
	('005', 'author5', '19', 'address1');

insert into borrow
values
	('001', '001', to_date('12/08/2017', 'dd-mm-yyyy'), NULL);
insert into borrow
values
	('002', '002', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('13/09/2017','dd-mm-yyyy'));
insert into borrow
values
	('003', '001', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('12/09/2017','dd-mm-yyyy'));
insert into borrow
values
	('004', '003', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('20/09/2017','dd-mm-yyyy'));
insert into borrow
values
	('005', '002', to_date('11/08/2015', 'dd-mm-yyyy'), NULL);
insert into borrow
values
	('005', '003', to_date('11/08/2016', 'dd-mm-yyyy'), to_date('12/08/2017','dd-mm-yyyy'));
insert into borrow
values
	('006', '003', to_date('11/08/2014', 'dd-mm-yyyy'), to_date('19/09/2017','dd-mm-yyyy'));
insert into borrow
values
	('007', '003', to_date('11/08/2017', 'dd-mm-yyyy'), NULL);
insert into borrow
values
	('008', '004', to_date('11/08/2017', 'dd-mm-yyyy'), to_date('18/09/2017','dd-mm-yyyy'));
insert into borrow
values
	('009', '002', to_date('11/08/2012', 'dd-mm-yyyy'), NULL);
