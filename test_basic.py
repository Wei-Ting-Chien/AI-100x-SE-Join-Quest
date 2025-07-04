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
    ThresholdDiscountPromotion, BuyOneGetOnePromotion, Double11Promotion
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
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 斷言驗證
    assert summary.total_amount == 500, f"Expected 500, got {summary.total_amount}"
    assert len(delivery_items) == 1, f"Expected 1 delivery item, got {len(delivery_items)}"
    assert delivery_items[0].product_name == "T-shirt", f"Expected T-shirt, got {delivery_items[0].product_name}"
    assert delivery_items[0].quantity == 1, f"Expected quantity 1, got {delivery_items[0].quantity}"
    
    print("✅ 測試通過!")


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
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 斷言驗證
    assert summary.original_amount == 1600, f"Expected original 1600, got {summary.original_amount}"
    assert summary.discount == 100, f"Expected discount 100, got {summary.discount}"
    assert summary.total_amount == 1500, f"Expected total 1500, got {summary.total_amount}"
    
    print("✅ 測試通過!")


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
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 檢查交付項目
    delivery_dict = {item.product_name: item.quantity for item in delivery_items}
    
    # 斷言驗證
    assert summary.total_amount == 700, f"Expected total 700, got {summary.total_amount}"
    assert delivery_dict["口紅"] == 2, f"Expected 口紅 quantity 2, got {delivery_dict['口紅']}"
    assert delivery_dict["粉底液"] == 2, f"Expected 粉底液 quantity 2, got {delivery_dict['粉底液']}"
    
    print("✅ 測試通過!")


def test_double11_promotion():
    """測試：雙 11 促銷"""
    print("\n=== 測試：雙 11 促銷 ===")
    
    # Given: 雙 11 促銷活動
    order_service = OrderService()
    promotion = Double11Promotion()
    order_service.add_promotion(promotion)
    
    # When: 客戶購買 12 個相同商品
    product = Product("Socks", Category.APPAREL, 100)
    order_item = OrderItem(product, 12)
    order_items = [order_item]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 計算促銷詳細資訊
    sets_of_10 = order_item.quantity // 10
    remaining = order_item.quantity % 10
    print(f"   - 促銷詳細: {order_item.quantity}個商品 = {sets_of_10}組(每組10個) + {remaining}個剩餘")
    print(f"   - 每組折扣: 10個商品只收8個的錢，省{2 * product.unit_price}元")
    print(f"   - 總省金額: {sets_of_10} x {2 * product.unit_price} = {summary.discount}元")
    
    # 斷言驗證
    assert summary.original_amount == 1200, f"Expected original amount 1200, got {summary.original_amount}"
    assert summary.discount == 200, f"Expected discount 200, got {summary.discount}"
    assert summary.total_amount == 1000, f"Expected total amount 1000, got {summary.total_amount}"
    assert delivery_items[0].quantity == 12, f"Expected delivery quantity 12, got {delivery_items[0].quantity}"
    
    print("✅ 測試通過!")


def test_double11_promotion_advanced():
    """測試：雙 11 促銷進階測試 - 27個商品"""
    print("\n=== 測試：雙 11 促銷進階測試 ===")
    
    # Given: 雙 11 促銷活動
    order_service = OrderService()
    promotion = Double11Promotion()
    order_service.add_promotion(promotion)
    
    # When: 客戶購買 27 個相同商品
    product = Product("Socks", Category.APPAREL, 100)
    order_item = OrderItem(product, 27)
    order_items = [order_item]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 計算促銷詳細資訊
    sets_of_10 = order_item.quantity // 10
    remaining = order_item.quantity % 10
    print(f"   - 促銷詳細: {order_item.quantity}個商品 = {sets_of_10}組(每組10個) + {remaining}個剩餘")
    print(f"   - 每組折扣: 10個商品只收8個的錢，省{2 * product.unit_price}元")
    print(f"   - 總省金額: {sets_of_10} x {2 * product.unit_price} = {summary.discount}元")
    
    # 斷言驗證
    assert summary.original_amount == 2700, f"Expected original amount 2700, got {summary.original_amount}"
    assert summary.discount == 400, f"Expected discount 400, got {summary.discount}"
    assert summary.total_amount == 2300, f"Expected total amount 2300, got {summary.total_amount}"
    assert delivery_items[0].quantity == 27, f"Expected delivery quantity 27, got {delivery_items[0].quantity}"
    
    print("✅ 測試通過!")


def test_multiple_promotions_detailed():
    """測試：多重促銷詳細驗證"""
    print("\n=== 測試：多重促銷詳細驗證 ===")
    
    # Given: 滿額折扣 + 化妝品買一送一促銷
    order_service = OrderService()
    threshold_promotion = ThresholdDiscountPromotion(1000, 100)
    bogo_promotion = BuyOneGetOnePromotion(Category.COSMETICS)
    order_service.add_promotion(threshold_promotion)
    order_service.add_promotion(bogo_promotion)
    
    # When: 客戶下訂單
    products = [
        Product("T-shirt", Category.APPAREL, 500),
        Product("口紅", Category.COSMETICS, 300)
    ]
    order_items = [
        OrderItem(products[0], 3),  # T-shirt x3 = 1500
        OrderItem(products[1], 1)   # 口紅 x1 = 300
    ]
    
    summary, delivery_items = order_service.create_order(order_items)
    
    # Then: 驗證結果
    print(f"📋 驗證結果:")
    print(f"   - 原始金額: {summary.original_amount}")
    print(f"   - 折扣金額: {summary.discount}")
    print(f"   - 總金額: {summary.total_amount}")
    print(f"   - 交付項目數量: {len(delivery_items)}")
    for i, item in enumerate(delivery_items, 1):
        print(f"   - 交付項目{i}: {item.product_name} x {item.quantity}")
    
    # 促銷詳細分析
    print(f"   - 促銷分析:")
    print(f"     * 滿額折扣: 原始金額{summary.original_amount}元 >= 1000元，享受100元折扣")
    print(f"     * 買一送一: 口紅買1送1，實際得到2個")
    
    # 檢查交付項目
    delivery_dict = {item.product_name: item.quantity for item in delivery_items}
    
    # 斷言驗證
    assert summary.original_amount == 1800, f"Expected original amount 1800, got {summary.original_amount}"
    assert summary.discount == 100, f"Expected discount 100, got {summary.discount}"
    assert summary.total_amount == 1700, f"Expected total amount 1700, got {summary.total_amount}"
    assert delivery_dict["T-shirt"] == 3, f"Expected T-shirt quantity 3, got {delivery_dict['T-shirt']}"
    assert delivery_dict["口紅"] == 2, f"Expected 口紅 quantity 2, got {delivery_dict['口紅']}"
    
    print("✅ 測試通過!")


if __name__ == "__main__":
    print("開始執行基本功能測試...")
    
    try:
        test_single_product_without_promotions()
        test_threshold_discount()
        test_buy_one_get_one_cosmetics()
        test_double11_promotion()
        test_double11_promotion_advanced()
        test_multiple_promotions_detailed()
        
        print("\n🎉 所有測試都通過了!")
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        sys.exit(1) 