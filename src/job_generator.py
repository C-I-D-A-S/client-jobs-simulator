import numpy as np

from config import JOB_TRIGGER_CONFIG, JOBS_CONFIG


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
    def get_job(cls):
        return {
            "job_type": cls.get_value("job_type"),
            "trigger_time": int(cls.get_value("random_trigger_time")),
            "schedule_time": cls.get_value("schedule_time"),
            "computing_time": cls.get_value("computing_time"),
            "executors": cls.get_value("executors"),
            "cpu": cls.get_value("cpu"),
            "mem": cls.get_value("mem"),
        }

    @classmethod
    def gen(cls):
        jobs = [cls.get_job() for _ in range(JOB_TRIGGER_CONFIG["RANDOM_JOB_NUM"])]

        return sorted(jobs, key=lambda x: x["trigger_time"])
