import csv
import pickle
from datetime import datetime
f = open('../../../../../../../Volumes/Transcend/raw_mimic/CHARTEVENTS.csv','rU')
header = f.readline()
wf = open('../../../../../../../Volumes/Transcend/raw_mimic/CHARTEVENTS_reduced_12_13_16.csv','w+')
wf.write(header) 
header = header.split(',')

# bp = {}
# hr = {} 
# rr = {} 
most_recent = {} 
patient_rowid = {}

for line in f:  
	unsplit_line = line 
	line = line.split(',')
	row_id = line[0]
	subject_id = line[1]
	itemid = line[4]
	charttime = line[5]

	#Only add row for each patient for each of these categories 
	if itemid == '220052':
		print subject_id
		#bp[subject_id] = True 
		wf.write(unsplit_line)

	elif itemid == '220045':
		print subject_id
		#hr[subject_id] = True 
		wf.write(unsplit_line)

	elif itemid == '220210':
		print subject_id
		# rr[subject_id] = True 
		wf.write(unsplit_line)

	# if subject_id in bp and subject_id in hr and subject_id in rr and subject_id not in distinct_patients: 
	# 	distinct_patients.append(subject_id)
	# 	print (subject_id,len(distinct_patients))

print "DONE!"
#print "Distinct Patients: ",distinct_patients

# 	year, month, day = charttime.split(' ')[0].split('-')
# 	month,day,year = int(month),int(day), int(year)

# 	if subject_id in most_recent: 
# 		logged_datetime = most_recent[subject_id]
		
# 		if datetime(year,month,day) > logged_datetime: 
# 			most_recent[subject_id] = datetime(year,month,day)
# 			patient_rowid[subject_id] = row_id 
# 	else: 
# 		most_recent[subject_id] = datetime(year,month,day)
# 		patient_rowid[subject_id] = row_id

# with open('subject_id_d.pkl','wb') as sr: 
# 	pickle.dump(patient_rowid,sr,pickle.HIGHEST_PROTOCOL)




	# past = datetime.now()
# >>> present = datetime.now()
# >>> past < present
# True
# >>> datetime(3000, 1, 1) < present
# False
# >>> present - datetime(2000, 4, 4)
# datetime.timedelta(4242, 75703, 762105)
	


#('99255', 8941)

# import pickle
# with open('subject_id_row_id.pkl', 'rb') as fp:
#     data = pickle.load(fp)
#     print data['5315']




