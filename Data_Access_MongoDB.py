import mongoengine as me
import datetime

'''
work with MongoDB base
'''

class Users(me.Document):

    '''
    users MongoDB base
    :field name: str user's name
    :field login: str user's login
    :field password: str user's password
    :field isAdmin: bool permission for work with Users directory
    :field isWorker: bool permission for work data (Items, Orders)
    '''

    name = me.StringField(unique=True,required=True, max_length=200)
    login = me.StringField(required=True, max_length=200)
    password = me.StringField(required=True, max_length=200)
    session = me.StringField(max_length=200)
    isAdmin = me.BooleanField(required=True, default=False)
    isWorker = me.BooleanField(required=True, default=False)

class Items(me.Document):

    '''
    items MongoDB base
    :field title: str item's name
    :field price: int item's price
    :field author: User user, who change/create this item
    :field published: date when this item was changed/created
    '''

    title = me.StringField(unique=True,required=True, max_length=200)
    price = me.IntField(default=0, min_value=0)
    author = me.ReferenceField(Users)
    published = me.DateTimeField(default=datetime.datetime.now)

class Order(me.Document):

    '''
    orders MongoDB base
    :field number: str item's name
    :field author: User user, who change/create this item
    :field date: date when this order was changed/created
    :field isIn: bool if we buy
    :field isOut: bool if we sale
    :field table_items: list items
    '''

    number = me.StringField(required=True, max_length=50)
    author = me.ReferenceField(Users)
    date = me.DateTimeField(default=datetime.datetime.now())
    isIn = me.BooleanField(default=True)
    isOut = me.BooleanField(default=False)
    sum = me.FloatField(default=0)
    table_items = me.ListField()

def authorisation(login_, password_):

    '''
    authorisation for users
    :param login_: str user's login
    :param password_: str user's password
    :return: tuple user's name, fields isAdmin, isWorker
    '''
    res = Users.objects(login=login_,  password=password_)

    if len(res) > 0:
        return res[0].name, res[0].isAdmin, res[0].isWorker
    else:
        return (None, False, False)

def get_Items():

    '''
    list of items
    :return: list of lists item's id, item's name, item's price, name of user, who change/create item
    '''

    result = Items.objects()
    list = []
    for i in result:
        list.append([str(i.id), i.title, i.price, i.author.name])

    return list

def save_Items(id_, new_):

    '''
    save/update Item
    :param id: item's id for search
    :param new_: dict for save/update
    :return: Exception, str - result
    '''

    try:
        if id_ != '':
            Items.objects(id=id_)[0].update(title=new_['title'],
                                                   price=new_['price'],
                                                   author=Users.objects(name=new_['author'])[0])
            return ''
        else:
            item = Items(
                title = new_['title'],
                price = new_['price'],
                author = Users.objects(name=new_['author'])[0]
            )
            item.save()
            return str(item.id)
    except Exception as e:
        return e

def delete_item(item_id):

    '''
    delete Item
    :param item_id: item's id for delete
    :return: bool
    '''

    try:
        Items.objects(id = item_id).delete()
        return True
    except Exception as e:
        return False

def get_Items_id_by_Name(name):

    '''
    find Item by id
    :param id: item's id for search
    :return: str - id or '' if item not found
    '''

    res = Items.objects(title = name)
    if len(res) > 0:
        return str(res[0].id)
    return ''

def get_Users():

    '''
    list of Users
    :return: list of lists user's id, user's name, user's isAdmin, user's isWorker
    '''

    result = Users.objects()
    list = []
    for i in result:
        list.append([str(i.id), i.name, i.isAdmin, i.isWorker])
    return list

def save_Users(id_, new_):

    '''
    save/update User
    :param id: user's id for search
    :param new_: dict for save/update
    :return: Exception, str - result
    '''

    try:
        if id_ != '':
            Users.objects(id=id_)[0].update(name=new_['name'],
                                                   isAdmin=new_['isAdmin'],
                                                   isWorker=new_['isWorker'],
                                                   login=new_['login'],
                                                   password=new_['password'])
            return ''
        else:
            user = Users(
                name = new_['name'],
                isAdmin = new_['isAdmin'],
                isWorker = new_['isWorker'],
                login = new_['login'],
                password = new_['password'])
            user.save()
            return str(user.id)
    except Exception as e:
        return str(e)

def delete_user(user_id):

    '''
    delete User
    :param user_id: User's id for delete
    :return: bool, Exception
    '''

    try:
        Users.objects(id=user_id).delete()
        return True
    except Exception as e:
        return False


def get_Orders():

    '''
    list of Orders
    :return: list of lists order's id, order's number, order's isIn, order's isOut,, name of user, who change/create order
    '''

    result = Order.objects()
    list = []
    for i in result:
        list.append([str(i.id), i.number, str(i.date), i.isIn, i.isOut, i.sum, str(i.author.name)])
    return list


def get_Order_table(id_):

    '''
    list of order's items
    :return: list of lists item's id, item's title, price, quatuty, sum
    '''

    result = []
    for i in Order.objects(id = id_)[0].table_items:
        result.append([str(i[0].id), i[0].title, i[1], i[2], i[3]])
    return result

def save_Orders(id_, new_):

    '''
    save/update Order
    :param id: order's id for search
    :param new_: dict for save/update
    :return: Exception, str - result
    '''

    try:
        list = []
        for i in new_['table_items']:
            list.append([Items.objects(id=i[0])[0], i[2], i[3], i[4]])
        author = Users.objects(name=new_['author'])[0]

        if new_['date'] == '':
            date = datetime.datetime.now
        else:
            date = datetime.datetime.strptime(new_['date'],"%Y-%m-%d %H:%M:%S.%f")
        print(f"*{new_['date']}* *{date}*")
        if id_ != '':
            Order.objects(id=id_)[0].update(number=new_['number'],
                                           author=author,
                                           date=date,
                                           isIn=new_['isIn'],
                                           isOut=new_['isOut'],
                                           sum=new_['sum'],
                                           table_items=list)
            print(Order.objects(id=id_)[0].date)
            return ''
        else:
            order = Order(
                number=new_['number'],
                author=author,
                date=date,
                isIn=new_['isIn'],
                isOut=new_['isOut'],
                sum=new_['sum'],
                table_items=list)
            order.save()
            print(order.date)
            return str(order.id)
    except Exception as e:
        return e


def delete_order(order_id):
    '''
    delete Order
    :param order_id: User's id for delete
    :return: bool
    '''

    try:
        Order.objects(id=order_id).delete()
        return True
    except Exception as e:
        return False


def get_Items_Name():
    '''
    list of item's titles
    :return: list
    '''

    result = Items.objects()
    list = []
    for i in result:
        list.append([i.title])
    return list

def connect():

    '''
    connect to MongoDB
    '''

    me.connect('mongoengine_warehouse', host='localhost', port=27017)

def disconnect():

    '''
    disconnect to MongoDB
    '''

    me.disconnect()

def fill_test_data():
    '''
    fill test data to MongoDB
    '''
    import Test_Data
    Test_Data.delete_data()
    Test_Data.fill_Test_Data()

def how_many_records():
    '''
    return count of records MongoDB
    :return: list
    '''
    return len(Items.objects) + len(Users.objects) + len(Order.objects)