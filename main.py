import sqlalchemy
import json

from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from models import create_tables, Stock, Book, Publisher, Sale, Shop

def search_publisher(session, name=None, id=None):
    if id is not None:
        result = session.query(Publisher).filter(Publisher.id == id).all()
        return result

    if name is not None:
        result = []
        for c in session.query(Publisher).filter(Publisher.name == name).all():
            result.append(c)
        return result

def search_shop(session, pub_id=None, pub_name=None):
    if pub_id is not None:
        result = []
        for c in session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == pub_id).all():
            result.append(c)
        return result

    if pub_name is not None:
        result = []
        for c in session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == pub_name).all():
            result.append(c)
        return result

def data_loader(session):
    with open('test_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

def get_DSN():
    with open('acess.json', 'r') as ac:
        data = json.load(ac)[0]
        return f"{data['database']}://{data['user']}:{data['pass']}@localhost:5432/{data['database_name']}"


# DSN = "postgresql://postgres:postgres@localhost:5432/netology_orm"
DSN = get_DSN()
engine = sqlalchemy.create_engine(DSN)

# create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# data_loader(session)

requ = input('Введите ID или название автора:')
if requ.isdigit():
    print('Автор: \n',*search_publisher(session, id=requ))
    print('Магазины: \n', *search_shop(session, pub_id=requ))
else:
    print('Автор: \n', *search_publisher(session, name=requ))
    print('Магазины: \n', *search_shop(session, pub_name=requ))
session.close()


