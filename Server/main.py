
#!/usr/bin/env python
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import errorcode

dbUser = 'root'
dbPassword = '0otis27kol7'
db = 'dartboard'
cnx = mysql.connector.connect(user = dbUser, password = dbPassword,
	host = '127.0.0.1',
	database = db)

cursor = cnx.cursor()

#INSERT FUNCTIONS
def insertPlayer(pid, name, sex, y, m, d):
	cursor = cnx.cursor()
	add_players = ("INSERT INTO players "
				"(pid, name, sex, birth)"
				"VALUES (%s, %s, %s, %s)")
	data_players = (pid, name, sex, date(y, m, d))
	cursor.execute(add_players, data_players)
	cnx.commit()

def insertBattlefield(gid, pid, mean_hits_per_round):
	add_battlefield = ("INSERT INTO battlefield "
	               "(gid, pid, mean_hits_per_round) "
	               "VALUES (%s, %s, %s)")
	data_battlefield = (gid, pid, mean_hits_per_round)
	cursor.execute(add_battlefield, data_battlefield)
	cnx.commit()

def insertx01(gid, pid, num_throws):
	add_x01 = ("INSERT INTO x01 "
	               "(gid, pid, num_throws) "
	               "VALUES (%s, %s, %s)")
	data_x01 = (gid, pid, num_throws)
	cursor.execute(add_x01, data_x01)
	cnx.commit()

#QUERY FUNCTIONS
def queryPlayerTable(name):
	query = ("SELECT pid, name FROM players WHERE name=%(name)s")
	cursor.execute(query, {'name' : name} )
	for (pid, name) in cursor:
		print("{}, {}".format(pid, name))
	return pid

def queryBattlefield(gid, pid):
	query = ("SELECT gid, pid, mean_hits_per_round FROM battlefield WHERE gid=%(gid)s AND pid=%(pid)s")
	data = ({'gid' : gid, 'pid' : pid})
	cursor.execute(query, data)
	for (gid, pid, mean_hits_per_round) in cursor:
		print("{}, {}, {}". format(gid, pid, mean_hits_per_round))
	return mean_hits_per_round

def queryx01(gid, pid):
	query = ("SELECT gid, pid, num_throws FROM x01 WHERE gid=%(gid)s AND pid=%(pid)s")
	data = ({'gid' : gid, 'pid' : pid})
	cursor.execute(query, data)
	for (gid, pid, num_throws) in cursor:
		print("{}, {}, {}". format(gid, pid, num_throws))
	return num_throws

#RUNNING TOTAL DATA
def queryAvgBattlefield(pid):
	query = ("SELECT pid, AVG(mean_hits_per_round) FROM battlefield WHERE pid=%(pid)s GROUP BY pid")
	data = ({'pid' : pid})
	cursor.execute(query, data)
	for(pid, mean_hits_per_round) in cursor:
		print("Average Battlefield Score\nPid:{}, Avg:{}".format(pid, mean_hits_per_round))
	return mean_hits_per_round

def queryAvgx01(pid):
	query = ("SELECT pid, AVG(num_throws) FROM x01 WHERE pid=%(pid)s GROUP BY pid")
	data = ({'pid' : pid})
	cursor.execute(query, data)
	for(pid, num_throws) in cursor:
		print("Average x01 Score\nPid:{}, Avg:{}".format(pid, num_throws))
	return num_throws

queryAvgx01(1)

cursor.close()
cnx.close()
