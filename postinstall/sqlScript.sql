drop table if exists getfit.positioning;
create or replace view getfit.location as select to_timestamp(json_array_elements->>'datetime', 'YYYY-MM-DD HH24:MI:SS:MS:US') as datetime,
 json_array_elements->'lat' as latitude,
 json_array_elements->'lon' as longitude,
 json_array_elements->'spd' as speed,
 json_array_elements->'crs' as course,
 json_array_elements->'vert_acc' as vertical_accuracy,
 json_array_elements->'hor_acc' as horizontal_accuracy,
 json_array_elements->'alt' as altitude
 from (select * from (select json_array_elements (data) from getfit.opensense) as alldata where json_array_elements ->>'probe' = 'positioning') as temptable;


-- create the motion view
drop table if exists getfit.motion;
create or replace view getfit.motion as select to_timestamp(json_array_elements->>'datetime', 'YYYY-MM-DD HH24:MI:SS:MS:US') as datetime,
 json_array_elements->'aR' as attitude_roll,
 json_array_elements->'aP' as attitude_pitch,
 json_array_elements->'aY' as attitude_yaw,
 json_array_elements->'rX' as rotation_x,
 json_array_elements->'rY' as rotation_y,
 json_array_elements->'rZ' as rotation_z,
 json_array_elements->'gX' as gravity_x,
 json_array_elements->'gY' as gravity_y,
 json_array_elements->'gZ' as gravity_z,
 json_array_elements->'uaX' as user_acceleration_x,
 json_array_elements->'uaY' as user_acceleration_y,
 json_array_elements->'yaZ' as user_acceleration_z
 from (select * from (select json_array_elements (data) from getfit.opensense) as alldata where json_array_elements ->>'probe' = 'motion') as temptable;

-- create the battery view
drop table if exists getfit.battery;

create or replace view getfit.battery as select to_timestamp(json_array_elements->>'datetime', 'YYYY-MM-DD HH24:MI:SS:MS:US') as datetime,
 json_array_elements->'state' as state,
 json_array_elements->'level' as level
 from (select * from (select json_array_elements (data) from getfit.opensense) as alldata where json_array_elements ->>'probe' = 'battery') as temptable;


-- create the proximity view
drop table if exists getfit.proximity;

create or replace view getfit.proximity as select to_timestamp(json_array_elements->>'datetime', 'YYYY-MM-DD HH24:MI:SS:MS:US') as datetime,
 json_array_elements->'state' as state
 from (select * from (select json_array_elements (data) from getfit.opensense) as alldata where json_array_elements ->>'probe' = 'proximity') as temptable;


-- create the deviceinfo view
drop table if exists getfit.deviceinfo;

create or replace view getfit.deviceinfo as select to_timestamp(json_array_elements->>'datetime', 'YYYY-MM-DD HH24:MI:SS:MS:US') as datetime,
 json_array_elements->>'lang' as language,
 json_array_elements->'bright' as screen_brightness,
 json_array_elements->>'country' as country,
 json_array_elements->>'version' as version,
 json_array_elements->>'model' as model
 from (select * from (select json_array_elements (data) from getfit.opensense) as alldata where json_array_elements ->>'probe' = 'deviceinfo') as temptable;

-- create the activity view
drop table if exists getfit.activity;

CREATE or replace view getfit.activities as select 
    activities->'act' as activity, 
    activities->'conf' as confidence,
    to_timestamp(activities->>'start', 'YYYY-MM-DD HH24:MI:SS:MS:US') as start,
    to_timestamp(activities->>'end', 'YYYY-MM-DD HH24:MI:SS:MS:US') as end
from (
        select json_array_elements(json_array_elements->'activityLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager') as foo;

-- create the step view
CREATE or replace view getfit.steps as select 
    activities->>'step' as steps, 
    to_timestamp(activities->>'start', 'YYYY-MM-DD HH24:MI:SS:MS:US') as start,
    to_timestamp(activities->>'end', 'YYYY-MM-DD HH24:MI:SS:MS:US') as end
from (
        select json_array_elements(json_array_elements->'stepLog') as activities from (
        select json_array_elements (data) from getfit.opensense
        ) as alldata where json_array_elements ->>'probe' = 'activitymanager') as foo;

-- drop the device table, now that constraints are removed
drop table if exists getfit.device;