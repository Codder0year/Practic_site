from django import forms
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Передаем валидатору данные из формы
        for field_name, field in self.fields.items():  # Перебираем все поля формы
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        prohibited_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
            'бесплатно', 'обман', 'полиция', 'радар', 'owner'
        ]
        for word in prohibited_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Вы не можете использовать слово "{word}" в названии продукта')
        return cleaned_data


class VersionForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Version
        fields = ['number_version', 'name_version', 'current_version']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  # Передаем валидатору данные из формы
    #     for field_name, field in self.fields.items():  # Перебираем все поля формы
    #         field.widget.attrs['class'] = 'form-control'


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_published', 'category']