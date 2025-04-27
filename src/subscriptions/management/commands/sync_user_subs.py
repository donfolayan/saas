import helpers.billing
from typing import Any
from customers.models import Customer
from django.core.management.base import BaseCommand
from subscriptions import utils as subs_utils

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--clear-dangling', action='store_true', default=False)

    def handle(self, *args:Any, **options:Any):
        clear_dangling = options.get('clear_dangling')
        if clear_dangling:
            print('Clearing dangling subscriptions')
            subs_utils.clear_dangling_subs()
        else:
            print('Sync active subscriptions')  
            done = subs_utils.refresh_active_user_subscriptions(active_only=True, verbose=True)
            print('Finished syncing active subscriptions') if done else print('Failed syncing active subscriptions')
        