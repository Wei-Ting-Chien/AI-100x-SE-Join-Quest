"""
Order Feature Step Definitions
"""

from behave import given, when, then
import sys
import os

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from order_service import (
    OrderService, Product, OrderItem, Category,
    ThresholdDiscountPromotion, BuyOneGetOnePromotion
)


@given('no promotions are applied')
def step_no_promotions(context):
    """設定無促銷活動的情境"""
    context.order_service = OrderService()


@given('the threshold discount promotion is configured')
def step_threshold_discount_configured(context):
    """設定滿額折扣促銷"""
    context.order_service = OrderService()
    
    for row in context.table:
        threshold = int(row['threshold'])
        discount = int(row['discount'])
        promotion = ThresholdDiscountPromotion(threshold, discount)
        context.order_service.add_promotion(promotion)


@given('the buy one get one promotion for cosmetics is active')
def step_buy_one_get_one_cosmetics(context):
    """設定化妝品買一送一促銷"""
    if not hasattr(context, 'order_service'):
        context.order_service = OrderService()
    
    promotion = BuyOneGetOnePromotion(Category.COSMETICS)
    context.order_service.add_promotion(promotion)


@when('a customer places an order with')
def step_customer_places_order(context):
    """客戶下訂單"""
    order_items = []
    
    for row in context.table:
        product_name = row['productName']
        quantity = int(row['quantity'])
        unit_price = int(row['unitPrice'])
        
        # 決定產品分類
        if 'category' in row.headings:
            category_str = row['category']
            category = Category.COSMETICS if category_str == 'cosmetics' else Category.APPAREL
        else:
            # 根據產品名稱推斷分類
            cosmetics_keywords = ['口紅', '粉底液', '眼影', '腮紅']
            if any(keyword in product_name for keyword in cosmetics_keywords):
                category = Category.COSMETICS
            else:
                category = Category.APPAREL
        
        product = Product(product_name, category, unit_price)
        order_item = OrderItem(product, quantity)
        order_items.append(order_item)
    
    # 建立訂單
    context.order_summary, context.delivery_items = context.order_service.create_order(order_items)


@then('the order summary should be')
def step_verify_order_summary(context):
    """驗證訂單摘要"""
    expected_row = context.table[0]
    
    if 'totalAmount' in expected_row.headings:
        expected_total = int(expected_row['totalAmount'])
        assert context.order_summary.total_amount == expected_total, \
            f"Expected total amount {expected_total}, but got {context.order_summary.total_amount}"
    
    if 'originalAmount' in expected_row.headings:
        expected_original = int(expected_row['originalAmount'])
        assert context.order_summary.original_amount == expected_original, \
            f"Expected original amount {expected_original}, but got {context.order_summary.original_amount}"
    
    if 'discount' in expected_row.headings:
        expected_discount = int(expected_row['discount'])
        assert context.order_summary.discount == expected_discount, \
            f"Expected discount {expected_discount}, but got {context.order_summary.discount}"


@then('the customer should receive')
def step_verify_delivery_items(context):
    """驗證交付項目"""
    expected_items = {}
    for row in context.table:
        product_name = row['productName']
        quantity = int(row['quantity'])
        expected_items[product_name] = quantity
    
    actual_items = {}
    for item in context.delivery_items:
        actual_items[item.product_name] = item.quantity
    
    assert expected_items == actual_items, \
        f"Expected delivery items {expected_items}, but got {actual_items}" 