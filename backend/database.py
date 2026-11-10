from features.company_data.mongodb import companies, job_roles

def get_companies():
    return list(companies.find({}, {"_id": 0}))

def get_job_roles():
    return list(job_roles.find({}, {"_id": 0}))