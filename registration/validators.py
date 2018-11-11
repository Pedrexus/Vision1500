from django.core.validators import RegexValidator

message = "O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos são permitidos."
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=message)
