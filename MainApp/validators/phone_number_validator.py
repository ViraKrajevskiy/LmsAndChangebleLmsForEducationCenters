from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?998\d{9}$',
    message="Телефон должен быть в формате +998XXXXXXXXX"
)