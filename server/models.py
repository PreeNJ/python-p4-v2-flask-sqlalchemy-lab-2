from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Task 1: Add Review model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    
    # Task 3: Serialization Rules for Review
    serialize_rules = ('-customer.reviews', '-item.reviews',)
    
    def __repr__(self):
        return f'<Review {self.id}>'

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Task 1: Add relationship to Review
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    
    # Task 2: Add Association Proxy
    items = association_proxy('reviews', 'item')
    
    # Task 3: Serialization Rules for Customer
    serialize_rules = ('-reviews.customer',)
    
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Task 1: Add relationship to Review
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')
    
    # Task 3: Serialization Rules for Item
    serialize_rules = ('-reviews.item',)
    
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'