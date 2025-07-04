#!/usr/bin/env python3
"""
基本測試腳本 - 驗證 order_service 功能
"""

import sys
import os

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from order_service import (
    OrderService, Product, OrderItem, Category,
    ThresholdDiscountPromotion, BuyOneGetOnePromotion
)


def test_single_product_without_promotions():
    """測試：單一產品無促銷"""
    print("=== 測試：單一產品無促銷 ===")
    
    # Given: 無促銷活動
    order_service = OrderService()
    
    # When: 客戶下訂單
    product = Product("T-shirt", Category.APPAREL, 500)
    order_item = OrderItem(product, 1)
    order_items = [order_item]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    assert summary.total_amount == 500, f"Expected 500, got {summary.total_amount}"
    assert len(delivery_items) == 1, f"Expected 1 delivery item, got {len(delivery_items)}"
    assert delivery_items[0].product_name == "T-shirt", f"Expected T-shirt, got {delivery_items[0].product_name}"
    assert delivery_items[0].quantity == 1, f"Expected quantity 1, got {delivery_items[0].quantity}"
    
    print("✅ 測試通過!")
    print(f"   總金額: {summary.total_amount}")
    print(f"   交付項目: {delivery_items[0].product_name} x {delivery_items[0].quantity}")


def test_threshold_discount():
    """測試：滿額折扣"""
    print("\n=== 測試：滿額折扣 ===")
    
    # Given: 滿 1000 折 100 的促銷
    order_service = OrderService()
    promotion = ThresholdDiscountPromotion(1000, 100)
    order_service.add_promotion(promotion)
    
    # When: 客戶下訂單
    products = [
        Product("T-shirt", Category.APPAREL, 500),
        Product("褲子", Category.APPAREL, 600)
    ]
    order_items = [
        OrderItem(products[0], 2),  # T-shirt x2 = 1000
        OrderItem(products[1], 1)   # 褲子 x1 = 600
    ]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    assert summary.original_amount == 1600, f"Expected original 1600, got {summary.original_amount}"
    assert summary.discount == 100, f"Expected discount 100, got {summary.discount}"
    assert summary.total_amount == 1500, f"Expected total 1500, got {summary.total_amount}"
    
    print("✅ 測試通過!")
    print(f"   原始金額: {summary.original_amount}")
    print(f"   折扣: {summary.discount}")
    print(f"   總金額: {summary.total_amount}")


def test_buy_one_get_one_cosmetics():
    """測試：化妝品買一送一"""
    print("\n=== 測試：化妝品買一送一 ===")
    
    # Given: 化妝品買一送一促銷
    order_service = OrderService()
    promotion = BuyOneGetOnePromotion(Category.COSMETICS)
    order_service.add_promotion(promotion)
    
    # When: 客戶下訂單
    products = [
        Product("口紅", Category.COSMETICS, 300),
        Product("粉底液", Category.COSMETICS, 400)
    ]
    order_items = [
        OrderItem(products[0], 1),  # 口紅 x1
        OrderItem(products[1], 1)   # 粉底液 x1
    ]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    assert summary.total_amount == 700, f"Expected total 700, got {summary.total_amount}"
    
    # 檢查交付項目
    delivery_dict = {item.product_name: item.quantity for item in delivery_items}
    assert delivery_dict["口紅"] == 2, f"Expected 口紅 quantity 2, got {delivery_dict['口紅']}"
    assert delivery_dict["粉底液"] == 2, f"Expected 粉底液 quantity 2, got {delivery_dict['粉底液']}"
    
    print("✅ 測試通過!")
    print(f"   總金額: {summary.total_amount}")
    print(f"   交付項目: 口紅 x {delivery_dict['口紅']}, 粉底液 x {delivery_dict['粉底液']}")


if __name__ == "__main__":
    print("開始執行基本功能測試...")
    
    try:
        test_single_product_without_promotions()
        test_threshold_discount()
        test_buy_one_get_one_cosmetics()
        
        print("\n🎉 所有測試都通過了!")
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        sys.exit(1) 