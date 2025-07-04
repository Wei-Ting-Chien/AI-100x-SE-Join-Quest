#!/usr/bin/env python3
"""
簡化的 BDD 測試運行器
模擬 behave 的行為，按照 BDD 流程執行測試
"""

import sys
import os
import re
from dataclasses import dataclass
from typing import List, Dict, Any

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from order_service import (
    OrderService, Product, OrderItem, Category,
    ThresholdDiscountPromotion, BuyOneGetOnePromotion
)


@dataclass
class TableRow:
    """模擬 behave 的 table row"""
    data: Dict[str, str]
    
    def __getitem__(self, key):
        return self.data[key]
    
    @property
    def headings(self):
        return list(self.data.keys())


@dataclass
class Table:
    """模擬 behave 的 table"""
    rows: List[TableRow]
    
    def __iter__(self):
        return iter(self.rows)
    
    def __getitem__(self, index):
        return self.rows[index]


class Context:
    """模擬 behave 的 context"""
    def __init__(self):
        self.table = None
        self.order_service = None
        self.order_summary = None
        self.delivery_items = None


class SimpleBDDRunner:
    """簡化的 BDD 測試運行器"""
    
    def __init__(self):
        self.context = Context()
        self.passed_scenarios = 0
        self.failed_scenarios = 0
        self.total_steps = 0
        
    def parse_table(self, table_text: str) -> Table:
        """解析表格文本"""
        lines = [line.strip() for line in table_text.strip().split('\n') if line.strip()]
        if not lines:
            return Table([])
        
        # 解析表頭
        header_line = lines[0]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]  # 移除首尾空元素
        
        # 解析數據行
        rows = []
        for line in lines[1:]:
            values = [v.strip() for v in line.split('|')[1:-1]]  # 移除首尾空元素
            if len(values) == len(headers):
                row_data = dict(zip(headers, values))
                rows.append(TableRow(row_data))
        
        return Table(rows)
    
    def run_scenario_1(self):
        """
        Scenario: Single product without promotions
        """
        print("運行 Scenario 1: Single product without promotions")
        
        try:
            # Given no promotions are applied
            self.given_no_promotions()
            
            # When a customer places an order with
            order_table = """
            | productName | quantity | unitPrice |
            | T-shirt     | 1        | 500       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | totalAmount |
            | 500         |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | T-shirt     | 1        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 1 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 1 失敗: {e}")
            raise
    
    def run_scenario_2(self):
        """
        Scenario: Threshold discount applies when subtotal reaches 1000
        """
        print("運行 Scenario 2: Threshold discount applies when subtotal reaches 1000")
        
        try:
            # Given the threshold discount promotion is configured
            promotion_table = """
            | threshold | discount |
            | 1000      | 100      |
            """
            self.context.table = self.parse_table(promotion_table)
            self.given_threshold_discount_promotion()
            
            # When a customer places an order with
            order_table = """
            | productName | quantity | unitPrice |
            | T-shirt     | 2        | 500       |
            | 褲子        | 1        | 600       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | originalAmount | discount | totalAmount |
            | 1600           | 100      | 1500        |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | T-shirt     | 2        |
            | 褲子        | 1        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 2 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 2 失敗: {e}")
            raise
    
    def run_scenario_3(self):
        """
        Scenario: Buy-one-get-one for cosmetics - multiple products
        """
        print("運行 Scenario 3: Buy-one-get-one for cosmetics - multiple products")
        
        try:
            # Given the buy one get one promotion for cosmetics is active
            self.given_buy_one_get_one_cosmetics_promotion()
            
            # When a customer places an order with
            order_table = """
            | productName | category  | quantity | unitPrice |
            | 口紅        | cosmetics | 1        | 300       |
            | 粉底液      | cosmetics | 1        | 400       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | totalAmount |
            | 700         |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | 口紅        | 2        |
            | 粉底液      | 2        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 3 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 3 失敗: {e}")
            raise
    
    def run_scenario_4(self):
        """
        Scenario: Buy-one-get-one for cosmetics - same product twice
        """
        print("運行 Scenario 4: Buy-one-get-one for cosmetics - same product twice")
        
        try:
            # Given the buy one get one promotion for cosmetics is active
            self.given_buy_one_get_one_cosmetics_promotion()
            
            # When a customer places an order with
            order_table = """
            | productName | category  | quantity | unitPrice |
            | 口紅        | cosmetics | 2        | 300       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | totalAmount |
            | 600         |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | 口紅        | 3        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 4 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 4 失敗: {e}")
            raise
    
    def run_scenario_5(self):
        """
        Scenario: Buy-one-get-one for cosmetics - mixed categories
        """
        print("運行 Scenario 5: Buy-one-get-one for cosmetics - mixed categories")
        
        try:
            # Given the buy one get one promotion for cosmetics is active
            self.given_buy_one_get_one_cosmetics_promotion()
            
            # When a customer places an order with
            order_table = """
            | productName | category  | quantity | unitPrice |
            | 襪子        | apparel   | 1        | 100       |
            | 口紅        | cosmetics | 1        | 300       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | totalAmount |
            | 400         |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | 襪子        | 1        |
            | 口紅        | 2        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 5 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 5 失敗: {e}")
            raise
    
    def run_scenario_6(self):
        """
        Scenario: Multiple promotions stacked
        """
        print("運行 Scenario 6: Multiple promotions stacked")
        
        try:
            # Given the threshold discount promotion is configured
            promotion_table = """
            | threshold | discount |
            | 1000      | 100      |
            """
            self.context.table = self.parse_table(promotion_table)
            self.given_threshold_discount_promotion()
            
            # And the buy one get one promotion for cosmetics is active
            self.given_buy_one_get_one_cosmetics_promotion()
            
            # When a customer places an order with
            order_table = """
            | productName | category  | quantity | unitPrice |
            | T-shirt     | apparel   | 3        | 500       |
            | 口紅        | cosmetics | 1        | 300       |
            """
            self.context.table = self.parse_table(order_table)
            self.when_customer_places_order()
            
            # Then the order summary should be
            summary_table = """
            | originalAmount | discount | totalAmount |
            | 1800           | 100      | 1700        |
            """
            self.context.table = self.parse_table(summary_table)
            self.then_order_summary_should_be()
            
            # And the customer should receive
            delivery_table = """
            | productName | quantity |
            | T-shirt     | 3        |
            | 口紅        | 2        |
            """
            self.context.table = self.parse_table(delivery_table)
            self.then_customer_should_receive()
            
            self.passed_scenarios += 1
            print("✅ Scenario 6 通過!")
            
        except Exception as e:
            self.failed_scenarios += 1
            print(f"❌ Scenario 6 失敗: {e}")
            raise
    
    def given_no_promotions(self):
        """Given: no promotions are applied"""
        self.context.order_service = OrderService()
        self.total_steps += 1
    
    def given_threshold_discount_promotion(self):
        """Given: the threshold discount promotion is configured"""
        self.context.order_service = OrderService()
        
        for row in self.context.table:
            threshold = int(row['threshold'])
            discount = int(row['discount'])
            promotion = ThresholdDiscountPromotion(threshold, discount)
            self.context.order_service.add_promotion(promotion)
        
        self.total_steps += 1
    
    def given_buy_one_get_one_cosmetics_promotion(self):
        """Given: the buy one get one promotion for cosmetics is active"""
        if not hasattr(self.context, 'order_service') or self.context.order_service is None:
            self.context.order_service = OrderService()
        
        promotion = BuyOneGetOnePromotion(Category.COSMETICS)
        self.context.order_service.add_promotion(promotion)
        self.total_steps += 1
    
    def when_customer_places_order(self):
        """When: a customer places an order with"""
        order_items = []
        
        for row in self.context.table:
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
        self.context.order_summary, self.context.delivery_items = self.context.order_service.create_order(order_items)
        self.total_steps += 1
    
    def then_order_summary_should_be(self):
        """Then: the order summary should be"""
        expected_row = self.context.table[0]
        
        if 'totalAmount' in expected_row.headings:
            expected_total = int(expected_row['totalAmount'])
            actual_total = self.context.order_summary.total_amount
            assert actual_total == expected_total, \
                f"Expected total amount {expected_total}, but got {actual_total}"
        
        if 'originalAmount' in expected_row.headings:
            expected_original = int(expected_row['originalAmount'])
            actual_original = self.context.order_summary.original_amount
            assert actual_original == expected_original, \
                f"Expected original amount {expected_original}, but got {actual_original}"
        
        if 'discount' in expected_row.headings:
            expected_discount = int(expected_row['discount'])
            actual_discount = self.context.order_summary.discount
            assert actual_discount == expected_discount, \
                f"Expected discount {expected_discount}, but got {actual_discount}"
        
        self.total_steps += 1
    
    def then_customer_should_receive(self):
        """Then: the customer should receive"""
        expected_items = {}
        for row in self.context.table:
            product_name = row['productName']
            quantity = int(row['quantity'])
            expected_items[product_name] = quantity
        
        actual_items = {}
        for item in self.context.delivery_items:
            actual_items[item.product_name] = item.quantity
        
        assert expected_items == actual_items, \
            f"Expected delivery items {expected_items}, but got {actual_items}"
        
        self.total_steps += 1
    
    def run_all_scenarios(self, only_scenario=None):
        """運行所有 scenarios"""
        print("=== 簡化 BDD 測試運行器 ===")
        
        scenarios = {
            1: self.run_scenario_1,
            2: self.run_scenario_2,
            3: self.run_scenario_3,
            4: self.run_scenario_4,
            5: self.run_scenario_5,
            6: self.run_scenario_6
        }
        
        if only_scenario:
            print(f"僅運行 Scenario {only_scenario}...")
            try:
                scenarios[only_scenario]()
            except KeyError:
                print(f"❌ Scenario {only_scenario} 不存在")
                return False
        else:
            print("運行所有 scenarios...")
            for scenario_num, scenario_func in scenarios.items():
                try:
                    scenario_func()
                except Exception as e:
                    print(f"❌ Scenario {scenario_num} 失敗，停止運行")
                    break
        
        print(f"\n=== 測試結果 ===")
        print(f"Scenarios: {self.passed_scenarios} passed, {self.failed_scenarios} failed")
        print(f"Steps: {self.total_steps} steps")
        
        if self.failed_scenarios == 0:
            print("🎉 所有測試通過!")
            return True
        else:
            print("❌ 有測試失敗")
            return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='簡化 BDD 測試運行器')
    parser.add_argument('--scenario', type=int, help='僅運行指定的 scenario')
    args = parser.parse_args()
    
    runner = SimpleBDDRunner()
    success = runner.run_all_scenarios(only_scenario=args.scenario)
    sys.exit(0 if success else 1) 