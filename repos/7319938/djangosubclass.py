class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class ObjectManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

    def get(self, *args, **kwargs):
        obj = super(ObjectManager, self).get(*args, **kwargs)
        return obj.as_leaf_class()


class MyObject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True, editable=True)
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    objects = ObjectManager()


    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Device, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Device):
            return self
        return model.objects.get(id=self.id)
