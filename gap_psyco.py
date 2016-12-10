import psycopg2 
import pprint 
import psycopg2.extras 
import random 


def makeDBConnection(): 
	info = "host='localhost' dbname='mimic'"
	source = "mimiciii"
	connection = psycopg2.connect(info)
	cursor = connection.cursor()
	#cursor.execute('SELECT count(*) FROM ace;')
	#rowCount = int(cursor.fetchall()[0])
	return cursor

	#cursor.execute('SELECT * from ace limit 10;')

def induceGaps(gapPercentages,totalRows,cursor): 
	for percent in gapPercentages: 
		gapCount = totalRows * percent 
		rowIdsToRemove = set() 
		while len(rowIdsToRemove) < gapCount: 
			rowIdsToRemove.add(random.randint(0,totalRows))
		strifiedRowsIds = "[" + ",".join(str(ID) for ID in rowIdsToRemove) + "]"
		cursor.execute('SELECT a.subject_id,a.heartrate,a.bloodpressure,a.resprate FROM ( '+
			'SELECT *,row_number() over(ORDER BY ace.subject_id) as rid from ace) AS a') 




		('SELECT subject_id,heartrate,bloodpressure,resprate FROM ( '+
			'SELECT row_number() over(ORDER BY ace.subject_id) as rid,* from ace where rid not in' +" [2,3,4]" + 
			') AS preserved;')



			

#SELECT row_number() over(order by ace.subject_id) from ace limit 10;