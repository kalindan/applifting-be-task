from app.models.product_model import Product
from app.utils.utils import register_product


async def test_register_product():
    product = Product(name="Test product", description="Test description")
    result = await register_product(product)
    assert result == True
