from django.db import models

def icon_category_directory_path(instanse: "Category", filename: str) -> str:
    if instanse.subcategory:
        return 'catalog/icons/{subcategory}/{category}/{filename}'.format(
            subcategory=instanse.subcategory,
            category=instanse.title,
            filename=filename
        )
    else:
        return 'catalog/icons/{category}/{filename}'.format(
            category=instanse.title,
            filename=filename
        )


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='subcategories')
    favorite = models.BooleanField(default=False)
    image = models.ImageField(upload_to=icon_category_directory_path, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk',]

    def href(self):
        return f'catalog/{self.pk}'
    
    def __str__(self):
        return self.title
    
