# dezoomcamp_FinalProject

### Project Description

### Data Flow

#### Steps

1. Data is Extracted with API from external site.
2. Data is Transformed and Loaded to Google Cloud Storage Bucket (parquet format, partitioned by date) and Big Query (DWH).
3. With DBT, datamarts layer is created from DWH fact table.
4. In Looker Studio, dashboard is build on datamarts source.

</br>

#### Tools

<p>ETL (points 1-2): Mage orchestrator. Python librarise used: requests (for API), Pandas (transform data), pyarrow (convert to parquet and partition), SQL merge (for DWH).</p>
<p>Datamarts (point 3): DBT.</p>
<p>Data vizualization dashboard (point 4): Looker Studio.</p>
<p>Data storage: (points 2-3): Google Cloud Bucket, Big Query.</p>

</br>

#### Auto run scheduled with Mage trigger and DBT job

<p>Is project run manually?</p>
<p>No, it's run auto without any manual interference.</p>
<p>Trigger in Mage is run daily at 8:00 AM UTC. Mage is stored at Google Cloud Run It takes ~ 1 hour for data to get from API and load to DWH (mainly because 1 minut timeout is set for not to be banned). After trigger data is stored in Google Cloud Bucket and updated at DWH.</p>
<p>Job at DBT is run daily at 10:00 AM UTC to recreate datamarts.</p>

</br>

#### Data flow schema

![project_steps (5)](https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/ae97237a-228f-4395-93ab-ace6444d2f92)



### How to run project

1. Store Mage at Google Cloud Run as described at Course 2 of Data Engineering Zoomcamp [here]([docs/CONTRIBUTING.md](https://dezoomcamp.streamlit.app/~/+/Module%202%20Workflow%20Orchestration)) at point 7 and set credentials at io_config.yaml file for Big Query connection (all necessary access to store data at Google Cloud Bucket and Google Big Query). 
2. Replicate blocks with data flow. Before 1st block 'crimes_dwh' run (and after block 'crimes_export_base_layer' is successfully completed, create schema and empty table in Google Big Query, e.g. code: 
```
create schema crimes_project;

CREATE OR REPLACE EXTERNAL TABLE crimes_project.crimes
  OPTIONS (
  format = 'parquet',
  uris = ['gs://crimes_data/crimes_data/*']);
```
Hack: for first test run you can set variable `page` in block crimes load data to 45. (Now it's value is for full data 1). This variable indiates amount of pages for api request, dailyy it's up to 50 pages.

3. Set trigger in Mage to run daily.
4. 

### ETL Mage Blocks Schema

<img width="806" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/0c1f2826-9a31-41df-8437-499075467d36">



### Dashboard

### Jobs, Triggers, Storage data

#### Mage trigger

<img width="401" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/9b382d2e-6dbc-4626-9ebe-f6b4caf317a2">
<img width="1436" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/46ae506f-80dd-4b55-831a-208e5b1a23e8">

#### DBT job

<img width="1219" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/2ea9fb90-e9a6-415b-ab0e-c543c0daecd1">
<img width="1529" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/b5b1b44d-c2e1-4a08-b805-e5a6fac0ab5a">

#### DWH Tables

<p>Bucket</p>
<img width="595" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/d52aee4f-7369-466f-91f3-232a2d868e50">

<p>DWH layer</p>
<img width="896" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/3c2f1e8b-09af-4cf4-af19-176700890a72">

<p>Datamarts layer</p>
<img width="783" alt="image" src="https://github.com/iharmcd/dezoomcamp_FinalProject/assets/65395256/505c56a5-b36b-4a54-8d52-156e08a7a072">



