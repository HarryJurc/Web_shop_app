from django import forms
from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_available', 'category']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

    def clean_name(self):
        name = self.cleaned_data['name']
        self._check_forbidden_words(name, 'названии')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        self._check_forbidden_words(description, 'описании')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def _check_forbidden_words(self, text, field_name):
        for word in FORBIDDEN_WORDS:
            if word.lower() in text.lower():
                raise forms.ValidationError(f"Запрещенное слово '{word}' обнаружено в {field_name}.")
