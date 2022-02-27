from sqlalchemy import create_engine, MetaData, Table, Integer, Column, String, ForeignKey, select
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


def insert_data_using_obj_add():
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

    session = Session(engine)
    print(session.get(User, 1))

    # add to session
    session.add(squidward)
    session.add(krabs)
    print(session.new)

    # The transaction now remains open until we call any of the Session.commit(), Session.rollback(), or Session.close() methods of Session.
    session.flush()
    # While Session.flush() may be used to manually push out pending changes to the current transaction,
    # it is usually unnecessary as the Session features a behavior known as autoflush, which we will illustrate later.
    # It also flushes out changes whenever Session.commit() is called.
    print("before commit")
    print(squidward.id)
    print(krabs.id)

    session.commit()

    # after commit (persistent) the object retrieved data from remote and filled in object.
    print("after commit")
    print(squidward.id)
    print(krabs.id)


def update_data_using_obj():
    session = Session(engine)
    # sandy represent a obj in database
    sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
    # edit attribute of the obj to change the data in database (will not commit to database until commit)
    sandy.full_name = "test name"

    print(sandy in session.dirty)
    # True // after editing, sandy now is a dirty obj that need to be flushed and commited

    # after select again, autoflush will be executed to save changes in mem, but still waiting for commit
    sandy_fullname = session.execute(
        select(User.fullname).where(User.id == 2)
    ).scalar_one()
    print(sandy_fullname)

    print(sandy in session.dirty)
    # False


def query_update_using_obj():
    class Keys:
        key_name = "env_name"
        key_master_ip = "master_node_ip"
        key_user = "user"
        key_pwd = "password"
        key_link = "link"
        key_page_id = "id"
        key_env_type = "type"
        key_port = "port"

    ENV_KEY = Keys()
    ti_envs = [
        {
            ENV_KEY.key_page_id: "111111",
            ENV_KEY.key_name: "title",
            ENV_KEY.key_env_type: "体验",
            ENV_KEY.key_master_ip: "192.0.0.1",
            ENV_KEY.key_user: "usr",
            ENV_KEY.key_pwd: "1234",
            ENV_KEY.key_link: "https://link.com/",
        }
    ]
    print("start scanning")
    for env in ti_envs:
        print()
        print(env[ENV_KEY.key_page_id])
        print(env[ENV_KEY.key_name])
        print(env.get(ENV_KEY.key_port, "22"))
        print(env[ENV_KEY.key_pwd])

        with Session(engine) as session:
            db_env = session.query("someclass").filter_by(id=env[ENV_KEY.key_page_id]).first()
            if db_env is not None:
                db_env.node_password = env[ENV_KEY.key_pwd]
                db_env.node_port = env.get(ENV_KEY.key_port, "22")
                db_env.master_node_ip = env.get(ENV_KEY.key_master_ip)
            session.commit()


if __name__ == '__main__':
    insert_data_using_obj_add()
    update_data_using_obj()
    query_update_using_obj()
