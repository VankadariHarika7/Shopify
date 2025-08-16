
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    about_text = Column(Text)
    privacy_policy = Column(Text)
    refund_policy = Column(Text)
    products = relationship("Product", back_populates="brand")
    faqs = relationship("FAQ", back_populates="brand")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    price = Column(Float)
    url = Column(String(255))
    image_url = Column(String(255))
    is_hero = Column(Integer, default=0)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="products")

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="faqs")
