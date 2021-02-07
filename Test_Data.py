from mongoengine import *
import datetime

class Users(Document):

    '''
    users MongoDB base
    :field name: str user's name
    :field login: str user's login
    :field password: str user's password
    :field isAdmin: bool permission for work with Users directory
    :field isWorker: bool permission for work data (Items, Orders)
    '''

    name = StringField(unique=True,required=True, max_length=200)
    login = StringField(required=True, max_length=200)
    password = StringField(required=True, max_length=200)
    session = StringField(required=True, max_length=200)
    isAdmin = BooleanField(required=True, default=False)
    isWorker = BooleanField(required=True, default=False)

class Items(Document):

    '''
    items MongoDB base
    :field title: str item's name
    :field price: int item's price
    :field author: User user, who change/create this item
    :field published: date when this item was changed/created
    '''

    title = StringField(unique=True,required=True, max_length=200)
    price = IntField(default=0, min_value=0)
    author = ReferenceField(Users)
    published = DateTimeField(default=datetime.datetime.now())

class Order(Document):

    '''
     orders MongoDB base
     :field number: str item's name
     :field author: User user, who change/create this item
     :field date: date when this order was changed/created
     :field isIn: bool if we buy
     :field isOut: bool if we sale
     :field table_items: list items
     '''

    number = StringField(required=True, max_length=50)
    author = ReferenceField(Users)
    date = DateTimeField(default=datetime.datetime.now)
    isIn = BooleanField(default=True)
    isOut = BooleanField(default=False)
    sum = FloatField(default=0)
    table_items = ListField()

def delete_data():

    '''
    delete ALL DATA from DB
    '''

    connect('mongoengine_warehouse', host='localhost', port=27017)
    Order.drop_collection()
    Items.drop_collection()
    Users.drop_collection()


def fill_Test_Users():
    '''
    fill Users collection
    '''

    connect('mongoengine_warehouse', host='localhost', port=27017)
    admin = Users(
        name='Administrator',
        login='admin',
        password='admin',
        session='',
        isAdmin=True,
        isWorker=False
    )
    admin.save()

    worker = Users(
        name='Worker',
        login='worker',
        password='worker',
        session='',
        isAdmin=False,
        isWorker=True
    )
    worker.save()
    disconnect()

def fill_Test_Items():

    '''
    fill Items collection
    '''

    connect('mongoengine_warehouse', host='localhost', port=27017)
    item_1 = Items(
        title='milk',
        price=2,
        author= Users.objects(name = 'Administrator')[0]
    )
    item_1.save()

    item_2 = Items(
        title='broad',
        price=5,
        author= Users.objects(name = 'Worker')[0]
    )
    item_2.save()

    item_3 = Items(
        title='meat',
        price=10,
        author=Users.objects(name='Worker')[0]
    )
    item_3.save()
    disconnect()

def fill_Test_Orders():

    '''
    fill Order collection
    '''

    connect('mongoengine_warehouse', host='localhost', port=27017)
    list = []
    sum = 0
    newStr = [Items.objects(title = 'broad')[0], Items.objects(title = 'broad')[0].price, 5, Items.objects(title = 'broad')[0].price * 5]
    sum += Items.objects(title = 'broad')[0].price * 5
    list.append(newStr)
    newStr = [Items.objects(title = 'meat')[0], Items.objects(title = 'meat')[0].price, 3, Items.objects(title = 'meat')[0].price * 3]
    sum += Items.objects(title = 'meat')[0].price * 3
    list.append(newStr)
    # Order.objects(number = '1')[0].update(table_items = list)
    # doc(table_items = list).update()
    # print(Items.objects(title = 'milk2'))
    order = Order(
        number = "1",
        date = datetime.datetime.now,
        author = Users.objects(name='Worker')[0],
        isIn = True,
        isOut = False,
        sum=sum,
        table_items = list
    )
    order.save()

    list = []
    sum = 0
    newStr = [Items.objects(title = 'milk')[0], Items.objects(title = 'milk')[0].price, 5, Items.objects(title = 'milk')[0].price * 5]
    sum += Items.objects(title = 'milk')[0].price * 2
    list.append(newStr)
    newStr = [Items.objects(title = 'meat')[0], Items.objects(title = 'meat')[0].price, 3, Items.objects(title = 'meat')[0].price * 3]
    sum += Items.objects(title = 'meat')[0].price * 1
    list.append(newStr)
    # Order.objects(number = '1')[0].update(table_items = list)
    # doc(table_items = list).update()
    # print(Items.objects(title = 'milk2'))
    order = Order(
        number = "2",
        date = datetime.datetime.now,
        author = Users.objects(name='Worker')[0],
        isIn = False,
        isOut = False,
        sum = sum,
        table_items = list
    )
    order.save()
    disconnect()

def fill_Test_Data():

    '''
    fill DB by test data
    '''

    fill_Test_Users()
    fill_Test_Items()
    fill_Test_Orders()


if __name__ == '__main__':
    delete_data()
    fill_Test_Data()

