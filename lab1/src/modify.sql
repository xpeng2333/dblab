Create or Replace Procedure updateBookID
(oldID IN char, newID IN char)
AS
type tempbook is record
(
	ID char (8), 
	name varchar2 (10),
	author varchar2(10),
	price float, 
	status int 
);
tmp tempbook;
BEGIN
    select *
    into tmp
    from book
    where id = oldID;
    insert into book
    values
        (newID, tmp.name , tmp.author, tmp.price, tmp.status);

    Update borrow
Set book_id = newID
Where book_id = oldID;

    Delete From book
Where ID = oldID;
END;

Execute updateBookID
('011','010');