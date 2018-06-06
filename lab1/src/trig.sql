Create or Replace Trigger borrowtri
After 
Insert On borrow for each row
Begin
    Update book Set book.status=1
where book.id = :new.book_id;
End;

Create or Replace Trigger returntri
After
update On borrow for each row
Begin
    Update book Set book.status=0
where book.id = :new.book_id
        and :new.return_date is not NULL;
End;
