-- get rows of activity manager ACTIVITY data
create or replace view getfit.activityTemplate as
select json_array_elements(json_array_elements->'activityLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager'

-- get rows of activity manager STEP data
create or replace view getfit.stepTemplate as
select json_array_elements(json_array_elements->'stepLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager'



-- convert activities to sql tables
create or replace view getfit.activities as select 
    activities->'act' as activity, 
    activities->'conf' as confidence,
    to_timestamp(activities->>'start', 'YYYY-MM-DD HH24:MI:SS:MS:US') as start,
    to_timestamp(activities->>'end', 'YYYY-MM-DD HH24:MI:SS:MS:US') as end
from (
        select json_array_elements(json_array_elements->'activityLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager') as foo



-- convert steps to sql tables
create or replace view getfit.steps as select 
    activities->>'step' as steps, 
    to_timestamp(activities->>'start', 'YYYY-MM-DD HH24:MI:SS:MS:US') as start,
    to_timestamp(activities->>'end', 'YYYY-MM-DD HH24:MI:SS:MS:US') as end
from (
        select json_array_elements(json_array_elements->'stepLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager') as foo;

