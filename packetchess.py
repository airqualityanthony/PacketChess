#!/opt/venv/bin/python
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
print("running script")
import sys
import os
import sqlite3
import datetime
import configparser
import chess  # python-chess library for chess logic

print("imports complete, getting paths")
# get the directory path of the running script
script_path = os.path.dirname(os.path.abspath(__file__))

# build paths to required files
config_file_path = os.path.join(script_path, 'packetchess.ini')
db_file_path = os.path.join(script_path, 'packetchess.db')

print("loading config and connecting to database")
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
          next_move TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# get the user's callsign
# callsign = input().strip()
callsign = "M7TAW"
print(config['chess']['banner'])

# show the latest entries on the wall
num_entries = config['games'].getint('perpage')
max_message_length = config['games'].getint('maxlen')

start_index = 0


while True:
    ## print the current page of games
    c.execute('SELECT id, callsign, fen, next_move, timestamp FROM games ORDER BY timestamp DESC LIMIT ? OFFSET ?', (num_entries, start_index))
    games = c.fetchall()
    if not games:
        print("No more games.")
    for game in games:
        print(f"Game ID: {game[0]}, Callsign: {game[1]}, FEN: {game[2]}, NextMove: {game[3]}, LastMove: {game[4]}")
    print("\nCommands: [s]tart a new game, [l]oad game,[n]ext page, [p]revious page, E[x]it")
    command = input("Enter command: ").strip().lower()
    if command == 's':
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position FEN
        if "w" in fen:
            next_move = "w"
        else:
            next_move = "b"
        if len(fen) > max_message_length:
            print(f"FEN string exceeds maximum length of {max_message_length}.")
        else:
            c.execute('INSERT INTO games (callsign, fen, next_move) VALUES (?, ?, ?)', (callsign, fen, next_move))
            conn.commit()
            print("New game started.")
    elif command == 'l':
        game_id = input("Game ID to load: ").strip()
        c.execute('SELECT fen FROM games WHERE id = ?', (game_id,))
        result = c.fetchone()
        if result:
            print(f"Loaded game FEN: {result[0]}")
            board = chess.Board(result[0])
            while True:
                move = input("Enter your move in UCI format (e.g., e2e4): ").strip()
                try:
                    chess_move = chess.Move.from_uci(move)
                except ValueError:
                    print("Invalid move format.")
                    continue
                if chess_move in board.legal_moves:
                    board.push(chess_move)
                    fen = board.fen()
                    break
                else:
                    print("Illegal move.")
                    continue
            # set next_move based on the board's current turn
            next_move = 'w' if board.turn else 'b'
            c.execute('UPDATE games SET fen = ?, next_move = ?, timestamp = ? WHERE id = ?', (fen, next_move, datetime.datetime.now(), game_id))
            conn.commit()
            print(f"Move {move} made - Game updated.")
            action = input("Action: [r]eturn to games list, e[x]it to node: ").strip().lower()
            if action == 'r':
                # break this inner action loop and return to the main games list loop
                continue
            elif action == 'x':
                conn.close()
                print(config['chess']['exitmsg'])
                sys.exit(0)
            else:
                print("Invalid option.")
        else:
            print("Game ID not found.")
    elif command == 'n':
        start_index += num_entries
    elif command == 'p':
        start_index = max(0, start_index - num_entries)
    elif command == 'x':
        conn.close()
        print(config['chess']['exitmsg'])
        break
    else:
        print("Invalid command.")

