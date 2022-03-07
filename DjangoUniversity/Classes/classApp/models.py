from django.db import models


# define the model (database object):
class djangoClasses(models.Model):
    Title = models.CharField(max_length=40, default="")
    # Integer field needs a default value since it is not nullable by default
    CourseNumber = models.IntegerField(default=1)
    InstructorName = models.CharField(max_length=40, default="")
    Duration = models.DecimalField(default=0.00, max_digits=10000, decimal_places=2)

    # This makes the GUI use the object's title rather than 'Django Classes 1', etc..
    object = models.Manager()

    def __str__(self):
        return self.Title
