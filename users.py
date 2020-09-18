import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

class User(Base):

	__tablename__ = "user"
	id = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True)
	first_name = sa.Column(sa.TEXT)
	last_name = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	email = sa.Column(sa.TEXT)
	birthdate = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)

def request_data():

	print("Привет! Я запишу твои данные!")
	first_name = input("Введи своё имя: ")
	last_name = input("А теперь фамилию: ")
	email = input("Еще нужен адрес электронной почты: ")
	gender = input("И пол: ")
	height = input("А также рост: ")
	birthdate = input("И дата рождения (в формате ГГГГ-ММ-ДД): ")

	new_user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )
	return new_user

def main():
	session = connect_db()
	new_user = request_data()
	session.add(new_user)

	session.commit()
	print("Спасибо, данные сохранены!")

if __name__ == "__main__":
	main()