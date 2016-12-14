# data from all patients with all bp, hr, rr readings listed in different rows -> all patients with most recent bp, hr, rr readings listed in diff rows

CREATE VIEW mostrecent_chartevents AS
WITH most_recent AS (
SELECT subject_id, itemid, MAX(charttime) as charttime
FROM mimiciii.chartevents c 
GROUP BY subject_id, itemid
ORDER BY subject_id) 

SELECT c.subject_id, c.itemid, 
	case 
		when c.itemid = 220052
			then 'bloodpressure'
		when c.itemid = 220045
			then 'heartrate'
		when c.itemid = 220210 
			then 'resprate' 
		else null end 
	as label, 

	c.valuenum as val,

	case 
		when c.itemid = 220052
			then 'mmHg'
		when c.itemid = 220045
			then 'bpm'
		when c.itemid = 220210 
			then 'insp/min' 
		else null end 
	as valueuom,
	c.charttime

FROM mimiciii.chartevents c
INNER JOIN most_recent m 
ON m.charttime = c.charttime 
AND m.subject_id = c.subject_id
AND m.itemid = c.itemid

GROUP BY c.subject_id,c.itemid,c.valuenum,c.charttime
ORDER BY c.subject_id;

################################################
# all patients with most recent bp, hr, rr readings listed in diff rows -> only patients with all 3 readings

CREATE VIEW uniquePatients AS 
SELECT subject_id FROM (
	SELECT subject_id, count(subject_id) as numRows
	FROM mostrecent_chartevents
	GROUP BY subject_id
) AS counter 
WHERE numRows =3; 

# only patients with all 3 readings -> gets the readings and other info from those patients
CREATE VIEW alt_chartevents AS
SELECT a.* FROM mostrecent_chartevents a 
INNER JOIN uniquePatients
ON a.SUBJECT_ID = uniquePatients.SUBJECT_ID;

################################################

# gets the readings and other info from those patients -> the 3 separate readings turn into 1 row for each patient

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

# get all dead patients whose age and gender we are given
# patients over 89 years old have age fixed at 300 so we don't want these patients

CREATE VIEW dead_patients_ids AS 
SELECT *   
FROM mimiciii.patients p
WHERE p.dod is not null
AND ROUND( (cast(p.dod as date) - cast(p.dob as date)) / 365.242,2) < 300; 

# get all dead patients who has 3 readings as done above

CREATE VIEW dead_patient_ace AS 
SELECT a.* 
FROM ace a
INNER JOIN dead_patients_ids dp 
ON a.subject_id = dp.subject_id;

# export to be used as final table for NO join experiment
COPY (SELECT * FROM dead_patient_ace) to '/Users/ErinHong/Documents/dead_ace.csv' DELIMITER ',' CSV HEADER;

################################################

# get all dead patients who has 3 readings as done above and joined on age and gender
CREATE VIEW dead_patient_ace_joined AS 
SELECT dpa.*,
	ROUND( (cast(dpi.dod as date) - cast(dpi.dob as date)) / 365.242,2) AS age, 
	dpi.gender 
FROM dead_patient_ace dpa 
INNER JOIN dead_patients_ids dpi 
ON dpa.subject_id = dpi.subject_id
AND ROUND( (cast(dpi.dod as date) - cast(dpi.dob as date)) / 365.242,2) < 300; 

# export to be used as final table for join experiment
COPY (SELECT * FROM dead_patient_ace_joined) to '/Users/ErinHong/Documents/dead_ace_joined.csv' DELIMITER ',' CSV HEADER;
























