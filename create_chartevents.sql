CREATE VIEW pre_chartevents AS 
SELECT subject_id, itemid, 
	case 
		when c.itemid = 220052
			then 'bloodpressure'
		when c.itemid = 220045
			then 'heartrate'
		when c.itemid = 220210 
			then 'resprate' 
		else null end 
	as label, 

	avg(c.valuenum) as val,

	case 
		when c.itemid = 220052
			then 'mmHg'
		when c.itemid = 220045
			then 'bpm'
		when c.itemid = 220210 
			then 'insp/min' 
		else null end 
	as valueuom
	
FROM mimiciii.chartevents c 
GROUP BY subject_id,itemid
ORDER BY subject_id;

################################################

CREATE VIEW uniquePatients AS 
SELECT subject_id FROM (
	SELECT subject_id, count(subject_id) as numRows
	FROM pre_chartevents
	GROUP BY subject_id
) AS counter 
WHERE numRows =3; 

CREATE VIEW alt_chartevents AS
SELECT a.* FROM pre_chartevents a 
INNER JOIN uniquePatients
ON a.SUBJECT_ID = uniquePatients.SUBJECT_ID;

################################################

CREATE VIEW ace AS
SELECT ace1.subject_id,
	ace1.val heartrate,
	ace2.val bloodpressure,
	ace3.val resprate
FROM alt_chartevents ace1
JOIN alt_chartevents ace2 ON ace1.subject_id = ace2.subject_id AND ace2.label = 'bloodpressure'
JOIN alt_chartevents ace3 ON ace1.subject_id = ace3.subject_id AND ace3.label = 'resprate'
WHERE ace1.label = 'heartrate';

################################################
############## 12/12/2016 #######################
################################################


COPY (SELECT * FROM dead_patient_ace) to '/Users/ErinHong/Documents/dead_ace.csv';

CREATE VIEW dead_patients_ids AS 
SELECT *   
FROM mimiciii.patients p
WHERE p.dod is not null
AND ROUND( (cast(p.dod as date) - cast(p.dob as date)) / 365.242,2) < 300; 

# then run pre_chartevents 
# then run unique_patients 
# then run ace

CREATE VIEW dead_patient_ace AS 
SELECT a.* 
FROM ace a
INNER JOIN dead_patients_ids dp 
ON a.subject_id = dp.subject_id; 

################################################

CREATE VIEW dead_patient_ace_joined AS 
SELECT dpa.*,
	ROUND( (cast(dpi.dod as date) - cast(dpi.dob as date)) / 365.242,2) AS age, 
	dpi.gender 
FROM dead_patient_ace dpa 
INNER JOIN dead_patients_ids dpi 
ON dpa.subject_id = dpi.subject_id
AND ROUND( (cast(dpi.dod as date) - cast(dpi.dob as date)) / 365.242,2) < 300; 

COPY (SELECT * FROM dead_patient_ace) to '/Users/ErinHong/Documents/dead_ace.csv' DELIMITER ',' CSV HEADER;
COPY (SELECT * FROM dead_patient_ace_joined) to '/Users/ErinHong/Documents/dead_ace_joined.csv' DELIMITER ',' CSV HEADER;
























