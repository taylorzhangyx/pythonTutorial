from sqlalchemy import insert, create_engine, MetaData, Table, Integer, Column, String, ForeignKey, select, bindparam, \
    text, literal_column, union_all, update, delete
from sqlalchemy.orm import declarative_base, Session, relationship

engine = create_engine("mysql+mysqldb://root:aYhMZ*7986YvgA@9.135.69.57:3306/ti_platform_infra", echo=True,
                       future=True)

Base = declarative_base()
metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String(64))
)
print(user_table.primary_key)
address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String(128), nullable=False)
)


class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(64))
    age = Column(Integer)
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, age={self.age!r}, addresses={self.addresses!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(128), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def insert_data_using_values():
    stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("before commit", result.inserted_primary_key)
        conn.commit()
        print("after commit", result.inserted_primary_key)


def insert_data_using_exec():
    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"}
            ]
        )
        conn.commit()
        # print("res", result.inserted_primary_key_rows) # NOT WORKING


def insert_data_scala_subq():
    scalar_subq = (
        select(user_table.c.id).
            where(user_table.c.name == bindparam('username')).
            scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subq),
            [
                {"username": 'spongebob', "email_address": "spongebob@sqlalchemy.org"},
                {"username": 'sandy', "email_address": "sandy@sqlalchemy.org"},
                {"username": 'sandy', "email_address": "sandy@squirrelpower.org"},
            ]
        )

        conn.commit()


def insert_data_with_select():
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"], select_stmt
    )
    print(insert_stmt)
    '''
    # INSERT INTO address (user_id, email_address)
    # SELECT user_account.id, user_account.name || :name_1 AS anon_1
    # FROM user_account
    '''


def insert_data_with_returning():
    insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
    print(insert_stmt)
    '''
    # INSERT INTO address (id, user_id, email_address)
    # VALUES (:id, :user_id, :email_address)
    # RETURNING address.id, address.email_address
    '''

    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"], select_stmt
    )
    print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
    '''
    # INSERT INTO address (user_id, email_address)
    # SELECT user_account.id, user_account.name || :name_1 AS anon_1
    # FROM user_account RETURNING address.id, address.email_address
    '''


def select_data_where():
    # using table
    stmt = select(user_table).where(user_table.c.name == 'spongebob')
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

    # using ORM
    stme = select(User).where(User.name == 'spongebob')
    with Session(engine) as session:
        for row in session.execute(stmt):
            print(row)


def select_data_using_table_columns():
    # select all columns, like select * from
    stmt = select(user_table)
    print(stmt)

    # select only given columns
    stmt = select(user_table.c.name, user_table.c.fullname)
    print(stmt)


def select_data_using_orm_columns():
    print(select(User))
    with Session(engine) as session:
        # get the first matched res as a tuple
        row = session.execute(select(User)).first()
        print(row[0])

    print(select(User.fullname, User.name))
    with Session(engine) as session:
        row = session.execute(select(User.name, User.fullname)).first()
        print(row)

    with Session(engine) as session:
        # advanced use for me with a joined class
        session.execute(
            select(User.name, Address).
                where(User.id == Address.user_id).
                order_by(Address.id)
        ).all()


def select_data_using_label():
    stmt = (
        select(
            # this label is for marking this value as an attribute
            ("Username: " + user_table.c.name).label("username")
        )
            .order_by(user_table.c.name)
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
            # then we can access it using row.username
            print(f"{row.username}")


def select_data_using_textual_column_expr():
    """
        Note that in both cases, when using text() or literal_column(), we are writing a syntactical SQL expression,
        and not a literal value. We therefore have to include whatever quoting or syntaxes are necessary
        for the SQL we want to see rendered.
    """

    stmt = (
        select(
            text("'some phrase'"), user_table.c.name
        ).order_by(user_table.c.name)
    )
    with engine.connect() as conn:
        print(conn.execute(stmt).all())

    stmt = (
        select(
            literal_column("'some phrase'").label("p"), user_table.c.name
        ).order_by(user_table.c.name)
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.p}, {row.name}")


def select_data_using_where():
    print(
        select(address_table.c.email_address).
            where(user_table.c.name == 'squidward').
            where(address_table.c.user_id == user_table.c.id)
    )

    print(
        select(address_table.c.email_address).
            where(
            user_table.c.name == 'squidward',
            address_table.c.user_id == user_table.c.id
        )
    )

    from sqlalchemy import and_, or_
    print(
        select(Address.email_address).
            where(
            and_(
                or_(User.name == 'squidward', User.name == 'sandy'),
                Address.user_id == User.id
            )
        )
    )

    print(
        select(User).filter_by(name='spongebob', fullname='Spongebob Squarepants')
    )


def select_data_using_union():
    stmt1 = select(user_table).where(user_table.c.name == 'sandy')
    stmt2 = select(user_table).where(user_table.c.name == 'spongebob')
    u = union_all(stmt1, stmt2)
    with engine.connect() as conn:
        result = conn.execute(u)
        print(result.all())


def update_date_using_core():
    stmt = (
        update(user_table).where(user_table.c.name == 'patrick').
            values(fullname='Patrick the Star')
    )
    print(stmt)

    # update many
    stmt = (
        update(user_table).
            where(user_table.c.name == bindparam('oldname')).
            values(name=bindparam('newname'))
    )
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {'oldname': 'jack', 'newname': 'ed'},
                {'oldname': 'wendy', 'newname': 'mary'},
                {'oldname': 'jim', 'newname': 'jake'},
            ]
        )


def delete_data_using_core():
    stmt = delete(user_table).where(user_table.c.name == 'patrick')
    print(stmt)


def affected_row_count():
    with engine.begin() as conn:
        result = conn.execute(
            update(user_table).
                values(fullname="Patrick McStar233").
                where(user_table.c.name == 'patrick')
        )
        # The value returned is the number of rows matched by the WHERE clause of the statement.
        # It does not matter if the row were actually modified or not.
        print(result.rowcount)


def returning_data_with_upadte_and_delete():
    update_stmt = (
        update(user_table).where(user_table.c.name == 'patrick').
            values(fullname='Patrick the Star').
            returning(user_table.c.id, user_table.c.name)
    )
    print(update_stmt)

    delete_stmt = (
        delete(user_table).where(user_table.c.name == 'patrick').
            returning(user_table.c.id, user_table.c.name)
    )
    print(delete_stmt)


if __name__ == '__main__':
    insert_data_using_values()
    insert_data_using_exec()
    insert_data_scala_subq()
    insert_data_with_select()
    insert_data_with_returning()

    select_data_where()
    select_data_using_table_columns()
    select_data_using_orm_columns()
    select_data_using_label()
    select_data_using_textual_column_expr()
    select_data_using_where()
    select_data_using_union()

    update_date_using_core()

    delete_data_using_core()

    affected_row_count()
    returning_data_with_upadte_and_delete()
