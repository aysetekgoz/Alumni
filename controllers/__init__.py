from .user_controller import UserController, router as user_router
from .api_user_controller import ApiUserController, router as api_user_router
from .announcement_controller import AnnouncementController, router as announcement_router
from .job_controller import JobController, router as job_router
from .api_announcement_controller import (
    ApiAnnouncementController,
    router as api_announcement_router,
)
from .api_job_posting_controller import (
    ApiJobPostingController,
    router as api_job_posting_router,
    nested_router as api_user_job_posting_router,
)
from .api_application_controller import (
    ApiApplicationController,
    router as api_application_router,
    user_nested_router as api_user_application_router,
    job_nested_router as api_job_posting_application_router,
)

__all__ = [
    "UserController",
    "ApiUserController",
    "user_router",
    "api_user_router",
    "AnnouncementController",
    "ApiAnnouncementController",
    "announcement_router",
    "JobController",
    "job_router",
    "api_announcement_router",
    "ApiJobPostingController",
    "api_job_posting_router",
    "api_user_job_posting_router",
    "ApiApplicationController",
    "api_application_router",
    "api_user_application_router",
    "api_job_posting_application_router",
]

