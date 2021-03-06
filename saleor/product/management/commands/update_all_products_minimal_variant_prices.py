import logging

from django.core.management.base import BaseCommand
from tqdm import tqdm

from ....discount.utils import fetch_active_discounts
from ...models import Product
from ...utils.variant_prices import update_product_minimal_variant_price

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Recalculates the minimal variant prices for all products."

    def handle(self, *args, **options):
        self.stdout.write('Updating "minimal_variant_price" field of all the products.')
        # Fetching the discounts just once and reusing them
        discounts = fetch_active_discounts()
        # Run the update on all the products with "progress bar" (tqdm)
        qs = Product.objects.all()
        for product in tqdm(qs.iterator(), total=qs.count()):
            update_product_minimal_variant_price(product, discounts=discounts)
