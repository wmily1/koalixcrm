# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _


class Position(models.Model):
    position_number = models.PositiveIntegerField(verbose_name=_("Position Number"))
    quantity = models.DecimalField(verbose_name=_("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), blank=True, null=True)
    unit = models.ForeignKey("Unit", verbose_name=_("Unit"), blank=True, null=True)
    sent_on = models.DateField(verbose_name=_("Shipment on"), blank=True, null=True)
    overwrite_product_price = models.BooleanField(verbose_name=_('Overwrite Product Price'))
    position_price_per_unit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2,
                                               blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Price"),
                                                blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Tax"),
                                              blank=True, null=True)

    def __str__(self):
        return _("Position") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        ordering = ["position_number"]
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesDocumentPosition(Position):
    sales_document = models.ForeignKey("SalesDocument", verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Position in Sales Document')
        verbose_name_plural = _('Positions Sales Document')

    def create_position(self, calling_model, attach_to_model):
        """Copies all the content of the calling model and attaches
        links itself to the attach_to_model, this function is usually
        used within the create invoice, quote, reminder,... functions"""

        self.product = calling_model.product
        self.position_number = calling_model.position_number
        self.quantity = calling_model.quantity
        self.description = calling_model.description
        self.discount = calling_model.discount
        self.product = calling_model.product
        self.unit = calling_model.unit
        self.sent_on = calling_model.sent_on
        self.overwrite_product_price = calling_model.overwrite_product_price
        self.position_price_per_unit = calling_model.position_price_per_unit
        self.last_pricing_date = calling_model.last_pricing_date
        self.last_calculated_price = calling_model.last_calculated_price
        self.last_calculated_tax = calling_model.last_calculated_tax
        self.sales_document = attach_to_model
        self.save()

    def __str__(self):
        return _("Sales Document Position") + ": " + str(self.id)


class SalesDocumentInlinePosition(admin.TabularInline):
    model = SalesDocumentPosition
    extra = 1
    classes = ['expand']
    fieldsets = (
        ('', {
            'fields': (
            'position_number', 'quantity', 'unit', 'product', 'description', 'discount', 'overwrite_product_price',
            'position_price_per_unit', 'sent_on')
        }),
    )
    sortable_field_name = "position_number"
    allow_add = True

