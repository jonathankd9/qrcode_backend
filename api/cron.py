from django_cron import CronJobBase, Schedule
from qrmark_database.models import UniqueCode

class DeleteUniqueCodes(CronJobBase):
    RUN_EVERY_MINS = 150 # every 2 hours 30 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'qrmark_backend.delete_unique_codes'    # a unique code

    def do(self):
        '''Delete all expired unique codes'''
        # Get all unique codes
        unique_codes = UniqueCode.objects.all()
        # Iterate over each unique code
        for unique_code in unique_codes:
            # Delete all codes
            unique_code.delete()
            
        