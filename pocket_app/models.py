from django.db import models
from django.utils import timezone
from datetime import timedelta
from admin_app.models import *

# Create your models here.
"""
This is the model for the pocket_app. It also uses the models from the admin_app.
It contains the following classes:
    - Item - The detail of an item in a pocket, can be used as a template for a transaction
    - Category - A model for the category of an item
    - ItemInstance - A transaction in a pocket
    - Comment - A comment on an item instance
    - Repeatability - A model for the repeatability of an item, enabling automatic generation of item instances
    - Weekday - A model for the days of the week
"""


class Weekday(models.Model):
    """
    This is the Weekday model. It represents a day of the week.
    Each weekday has a uniqueID assigned by Django and the following attributes:
        - name - Charfield (50 characters)
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Repeatability(models.Model):
    """
    This is the Repeatability model. It is a model for the repeatability of an item.
    Each repeatability has a uniqueID assigned by Django and the following attributes:
        - Repeatable Daily - Boolean
        - Repeatable Weekly - a list of values from Monday to Sunday
        - Weekly Repeat Interval - Integer
    """

    RepeatableDaily = models.BooleanField(default=False)
    RepeatableWeekly = models.ManyToManyField(Weekday, blank=True)
    WeeklyRepeatInterval = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Repeatability {self.id}"


class Category(models.Model):
    """
    This is the Category model. It is a model for the category of an item.
    Each category has a uniqueID assigned by Django and the following attributes:
        - Category name - Charfield (100 characters)
    """
    category_name = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.category_name


class Item(models.Model):
    """
    This is the Item model. It is a template for an item in a pocket.
    Each item has a uniqueID assigned by Django and the following attributes:
        - Item name - Charfield (50 characters)
        - Item description - Charfield (200 characters)
        - Item category - from a list of categories (Foreign key to Category)
        - Item type - from a list of: Task, Consequence, Reward and Adjustment
        - Item value - A integer representing the units of the item
        - createdon - DateTimeField (auto-generated by Django)
        - createdby - Foreign key to admin.User
        - Repeatability - boolean
        - repeatID - Foreign key to Repeatability
    """

    ITEM_TYPE = (
        ('Task', 'Pollen'),
        ('Consequence', 'Sting'),
        ('Reward', 'Honey'),
        ('Adjustment', 'Adjustment')
    )
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=200)
    item_category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE)
    item_value = models.IntegerField()
    createdon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, on_delete=models.PROTECT)
    repeatability = models.BooleanField(default=False)
    repeatID = models.ForeignKey(
        Repeatability, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.item_name

class ItemInstance(models.Model):
    """
    This is the ItemInstance model. It is a transaction in a pocket.
    Each item instance has a uniqueID assigned by Django and the following attributes:
        - Item - Foreign key to Item
        - BeePocketID - Foreign key to BeePocket (from admin_app)
        - Lasteditedby - Foreign key to User
        - Lasteditedon - DateTimeField (auto-generated by Django)
        - CreatedBy - Foreign key to User
        - CreatedOn - DateTimeField (auto-generated by Django)
        - Expireon - a DateTimeField
        - ActiveStatus - boolean
        - Approved - boolean
        - ApprovedBy - a string of the userid|username
        - ApprovedOn - DateTimeField (auto-generated by Django)
    """
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    BeePocketID = models.ForeignKey(BeePocket, on_delete=models.CASCADE)
    Lasteditedby = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_edited_items')
    Lasteditedon = models.DateTimeField(auto_now=True)
    CreatedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_items')
    CreatedOn = models.DateTimeField(auto_now_add=True)
    expireon = models.DateTimeField(default=(timezone.now() + timedelta(hours=24)))
    ActiveStatus = models.BooleanField(default=True)
    Approved = models.BooleanField(default=False)
    ApprovedBy = models.CharField(max_length=255, null=True, blank=True)
    ApprovedOn = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.item.item_name

    def save(self, *args, **kwargs):
        if self.Approved and isinstance(self.ApprovedBy, User):
            self.ApprovedBy = f"{self.ApprovedBy.id}|{self.ApprovedBy.username}"
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    This is the Comment model. It is a comment on an item instance.
    Each comment has a uniqueID assigned by Django and the following attributes:
        - ItemInstance - Foreign key to ItemInstance
        - Comment - Charfield (500 characters)
        - CreatedBy - Foreign key to User
        - CreatedOn - DateTimeField (auto-generated by Django)
    """
    ItemInstance = models.ForeignKey(ItemInstance, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=500)
    CreatedBy = models.ForeignKey(User, on_delete=models.PROTECT)
    CreatedOn = models.DateTimeField(auto_now_add=True)
    ReadFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.Comment
    
class CommentReadStatus(models.Model):
    """
    This is the CommentReadStatus model. It is a model for the read status of a comment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'comment')
