from __future__ import absolute_import

from celery import shared_task
import praw

from .commonTasks import *
from .models import Redditor, RedditorStatus, Status


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def update_user(redditor):
    update_user_status(redditor, 10)
    get_submissions(redditor)
    update_user_status(redditor, 20)
    get_comments(redditor)
    update_user_status(redditor, 30)


@shared_task
def write_user(user):
    create_user(user)



