import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import User
from datetime import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

class Athelete(Base):
	__tablename__  = "athelete"
	id = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True)
	age = sa.Column(sa.INTEGER)
	birthdate = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)
	name = sa.Column(sa.TEXT)
	weight = sa.Column(sa.INTEGER)
	gold_medals = sa.Column(sa.INTEGER)
	silver_medals = sa.Column(sa.INTEGER)
	bronze_medals = sa.Column(sa.INTEGER)
	total_medals = sa.Column(sa.INTEGER)
	sport = sa.Column(sa.TEXT)
	country = sa.Column(sa.TEXT)

def request_user(session):
	request_id = input("Введите идентификатор пользователя: ")
	finded_user = session.query(User).filter(User.id == request_id).first()
	return finded_user

def find_athlete_by_height(session, user_height):
	height_difference = None
	min_height_difference = None
	finded_athlete_h_name = None
	finded_athlete_h_height = None
	query = session.query(Athelete).filter(Athelete.height != None)
	athletes_heights = {athlete.name: athlete.height for athlete in query.all()}
	for athlete_name, athlete_height in athletes_heights.items():
		height_difference = abs(athlete_height - user_height)
		if min_height_difference == None or height_difference < min_height_difference:
			min_height_difference = height_difference
			finded_athlete_h_name = athlete_name
			finded_athlete_h_height = athlete_height
	return (finded_athlete_h_name, finded_athlete_h_height)

def find_athlete_by_birthdate(session, user_birthdate):
	user_birthdate = transform_to_date(user_birthdate)
	birthdate_difference = None
	min_birthdate_difference = None
	finded_athlete_b_name = None
	finded_athlete_b_birthdate = None
	query = session.query(Athelete)
	athletes_birthdates = {athlete.name: athlete.birthdate for athlete in query.all()}
	for athlete_name, athlete_birthdate in athletes_birthdates.items():
		athlete_birthdate_ = transform_to_date(athlete_birthdate)
		birthdate_difference = abs((athlete_birthdate_ - user_birthdate).days)
		if min_birthdate_difference == None or birthdate_difference < min_birthdate_difference:
			min_birthdate_difference = birthdate_difference
			finded_athlete_b_name = athlete_name
			finded_athlete_b_birthdate = athlete_birthdate
	return (finded_athlete_b_name, finded_athlete_b_birthdate)

def transform_to_date(birthdate):
	birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
	return birthdate

def main():
	session = connect_db()
	finded_user = request_user(session)
	if finded_user is None:
		print("Пользователь с таким идентификатором отсутствует в базе данных.")
	else:
		print("Найден пользователь {} {}. Рост - {}, дата рождения - {}.".format(finded_user.first_name, finded_user.last_name, finded_user.height, finded_user.birthdate))
		finded_athlete_h_name, finded_athlete_h_height = find_athlete_by_height(session, finded_user.height)
		print("Ближайший к пользователю атлет по росту - {}, его рост - {}".format(finded_athlete_h_name, finded_athlete_h_height))
		finded_athlete_b_name, finded_athlete_b_birthdate = find_athlete_by_birthdate(session, finded_user.birthdate)
		print("Ближайший к пользователю атлет по возрасту - {}, его дата рождения - {}".format(finded_athlete_b_name, finded_athlete_b_birthdate))
		find_athlete_by_birthdate(session, finded_user.birthdate)

if __name__ == "__main__":
	main()