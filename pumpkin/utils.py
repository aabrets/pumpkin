from rest_framework import serializers


class PrimaryKeyRelatedFieldQueryset(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(PrimaryKeyRelatedFieldQueryset, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset
