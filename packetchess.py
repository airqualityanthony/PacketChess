#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
packetchess.py

Title: Node Packet Chess
Description: 
Author: Anthony Walker airqualityanthony@github
Created: Dec 2025
Version: 1.0


Changelog:
* Init
"""
import sys
import os
import sqlite3
import datetime
import configparser

# get the directory path of the running script
script_path = os.path.dirname(os.path.abspath(__file__))

# build paths to required files
config_file_path = os.path.join(script_path, 'packetchess.ini')
db_file_path = os.path.join(script_path, 'packetchess.db')

# load config file
config = configparser.ConfigParser()
config.read(config_file_path)

# connect to the database
conn = sqlite3.connect(db_file_path)
c = conn.cursor()

# create a table for the packetchess games
c.execute('''CREATE TABLE IF NOT EXISTS games
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              callsign TEXT,
              fen TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# get the user's callsign
callsign = input().strip()
print(config['chess']['banner'])

# show the latest entries on the wall
num_entries = config['games'].getint('perpage')
max_message_length = config['games'].getint('maxlen')

start_index = 0

while True:
    ## print the current page of games
    c.execute('SELECT id, callsign, fen, timestamp FROM games ORDER BY timestamp DESC LIMIT ? OFFSET ?', (num_entries, start_index))
    games = c.fetchall()
    if not games:
        print("No more games.")
        break
    for game in games:
        print(f"Game ID: {game[0]} | Player: {game[1]} | FEN: {game[2]} | Time: {game[3]}")
    print("\nCommands: [n]ext page, [p]revious page, E[x]it")
    command = input("Enter command: ").strip().upper()
    if command == 'n':
        start_index += num_entries
    elif command == 'p':
        start_index = max(0, start_index - num_entries)
    elif command == 'x':
        conn.close()
        print(config['chess']['exitmsg'])
        break
    else:
        print("Invalid command.")
