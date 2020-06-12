import time
import json
import threading
from collections import Counter

from loguru import logger

from config import SYSTEM_CONFIG
from utils import send_post_request


class JobSender:
    @staticmethod
    def _send_req_in_thread(job):
        headers = {"Content-Type": "application/json", "username": "ncku"}
        data = json.dumps(
            {
                "job_type": job["job_type"],
                "job_parameters": {
                    "num": 1,
                    "resources": {
                        "executors": job["executors"],
                        "cpu": job["cpu"],
                        "mem": job["mem"],
                        "computing_time": job["computing_time"],
                    },
                },
                "deadline": job["computing_time"] + job["schedule_time"],
            }
        )
        threading.Thread(
            target=send_post_request, args=(SYSTEM_CONFIG["TARGET_URL"], headers, data)
        ).start()

    @classmethod
    def send(cls, jobs):
        logger.info(f"Job Len: {len(jobs)} - \n\n {jobs}\n")

        sleep_list = [
            jobs[num + 1]["trigger_time"] - jobs[num]["trigger_time"]
            for num, job in enumerate(jobs[:-1])
        ]

        # add time logger
        trigger_times = [job["trigger_time"] for job in jobs]
        schedule_times = [job["schedule_time"] for job in jobs]
        job_levels = [
            0 if schedule_time < 600 else 1 if schedule_time < 1200 else 2
            for schedule_time in schedule_times
        ]
        logger.info(f"trigger_time range: {sorted(trigger_times)}")
        logger.info(f"schedule_time order: {sorted(schedule_times)}")
        logger.info(f"job level order: {job_levels}")
        logger.info(f"level counts: {Counter(job_levels)}\n")

        total_time = 0
        logger.info(
            f"wait: 0s current {total_time}s"
            + f" - req: 0 success - schedule_time: {jobs[0]['schedule_time']} - {job_levels[0]}"
        )

        cls._send_req_in_thread(jobs[0])

        for num, sleep_time in enumerate(sleep_list):
            time.sleep(sleep_time)
            total_time += sleep_time

            cls._send_req_in_thread(jobs[num + 1])
            logger.info(
                f"wait: {sleep_time}s current {total_time}s"
                + f" - req: {num + 1} success - schedule_time: {jobs[num + 1]['schedule_time']} - {job_levels[num + 1]}"
            )
