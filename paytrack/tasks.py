from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from bot import botstart

@shared_task(name = "bot_run")
def run_bot(*args, **kwargs):
    botstart()