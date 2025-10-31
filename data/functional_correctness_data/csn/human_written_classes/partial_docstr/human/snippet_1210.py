from chamber.shortcuts import change_and_save, change, bulk_change_and_save

class SmartQuerySetMixin:

    def fast_distinct(self):
        """
        Because standard distinct used on the all fields are very slow and works only with PostgreSQL database
        this method provides alternative to the standard distinct method.
        :return: qs with unique objects
        """
        qs = self.model.objects.filter(pk__in=self.values('pk'))
        if self.query.order_by:
            qs = qs.order_by(*self.query.order_by)
        return qs

    def change_and_save(self, update_only_changed_fields=False, **changed_fields):
        """
        Changes a given `changed_fields` on each object in the queryset, saves objects
        and returns the changed objects in the queryset.
        """
        bulk_change_and_save(self, update_only_changed_fields=update_only_changed_fields, **changed_fields)
        return self.filter()

    def first(self, *field_names):
        """
        Adds possibility to set order fields to default Django first method.
        """
        if field_names:
            return self.order_by(*field_names).first()
        else:
            return super().first()

    def last(self, *field_names):
        """
        Adds possibility to set order fields to default Django last method.
        """
        if field_names:
            return self.order_by(*field_names).last()
        else:
            return super().last()