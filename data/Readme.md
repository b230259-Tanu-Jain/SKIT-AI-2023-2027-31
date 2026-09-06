# WorkSphere Dataset

This folder contains the datasets and data-processing resources used in the WorkSphere project.

## Dataset Sources

### 1. Glassdoor Dataset

**Source:** [Glassdoor Dataset](https://www.kaggle.com/datasets/davidgauthier/glassdoor-job-reviews)

Main uses:
- Company review analysis
- Sentiment analysis
- Aspect-based analysis
- Company ratings and insights
- Work-culture and work-life-balance insights

### 2. Job and Skill Dataset

**Source:** [Job and Skill Dataset](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set)

Main uses:
- Job-role identification
- Required skill extraction
- Skill-to-role mapping
- Resume-to-job matching
- Skill-gap identification

## Data Pipeline

Raw datasets are collected from their respective sources and processed before being used by the ML modules.

Raw Data → Data Cleaning → NLP/Feature Extraction → Processed Data → ML Models

## Directory Structure

- `raw/` – Original datasets. 
- `processed/` – Cleaned and transformed datasets used by the project.