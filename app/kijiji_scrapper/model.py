from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy import String

Base = declarative_base()


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    picture = Column(String(500))
    title = Column(String(250))
    location = Column(String(250))
    date = Column(Date, )
    beds = Column(String(250))
    description = Column(Text)
    price = Column(Numeric)
    currency = Column(String(100))


