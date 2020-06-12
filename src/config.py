"""
Module of flask config
Author: Po-Chun, Lu

"""
import os

from dotenv import load_dotenv


load_dotenv()


def str_to_list(values):
    if not values:
        return []

    return list(map(int, values.split(",")))


# DISTRIBUTION_CENTER OPTION: default, normal, avg, slope
# slope option: ASC, DESC


SYSTEM_CONFIG = {
    "TARGET_URL": os.environ.get("TARGET_URL", "http://localhost:5000/qol/jobs"),
    "EXP_TIME": int(os.environ.get("EXP_TIME", 60)),  # unit seconds,
    "EXP_VARIABLE": os.environ.get("EXP_VARIABLE", "schedule_time,"),
}

JOB_TRIGGER_CONFIG = {
    "RANDOM_JOB_NUM": int(os.environ.get("RANDOM_JOB_NUM", 10)),
    "SCHEDULE_JOB_NUM": int(os.environ.get("SCHEDULE_JOB_NUM", 10)),
    "SCHEDULE_JOB_INTERVAL": str_to_list(os.environ.get("SCHEDULE_JOB_INTERVAL", "30")),
}

JOBS_CONFIG = {
    "job_type": {
        "default": "demand_forecasting_1hr",
        "range": os.environ.get(
            "JOB_TYPE_RANGE", "demand_forecasting_1hr,demand_forecasting_1hr"
        ).split(","),
        "distribution": os.environ.get("JOB_TYPE_DISTRIBUTION", "default"),
        "distribution_center": os.environ.get("JOB_TYPE_DISTRIBUTION_CENTER", "normal"),
        "slope": os.environ.get("JOB_TYPE_DISTRIBUTION_SLOPE", "ASC"),
    },
    "random_trigger_time": {
        "default": 0,
        "range": str_to_list(
            os.environ.get("JOB_TRIGGER_RANGE", "0,10")
        ),  # unit seconds
        "distribution": os.environ.get("JOB_TRIGGER_DISTRIBUTION", "uniform"),
        "distribution_center": os.environ.get(
            "JOB_TRIGGER_DISTRIBUTION_CENTER", "normal"
        ),
        "slope": os.environ.get("JOB_TRIGGER_DISTRIBUTION_SLOPE", "ASC"),
    },
    "schedule_time": {
        "default": int(os.environ.get("JOB_SCHEDULE_DEFAULT", 500)),
        "range": str_to_list(
            os.environ.get("JOB_SCHEDULE_RANGE", "0,600,1200")
        ),  # unit seconds
        "distribution": os.environ.get("JOB_SCHEDULE_DISTRIBUTION", "normal"),
        "distribution_center": os.environ.get(
            "JOB_SCHEDULE_DISTRIBUTION_CENTER", "normal"
        ),
        "slope": os.environ.get("JOB_SCHEDULE_DISTRIBUTION_SLOPE", "ASC"),
    },
    "computing_time": {
        "default": int(os.environ.get("JOB_COMPUTING_DEFAULT", 15)),
        "range": str_to_list(
            os.environ.get("JOB_COMPUTING_RANGE", "15,30")
        ),  # unit seconds
        "distribution": os.environ.get("JOB_COMPUTING_DISTRIBUTION", "default"),
        "distribution_center": os.environ.get(
            "JOB_COMPUTING_DISTRIBUTION_CENTER", "normal"
        ),
        "slope": os.environ.get("JOB_COMPUTING_DISTRIBUTION_SLOPE", "ASC"),
    },
    "executors": {
        "default": int(os.environ.get("JOB_EXPCUTORS_DEFAULT", 1)),
        "range": str_to_list(os.environ.get("JOB_EXECUTORS_RANGE", "1,6")),
        "distribution": os.environ.get("JOB_EXECUTORS_DISTRIBUTION", "default"),
        "distribution_center": os.environ.get(
            "JOB_EXECUTORS_DISTRIBUTION_CENTER", "normal"
        ),
        "slope": os.environ.get("JOB_EXECUTORS_DISTRIBUTION_SLOPE", "ASC"),
    },
    "cpu": {
        "default": int(os.environ.get("JOB_CPU_DEFAULT", 1)),
        "range": str_to_list(os.environ.get("JOB_CPU_RANGE", "1,4")),
        "distribution": os.environ.get("JOB_CPU_DISTRIBUTION", "default"),
        "distribution_center": os.environ.get("JOB_CPU_DISTRIBUTION_CENTER", "normal"),
        "slope": os.environ.get("JOB_CPU_DISTRIBUTION_SLOPE", "ASC"),
    },
    "mem": {
        "default": int(os.environ.get("JOB_MEM_DEFAULT", 1)),  # unit G
        "range": str_to_list(os.environ.get("JOB_MEM_RANGE", "1,8")),  # unit G
        "distribution": os.environ.get("JOB_MEM_DISTRIBUTION", "default"),
        "distribution_center": os.environ.get("JOB_MEM_DISTRIBUTION_CENTER", "normal"),
        "slope": os.environ.get("JOB_MEM_DISTRIBUTION_SLOPE", "ASC"),
    },
}
