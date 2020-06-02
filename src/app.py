"""
Entry Module
Author: Po-Chun, Lu

"""

from loguru import logger

from job_generator import JobGenerator
from job_sender import JobSender


def main():
    """main function for defining simulate app"""
    jobs = JobGenerator.gen()
    JobSender.send(jobs)
    logger.info(f'\n{"="*10}\n Finish \n{"="*10}')


if __name__ == "__main__":
    main()
