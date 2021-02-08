#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse

'''
run client/server
main.py -t client - run client
main.py -t server - run server
'''

def createParser():

    '''
    parser argv
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-t')

    return parser

if __name__ == '__main__':
    parser = createParser()
    type_run = parser.parse_args(sys.argv[1:])

    if type_run.t == 'server':
        import Server

        serv = Server.ServerSocket()
        serv.run()

    elif type_run.t == 'client':
        import Client_GUI

        client = Client_GUI.ClientGUI()
        while client.user == None:

            event, values = client.Login()
            if event == None or event == 'Cancel''':  # close
                client.log.trace(f'Close application', 0)
                quit()
            elif event == 'Submit':
                client.CheckLogin(values['-LOGIN-'], values['-PASSWORD-'])
                if client.user != None:
                    break
                else:
                    client.log.trace(f"Can't find user", 0)
        client.Main_Window()