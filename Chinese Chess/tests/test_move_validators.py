import pytest
from src.chess_engine import (
    GeneralMoveValidator, GuardMoveValidator, RookMoveValidator,
    HorseMoveValidator, CannonMoveValidator, ElephantMoveValidator,
    SoldierMoveValidator
)

class TestGeneralMoveValidatorDetailed:
    """將/帥移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = GeneralMoveValidator()
    
    def test_red_general_palace_boundaries(self):
        """測試紅方將軍九宮格邊界"""
        piece = {'color': 'Red', 'type': 'General'}
        board = {}
        
        # 測試九宮格內的有效移動
        valid_moves = [
            ((1, 4), (1, 5)),  # 水平移動
            ((1, 5), (2, 5)),  # 垂直移動
            ((2, 5), (3, 5)),  # 垂直移動到邊界
            ((3, 6), (3, 5)),  # 水平移動到邊界
        ]
        
        for from_pos, to_pos in valid_moves:
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == True, f"Move from {from_pos} to {to_pos} should be valid"
        
        # 測試超出九宮格的無效移動
        invalid_moves = [
            ((1, 4), (1, 3)),  # 左邊界外
            ((1, 6), (1, 7)),  # 右邊界外
            ((1, 5), (0, 5)),  # 上邊界外
            ((3, 5), (4, 5)),  # 下邊界外
        ]
        
        for from_pos, to_pos in invalid_moves:
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == False, f"Move from {from_pos} to {to_pos} should be invalid"
    
    def test_black_general_palace_boundaries(self):
        """測試黑方將軍九宮格邊界"""
        piece = {'color': 'Black', 'type': 'General'}
        board = {}
        
        # 測試九宮格內的有效移動
        valid_moves = [
            ((8, 4), (8, 5)),  # 水平移動
            ((8, 5), (9, 5)),  # 垂直移動
            ((9, 5), (10, 5)), # 垂直移動到邊界
            ((10, 6), (10, 5)), # 水平移動到邊界
        ]
        
        for from_pos, to_pos in valid_moves:
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == True, f"Move from {from_pos} to {to_pos} should be valid"
    
    def test_generals_face_to_face_detection(self):
        """測試將帥照面檢測"""
        piece = {'color': 'Red', 'type': 'General'}
        board = {
            (8, 5): {'color': 'Black', 'type': 'General'}
        }
        
        # 移動到與黑將同列會造成照面
        result = self.validator.is_valid_move(board, 2, 4, 2, 5, piece)
        assert result == False, "Should detect generals facing each other"
        
        # 測試九宮格內的有效移動（不同列，不會造成照面）
        result = self.validator.is_valid_move(board, 2, 5, 2, 4, piece)
        assert result == True, "Should allow valid move in different file within palace"

class TestRookMoveValidatorDetailed:
    """車移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = RookMoveValidator()
    
    def test_path_blocking_scenarios(self):
        """測試路徑阻擋情況"""
        piece = {'color': 'Red', 'type': 'Rook'}
        
        # 測試水平路徑阻擋
        board = {(4, 5): {'color': 'Black', 'type': 'Soldier'}}
        result = self.validator.is_valid_move(board, 4, 1, 4, 9, piece)
        assert result == False, "Horizontal path should be blocked"
        
        # 測試垂直路徑阻擋
        board = {(5, 5): {'color': 'Black', 'type': 'Soldier'}}
        result = self.validator.is_valid_move(board, 1, 5, 9, 5, piece)
        assert result == False, "Vertical path should be blocked"
        
        # 測試路徑暢通
        board = {}
        result = self.validator.is_valid_move(board, 1, 1, 1, 9, piece)
        assert result == True, "Clear path should be valid"
    
    def test_edge_cases(self):
        """測試邊界情況"""
        piece = {'color': 'Red', 'type': 'Rook'}
        board = {}
        
        # 測試單格移動
        result = self.validator.is_valid_move(board, 5, 5, 5, 6, piece)
        assert result == True, "Single step move should be valid"
        
        # 測試跨整個棋盤的移動
        result = self.validator.is_valid_move(board, 1, 1, 10, 1, piece)
        assert result == True, "Full board span should be valid"

class TestHorseMoveValidatorDetailed:
    """馬移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = HorseMoveValidator()
    
    def test_all_l_shape_moves(self):
        """測試所有L型移動"""
        piece = {'color': 'Red', 'type': 'Horse'}
        board = {}
        
        # 從(5,5)出發的所有有效L型移動
        valid_l_moves = [
            ((5, 5), (3, 4)),  # 上左
            ((5, 5), (3, 6)),  # 上右
            ((5, 5), (7, 4)),  # 下左
            ((5, 5), (7, 6)),  # 下右
            ((5, 5), (4, 3)),  # 左上
            ((5, 5), (6, 3)),  # 左下
            ((5, 5), (4, 7)),  # 右上
            ((5, 5), (6, 7)),  # 右下
        ]
        
        for from_pos, to_pos in valid_l_moves:
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == True, f"L-shape move from {from_pos} to {to_pos} should be valid"
    
    def test_leg_blocking_scenarios(self):
        """測試馬腳阻擋情況"""
        piece = {'color': 'Red', 'type': 'Horse'}
        
        # 測試各個方向的馬腳阻擋
        blocking_scenarios = [
            # (馬腳位置, 起點, 終點)
            ((4, 5), (5, 5), (3, 6)),  # 上方馬腳阻擋
            ((6, 5), (5, 5), (7, 6)),  # 下方馬腳阻擋
            ((5, 4), (5, 5), (6, 3)),  # 左方馬腳阻擋
            ((5, 6), (5, 5), (6, 7)),  # 右方馬腳阻擋
        ]
        
        for leg_pos, from_pos, to_pos in blocking_scenarios:
            board = {leg_pos: {'color': 'Black', 'type': 'Soldier'}}
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == False, f"Horse leg at {leg_pos} should block move from {from_pos} to {to_pos}"

class TestCannonMoveValidatorDetailed:
    """炮移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = CannonMoveValidator()
    
    def test_movement_mode_vs_attack_mode(self):
        """測試移動模式與攻擊模式"""
        piece = {'color': 'Red', 'type': 'Cannon'}
        
        # 移動模式：目標位置無棋子，路徑暢通
        board = {}
        result = self.validator.is_valid_move(board, 6, 2, 6, 8, piece)
        assert result == True, "Movement mode should work like Rook"
        
        # 移動模式：路徑被阻擋
        board = {(6, 5): {'color': 'Black', 'type': 'Soldier'}}
        result = self.validator.is_valid_move(board, 6, 2, 6, 8, piece)
        assert result == False, "Movement mode should be blocked by pieces"
        
        # 攻擊模式：一個炮台，有目標
        board = {
            (6, 5): {'color': 'Black', 'type': 'Soldier'},  # 炮台
            (6, 8): {'color': 'Black', 'type': 'Guard'}     # 目標
        }
        result = self.validator.is_valid_move(board, 6, 2, 6, 8, piece)
        assert result == True, "Attack mode with one screen should work"
    
    def test_screen_count_validation(self):
        """測試炮台數量驗證"""
        piece = {'color': 'Red', 'type': 'Cannon'}
        
        # 零個炮台攻擊（無效）
        board = {(6, 8): {'color': 'Black', 'type': 'Guard'}}
        result = self.validator.is_valid_move(board, 6, 2, 6, 8, piece)
        assert result == False, "Attack without screen should fail"
        
        # 兩個炮台攻擊（無效）
        board = {
            (6, 4): {'color': 'Red', 'type': 'Soldier'},   # 炮台1
            (6, 5): {'color': 'Black', 'type': 'Soldier'}, # 炮台2
            (6, 8): {'color': 'Black', 'type': 'Guard'}    # 目標
        }
        result = self.validator.is_valid_move(board, 6, 2, 6, 8, piece)
        assert result == False, "Attack with multiple screens should fail"

class TestElephantMoveValidatorDetailed:
    """象移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = ElephantMoveValidator()
    
    def test_field_pattern_moves(self):
        """測試田字型移動"""
        piece = {'color': 'Red', 'type': 'Elephant'}
        board = {}
        
        # 有效的田字型移動
        valid_moves = [
            ((3, 3), (5, 5)),  # 右下
            ((3, 5), (5, 3)),  # 左下
            ((5, 3), (3, 5)),  # 右上
            ((5, 5), (3, 3)),  # 左上
        ]
        
        for from_pos, to_pos in valid_moves:
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == True, f"Field move from {from_pos} to {to_pos} should be valid"
    
    def test_river_crossing_restriction(self):
        """測試過河限制"""
        board = {}
        
        # 紅方象不能過河（第6行以上）
        piece = {'color': 'Red', 'type': 'Elephant'}
        result = self.validator.is_valid_move(board, 5, 3, 7, 5, piece)
        assert result == False, "Red Elephant should not cross river"
        
        # 黑方象不能過河（第5行以下）
        piece = {'color': 'Black', 'type': 'Elephant'}
        result = self.validator.is_valid_move(board, 6, 3, 4, 5, piece)
        assert result == False, "Black Elephant should not cross river"
    
    def test_midpoint_blocking(self):
        """測試象眼阻擋"""
        piece = {'color': 'Red', 'type': 'Elephant'}
        
        # 測試各個方向的象眼阻擋
        blocking_scenarios = [
            ((4, 4), (3, 3), (5, 5)),  # 右下象眼
            ((4, 6), (3, 7), (5, 5)),  # 左下象眼
            ((6, 4), (5, 3), (7, 5)),  # 右上象眼
            ((6, 6), (5, 7), (7, 5)),  # 左上象眼
        ]
        
        for eye_pos, from_pos, to_pos in blocking_scenarios:
            board = {eye_pos: {'color': 'Black', 'type': 'Soldier'}}
            result = self.validator.is_valid_move(board, from_pos[0], from_pos[1], to_pos[0], to_pos[1], piece)
            assert result == False, f"Elephant eye at {eye_pos} should block move from {from_pos} to {to_pos}"

class TestSoldierMoveValidatorDetailed:
    """兵/卒移動驗證器詳細測試"""
    
    def setup_method(self):
        self.validator = SoldierMoveValidator()
    
    def test_river_crossing_detection(self):
        """測試過河判斷"""
        # 紅方兵過河判斷
        assert self.validator._has_crossed_river(3, 'Red') == False, "Red soldier at row 3 should not have crossed"
        assert self.validator._has_crossed_river(6, 'Red') == True, "Red soldier at row 6 should have crossed"
        assert self.validator._has_crossed_river(8, 'Red') == True, "Red soldier at row 8 should have crossed"
        
        # 黑方卒過河判斷
        assert self.validator._has_crossed_river(8, 'Black') == False, "Black soldier at row 8 should not have crossed"
        assert self.validator._has_crossed_river(5, 'Black') == True, "Black soldier at row 5 should have crossed"
        assert self.validator._has_crossed_river(3, 'Black') == True, "Black soldier at row 3 should have crossed"
    
    def test_pre_river_movement_restrictions(self):
        """測試過河前移動限制"""
        board = {}
        
        # 紅方兵過河前只能向前
        piece = {'color': 'Red', 'type': 'Soldier'}
        assert self.validator.is_valid_move(board, 4, 5, 3, 5, piece) == True, "Red soldier should move forward"
        assert self.validator.is_valid_move(board, 4, 5, 4, 4, piece) == False, "Red soldier should not move sideways before river"
        assert self.validator.is_valid_move(board, 4, 5, 5, 5, piece) == False, "Red soldier should not move backward"
        
        # 黑方卒過河前只能向前
        piece = {'color': 'Black', 'type': 'Soldier'}
        assert self.validator.is_valid_move(board, 7, 5, 8, 5, piece) == True, "Black soldier should move forward"
        assert self.validator.is_valid_move(board, 7, 5, 7, 4, piece) == False, "Black soldier should not move sideways before river"
        assert self.validator.is_valid_move(board, 7, 5, 6, 5, piece) == False, "Black soldier should not move backward"
    
    def test_post_river_movement_flexibility(self):
        """測試過河後移動靈活性"""
        board = {}
        
        # 紅方兵過河後可以橫移和向前
        piece = {'color': 'Red', 'type': 'Soldier'}
        assert self.validator.is_valid_move(board, 7, 5, 6, 5, piece) == True, "Red soldier should move forward after river"
        assert self.validator.is_valid_move(board, 7, 5, 7, 4, piece) == True, "Red soldier should move sideways after river"
        assert self.validator.is_valid_move(board, 7, 5, 7, 6, piece) == True, "Red soldier should move sideways after river"
        assert self.validator.is_valid_move(board, 7, 5, 8, 5, piece) == False, "Red soldier should not move backward"
        
        # 黑方卒過河後可以橫移和向前
        piece = {'color': 'Black', 'type': 'Soldier'}
        assert self.validator.is_valid_move(board, 4, 5, 5, 5, piece) == True, "Black soldier should move forward after river"
        assert self.validator.is_valid_move(board, 4, 5, 4, 4, piece) == True, "Black soldier should move sideways after river"
        assert self.validator.is_valid_move(board, 4, 5, 4, 6, piece) == True, "Black soldier should move sideways after river"
        assert self.validator.is_valid_move(board, 4, 5, 3, 5, piece) == False, "Black soldier should not move backward"

if __name__ == "__main__":
    pytest.main([__file__]) 