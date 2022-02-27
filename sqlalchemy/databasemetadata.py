from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("mysql+mysqldb://root:aYhMZ*7986YvgA@9.135.69.57:3306/ti_platform_infra", echo=True,
                       future=True)

Base = declarative_base()
metadata_obj = MetaData()

def settingup_using_table_object():
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
    metadata_obj.drop_all(engine)


def settingup_using_orm_classes():
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

    print(User(name="testuser"))
    Base.metadata.create_all(engine)


def table_reflection():
    # https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#table-reflection
    user_account = Table("user_account", metadata_obj, autoload_with=engine)
    print(user_account)


if __name__ == '__main__':
    # settingup_using_table_object()
    settingup_using_orm_classes()
    table_reflection()
