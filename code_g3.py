import csv
import json
import logging
from datetime import datetime
from jobspy import scrape_jobs
import pandas as pd
import sys
import re

def configure_logging():
    """Set up basic logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('job_scraper.log'),
            logging.StreamHandler()
        ]
    )

def scrape_job_listings(search_params):
    """
    Scrape job listings based on provided parameters
    Args:
        search_params (dict): Dictionary containing search parameters
    Returns:
        pd.DataFrame: DataFrame containing scraped job listings
    """
    try:
        logging.info(f"Starting job scraping with parameters: {search_params}")

        jobs = scrape_jobs(
            site_name=search_params['site_names'],
            search_term=search_params['search_term'],
            location=search_params['location'],
            results_wanted=search_params['results_wanted'],
            hours_old=search_params['hours_old'],
            country_indeed=search_params['country_indeed']
        )

        logging.info(f"Successfully scraped {len(jobs)} jobs")
        return jobs

    except Exception as e:
        logging.error(f"Error during job scraping: {str(e)}")
        raise

def clean_job_data(jobs_df):
    """
    Clean and preprocess the scraped job data
    Args:
        jobs_df (pd.DataFrame): Raw job data
    Returns:
        pd.DataFrame: Cleaned job data
    """
    try:
        # Make a copy of the dataframe to avoid SettingWithCopyWarning
        df = jobs_df.copy()
        
        # Remove duplicate jobs based on job URL
        initial_count = len(df)
        df.drop_duplicates(subset=['job_url'], keep='first', inplace=True)
        logging.info(f"Removed {initial_count - len(df)} duplicate jobs")
        
        # List of columns to keep - modify as needed based on your specific needs
        columns_to_keep = [
            'job_id', 'title', 'company', 'location', 'job_type', 
            'date_posted', 'job_url', 'description', 'salary', 
            'job_site'
        ]
        
        # Keep only columns that exist in the dataframe
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]
        
        # Clean text fields
        text_columns = ['title', 'company', 'location', 'description', 'salary']
        for col in text_columns:
            if col in df.columns:
                # Replace newlines with spaces
                df[col] = df[col].apply(lambda x: ' '.join(str(x).splitlines()) if isinstance(x, str) else x)
                # Remove extra spaces
                df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip() if isinstance(x, str) else x)
                # Remove any non-printable characters
                df[col] = df[col].apply(lambda x: ''.join(c for c in str(x) if c.isprintable()) if isinstance(x, str) else x)
        
        # Convert date columns to datetime
        if 'date_posted' in df.columns:
            df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
        
        # Clean location data
        if 'location' in df.columns:
            # Extract city and country if possible
            df['location'] = df['location'].apply(lambda x: clean_location(x) if isinstance(x, str) else x)
        
        # Standardize job_type values
        if 'job_type' in df.columns:
            df['job_type'] = df['job_type'].apply(lambda x: standardize_job_type(x) if isinstance(x, str) else x)
        
        # Extract salary information in a more structured way if present
        if 'salary' in df.columns:
            df['salary_cleaned'] = df['salary'].apply(clean_salary)
        
        logging.info(f"Data cleaning completed. Final dataset has {len(df)} rows and {len(df.columns)} columns")
        return df
        
    except Exception as e:
        logging.error(f"Error during data cleaning: {str(e)}")
        raise

def clean_location(location_text):
    """Clean and standardize location information"""
    if pd.isna(location_text) or not location_text:
        return ""
    
    # Remove terms like "Remote" or "Hybrid" from location
    location_text = re.sub(r'\b(Remote|Hybrid|Télétravail|À distance)\b', '', location_text, flags=re.IGNORECASE)
    
    # Clean up any commas and extra spaces
    location_text = re.sub(r'\s+', ' ', location_text).strip()
    location_text = re.sub(r',\s*,', ',', location_text)
    location_text = re.sub(r'^\s*,\s*|\s*,\s*$', '', location_text)
    
    return location_text

def standardize_job_type(job_type):
    """Standardize job type values"""
    job_type = job_type.lower()
    
    if any(term in job_type for term in ['full', 'temps plein', 'cdi']):
        return 'Full-time'
    elif any(term in job_type for term in ['part', 'temps partiel']):
        return 'Part-time'
    elif any(term in job_type for term in ['contract', 'cdd']):
        return 'Contract'
    elif any(term in job_type for term in ['intern', 'stage']):
        return 'Internship'
    elif any(term in job_type for term in ['altern', 'apprenti']):
        return 'Apprenticeship'
    else:
        return job_type.capitalize()

def clean_salary(salary_text):
    """Extract and clean salary information"""
    if pd.isna(salary_text) or not salary_text:
        return None
    
    # Try to extract salary range and currency
    salary_pattern = r'(\d[\d\s,.]*[€$£k]*\s*[-–]\s*\d[\d\s,.]*[€$£k]*|\d[\d\s,.]*[€$£k]+)'
    match = re.search(salary_pattern, salary_text)
    
    if match:
        return match.group(0).strip()
    else:
        return salary_text.strip()

def analyze_job_data(jobs_df):
    """
    Perform basic analysis on the job data
    Args:
        jobs_df (pd.DataFrame): Cleaned job data
    Returns:
        dict: Dictionary containing analysis results
    """
    analysis = {}

    analysis['total_jobs'] = len(jobs_df)

    if 'company' in jobs_df.columns:
        analysis['top_companies'] = jobs_df['company'].value_counts().head(5).to_dict()

    if 'location' in jobs_df.columns:
        analysis['top_locations'] = jobs_df['location'].value_counts().head(5).to_dict()

    if 'job_type' in jobs_df.columns:
        analysis['job_types'] = jobs_df['job_type'].value_counts().to_dict()

    if 'date_posted' in jobs_df.columns:
        analysis['newest_job'] = jobs_df['date_posted'].max()
        analysis['oldest_job'] = jobs_df['date_posted'].min()

    return analysis

def save_jobs_to_csv(jobs_df, filename):
    """
    Save job data to CSV file with proper formatting
    Args:
        jobs_df (pd.DataFrame): Job data to save
        filename (str): Output filename
    """
    try:
        # Create a copy of the dataframe for export
        export_df = jobs_df.copy()
        
        # Convert datetime to string for better CSV compatibility
        if 'date_posted' in export_df.columns and export_df['date_posted'].dtype == 'datetime64[ns]':
            export_df['date_posted'] = export_df['date_posted'].dt.strftime('%Y-%m-%d')
        
        export_df.to_csv(
            filename,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar="\\",
            index=False,
            encoding='utf-8'
        )
        logging.info(f"Successfully saved job data to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")
        raise

def save_jobs_to_json(jobs_df, filename):
    """
    Save job data to JSON file
    Args:
        jobs_df (pd.DataFrame): Job data to save
        filename (str): Output filename
    """
    try:
        # Create a copy of the dataframe for export
        export_df = jobs_df.copy()
        
        # Convert datetime to string for JSON compatibility
        if 'date_posted' in export_df.columns and export_df['date_posted'].dtype == 'datetime64[ns]':
            export_df['date_posted'] = export_df['date_posted'].dt.strftime('%Y-%m-%d')
        
        # Convert to records format for clean JSON structure
        jobs_records = export_df.to_dict(orient='records')
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs_records, f, ensure_ascii=False, indent=2)
            
        logging.info(f"Successfully saved job data to {filename}")
    except Exception as e:
        logging.error(f"Error saving to JSON: {str(e)}")
        raise

def main():
    """Main function to execute the job scraping workflow"""
    configure_logging()

    # Define search parameters
    search_params = {
        'site_names': ["indeed"],
        'search_term': '"alternance" AND ("data scientist" OR "data science" OR "data analyst" OR "data analyse" OR "quantitative" OR "statisticien")',
        'location': "France",
        'results_wanted': 200,
        'hours_old': 72,
        'country_indeed': 'France'
    }

    try:
        # Step 1: Scrape job listings
        jobs = scrape_job_listings(search_params)

        # Step 2: Clean and preprocess data
        cleaned_jobs = clean_job_data(jobs)

        # Step 3: Perform basic analysis
        analysis_results = analyze_job_data(cleaned_jobs)

        # Log analysis results
        logging.info("\nJob Data Analysis Results:")
        for key, value in analysis_results.items():
            logging.info(f"{key.replace('_', ' ').title()}: {value}")

        # Step 4: Save results to CSV and JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"jobs_{timestamp}.csv"
        json_filename = f"jobs_{timestamp}.json"
        
        save_jobs_to_csv(cleaned_jobs, csv_filename)
        save_jobs_to_json(cleaned_jobs, json_filename)

        # Display sample data
        logging.info("\nSample Cleaned Job Data:")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        logging.info(cleaned_jobs.head(5).to_string())

        print(f"\nJob scraping completed successfully!")
        print(f"- Total jobs scraped: {analysis_results['total_jobs']}")
        print(f"- Data saved to: {csv_filename} and {json_filename}")
        print(f"- See job_scraper.log for detailed information")

    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
