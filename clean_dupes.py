import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Admission, UserProfile
from django.db.models import Count

def clean_duplicates():
    print("Checking for duplicates in Admission...")
    dupes = Admission.objects.values('phone').annotate(count=Count('id')).filter(count__gt=1)
    for dupe in dupes:
        phone = dupe['phone']
        print(f"Found {dupe['count']} entries for phone {phone}")
        records = Admission.objects.filter(phone=phone).order_by('-id')
        # Keep the latest one, delete the rest
        to_delete = records[1:]
        for r in to_delete:
            print(f"Deleting duplicate for {r.name} ({r.phone})")
            r.delete()

    print("\nChecking for duplicates in UserProfile...")
    dupes_p = UserProfile.objects.values('phone').annotate(count=Count('id')).filter(count__gt=1)
    for dupe in dupes_p:
        phone = dupe['phone']
        if not phone: continue # Skip empty phone numbers if they are allowed (but we have unique=True now)
        print(f"Found {dupe['count']} entries for phone {phone}")
        records = UserProfile.objects.filter(phone=phone).order_by('-id')
        to_delete = records[1:]
        for r in to_delete:
            print(f"Deleting duplicate profile for {r.user.username} ({r.phone})")
            r.delete()

if __name__ == "__main__":
    clean_duplicates()
