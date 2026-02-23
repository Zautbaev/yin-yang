from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NewsPost(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, blank=True)
    cover_image = models.ImageField('Обложка', upload_to='news/covers/', blank=True, null=True)
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата публикации', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            # ensure uniqueness
            original_slug = self.slug
            counter = 1
            while NewsPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('modteam:news_detail', kwargs={'slug': self.slug})


class NewsImage(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='images', verbose_name='Новость')
    image = models.ImageField('Изображение', upload_to='news/gallery/')
    caption = models.CharField('Подпись', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'Фото к «{self.post.title}»'


class NewsLink(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='links', verbose_name='Новость')
    label = models.CharField('Название ссылки', max_length=255)
    url = models.URLField('URL')

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return self.label


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Руководитель'),
        ('developer', 'Разработчик'),
        ('artist', 'Художник'),
        ('writer', 'Сценарист'),
        ('tester', 'Тестировщик'),
        ('other', 'Другое'),
    ]

    name = models.CharField('Имя / Ник', max_length=100)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='other')
    custom_role = models.CharField('Своя роль', max_length=100, blank=True)
    avatar = models.ImageField('Аватар', upload_to='team/avatars/', blank=True, null=True)
    bio = models.TextField('О себе', blank=True)
    vk_url = models.URLField('VK', blank=True)
    discord = models.CharField('Discord', max_length=100, blank=True)
    github_url = models.URLField('GitHub', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_display_role(self):
        return self.custom_role if self.custom_role else self.get_role_display()


class AboutPage(models.Model):
    team_name = models.CharField('Название команды', max_length=200, default='Mod Team')
    tagline = models.CharField('Слоган', max_length=300, blank=True)
    description = models.TextField('О команде')
    logo = models.ImageField('Логотип', upload_to='about/', blank=True, null=True)
    founded_year = models.PositiveIntegerField('Год основания', blank=True, null=True)
    mods_count = models.PositiveIntegerField('Кол-во модов', default=0)
    members_count = models.PositiveIntegerField('Кол-во участников', default=0)
    vk_group = models.URLField('VK группа', blank=True)
    discord_server = models.URLField('Discord сервер', blank=True)
    github_org = models.URLField('GitHub организация', blank=True)

    class Meta:
        verbose_name = 'Страница «О нас»'
        verbose_name_plural = 'Страница «О нас»'

    def __str__(self):
        return self.team_name
