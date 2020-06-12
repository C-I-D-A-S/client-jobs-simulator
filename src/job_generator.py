import numpy as np
from loguru import logger

from config import JOB_TRIGGER_CONFIG, JOBS_CONFIG, SYSTEM_CONFIG


class JobGenerator:
    @staticmethod
    def get_value(key):
        def get_normal_value(key):
            if isinstance(JOBS_CONFIG[key]["range"][-1], int):
                value_size = (
                    JOBS_CONFIG[key]["range"][-1] - JOBS_CONFIG[key]["range"][0]
                )
                mean_value = np.mean(JOBS_CONFIG[key]["range"])

                normal_value = int(
                    np.random.normal(loc=mean_value, scale=value_size * 0.1)
                )
            else:
                value_size = len(JOBS_CONFIG[key]["range"])
                mean_value = int(np.mean(range(value_size)))

                normal_value = int(
                    np.random.normal(loc=mean_value, scale=value_size * 0.1)
                )
                return JOBS_CONFIG[key]["range"][normal_value]

            return normal_value

        def get_uniform_value(key):
            if isinstance(JOBS_CONFIG[key]["range"][-1], int):
                return int(
                    np.random.uniform(
                        low=JOBS_CONFIG[key]["range"][0],
                        high=JOBS_CONFIG[key]["range"][-1],
                    )
                )

            index = int(
                np.random.uniform(low=0, high=len(JOBS_CONFIG[key]["range"]) - 1)
            )

            return JOBS_CONFIG[key]["range"][index]

        def get_slope_value(key):
            """ e.g. range: 1~3 -> probabilites = 1/6, 2/6, 3/6
            """
            if isinstance(JOBS_CONFIG[key]["range"][-1], int):
                value_size = (
                    JOBS_CONFIG[key]["range"][-1] - JOBS_CONFIG[key]["range"][0]
                ) + 1
            else:
                value_size = len(JOBS_CONFIG[key]["range"])

            probabilites = np.arange(1, value_size + 1) / (
                sum(range(1, value_size + 1))
            )

            if JOBS_CONFIG[key]["slope"] == "DESC":
                probabilites = probabilites[::-1]

            if isinstance(JOBS_CONFIG[key]["range"][-1], int):
                if (JOBS_CONFIG[key]["range"][-1] - JOBS_CONFIG[key]["range"][0]) == 0:
                    return JOBS_CONFIG[key]["range"][0]

                return int(
                    np.random.choice(
                        np.arange(
                            JOBS_CONFIG[key]["range"][0],
                            JOBS_CONFIG[key]["range"][-1] + 1,
                        ),
                        p=probabilites,
                    )
                )
            else:
                index = np.random.choice(np.arange(0, value_size), p=probabilites)
                return JOBS_CONFIG[key]["range"][index]

        value_map = {
            "default": JOBS_CONFIG[key]["default"],
            "normal": get_normal_value(key),
            "uniform": get_uniform_value(key),
            "slope": get_slope_value(key),
        }

        return value_map[JOBS_CONFIG[key]["distribution"]]

    @classmethod
    def get_job(cls, trigger_time=None):
        if not trigger_time:
            trigger_time = int(cls.get_value("random_trigger_time"))

        return {
            "job_type": cls.get_value("job_type"),
            "trigger_time": trigger_time,
            "schedule_time": cls.get_value("schedule_time"),
            "computing_time": cls.get_value("computing_time"),
            "executors": cls.get_value("executors"),
            "cpu": cls.get_value("cpu"),
            "mem": cls.get_value("mem"),
        }

    @classmethod
    def get_schedule_jobs(cls):
        logger.warning(f"Exp Time: {SYSTEM_CONFIG['EXP_TIME']}")
        logger.warning(
            f"Schedule Job Interval: {JOB_TRIGGER_CONFIG['SCHEDULE_JOB_INTERVAL']}"
        )

        jobs = []
        for schedule_trigger_time in JOB_TRIGGER_CONFIG["SCHEDULE_JOB_INTERVAL"]:
            start_time = 1
            while start_time < SYSTEM_CONFIG["EXP_TIME"]:
                job = cls.get_job(start_time)
                start_time += schedule_trigger_time
                jobs.append(job)

        return jobs

    @classmethod
    def gen(cls):
        # random on-demand jobs
        jobs = [cls.get_job() for _ in range(JOB_TRIGGER_CONFIG["RANDOM_JOB_NUM"])]
        # pre-defined schedule jobs
        schedule_jobs = cls.get_schedule_jobs()

        return sorted([*jobs, *schedule_jobs], key=lambda x: x["trigger_time"])
