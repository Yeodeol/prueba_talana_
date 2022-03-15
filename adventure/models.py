from django.db import models
import re
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers


    def get_distribution(personas):
        """returns a matrix filled of booleans
            with the "standard distribution" in a vehicle
        """
        try:
            retorno = []
            rows = int(personas/2)
        
            par = True
            if personas % 2 == 1: #impar
                rows += 1
                par = False
            
            for el in range(rows):
                if (el+1) == rows and not par:
                    ocupados = [True,False]
                else:
                    ocupados = [True,True]
                retorno.append(ocupados)
            
            return retorno
        except Exception as err:
            return []

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        """return depends on the end value """
        if self.end is None:
            return False
        else:
            return True


def validate_number_plate(plate):
    """ valid number plate consists of three pairs of alphanumeric chars separated by hyphen
        the first pair must be letters and the rest must be numbers"""
    try:
        if re.match('([a-zA-Z]{0,2})-([0-9]{0,2})-([0-9]{0,2})',plate):
            return True
        else:
            return False
    except Exception as err:
        return False