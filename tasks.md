# ALL Tasks

## Components
1. Infrastrucutre
2. Front End
3. Back End
4. Data Base (S3)

## OverView

Since the given time line we can't be using stream of data . We dont need specific data base to hold the process

Hence we can load the files from s3 

Mostly we only show automation , but given the costs of load from s3 . we are mostlikely to load from s3 once into ec2 machine and use it from there . 
Only update them via lambda once there is a change

### Backend Data clean up

### Pipline

Vaex as data frame over pandas since we need run certae and process 7 million records for grouping 
###
Data cleanup tasks/filters

Primary/core filters
1. Date inputs ( cut data frame based on date)
2. Primary Type
3. Year
4. Month

# subfilters for graphs 
1. Add geo json grouping filter  ( needs work)
1. Add primary type grouping 
1. Add selected district groupy filter
2. Date range filter ( given a. date range select data and apply all filter based on these)( multi filter)(can be done via call back)
3. Tooltip data ( can be achived via select filter)
4. 
5. 
