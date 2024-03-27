{{ config(materialized='table') }}

select 
    check_date,
    crime_classification,
    reward_value,
    coalesce(sex, 'undefined') as sex,
    coalesce(race, 'undefined') as race,
    coalesce(nationality, 'undefined') as nationality,
    count(distinct id) as people_in_search_cnt
from 

{{ source('staging', 'dwh_crimes_data')}}

group by 1,2,3,4,5,6