"""
GREEN BULL DATA ENGINE
Module: backend/automation/job_registry.py

Enterprise Automation Job Registry
Python 3.13 Compatible
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional


# ==========================================================
# JOB MODEL
# ==========================================================

@dataclass(slots=True)
class Job:

    name: str
    description: str
    schedule: str
    enabled: bool
    priority: int
    runner: Optional[Callable] = None


# ==========================================================
# JOB REGISTRY
# ==========================================================

_registry: Dict[str, Job] = {}


def register(job: Job) -> None:
    """
    Register a job.
    """

    _registry[job.name] = job


def unregister(name: str) -> None:
    """
    Remove a job.
    """

    _registry.pop(name, None)


def exists(name: str) -> bool:
    """
    Check job exists.
    """

    return name in _registry


def get(name: str) -> Optional[Job]:
    """
    Get a job.
    """

    return _registry.get(name)


def all_jobs() -> Dict[str, Job]:
    """
    Return all jobs.
    """

    return dict(_registry)


def enabled_jobs() -> Dict[str, Job]:
    """
    Return enabled jobs sorted by priority.
    """

    jobs = {
        name: job
        for name, job in sorted(
            _registry.items(),
            key=lambda item: item[1].priority,
        )
        if job.enabled
    }

    return jobs


def disable(name: str) -> None:

    job = _registry.get(name)

    if job:
        job.enabled = False


def enable(name: str) -> None:

    job = _registry.get(name)

    if job:
        job.enabled = True


def clear() -> None:
    """
    Remove all jobs.
    """

    _registry.clear()


# ==========================================================
# DEFAULT JOBS
# ==========================================================

register(
    Job(
        name="daily_sync",
        description="Daily Market Synchronization",
        schedule="daily",
        enabled=True,
        priority=10,
    )
)

register(
    Job(
        name="weekly_sync",
        description="Weekly Fundamental Synchronization",
        schedule="weekly",
        enabled=True,
        priority=20,
    )
)

register(
    Job(
        name="monthly_sync",
        description="Monthly Database Refresh",
        schedule="monthly",
        enabled=True,
        priority=30,
    )
)

register(
    Job(
        name="retry_failed",
        description="Retry Failed Symbols",
        schedule="hourly",
        enabled=True,
        priority=40,
    )
)

register(
    Job(
        name="health_monitor",
        description="Pipeline Health Monitoring",
        schedule="5min",
        enabled=True,
        priority=50,
    )
)

register(
    Job(
        name="cleanup",
        description="Database Cleanup",
        schedule="weekly",
        enabled=True,
        priority=60,
    )
)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    for name, job in enabled_jobs().items():

        print(
            f"{job.priority:02d} | "
            f"{job.name:<20} | "
            f"{job.schedule:<10} | "
            f"{job.enabled}"
        )

    print("=" * 60)

