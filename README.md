# FBI Crimes data

### Project Description

This project gets data from FBI site on people in search. Data is updated at site daily, but without dynamics. Project is made for this purpose: by getting data's actual state daily, it builds history to analyze trends, as well as monitor actual state by grouped parameters.

### Data Flow

![project_steps (5)](https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/ae97237a-228f-4395-93ab-ace6444d2f92)

#### Steps

1. Data is Extracted with API from external site.
2. Data is Transformed and Loaded to Google Cloud Storage Bucket (parquet format, partitioned by date) and Big Query (DWH, SQL merge).
3. With DBT, datamarts layer is created from DWH fact table.
4. In Looker Studio, dashboard is build on datamarts.

</br>

#### Tools

<p>ETL (points 1-2): Mage orchestrator. Python main libraries used: requests (for API), Pandas (transform data), pyarrow (convert to parquet with partition), SQL merge (for DWH).</p>
<p>Datamarts (point 3): DBT.</p>
<p>Data vizualization dashboard (point 4): Looker Studio.</p>
<p>Data storage: (points 2-3): Google Cloud Bucket, Big Query.</p>

</br>

#### Auto run scheduled with Mage trigger and DBT job

<p>Is project run each time manually?</p>
<p>No, it's run auto without any manual interference.</p>
<p>Trigger in Mage is run daily at 8:00 AM UTC. Mage is stored at Google Cloud Run. It takes ~ 1 hour to get data by API, transform it and load to DWH (mainly because 1 minut timeout is set for not to be banned for continuous requests to site). Data is stored in Google Cloud Bucket and updated at DWH.</p>
<p>Job at DBT is run daily at 10:00 AM UTC to recreate datamarts.</p>

</br>



### How to run project

<p>Mage (pipeline blocks) and DBT Files (schema, model) are attached to folder.</p>
1. Mage set credentials at io_config.yaml file for Big Query and Google Cloud Bucket connection.
(for project Mage was stored at Google Cloud Run as described at Course 2 of Data Engineering Zoomcamp [here]([docs/CONTRIBUTING.md](https://dezoomcamp.streamlit.app/~/+/Module%202%20Workflow%20Orchestration)) at point 7)
3. Replicate blocks with data flow. Before 1st block 'crimes_dwh' run (and after block 'crimes_export_base_layer' is successfully completed), create schema and empty table in Google Big Query, e.g. code: 

```
create schema crimes_project;

CREATE OR REPLACE EXTERNAL TABLE crimes_project.crimes
  OPTIONS (
  format = 'parquet',
  uris = ['gs://crimes_data/crimes_data/*']);

create or replace table crimes_project.dwh_crimes_data as 
select current_date() as check_date,
            * from crimes_project.crimes where 1 = 0;
```

<p>Hint for first test run you can set variable `page` in block crimes_load_data to 45. (Now it's value is for full data is 1). This variable indiates amount of pages for api request, daily it's up to 50 pages.</p>

4. Set trigger in Mage to run daily.
5. Configure dbt and create models. Set your database name there.
6. Configure dbt job to run daily, ~ 2 hours after Mage pipeline start.
7. Create dashboard in Looket Studio, source - datamart (table) created by DBT. For pie charts set default date range "today" otherwise they will show non-intepretable data from logical point of view.
 

### Dashboard

<p>Full data for 26 and 27 March 2024.</p>

<img width="1190" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/89e76828-9a26-43c0-9ede-93af0b76660d">


