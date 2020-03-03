CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR')
)

SR_PRIVAT, SR_MONO, SR_VKURSE, SR_OBMEN, SR_MTB, SR_INDUSTRIAL = range(1, 7)
SOURCE_CHOICES = (
    (SR_PRIVAT, 'Privat Bank'),
    (SR_MONO, 'Mono Bank'),
    (SR_VKURSE, 'Vkurse'),
    (SR_OBMEN, 'Obmen'),
    (SR_MTB, 'MTB Bank'),
    (SR_INDUSTRIAL, 'Industrial Bank')
)
