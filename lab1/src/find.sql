select ID, address
from Reader
where name = 'Rose';

select Book.name, borrow.borrow_date
from Book, Reader, borrow
where Reader.ID = borrow.READER_ID
    and Book.ID = borrow.BOOK_ID
    and Reader.name = 'Rose';

select ID
from Reader
where ID not in 
(select reader_id
from borrow);

select name, price
from Book
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

Create View libview
(
    rid,
    rname,
    bid,
    bname,
    bdate
)
As
    Select reader.id, reader.name, book.id, book.name, BORROW.BORROW_DATE
    From book, reader, borrow
    Where book.id = borrow.book_id
        and reader.id = borrow.reader_id
With Read Only;

select rid, count(distinct bname) as num
from libview
where bdate < to_date('01/04/2017', 'dd-mm-yyyy')
group by rid;