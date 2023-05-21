from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Subscription(models.Model):
    DURATION_CHOICES = [
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]
    name = models.CharField(max_length=20)
    duration = models.CharField(max_length=1, choices=DURATION_CHOICES, default='M')
    cost = models.IntegerField()
    features = models.TextField(blank=True, null=True)
    payment_id = models.CharField(max_length=100)

    def get_list(self):
        return self.features.split(',')

    def set_list(self, value):
        self.features = ','.join(value)

    def __str__(self):
        return self.name

    feature_list = property(get_list, set_list)


class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscript = models.ForeignKey(Subscription, verbose_name='Product', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    status = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True)
    is_paid = models.BooleanField(default=False)
    paid_until = models.DateField(null=True, blank=True)
    trial_valid_until = models.DateField(default=datetime.date.today() + timedelta(days=15))
    subscription_type = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, null=True, blank=True)

    def has_paid_for_current_date(self):
        current_date = datetime.date.today()
        return current_date < self.paid_until

    def is_trial_over(self):
        current_date = datetime.date.today()
        return current_date > self.trial_valid_until

    @staticmethod
    def is_paid_user(user):
        activation = Activation.objects.filter(user=user).first()
        return activation

    @staticmethod
    def check_paid_user(user):
        activation = Activation.objects.filter(user=user).first()
        if activation is None:
            return False
        return True

    @staticmethod
    def activate(stripe_session, line_items, user):
        email = stripe_session["customer_email"]
        created_at = datetime.datetime.fromtimestamp(stripe_session["created"])
        expired_at = datetime.datetime.today() + timedelta(days=30)
        # expired_at = datetime.datetime.fromtimestamp(stripe_session["expires_at"])
        is_paid = stripe_session["payment_status"]
        code = stripe_session["subscription"]
        if len(line_items["data"]) > 0:
            payment_id = line_items["data"][0]["price"]["id"]
            subscription = Subscription.objects.get(payment_id=payment_id)
        else:
            return None,None

        if is_paid == "paid":
            stripe_payment_intent = stripe_session["id"]
            amount = stripe_session["amount_total"]
            activation = Activation.objects.create(user=user, created_at=created_at, code=code, email=email,
                                                   is_paid=True,
                                                   paid_until=expired_at, subscription_type=subscription)
            order_details = OrderDetail.objects.create(user=user, subscript=subscription, amount=amount,
                                                       stripe_payment_intent=stripe_payment_intent, status=True,
                                                       created_on=created_at)

            return activation, order_details

        else:
            return None,None

    # def deactivate(self):
    #     self.is_paid = False
    #     self.paid_until = None
    #     self.save()


"""
class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    desc = models.TextField(blank=True, default='')
    type = models.CharField(max_length=20, choices=subscription_choices, default="FREE")
    duration = models.CharField(max_length=20, choices=duration_choices, default="select duration")
    cost = models.IntegerField()

    def duration_in_days(self):
        if self.duration == 'monthly':
            return 30  # or any number of days you choose
        elif self.duration == 'yearly':
            return 365  # or any number of days you choose
        else:
            raise ValueError('Invalid duration')'''
 
class Subscription(models.Model):
        def __init__(self, id, subscription_type, desc, price, storage_limit, features):
            self.id = id
            self.subscription_type = subscription_type
            self.desc = desc
            self.price = price
            self.storage_limit = storage_limit
            self.features = features
        def __str__(self):
            self.subscription_type
        def create_stripe_plan(self):
            stripe.api_key = 'pk_test_51McS4uSG4BR6YpnQyLUy50KAqQNkBeFUzLYsJ1vbj60tMkmkEg2hfAfZIWbgpHD8MNdo8QMxUooIGQyyb31xu4n500kxM0whTq'
            plan = stripe.Plan.create(
                amount=int(self.price * 100),
                interval='month',
                product={
                    'name': self.subscription_type,
                    'type': 'service',
                },
                currency='usd',
                id=self.stripe_plan_id,
            )
            return plan

        def create_stripe_subscription(self, customer_id, metadata=None):
            stripe.api_key = 'pk_test_51McS4uSG4BR6YpnQyLUy50KAqQNkBeFUzLYsJ1vbj60tMkmkEg2hfAfZIWbgpHD8MNdo8QMxUooIGQyyb31xu4n500kxM0whTq'
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': self.stripe_plan_id,
                    },
                ],
                metadata=metadata,
            )
            return subscription



class UserProfilePic(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

    def set_avatar(self):
        avatar = self.avatar
        if not avatar:
            self.avatar="path/to/default/avatar.png"

"""
