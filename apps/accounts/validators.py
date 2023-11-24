from django.forms import ValidationError
from django.core.validators import RegexValidator


def validate_name(value):
    if len(value.split()) > 1:
        raise ValidationError("No spaces between names")
    elif not value.isalpha():
        raise ValidationError("Alphabetical characters only")
    return value


alternate_validate_name = RegexValidator(
    regex=r"^[a-zA-Z]*$", message="No spaces between names"
)
