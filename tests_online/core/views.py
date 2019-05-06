from rest_framework.generics import GenericAPIView

_null = object()


class CachedObjectMixin(GenericAPIView):
    def get_object(self):
        obj = getattr(self, '_get_object_cache', _null)
        if obj is _null:
            obj = super().get_object()
            setattr(self, '_get_object_cache', obj)
        return obj
