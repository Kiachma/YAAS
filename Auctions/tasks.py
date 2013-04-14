__author__ = 'eaura'
from models import Auction,AuctionStatus
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from celery.schedules import crontab
from celery.task import periodic_task

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
def sendMails(auction):
    send_mail('You won' + auction.name,
              'Congratulations! You won auction ' + auction.name + '. Your winning bid was' + str(
                  auction.getLatestBid().bid), 'YAAS@YAAS.fi',
              [auction.getLatestBid().user.email], fail_silently=False)
    for bid in auction.bid_set.all():
        send_mail(auction.name + ' Resolved', 'Te auction' + auction.name+ ' has been resolved. The winner is ' +auction.getLatestBid().user.get_full_name(), 'YAAS@YAAS.fi',
                  [bid.user.email], fail_silently=False)



@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def updateAuctions():
    auctions = Auction.objects.filter(Q(status=AuctionStatus.active))
    i=0
    for auction in auctions:
        if auction.deadline<timezone.now():
            auction.status=AuctionStatus.adjudicated
            i += 1
            winner = auction.getLatestBid()
            if winner is not None:
                sendMails(auction)
            auction.save()
    return i
