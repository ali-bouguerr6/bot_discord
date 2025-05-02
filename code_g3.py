import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed"],				#renseigner ici la palteforme souhaitée (indeed / linkedin / googlejobs)
    search_term='"alternance" AND ("data scientist" OR "data science" OR "data analyst" OR "data analyse" OR "quantitative" OR "statisticien")',			#intitulé du poste recherché
    location="France",					#ville/ région 
    results_wanted=200,					#nombre de résultats voulus
    hours_old=72,						#temps maximum depuis la publication (en heures)
    country_indeed='France',			#pays pour indeed 
   
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())						#verification des resultats
jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) #enregistrement au format csv
