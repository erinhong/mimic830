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

SELECT ace1.subject_id,
	ace1.val heartrate,
	ace2.val bloodpressure,
	ace3.val resprate
FROM alt_chartevents ace1
JOIN alt_chartevents ace2 ON ace1.subject_id = ace2.subject_id AND ace2.label = 'bloodpressure'
JOIN alt_chartevents ace3 ON ace1.subject_id = ace3.subject_id AND ace3.label = 'resprate'
WHERE ace1.label = 'heartrate';




