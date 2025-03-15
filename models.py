from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey

from sqlalchemy.orm import backref, relationship
from database import Base
from datetime import datetime

class Member(Base):
    __tablename__ = 'member'

    member_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    booking_count = Column(Integer)
    date_joined = Column(DateTime)

class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    remaining_count = Column(Integer)
    expiration_date = Column(Date)


class BookingTrip(Base):
    __tablename__= 'bookingtrips'

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey(Member.member_id), nullable=False)
    inventory_id = Column(Integer, ForeignKey(Inventory.inventory_id), nullable=False)
    booking_time = Column(DateTime, default=datetime.now())


    member = relationship("Member", backref=backref("request", uselist=False))
    inventory = relationship("Inventory", backref=backref("inventory", uselist=False))
