LOCATION_CHOICES = (
    ('HIR', 'Guadalcanal, Solomon Islands'),
    ('EME', 'Emden, Germany'),
    ('FO', 'Faroe Islands'),
    ('RYO', 'Río Turbio, Argentina'),
    ('UR', 'Uruguay'),
    ('CO', 'Colombia'),
    ('MPA', 'Katima Mulilo, Namibia'),
    ('NY', 'New York City, New York')
)

CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('USD', 'Dollar'),
    ('RUB', 'Ruble')
)

LANGUAGE_CHOICES = (
    ('EN', 'English'),
)

TIMEZONE_CHOICES = (
    ('0', 'UTC +4'),
    ('1', 'UTC 0'),
    ('2', 'UTC -1')
)

PLAN_CHOICES = (
    (0, 'Demo'),
    (1, 'Standard'),
    (2, 'Premium'),
)

PLAN_PERIOD_CHOICES = (
    (0, 'Demo'),
    (30, 'Monthly'),
    (365, 'Annual'),
)