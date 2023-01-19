from django import template


register = template.Library()

bad_words = ('редиска', 'картошка', 'морковь')
specialsimbols = ('!', ',', '.', ':', ';')

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'

@register.filter()
def censor(value):
   if not isinstance(value, str):
      raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

   for word in value.split():
      if word[len(word) - 1] in specialsimbols:
         word = word[:len(word) - 1]
      if word.lower() in bad_words:
         value = value.replace(word, f"{word[0]}{'*' * (len(word) - 2)}")
   return value