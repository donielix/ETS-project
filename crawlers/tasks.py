import os

import jsonutils as js
from celery import group, shared_task
from root.settings import BASE_DIR
import pandas as pd

