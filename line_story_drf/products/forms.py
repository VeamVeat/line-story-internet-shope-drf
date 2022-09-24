from django import forms

from products.models import Product


class ProductAdminForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, max_length=255)

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        fields = '__all__'
        model = Product
