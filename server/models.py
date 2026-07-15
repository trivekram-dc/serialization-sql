from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')

    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')

    customers = association_proxy('reviews', 'customer')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

class CustomerSchema(Schema):
    id = fields.Int()
    name = fields.String()
    reviews = fields.List(fields.Nested(lambda: ReviewSchema(exclude=("customer", "item"))))
    items = fields.List(fields.Nested(lambda: ItemSchema(exclude=("customers", "reviews"))))

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.String()
    price = fields.Float()
    reviews = fields.List(fields.Nested(lambda: ReviewSchema(exclude=("item", "customer"))))
    customers = fields.List(fields.Nested(CustomerSchema(exclude=("items", "reviews"))))

class ReviewSchema(Schema):
    id = fields.Int()
    name = fields.String()
    comment = fields.String()
    customer = fields.Nested(CustomerSchema(exclude=("reviews", "items")))
    item = fields.Nested(ItemSchema(exclude=("reviews", "customers")))
