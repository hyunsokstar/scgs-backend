from django.db import models
from common.models import CommonModel


# class Room(models.Model):
class Room(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHRED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=180,
        default="",
    )

    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveBigIntegerField()
    rooms = models.PositiveBigIntegerField()

    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)

    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    amenities = models.ManyToManyField(
            "rooms.Amenity",
            related_name="rooms"  
        )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms"
    )

    def __str__(self) -> str:
        return self.name
    
    # custom field 추가
    def total_amenities(self):
        print(self.amenities.all())
        return self.amenities.count()

    def rating(room):
        count = room.reviews.count()
        print("room.reviews.all().values : ", room.reviews.all().values("rating"))
        if count == 0:
            # return "No Reviews
            return 0
        else:
            total_rating = 0
            print("room.reviews.all().values : ", room.reviews.all().values("rating"))
            for review in room.reviews.all().values("rating"):
                total_rating += review['rating']
            return round(total_rating / count, 2)

# class Amenity(models.Model):
class Amenity(CommonModel):
    """ Amenity Definition """
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, default="", null=True)

    def __str__(self):
        return '%s: %s' % (self.name, self.description)

    class Meta:
        verbose_name_plural = "Amenities"