"""
Order Service Module
提供訂單處理和促銷計算的核心邏輯
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class Category(Enum):
    """產品分類枚舉"""
    APPAREL = "apparel"
    COSMETICS = "cosmetics"


@dataclass
class Product:
    """產品類別"""
    name: str
    category: Category
    unit_price: int
    
    
@dataclass
class OrderItem:
    """訂單項目"""
    product: Product
    quantity: int
    
    @property
    def subtotal(self) -> int:
        """計算該項目的小計"""
        return self.product.unit_price * self.quantity


@dataclass
class OrderSummary:
    """訂單摘要"""
    original_amount: int
    discount: int = 0
    
    @property
    def total_amount(self) -> int:
        """計算總金額"""
        return self.original_amount - self.discount


@dataclass
class DeliveryItem:
    """交付項目"""
    product_name: str
    quantity: int


class Promotion:
    """促銷基礎類別"""
    
    def apply(self, order_items: List[OrderItem]) -> tuple[int, List[DeliveryItem]]:
        """
        應用促銷
        
        Args:
            order_items: 訂單項目列表
            
        Returns:
            tuple: (折扣金額, 交付項目列表)
        """
        raise NotImplementedError


class ThresholdDiscountPromotion(Promotion):
    """滿額折扣促銷"""
    
    def __init__(self, threshold: int, discount: int):
        self.threshold = threshold
        self.discount = discount
    
    def apply(self, order_items: List[OrderItem]) -> tuple[int, List[DeliveryItem]]:
        """應用滿額折扣"""
        total = sum(item.subtotal for item in order_items)
        discount_amount = self.discount if total >= self.threshold else 0
        
        # 交付項目就是原訂單項目
        delivery_items = [
            DeliveryItem(item.product.name, item.quantity)
            for item in order_items
        ]
        
        return discount_amount, delivery_items


class BuyOneGetOnePromotion(Promotion):
    """買一送一促銷"""
    
    def __init__(self, target_category: Category):
        self.target_category = target_category
    
    def apply(self, order_items: List[OrderItem]) -> tuple[int, List[DeliveryItem]]:
        """應用買一送一促銷"""
        delivery_items = []
        
        for item in order_items:
            if item.product.category == self.target_category:
                # 符合促銷條件的產品，每個產品最多送一個
                delivery_quantity = item.quantity + 1
            else:
                # 不符合促銷條件的產品，數量不變
                delivery_quantity = item.quantity
            
            delivery_items.append(
                DeliveryItem(item.product.name, delivery_quantity)
            )
        
        return 0, delivery_items  # 買一送一不提供折扣，只增加數量


class OrderService:
    """訂單服務"""
    
    def __init__(self):
        self.promotions: List[Promotion] = []
    
    def add_promotion(self, promotion: Promotion):
        """新增促銷"""
        self.promotions.append(promotion)
    
    def clear_promotions(self):
        """清除所有促銷"""
        self.promotions.clear()
    
    def create_order(self, order_items: List[OrderItem]) -> tuple[OrderSummary, List[DeliveryItem]]:
        """
        建立訂單
        
        Args:
            order_items: 訂單項目列表
            
        Returns:
            tuple: (訂單摘要, 交付項目列表)
        """
        original_amount = sum(item.subtotal for item in order_items)
        total_discount = 0
        final_delivery_items = []
        
        # 如果沒有促銷活動
        if not self.promotions:
            delivery_items = [
                DeliveryItem(item.product.name, item.quantity)
                for item in order_items
            ]
            summary = OrderSummary(original_amount, 0)
            return summary, delivery_items
        
        # 應用所有促銷
        current_delivery_items = [
            DeliveryItem(item.product.name, item.quantity)
            for item in order_items
        ]
        
        for promotion in self.promotions:
            discount, delivery_items = promotion.apply(order_items)
            total_discount += discount
            
            # 更新交付項目（取最新的結果）
            current_delivery_items = delivery_items
        
        summary = OrderSummary(original_amount, total_discount)
        return summary, current_delivery_items 