
class JobMarketplace:
    """
    This is a class that provides functionalities to publish positions, remove positions, submit resumes, withdraw resumes, search for positions, and obtain candidate information.
    """

    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        """
        This function is used to publish positions,and add the position information to the job_listings list.
        :param job_title: The title of the position,str.
        :param company: The company of the position,str.
        :param requirements: The requirements of the position,list.
        :return: None
        """
        self.job_listings.append(
            {'job_title': job_title, 'company': company, 'requirements': requirements})

    def remove_job(self, job):
        """
        This function is used to remove positions,and remove the position information from the job_listings list.
        :param job: The position information to be removed,dict.
        :return: None
        """
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        """
        This function is used to submit resumes,and add the resume information to the resumes list.
        :param name: The name of the resume,str.
        :param skills: The skills of the resume,list.
        :param experience: The experience of the resume,str.
        :return: None
        """
        self.resumes.append(
            {'name': name, 'skills': skills, 'experience': experience})

    def withdraw_resume(self, resume):
        """
        This function is used to withdraw resumes,and remove the resume information from the resumes list.
        :param resume: The resume information to be removed,dict.
        :return: None
        """
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        """
        This function is used to search for positions,and return the position information that meets the requirements.
        :param criteria: The requirements of the position,str.
        :return: The position information that meets the requirements,list.
        """
        return [job for job in self.job_listings if criteria in job['requirements']]

    def get_job_applicants(self, job):
        """
        This function is used to obtain candidate information,and return the candidate information that meets the requirements by calling the matches_requirements function.
        :param job: The position information,dict.
        :return: The candidate information that meets the requirements,list.
        """
        return [resume for resume in self.resumes if self.matches_requirements(resume, job['requirements'])]

    def matches_requirements(self, resume, requirements):
        """
        This helper function checks if a resume matches the job requirements.
        :param resume: The resume information,dict.
        :param requirements: The requirements of the job,list.
        :return: True if the resume matches the requirements, False otherwise,bool.
        """
        return all(requirement in resume['skills'] for requirement in requirements)
