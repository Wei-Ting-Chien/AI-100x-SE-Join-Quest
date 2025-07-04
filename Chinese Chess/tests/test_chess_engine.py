import pytest
from src.chess_engine import ChessEngine, MoveValidator, GeneralMoveValidator, GuardMoveValidator, RookMoveValidator, HorseMoveValidator, CannonMoveValidator, ElephantMoveValidator, SoldierMoveValidator

class TestChessEngine:
    """ChessEngine 基本功能測試"""
    
    def setup_method(self):
        """每個測試方法前的設置"""
        self.engine = ChessEngine()
        self.engine.setup_empty_board()
    
    def test_setup_empty_board(self):
        """測試建立空棋盤"""
        assert len(self.engine.board) == 0
        assert self.engine.game_result == "Continue"
    
    def test_place_piece(self):
        """測試放置棋子"""
        self.engine.place_piece('Red', 'General', 1, 5)
        assert (1, 5) in self.engine.board
        assert self.engine.board[(1, 5)]['color'] == 'Red'
        assert self.engine.board[(1, 5)]['type'] == 'General'
    
    def test_move_nonexistent_piece(self):
        """測試移動不存在的棋子"""
        result = self.engine.move_piece(1, 1, 2, 2)
        assert result == False
    
    def test_cannot_capture_own_piece(self):
        """測試不能吃自己的棋子"""
        self.engine.place_piece('Red', 'Rook', 1, 1)
        self.engine.place_piece('Red', 'Soldier', 1, 5)
        result = self.engine.move_piece(1, 1, 1, 5)
        assert result == False

class TestGeneralMoveValidator:
    """將/帥移動驗證器測試"""
    
    def setup_method(self):
        self.validator = GeneralMoveValidator()
        self.board = {}
    
    def test_valid_orthogonal_move_in_palace(self):
        """測試九宮格內有效的正交移動"""
        piece = {'color': 'Red', 'type': 'General'}
        result = self.validator.is_valid_move(self.board, 1, 5, 1, 4, piece)
        assert result == True
    
    def test_invalid_move_outside_palace(self):
        """測試移出九宮格的無效移動"""
        piece = {'color': 'Red', 'type': 'General'}
        result = self.validator.is_valid_move(self.board, 1, 6, 1, 7, piece)
        assert result == False
    
    def test_invalid_diagonal_move(self):
        """測試對角線移動（無效）"""
        piece = {'color': 'Red', 'type': 'General'}
        result = self.validator.is_valid_move(self.board, 1, 5, 2, 6, piece)
        assert result == False
    
    def test_black_general_palace_boundaries(self):
        """測試黑方將軍的九宮格邊界"""
        piece = {'color': 'Black', 'type': 'General'}
        # 有效移動
        result = self.validator.is_valid_move(self.board, 9, 5, 9, 4, piece)
        assert result == True
        # 無效移動（超出九宮格）
        result = self.validator.is_valid_move(self.board, 9, 4, 9, 3, piece)
        assert result == False

class TestGuardMoveValidator:
    """士/仕移動驗證器測試"""
    
    def setup_method(self):
        self.validator = GuardMoveValidator()
        self.board = {}
    
    def test_valid_diagonal_move_in_palace(self):
        """測試九宮格內有效的對角線移動"""
        piece = {'color': 'Red', 'type': 'Guard'}
        result = self.validator.is_valid_move(self.board, 1, 4, 2, 5, piece)
        assert result == True
    
    def test_invalid_orthogonal_move(self):
        """測試無效的正交移動"""
        piece = {'color': 'Red', 'type': 'Guard'}
        result = self.validator.is_valid_move(self.board, 2, 5, 2, 6, piece)
        assert result == False
    
    def test_invalid_move_outside_palace(self):
        """測試移出九宮格的無效移動"""
        piece = {'color': 'Red', 'type': 'Guard'}
        result = self.validator.is_valid_move(self.board, 3, 6, 4, 7, piece)
        assert result == False

class TestRookMoveValidator:
    """車移動驗證器測試"""
    
    def setup_method(self):
        self.validator = RookMoveValidator()
        self.board = {}
    
    def test_valid_horizontal_move(self):
        """測試有效的水平移動"""
        piece = {'color': 'Red', 'type': 'Rook'}
        result = self.validator.is_valid_move(self.board, 4, 1, 4, 9, piece)
        assert result == True
    
    def test_valid_vertical_move(self):
        """測試有效的垂直移動"""
        piece = {'color': 'Red', 'type': 'Rook'}
        result = self.validator.is_valid_move(self.board, 1, 1, 10, 1, piece)
        assert result == True
    
    def test_invalid_diagonal_move(self):
        """測試無效的對角線移動"""
        piece = {'color': 'Red', 'type': 'Rook'}
        result = self.validator.is_valid_move(self.board, 1, 1, 2, 2, piece)
        assert result == False
    
    def test_blocked_path(self):
        """測試被阻擋的路徑"""
        self.board[(4, 5)] = {'color': 'Black', 'type': 'Soldier'}
        piece = {'color': 'Red', 'type': 'Rook'}
        result = self.validator.is_valid_move(self.board, 4, 1, 4, 9, piece)
        assert result == False

class TestHorseMoveValidator:
    """馬移動驗證器測試"""
    
    def setup_method(self):
        self.validator = HorseMoveValidator()
        self.board = {}
    
    def test_valid_l_shape_move(self):
        """測試有效的L型移動"""
        piece = {'color': 'Red', 'type': 'Horse'}
        result = self.validator.is_valid_move(self.board, 3, 3, 5, 4, piece)
        assert result == True
    
    def test_invalid_non_l_shape_move(self):
        """測試無效的非L型移動"""
        piece = {'color': 'Red', 'type': 'Horse'}
        result = self.validator.is_valid_move(self.board, 3, 3, 5, 5, piece)
        assert result == False
    
    def test_blocked_by_leg(self):
        """測試被馬腳阻擋"""
        self.board[(4, 3)] = {'color': 'Black', 'type': 'Rook'}
        piece = {'color': 'Red', 'type': 'Horse'}
        result = self.validator.is_valid_move(self.board, 3, 3, 5, 4, piece)
        assert result == False

class TestCannonMoveValidator:
    """炮移動驗證器測試"""
    
    def setup_method(self):
        self.validator = CannonMoveValidator()
        self.board = {}
    
    def test_valid_rook_like_movement(self):
        """測試有效的車式移動（無目標棋子）"""
        piece = {'color': 'Red', 'type': 'Cannon'}
        result = self.validator.is_valid_move(self.board, 6, 2, 6, 8, piece)
        assert result == True
    
    def test_valid_jump_attack(self):
        """測試有效的跳躍攻擊（一個炮台）"""
        self.board[(6, 5)] = {'color': 'Black', 'type': 'Soldier'}  # 炮台
        self.board[(6, 8)] = {'color': 'Black', 'type': 'Guard'}    # 目標
        piece = {'color': 'Red', 'type': 'Cannon'}
        result = self.validator.is_valid_move(self.board, 6, 2, 6, 8, piece)
        assert result == True
    
    def test_invalid_attack_without_screen(self):
        """測試無效的無炮台攻擊"""
        self.board[(6, 8)] = {'color': 'Black', 'type': 'Guard'}    # 目標
        piece = {'color': 'Red', 'type': 'Cannon'}
        result = self.validator.is_valid_move(self.board, 6, 2, 6, 8, piece)
        assert result == False
    
    def test_invalid_attack_multiple_screens(self):
        """測試無效的多炮台攻擊"""
        self.board[(6, 4)] = {'color': 'Red', 'type': 'Soldier'}   # 炮台1
        self.board[(6, 5)] = {'color': 'Black', 'type': 'Soldier'} # 炮台2
        self.board[(6, 8)] = {'color': 'Black', 'type': 'Guard'}   # 目標
        piece = {'color': 'Red', 'type': 'Cannon'}
        result = self.validator.is_valid_move(self.board, 6, 2, 6, 8, piece)
        assert result == False

class TestElephantMoveValidator:
    """象移動驗證器測試"""
    
    def setup_method(self):
        self.validator = ElephantMoveValidator()
        self.board = {}
    
    def test_valid_diagonal_move(self):
        """測試有效的田字對角線移動"""
        piece = {'color': 'Red', 'type': 'Elephant'}
        result = self.validator.is_valid_move(self.board, 3, 3, 5, 5, piece)
        assert result == True
    
    def test_invalid_cross_river_red(self):
        """測試紅方象不能過河"""
        piece = {'color': 'Red', 'type': 'Elephant'}
        result = self.validator.is_valid_move(self.board, 5, 3, 7, 5, piece)
        assert result == False
    
    def test_invalid_cross_river_black(self):
        """測試黑方象不能過河"""
        piece = {'color': 'Black', 'type': 'Elephant'}
        result = self.validator.is_valid_move(self.board, 6, 3, 4, 5, piece)
        assert result == False
    
    def test_blocked_midpoint(self):
        """測試中心點被阻擋"""
        self.board[(4, 4)] = {'color': 'Black', 'type': 'Rook'}
        piece = {'color': 'Red', 'type': 'Elephant'}
        result = self.validator.is_valid_move(self.board, 3, 3, 5, 5, piece)
        assert result == False

class TestSoldierMoveValidator:
    """兵/卒移動驗證器測試"""
    
    def setup_method(self):
        self.validator = SoldierMoveValidator()
        self.board = {}
    
    def test_red_soldier_forward_before_river(self):
        """測試紅方兵過河前向前移動"""
        piece = {'color': 'Red', 'type': 'Soldier'}
        result = self.validator.is_valid_move(self.board, 3, 5, 2, 5, piece)
        assert result == True
    
    def test_red_soldier_sideways_before_river(self):
        """測試紅方兵過河前橫移（無效）"""
        piece = {'color': 'Red', 'type': 'Soldier'}
        result = self.validator.is_valid_move(self.board, 3, 5, 3, 4, piece)
        assert result == False
    
    def test_red_soldier_sideways_after_river(self):
        """測試紅方兵過河後橫移"""
        piece = {'color': 'Red', 'type': 'Soldier'}
        result = self.validator.is_valid_move(self.board, 6, 5, 6, 4, piece)
        assert result == True
    
    def test_red_soldier_backward_after_river(self):
        """測試紅方兵過河後後退（無效）"""
        piece = {'color': 'Red', 'type': 'Soldier'}
        result = self.validator.is_valid_move(self.board, 6, 5, 7, 5, piece)
        assert result == False
    
    def test_black_soldier_forward_before_river(self):
        """測試黑方卒過河前向前移動"""
        piece = {'color': 'Black', 'type': 'Soldier'}
        result = self.validator.is_valid_move(self.board, 8, 5, 9, 5, piece)
        assert result == True

class TestGameLogic:
    """遊戲邏輯測試"""
    
    def setup_method(self):
        self.engine = ChessEngine()
        self.engine.setup_empty_board()
    
    def test_capture_general_wins_game(self):
        """測試吃掉將軍贏得遊戲"""
        self.engine.place_piece('Red', 'Rook', 5, 5)
        self.engine.place_piece('Black', 'General', 5, 8)
        
        result = self.engine.move_piece(5, 5, 5, 8)
        assert result == True
        assert self.engine.game_result == "Red wins"
    
    def test_capture_non_general_continues_game(self):
        """測試吃掉非將軍棋子遊戲繼續"""
        self.engine.place_piece('Red', 'Rook', 5, 5)
        self.engine.place_piece('Black', 'Cannon', 5, 8)
        self.engine.place_piece('Black', 'General', 8, 5)
        
        result = self.engine.move_piece(5, 5, 5, 8)
        assert result == True
        assert self.engine.game_result == "Continue"
    
    def test_generals_face_to_face_is_illegal(self):
        """測試將帥照面是非法移動"""
        self.engine.place_piece('Red', 'General', 2, 4)
        self.engine.place_piece('Black', 'General', 8, 5)
        
        result = self.engine.move_piece(2, 4, 2, 5)
        assert result == False

class TestValidatorIntegration:
    """驗證器整合測試"""
    
    def setup_method(self):
        self.engine = ChessEngine()
        self.engine.setup_empty_board()
    
    def test_all_validators_registered(self):
        """測試所有驗證器都已註冊"""
        expected_validators = ['General', 'Guard', 'Rook', 'Horse', 'Cannon', 'Elephant', 'Soldier']
        for validator_type in expected_validators:
            assert validator_type in self.engine.validators
            assert isinstance(self.engine.validators[validator_type], MoveValidator)
    
    def test_unknown_piece_type_returns_false(self):
        """測試未知棋子類型返回 False"""
        self.engine.board[(1, 1)] = {'color': 'Red', 'type': 'UnknownPiece'}
        result = self.engine.move_piece(1, 1, 1, 2)
        assert result == False

if __name__ == "__main__":
    pytest.main([__file__]) 