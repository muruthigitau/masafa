import logging
from core.models import Reminder
from core.utils import send_custom_email, send_sms
from django.utils import timezone

logger = logging.getLogger(__name__)
from datetime import timedelta

from django.utils import timezone


def send_reminder_notifications():
    now = timezone.now()
    two_weeks_later = now + timedelta(weeks=2)
    reminders = Reminder.objects.filter(enabled=True, next_run__isnull=False, next_run__lte=two_weeks_later)

    for reminder in reminders:
        pre_reminder_time = reminder.get_pre_reminder_datetime()

        # Handle pre-reminder
        if pre_reminder_time and not reminder.prereminder_ran and pre_reminder_time <= now:
            for user in reminder.users.all():
                    notify_user(reminder, user)
            
            reminder.prereminder_ran = True
            reminder.save()

        # Handle actual reminder execution
        if reminder.next_run.date() == now.date():
            for user in reminder.users.all():
                    notify_user(reminder, user)
            
            reminder.update_next_run()
            reminder.save()

    
    now = timezone.now()
    ten_minutes = timedelta(minutes=10)
    
    # Filter reminders that are enabled and have a next_run in the future
    reminders = Reminder.objects.filter(enabled=True)
    
    

    logger.info(f"Running cron job. Found {reminders.count()} reminders to process.")

    for reminder in reminders:
        try:
            
            # Calculate prereminder time
            prereminder_time = reminder.next_run - reminder.prereminder

            if prereminder_time - ten_minutes <= now <= reminder.next_run and not reminder.prereminder_ran:
                # Send the prereminder notification
                for user in reminder.users.all():
                    notify_user(reminder, user)  # Send prereminder

                # Set prereminder_ran to True after sending the prereminder
                reminder.prereminder_ran = True
                reminder.save()

            # Check if we're within 10 minutes of the next_run time for the actual reminder
            elif reminder.next_run - ten_minutes <= now <= reminder.next_run + ten_minutes:
                # Send the main reminder notification
                for user in reminder.users.all():
                    notify_user(reminder, user)  # Send main reminder

                # Call calculate_next_run to determine the next scheduled reminder
                if reminder.frequency != "Once": reminder.calculate_next_run()

                # Reset prereminder_ran so it can be sent again before the next_run
                reminder.prereminder_ran = False
                reminder.save()
        except:
            pass



def notify_user(reminder, user):
    context = {
        'message': reminder.message,
    }
    
    if user.email:
        logger.info(f"Sending email to {user.email}")
        send_custom_email(
            subject=f"Reminder Notification - {reminder.name}",
            template_name="email/default.html",
            context=context,
            recipient_list=[user.email],
        )
    
    if user.phone:
        logger.info(f"Sending SMS to {user.phone}")
        send_sms(user.phone, f"Reminder Notification - {reminder.name} \n{reminder.message}")





