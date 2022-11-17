from django.forms import ModelForm

from .models import CategoryOffer,SubcategoryOffer,ProductOffer,Coupon


class CategoryOfferForm(ModelForm):
    class Meta:
        model=CategoryOffer
        fields=['category_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select Category"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Amount"}
        )


class SubcategoryOfferForm(ModelForm):
    class Meta:
        model=SubcategoryOffer
        fields=['subcategory_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subcategory_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select SubCategory"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Amount"}
        )


class ProductOfferForm(ModelForm):
    class Meta:
        model=ProductOffer
        fields=['product_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select Product"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Amount"}
        )


class CouponOfferForm(ModelForm):
    class Meta:
        model=Coupon
        fields=['code','discount','min_amount','valid_from','valid_to']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs.update(
            {"class":"form-control","placeholder":"Create Coupon Code"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter the discount amount"}
        )
        self.fields["min_amount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter the Minimum amount"}
        )
        self.fields["valid_from"].widget.attrs.update(
            {"class":"form-control","placeholder":"Valid from"}
        )
        self.fields["valid_to"].widget.attrs.update(
            {"class":"form-control","placeholder":"Valid to"}
        )