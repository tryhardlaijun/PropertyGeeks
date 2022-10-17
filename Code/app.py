import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker

engine = db.create_engine('mariadb+mariadbconnector://root:root@127.0.0.1:3306/projectdb', echo = False)
connection = engine.connect()
Base = declarative_base(engine)

class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'autoload': True}

    def __repr__(self):
        return "Name='%s', email='%s', faculty='%s'" % (self.name, self.email, self.faculty)

def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = loadSession()
    res = session.query(Student).all()
    for i in res:
        print(i)
