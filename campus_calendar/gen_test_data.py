# Run from within Django shell
from models import *


def gen_data():
    test_user = User.objects.create_user(username="admin",
                                         password="investigate711",
                                         is_staff=True,
                                         is_superuser=True)
    test_user.save()

    ucsb = Campus(name="UCSB")
    ucsb.save()
    ucla = Campus(name="UCLA")
    ucla.save()
    ucsd = Campus(name="UCSD")
    ucsd.save()

    UserProfile(user_id=test_user.id, main_campus=ucsb).save()

    ucsb_cal = CCalendar(name="UCSB Event Calendar", campus=ucsb)
    ucsb_cal.save()
    ucla_cal = CCalendar(name="UCLA Event Calendar", campus=ucla)
    ucla_cal.save()
    ucsd_cal = CCalendar(name="UCSD Event Calendar", campus=ucsd)
    ucsd_cal.save()

    org1 = Organization(name="Laughology", campus=ucsb, owner=test_user)
    org1.save()
    org2 = Organization(name="Basketball", campus=ucsb, owner=test_user)
    org2.save()

    event1 = Event(name="Funny Show",
                   datetime="2017-03-17 16:00",
                   location="E.Hall",
                   calendar=ucsb_cal,
                   organization=org1)
    event1.save()

    event2 = Event(name="BBall Game",
                   datetime="2017-03-16 16:00",
                   location="BBall Courts",
                   calendar=ucsb_cal,
                   organization=org2)
    event2.save()

