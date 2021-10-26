from django.db import models

from cabinet.models import AdvUser


class Build(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'build'

    def __str__(self):
        return f'{self.name}, {self.address}'


class Flat(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    room_count = models.IntegerField()
    type = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    owner = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flat'

    def __str__(self):
        return f'{self.build}, {self.type}'


class RentOrder(models.Model):
    renter = models.ForeignKey(AdvUser, on_delete=models.CASCADE,)
    # flat =
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        db_table = 'rent_order'

    def __str__(self):
        return f'{self.renter}'


class FlatRoom(models.Model):
    type = models.CharField(max_length=255)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = 'flat_room'

    def __str__(self):
        return self.type


class FlatAttribute(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'flat_attribute'

    def __str__(self):
        return self.name


class FlatAttributesValue(models.Model):
    attribute = models.ForeignKey(FlatAttribute, on_delete=models.CASCADE)
    flat_room = models.ForeignKey(FlatRoom, on_delete=models.CASCADE)
    count = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flat_attributes_value'

    def __str__(self):
        return f'{self.attribute}, {self.flat_room}'

