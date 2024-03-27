merge into crimes_project.dwh_crimes_data as target 
using (
       select
            date(check_date) as check_date,
            * except (check_date)
       from {{ df_1}}
       qualify row_number() over(partition by check_datetime, id order by check_datetime desc) = 1
) as source 
on target.check_datetime = source.check_datetime and target.id = source.id
and target.id = source.id 
when not matched then insert (
       check_date,
       check_datetime,
       title,
       id,
       crime_classification,
       reward_value,
       publication,
       caution,
       sex,
       race,
       eyes,
       hair,
       scars_and_marks,
       nationality,
       is_armed,
       is_dangerous,
       modified,
       remarks
)
values (
       source.check_date,
       source.check_datetime,
       source.title,
       source.id,
       source.crime_classification,
       source.reward_value,
       source.publication,
       source.caution,
       source.sex,
       source.race,
       source.eyes,
       source.hair,
       source.scars_and_marks,
       source.nationality,
       source.is_armed,
       source.is_dangerous,
       source.modified,
       source.remarks
)
;