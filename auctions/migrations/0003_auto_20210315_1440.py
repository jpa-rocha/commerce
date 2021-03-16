# Generated by Django 3.1.7 on 2021-03-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_category_comments_listing_watchlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bids',
            options={'verbose_name_plural': 'bids'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name_plural': 'comments'},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='date_end',
        ),
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
