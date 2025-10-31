
class JobMarketplace:
    """
    This is a class that provides functionalities to publish positions, remove positions, submit resumes, withdraw resumes, search for positions, and obtain candidate information.
    """

    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        job = {
            'job_title': job_title,
            'company': company,
            'requirements': requirements
        }
        self.job_listings.append(job)

    def remove_job(self, job):
        if job in self.job_listings:
            self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        resume = {
            'name': name,
            'skills': skills,
            'experience': experience
        }
        self.resumes.append(resume)

    def withdraw_resume(self, resume):
        if resume in self.resumes:
            self.resumes.remove(resume)

    def search_jobs(self, criteria):
        result = []
        for job in self.job_listings:
            if criteria in job.get('requirements', []):
                result.append(job)
        return result

    def get_job_applicants(self, job):
        def matches_requirements(resume, requirements):
            return all(req in resume.get('skills', []) for req in requirements)
        requirements = job.get('requirements', [])
        applicants = []
        for resume in self.resumes:
            if matches_requirements(resume, requirements):
                applicants.append(resume)
        return applicants
