# 3cixty_py
Researcher at CASA UCL involved in the 3cixty project

Workflow for environment RDF object data : Air quality pollutant concentration pm10

- Download the data from Kings college website: London air quality network (LAQN).
- Specify the sites, pollutant types and date range. For the London data 1 hour averaged readings are used.
- Change datetime variable to the correct format; yyyy-mm-dd hh:MM:ss.
- Upload to postgres using create table (pm10 or pm2.5) postgres query script.
- Merge the resulting table with kcl_sites table using merge table postgres query script and then output as csv.
- Run the airquality RDF object python script and output as ttl.
- Run the pyreplace python script to correct geo:lat and geo:lon to xsd:double and output as the final ttl.
