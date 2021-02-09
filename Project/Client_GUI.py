import PySimpleGUI as sg
import Data_Access_MongoDB as daMDB
import Client
import Log
from datetime import datetime as dt
import dbconfig

class ClientGUI:

    '''
    GUI class for client
    '''

    def __init__(self):

        '''
        initialize object
        log - object of class Log, help do logging
        client - client part of server-client model
        dataItem - current table part of items window
        dataUser - current table part of users window
        dataOrder - current table part of items window
        dataOrderTable - current table part of items window
        user - user, result authorisation
        isAdmin - access to users (from user)
        isWorker - access to items, orders (from user)
        headings - headings of table part

        first connection run filling base by test datd if base is empty
        '''

        self.keeplog = True
        self.minlevellog = 10

        settings = dbconfig.read_db_config('configDB.ini', 'connect_client')
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
            self.log = Log.Logs('client')
            self.log.rewriteFile()

        self.trace(f'Begin work client', 0)

        self.dataItem = None
        self.dataUser = None
        self.dataOrder = None
        self.dataOrderTable = None
        self.user = None
        self.isAdmin = False
        self.isWorker = False
        self.headings = None

        self.trace(f'Make client part', 0)

        self.client = Client.ClientSocket(settings['host'], int(settings['port']))
        self.trace(f'Initialising socket', 0)
        self.client.init_socket()
        self.trace(f'Try connect to server', 0)

        self.client.connect()

        self.trace(f'Fill test base', 0)
        command = self.make_command('Fill test data')
        self.trace(f'Send {command} type: {type(command)}', 5)
        res = self.client.send(command)
        self.trace(f'Result {res}', 10)

    def trace(self, message, levellog):
        if self.keeplog:
            if levellog <= self.minloglevel:
                self.log.trace(message, levellog)

    def make_command(self, command, param = {}):

        '''
        make dict with next structure (user, command, param)
        user - current user
        command - command for server to do
        param - parameters for command
        :param command: str command's name
        :param param: dict parameters
        :return: dict
        '''

        return {'user' : self.user, 'command' : command, 'param' : param}

    def CheckLogin(self, login, password):

        '''
        send login, password for find user
        :param login: login
        :param password: password
        :return: str, quit()
        '''

        try:
            param = {}
            param['login'] = login
            param['password'] = password
            command = self.make_command('CheckLogin', param)
            self.trace(f'Send {command} type: {type(command)}', 5)
            res = self.client.send(command)
            self.trace(f'Result {res}', 10)

            self.user, self.isAdmin, self.isWorker = res

            if self.user == None:
                quit()
        except Exception as e:
            self.trace(f"Input client exception check login {e} ", 1)
            quit()

    def Login(self):

        '''
        window for input login
        '''

        try:
            layout = [[sg.Text('Input Login & password', justification="center",size=(100,1))],
                             [sg.Text('Login', size=(15, 1)), sg.InputText(key='-LOGIN-',size=(85,1))],
                             [sg.Text('Password', size=(15, 1)), sg.InputText(key='-PASSWORD-',size=(85,1), password_char='*')],
                             [sg.Submit(), sg.Cancel()]]

            window = sg.Window('Window Title', layout)

            event, values = window.read()
            window.close()

            return event, values

        except Exception as e:
            self.trace(f"Erroe login window {e} ", 1)
            quit()

    def make_item_table(self, num_cols):
        '''
        fill dataItem
        :param num_cols: int quantity columns
        '''
        try:
            self.trace(f'make_item_table', 5)
            command = self.make_command('make_item_table')

            self.trace(f'Send {command} type: {type(command)}', 5)
            res = self.client.send(command)
            self.trace(f'Result {res}', 10)

            num = 0;
            self.dataItem = [[j for j in range(num_cols)] for i in range(len(res))]
            for i in res:
                self.dataItem[num] = [i[0], i[1], i[2], i[3]]
                num += 1

        except Exception as e:
            self.trace(f"Eroor fill table items {e} ", 1)
            quit()

    def update_item_table(self):
        '''
        update items table
        '''
        try:
            self.trace(f'update_item_table', 5)
            self.make_item_table(num_cols=4)
            self.headings = ['Id', 'Name', 'Price', 'User']
            layout = [[sg.Table(values=self.dataItem[:][:], headings=self.headings,  # max_col_width=25,
                                # auto_size_columns=True,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=20,
                                # alternating_row_color='lightyellow',
                                key='-TABLE-',
                                row_height=35,
                                col_widths=20,
                                tooltip='Items'

                                )],
                      [sg.Button('Edit'), sg.Button('New'), sg.Button('Delete')]]
            return layout
        except Exception as e:
            self.trace(f"Error update table items {e} ", 1)
            quit()

    def Main_Window(self):

        '''
        main window for choose collection for work
        depends on access user
        '''

        try:
            self.trace(f'update_item_table', 5)
            if self.isAdmin and self.isWorker:
                layout = [[sg.Text('Work with', justification="center", size=(100, 1))],
                          [sg.Button('Items', size=(100, 1))],
                          [sg.Button('Orders', size=(100, 1))],
                          [sg.Button('Users', size=(100, 1))]]

            elif self.isAdmin:
                layout = [[sg.Text('Work with', justification="center", size=(100, 1))],
                          [sg.Button('Users', size=(100, 1))]]

            elif self.isWorker:
                layout = [[sg.Text('Work with', justification="center", size=(100, 1))],
                          [sg.Button('Items', size=(100, 1))],
                          [sg.Button('Orders', size=(100, 1))]]

            else:
                quit()
            window = sg.Window('Main', layout)

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:  # always,  always give a way out!
                    break
                elif event == 'Items':
                    self.Main_Window_Item()
                elif event == 'Users':
                    self.Main_Window_User()
                elif event == 'Orders':
                    self.Main_Window_Order()

            window.close()
        except Exception as e:
            self.trace(f"Error main window {e} ", 1)
            quit()

    def Main_Window_Item(self):
        '''
        main window for work with items
        Edit - update existing element
        New - make new element
        Delete - delete existing element
        '''

        try:
            self.trace(f'Main_Window_Item', 5)
            layout = None
            layout = self.update_item_table()

            window = sg.Window('Items', layout
                               # font='Helvetica 25',
                               )
            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED:
                    break

                if event == 'Edit':
                    if len(values['-TABLE-']) > 0:
                        self.Windows_Item(values['-TABLE-'][0], False)
                        self.trace(f'Update Main_Window_Item', 5)
                        window.Element('-TABLE-').Update(self.dataItem[:][:])

                if event == 'New':
                    self.Windows_Item(None, True)
                    self.trace(f'Update Main_Window_Item', 5)
                    window.Element('-TABLE-').Update(self.dataItem[:][:])

                if event == 'Delete':
                    param = {}
                    param['id'] = self.dataItem[values['-TABLE-'][0]][0]
                    command = self.make_command('delete_item', param)
                    self.trace(f'Send {command} type: {type(command)}', 5)
                    res = self.client.send(command)
                    self.trace(f'Result {res}', 10)

                    self.trace(f"Delete from local data {self.dataItem[values['-TABLE-'][0]]}", 3)
                    del self.dataItem[values['-TABLE-'][0]]

                    self.trace(f'Update Main_Window_Item', 5)
                    window.Element('-TABLE-').Update(self.dataItem[:][:])

            window.close()
        except Exception as e:
            self.trace(f"Error Main Window Item {e} ", 1)
            quit()

    def Windows_Item(self, Index, isNew):
        '''
        window for make new/update item
        Submit - make/update element
        :param Index: int row's number in dataItem
        :param isNew: bool is new object
        '''
        try:
            self.trace(f'Main_Window_Item {Index} {isNew}', 5)
            name_Window = 'New'
            id = ''
            title = ''
            price = 0
            author = self.user

            if not isNew:
                name_Window = 'Edit'
                Item = self.dataItem[Index]
                id = Item[0]
                title = Item[1]
                price = Item[2]
                author = Item[3]

            layout = [[sg.Text('Id', size=(15, 1)), sg.Text(id, size=(85, 1))],
                      [sg.Text(f'Name', size=(15, 1)), sg.InputText(default_text=title, key='-NAME-', size=(85, 1))],
                      [sg.Text('Price', size=(15, 1)), sg.InputText(default_text=price, key='-PRICE-', size=(85, 1))],
                      [sg.Text('User', size=(15, 1)), sg.Text(self.user, size=(85, 1))],
                      [sg.Submit(), sg.Cancel()]]

            window = sg.Window(f'{name_Window} item', layout)

            event, values = window.read()

            if event == 'Submit':
                new = {}
                new['title'] = values['-NAME-']
                new['price'] = values['-PRICE-']
                new['author'] = self.user

                param = {}
                param['id'] = id
                param['new'] = new
                command = self.make_command('save_item', param)
                self.trace(f'Send {command} type: {type(command)}', 5)
                new_id = self.client.send(command)
                self.trace(f'Result {new_id}', 10)

                # new_id = daMDB.save_Items(id, new)

                if new_id != '' and type(new_id) == str:
                    id = new_id
                row =[id, values['-NAME-'], values['-PRICE-'], self.user]
                if isNew:
                    self.trace(f'append {row}', 3)
                    self.dataItem.append(row)
                else:
                    self.trace(f'update {row}', 3)
                    self.dataItem[Index] = row

            window.close()
        except Exception as e:
            self.trace(f"Error Windows Item {e} ", 1)
            quit()

    def make_user_table(self, num_cols):

        '''
        fill dataUser
        :param num_cols: int quantity columns
        '''

        try:
            self.trace(f'make_user_table', 5)
            command = self.make_command('make_user_table')

            self.trace(f'Send {command} type: {type(command)}', 5)
            res = self.client.send(command)
            self.trace(f'Result {res}', 10)

            num = 0;
            self.dataUser = [[j for j in range(num_cols)] for i in range(len(res))]
            for i in res:
                self.dataUser[num] = [i[0], i[1], i[2], i[3]]
                num += 1
        except Exception as e:
            self.trace(f"Error fill table users {e} ", 1)
            quit()

    def Main_Window_User(self):

        '''
        main window for work with users
        Edit - update existing element
        New - make new element
        Delete - delete existing element
        '''

        try:
            self.trace(f'Main_Window_User', 5)
            self.make_user_table(num_cols=4)
            self.headings = ['Id', 'Name', 'isAdmin', 'isWorker']
            layout = [[sg.Table(values=self.dataUser[:][:], headings=self.headings,  # max_col_width=25,
                                # auto_size_columns=True,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=20,
                                # alternating_row_color='lightyellow',
                                key='-TABLE-',
                                row_height=35,
                                col_widths=20,
                                tooltip='Users'
                                )],
                      [sg.Button('Edit'), sg.Button('New'), sg.Button('Delete')]]

            window = sg.Window('Users', layout
                               # font='Helvetica 25',
                               )
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'Edit':
                    if len(values['-TABLE-']) > 0:
                        self.Windows_User(values['-TABLE-'][0], False)
                        self.trace(f'Update Main_Window_User', 5)
                        window.Element('-TABLE-').Update(self.dataUser[:][:])

                if event == 'New':
                    self.Windows_User(None, True)
                    self.trace(f'Update Main_Window_User', 5)
                    window.Element('-TABLE-').Update(self.dataUser[:][:])

                if event == 'Delete':
                    param = {}
                    param['id'] = self.dataUser[values['-TABLE-'][0]][0]
                    command = self.make_command('delete_user', param)
                    self.trace(f'Send {command} type: {type(command)}', 5)
                    res = self.client.send(command)
                    self.trace(f'Result {res}', 10)

                    self.trace(f"Delete from local data {self.dataUser[values['-TABLE-'][0]]}", 3)
                    del self.dataUser[values['-TABLE-'][0]]

                    self.trace(f'Update Main_Window_User', 5)
                    window.Element('-TABLE-').Update(self.dataUser[:][:])

            window.close()
        except Exception as e:
            self.trace(f"Error Main Window User {e} ", 1)
            quit()

    def Windows_User(self, Index, isNew):

        '''
        window for make new/update user
        Submit - make/update element
        :param Index: int row's number in dataUser
        :param isNew: bool is new object
        '''

        try:
            self.trace(f'Main_Window_Item {Index} {isNew}', 5)
            name_Window = 'New'
            id = ''
            name = ''
            isAdmin = False
            isWorker = False
            login = ''
            password = ''
            if not isNew:
                name_Window = 'Edit'
                Item = self.dataUser[Index]
                id = Item[0]
                name = Item[1]
                isAdmin = Item[2]
                isWorker = Item[3]

            layout = [[sg.Text('Id', size=(15, 1)), sg.Text(id, size=(85, 1))],
                      [sg.Text(f'Name', size=(15, 1)), sg.InputText(default_text=name, key='-NAME-', size=(85, 1))],
                      [sg.Checkbox(text='is Admin', default=isAdmin, key='-ISADMIN-', size=(85, 1))],
                      [sg.Checkbox(text='is Worker', default=isWorker, key='-ISWORKER-', size=(85, 1))],
                      [sg.Text(f'Login', size=(15, 1)), sg.InputText(default_text=login, key='-LOGIN-', size=(85, 1))],
                      [sg.Text(f'Password', size=(15, 1)), sg.InputText(default_text=password, key='-PASSWORD-', size=(85, 1))],
                      [sg.Submit(), sg.Cancel()]]

            window = sg.Window(f'{name_Window} user', layout)

            event, values = window.read()
            if event == 'Submit':

                new = {}
                new['name'] = values['-NAME-']
                new['isAdmin'] = values['-ISADMIN-']
                new['isWorker'] = values['-ISWORKER-']
                new['login'] = values['-LOGIN-']
                new['password'] = values['-PASSWORD-']

                param = {}
                param['id'] = id
                param['new'] = new
                command = self.make_command('save_user', param)
                self.trace(f'Send {command} type: {type(command)}', 5)
                new_id = self.client.send(command)
                self.trace(f'Result {new_id}', 10)

                if new_id != '':
                    id = new_id
                row = [id, values['-NAME-'], values['-ISADMIN-'], values['-ISADMIN-'], values['-ISWORKER-']]
                if isNew:
                    self.trace(f'append {row}', 3)
                    self.dataUser.append(row)
                else:
                    self.trace(f'update {row}', 3)
                    self.dataUser[Index] = row

            window.close()
        except Exception as e:
            self.trace(f"Error Windows User {e} ", 1)
            quit()

    def make_order_table(self, num_cols):

        '''
        fill dataOrder
        :param num_cols: int quantity columns
        '''

        try:
            self.trace(f'make_order_table', 5)

            command = self.make_command('make_order_table')

            self.trace(f'Send {command} type: {type(command)}', 5)
            res = self.client.send(command)
            self.trace(f'Result {res}', 10)

            num = 0;
            self.dataOrder = [[j for j in range(num_cols)] for i in range(len(res))]
            for i in res:
                self.dataOrder[num] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
                num += 1

        except Exception as e:
            self.trace(f"Error fill table order {e} ", 1)
            quit()

    def make_order_table_table(self, id, num_cols):

        '''
        fill dataOrderTable
        :param id: str id Order
        :param num_cols: int quantity columns
        '''
        try:
            self.trace(f'make_order_table', 5)
            num = 0;
            if id != '':
                param = {}
                param['id'] = id
                command = self.make_command('make_order_table_table', param)
                self.trace(f'Send {command} type: {type(command)}', 5)
                res = self.client.send(command)
                self.trace(f'Result {res}', 10)

                self.dataOrderTable = []
                # self.dataOrderTable = [[j for j in range(num_cols)] for i in range(len(res))]
                for i in res:
                    self.dataOrderTable.append([i[0], i[1], i[2], i[3], i[4]])
                    num += 1
                if len(self.dataOrderTable) == 0:
                    self.dataOrderTable.append(['', '', '', '', ''])
            else:
                self.dataOrderTable = [['' for j in range(num_cols)]]
                # self.dataOrderTable.append(['', '', '', '', ''])
        except Exception as e:
            self.trace(f"Error fill table part order {e} ", 1)
            quit()

    def Main_Window_Order(self):

        '''
        main window for work with order
        Edit - update existing element
        New - make new element
        Delete - delete existing element
        '''

        try:
            self.trace(f'Main_Window_Order', 5)

            self.make_order_table(num_cols=7)
            self.headings = ['Id', 'Number', 'Date', 'Buy', 'Sale', 'Sum', 'Author']
            layout = [[sg.Table(values=self.dataOrder[:][:], headings=self.headings,  # max_col_width=25,
                                # auto_size_columns=True,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=20,
                                # alternating_row_color='lightyellow',
                                key='-TABLE-',
                                row_height=35,
                                col_widths=20,
                                tooltip='Order'

                                )],
                      [sg.Button('Edit'), sg.Button('New'), sg.Button('Delete')]]

            window = sg.Window('Documents', layout
                               # font='Helvetica 25',
                               )
            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED:
                    break
                if event == 'Edit':
                    if len(values['-TABLE-']) > 0:
                        self.Windows_Order(values['-TABLE-'][0], False)
                        window.Element('-TABLE-').Update(self.dataOrder[:][:])
                if event == 'New':
                    self.Windows_Order(None, True)
                    window.Element('-TABLE-').Update(self.dataOrder[:][:])

                if event == 'Delete':
                    daMDB.connect()
                    daMDB.delete_order(self.dataOrder[values['-TABLE-'][0]][0])
                    daMDB.disconnect()
                    del self.dataOrder[values['-TABLE-'][0]]
                    window.Element('-TABLE-').Update(self.dataOrder[:][:])

            window.close()
        except Exception as e:
            self.trace(f"Error fill Main Window Order {e} ", 1)
            quit()

    def sum(self):

        '''
        sum cost in dataOrderTable
        '''

        sum = 0
        for i in self.dataOrderTable:
            sum += int(i[4])
        return sum

    def Windows_Order(self, Index, isNew):

        '''
        window for make new/update order

        Edit - update existing row item
        New - make new row item
        Delete - delete existing row item
        Submit - make/update element

        :param Index: int row's number in dataOrder
        :param isNew: bool is new object

        '''

        try:
            self.trace(f'Windows_Order {Index} {isNew}', 5)
            command = self.make_command('get_Items')
            self.trace(f'Send {command} type: {type(command)}', 5)
            res = self.client.send(command)
            self.trace(f'Result {res}', 10)
            list_item = [i[1] for i in res]

            name_Window = 'New'
            id = ''
            number = ''
            date = ''
            isIn = False
            isOut = False
            sum = 0
            author = self.user

            self.headings = ['Id', 'Item', 'Price', 'Quantity', 'Sum']
            if not isNew:
                name_Window = 'Edit'
                Item = self.dataOrder[Index]
                id = Item[0]
                number = Item[1]
                date = Item[2]
                isIn = Item[3]
                isOut = Item[4]
                sum = Item[5]
                author = Item[6]
                self.make_order_table_table(id, num_cols=5)
            else:
                self.make_order_table_table('', num_cols=5)

            layout = [[sg.Text('Id', size=(15, 1)), sg.Text(id, size=(85, 1))],
                      [sg.Text(f'Number', size=(15, 1)), sg.InputText(default_text=number, key='-NUMBER-', size=(65, 1)),
                       sg.Text(f'{date}', size=(15, 1)), sg.CalendarButton(button_text="Change date", key='-DATA-', size=(20, 1))],
                      [sg.Checkbox(text='Incoming', default=isIn, key='-ISIN-', size=(85, 1))],
                      [sg.Checkbox(text='Expence', default=isOut, key='-ISOUT-', size=(85, 1))],
                      [sg.Text(f'Sum', size=(15, 1)), sg.Text(sum, size=(85, 1), key='-SUM-')],
                      [sg.Text(f'Author', size=(15, 1)), sg.Text(author, size=(85, 1))],
                      [sg.Frame(layout=[[sg.Button('Edit'), sg.Button('New'), sg.Button('Delete')]],
                                title='Edit/new rows',relief=sg.RELIEF_RAISED, tooltip='Use these to edit/new rows')],
                      [sg.Table(values=self.dataOrderTable[:][:], headings=self.headings,   max_col_width=100,
                                # auto_size_columns=True,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=20,
                                # alternating_row_color='lightyellow',
                                key='-TABLE-',
                                row_height=35,
                                col_widths=20,
                                tooltip='Items',
                                size=(100, 1)
                                )],
                      [sg.Submit(), sg.Cancel()]]

            window = sg.Window(f'{name_Window} order', layout)

            event, values = window.read()
            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED:
                    break
                if event == 'Edit':
                    if len(values['-TABLE-']) > 0:
                        self.Windows_Order_Table_Edit(values['-TABLE-'][0], list_item)
                        window.Element('-TABLE-').Update(self.dataOrderTable[:][:])
                        window.Element('-SUM-').Update(self.sum())

                if event == 'New':
                    if self.dataOrderTable[0][0] == '' or self.dataOrderTable[0][0] == '0':
                        self.Windows_Order_Table_Edit(0, list_item)
                    else:
                        self.Windows_Order_Table_Edit(None, list_item)
                    window.Element('-TABLE-').Update(self.dataOrderTable[:][:])
                    window.Element('-SUM-').Update(self.sum())

                if event == 'Delete':
                    self.trace(f"Delete row in order table {self.data[values['-TABLE-'][0]]}", 3)
                    del self.dataOrderTable[values['-TABLE-'][0]]
                    window.Element('-TABLE-').Update(self.dataOrderTable[:][:])
                    window.Element('-SUM-').Update(self.sum())

                if event == 'Submit':
                    new = {}

                    new['number'] = values['-NUMBER-']
                    if values['-DATA-'] != '':
                        new['date'] = str(values['-DATA-'])
                    elif isNew:
                        new['date'] = dt.now()
                    else:
                        new['date'] = date
                    new['isIn'] = values['-ISIN-']
                    new['isOut'] = values['-ISOUT-']
                    new['sum'] = sum
                    new['author'] = author
                    new['table_items'] = self.dataOrderTable


                    param = {}
                    param['id'] = id
                    param['new'] = new
                    command = self.make_command('save_order', param)
                    self.trace(f'Send {command} type: {type(command)}', 5)
                    new_id = self.client.send(command)
                    self.trace(f'Result {new_id}', 10)

                    if new_id != '' and type(new_id) == str:
                        id = new_id

                    row = [id, new['number'], new['date'], new['isIn'], new['isOut'], sum, self.user]
                    if isNew:
                        self.trace(f'append {row}', 3)
                        self.dataOrder.append(row)
                    else:
                        self.trace(f'update {row}', 3)
                        self.dataOrder[Index] = row
                    break

            window.close()
        except Exception as e:
            self.trace(f"Error Windows Order {e} ", 1)
            quit()

    def Windows_Order_Table_Edit(self, Index, list_item):
        '''
        window for make new/update row in table items
        Submit - make/update element
        :param Index: int row's number in dataOrderTable
        :param list_item: list list of item's title
        '''

        try:
            self.trace(f'Windows_Order_Table_Edit {Index} {list_item}', 5)
            name_Window = 'New'
            id = ''
            item = ''
            price = 0
            quantity = 0
            sum = 0
            value = None
            if Index != None:
                name_Window = 'Edit'
                Item = self.dataOrderTable[Index]
                id = Item[0]
                item = Item[1]
                price = Item[2]
                quantity = Item[3]
                sum = Item[4]
                if item != '':
                    value = list_item[list_item.index(item)]


            layout = [[sg.Text('Item', size=(15, 1)), sg.InputCombo(default_value= value, values=list_item, key='-ITEM-', size=(85, 1))],
                      [sg.Text('Price', size=(15, 1)), sg.InputText(default_text=price, key='-PRICE-', size=(85, 1))],
                      [sg.Text('Quantity', size=(15, 1)), sg.InputText(default_text=quantity, key='-QUANTITY-', size=(85, 1))],
                      [sg.Text('Sum', size=(15, 1)), sg.InputText(default_text=sum, key='-SUM-', size=(85, 1))],
                      [sg.Submit(), sg.Cancel()]]

            window = sg.Window(f'{name_Window} row in table', layout, keep_on_top=True)

            event, values = window.read()


            if event == 'Submit':
                if item != values['-ITEM-']:
                    param = {}
                    param['name'] = values['-ITEM-']
                    command = self.make_command('get_Items_id_by_Name', param)
                    self.trace(f'Send {command} type: {type(command)}', 5)
                    id = self.client.send(command)
                    self.trace(f'Result {id}', 10)

                row = [id, values['-ITEM-'], int(values['-PRICE-']) ,int(values['-QUANTITY-']), int(values['-SUM-'])]
                if Index != None:
                    self.trace(f'append {row}', 3)
                    self.dataOrderTable[Index] = row
                else:
                    self.trace(f'update {row}', 3)
                    self.dataOrderTable.append(row)
            window.close()

        except Exception as e:
            self.trace(f"Error Windows_Order_Table_Edit {e} ", 1)
            quit()

if __name__ == '__main__':
    client = ClientGUI()
    while client.user == None:
        event, values = client.Login()
        if event == None or event == 'Cancel''': # close
            client.trace(f'Close application', 0)
            quit()
        elif event == 'Submit':
            client.CheckLogin(values['-LOGIN-'], values['-PASSWORD-'])
            if client.user != None:
                break
            else:
                client.trace(f"Can't find user", 0)
    client.Main_Window()