import socket
import json
import Data_Access_MongoDB as daMDB
import Log
import dbconfig

class ServerSocket:

    '''
    server part
    '''

    def __init__(self, HOST = "", PORT = 33336):

        '''
        initialize object
        :param HOST: str host, default local server
        :param PORT: int port, default 33336
        log - object of class Log, help do logging
        connectionMDB - connection to MongoDB
        '''

        self.keeplog = True
        self.minlevellog = 10

        settings = dbconfig.read_db_config('configDB.ini', 'connect_server')
        if settings:
            self.host = settings['host']
            self.port = int(settings['port'])
            if str(settings['keeplog']).lower() == 'false':
                self.keeplog = False
            self.minloglevel = int(settings['minloglevel'])
        else:
            # self.log.trace(f"Can't find options to create socket", 0)
            quit()

        if self.keeplog:
            self.log = Log.Logs('server')
            self.log.rewriteFile()

        self.trace(f'Build server ', 0)

        self.parametres_Db_Connection = {}
        self.parametres_Db_Connection = dbconfig.read_db_config('configDB.ini', 'mongo')

        self.connectionMDB = None

    def trace(self, message, levellog):
        if self.keeplog:
            if levellog <= self.minloglevel:
                self.log.trace(message, levellog)

    def create(self):

        '''
        create socket
        '''

        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind((self.host, self.port))

    def make_connectionMDB(self):

        '''
        create connection to MongoDB
        '''

        self.trace(f'Try connect to MongoDB server ', 0)
        if self.parametres_Db_Connection:
            self.connectionMDB = daMDB.connect(self.parametres_Db_Connection['database'],
                                               self.parametres_Db_Connection['host'],
                                               int(self.parametres_Db_Connection['port']))
        else:
            self.trace(f"Can't find options to connect to MongoDB", 0)
            quit()

        self.trace(f'Result {self.connectionMDB} ', 10)

    def fill_test_data(self):

        '''
        fill MongoDB test data
        :return: str, Exception
        '''

        try:
            self.trace(f"Run 'how_many_records()' ", 5)
            count = daMDB.how_many_records()
            res = 'Base not empty'
            if count == 0:
                self.trace(f"Run 'how_many_records()'", 5)
                daMDB.fill_test_data()
                self.trace('fill data', 5)
                res = 'Base was filled'
            return res
        except Exception as e:
            self.trace(f"Error try fill test data {e} ", 1)
            return e

    def CheckLogin(self, param):

        '''
        find user by login, password
        :param param: dict login,password
        :return: str, Exception
        '''

        login = param['login']
        password = param['password']
        try:
            self.trace(f"Run 'authorisation' {login} {password}", 4)
            res = daMDB.authorisation(login, password)
            self.trace(f"Result  {res}", 10)
            if res == None:
                res = ''
            return res
        except Exception as e:
            self.trace(f"Error try CheckLogin {e} ", 1)
            return e

    def make_item_table(self):

        '''
        fill items table
        :return: list of lists item's id, item's name, item's price, name of user, who change/create item
        '''

        try:
            self.trace(f"Run 'make_item_table' ", 5)
            res = daMDB.get_Items()
            return res

        except Exception as e:
            self.trace(f"Error try make_item_table {e} ", 1)
            return e

    def delete_item(self, param):

        '''
        delete item by id
        :param param: dict with id
        :return: bool, Exception
        '''

        try:
            id = param['id']
            self.trace(f"Run 'delete_item' {id}", 5)
            res = daMDB.delete_item(id)
            return res

        except Exception as e:
            self.trace(f"Error try delete_item {e} ", 1)
            return e

    def save_item(self, param):

        '''
        save/update item by id
        :param param: dict with id, new datd
        :return: str, Exception
        '''

        try:
            id = param['id']
            new = param['new']
            self.trace(f"Run 'save_item' {id}", 5)
            res = daMDB.save_Items(id, new)
            return res

        except Exception as e:
            self.trace(f"Error try save_item {e} ", 1)
            return e

    def make_user_table(self):

        '''
        fill users table
        :return: list of lists user's id, user's name, user's isAdmin, user's isWorker
        '''

        try:
            self.trace(f"Run 'make_user_table' ", 5)
            res = daMDB.get_Users()
            return res

        except Exception as e:
            self.trace(f"Error try make_user_table {e} ", 1)
            return e

    def delete_user(self, param):

        '''
        delete user by id
        :param param: dict with id
        :return: bool, Exception
        '''

        try:
            id = param['id']
            self.trace(f"Run 'delete_user' {id}", 5)
            res = daMDB.delete_user(id)
            return res

        except Exception as e:
            self.trace(f"Error try delete_user {e} ", 1)
            return e

    def save_user(self, param):

        '''
        save/update user by id
        :param param: dict with id, new datd
        :return: str, Exception
        '''

        try:
            id = param['id']
            new = param['new']
            self.trace(f"Run 'save_user' {id}", 5)
            res = daMDB.save_Users(id, new)
            return res

        except Exception as e:
            self.trace(f"Error try save_user {e} ", 1)
            return e

    def make_order_table(self):

        '''
        fill order table
        :return: list of lists order's id, order's number, order's isIn, order's isOut,, name of user, who change/create order
        '''

        try:
            self.trace(f"Run 'make_order_table' ", 5)
            res = daMDB.get_Orders()
            return res

        except Exception as e:
            self.trace(f"Error try make_order_table {e} ", 1)
            return e

    def delete_order(self, param):

        '''
        delete order by id
        :param param: dict with id
        :return: bool, Exception
        '''

        try:
            id = param['id']
            self.trace(f"Run 'delete_order' {id}", 5)
            res = daMDB.delete_order(id)
            return res

        except Exception as e:
            self.trace(f"Error try delete_order {e} ", 1)
            return e

    def save_order(self, param):

        '''
        save/update order by id
        :param param: dict with id, new datd
        :return: str, Exception
        '''

        print(param, type(param))
        try:
            id = param['id']
            new = param['new']
            self.trace(f"Run 'save_Orders' {id}", 5)
            res = daMDB.save_Orders(id, new)
            return res

        except Exception as e:
            self.trace(f"Error try save_Orders {e} ", 1)
            return e

    def make_order_table_table(self, param):

        '''
        fill table items for order
        :return: Exception, list of lists item's id, item's title, price, quatuty, sum
        '''

        try:
            id = param['id']
            self.trace(f"Run 'make_order_table_table' ", 5)
            res = daMDB.get_Order_table(id)
            return res

        except Exception as e:
            self.trace(f"Error try make_order_table_table {e} ", 1)
            return e

    def get_Items(self):

        '''
        fill table items for order
        :return: Exception, list of lists item's id, item's title, price, quatuty, sum
        '''

        try:
            self.trace(f"Run 'get_Items' {id}", 5)
            res = daMDB.get_Items()
            return res

        except Exception as e:
            self.trace(f"Error try get_Items_Name {e} ", 1)
            return e

    def get_Items_id_by_Name(self, param):

        '''
        find item by title
        :param param: dict with id
        :return: str, Exception string id
        '''

        try:
            name = param['name']
            self.trace(f"Run 'get_Items_id_by_Name' {id}", 5)
            res = daMDB.get_Items_id_by_Name(name)
            return res

        except Exception as e:
            self.trace(f"Error try get_Items_Name {e} ", 1)
            return e

    def action(self, data):

        '''
        server's answer after getting command
        :return: result function
        '''

        res = None
        dict = json.loads(data)
        user = dict['user']
        command = dict['command']
        param = dict['param']
        self.trace(f"User {user} command {command}", 8)
        self.trace(f"Connection to MongoDB {self.connectionMDB}", 8)
        if self.connectionMDB == None:
            self.make_connectionMDB()
            self.trace(f"Try connection to MongoDB {self.connectionMDB}", 8)

        if command == 'Fill test data':
            return self.fill_test_data()
        elif command == 'CheckLogin':
            return self.CheckLogin(param)

        elif command == 'make_item_table':
            return self.make_item_table()
        elif command == 'delete_item':
            return self.delete_item(param)
        elif command == 'save_item':
            return self.save_item(param)
        elif command == 'get_Items':
            return self.get_Items()
        elif command == 'get_Items_id_by_Name':
            return self.get_Items_id_by_Name(param)

        elif command == 'make_user_table':
            return self.make_user_table()
        elif command == 'delete_user':
            return self.delete_user(param)
        elif command == 'save_user':
            return self.save_user(param)

        elif command == 'make_order_table':
            return self.make_order_table()
        elif command == 'delete_order':
            return self.delete_order(param)
        elif command == 'save_order':
            return self.save_order(param)
        elif command == 'make_order_table_table':
            return self.make_order_table_table(param)

    def run(self):

        '''
        run server
        server getting command and send result execution

        '''

        self.create()
        self.trace('Server create ', 0)

        if_continue = True
        if_continue_listen = True
        self.trace(f"Server {self.host} listen port {self.port}", 0)

        while if_continue_listen:
            self.srv.listen(1)
            sock, addr = self.srv.accept()

            last_recv_error = None
            last_send_error = None

            while if_continue:
                answer = None
                try:
                    message = sock.recv(1024)
                    if not message:
                        break
                    self.trace(f"Received from {addr} {message} {sock} ", 3)
                    answer = self.action(message)
                except Exception as e:
                    if type(last_recv_error) != type(e):
                        self.trace(f"Input server exception {e} try recv", 1)
                    last_recv_error = e
                    break

                else:
                    if answer != None:
                        try:
                            self.trace(f"answer {answer}, {type(answer)}", 3)
                            s = json.dumps(answer).encode('utf-8')
                            self.trace(f"send {s}, {type(s)}, {sock}", 3)
                            sock.send(s)
                            self.trace(f"success", 10)
                            answer = None

                        except Exception as e:
                            if type(last_send_error) != type(e):
                                self.trace(f"Out server exception {e} try send", 1)
                            last_send_error = e
                            break

        sock.close()
        self.trace('server stopped ', 0)

if __name__ == '__main__':
    serv = ServerSocket()
    serv.run()


