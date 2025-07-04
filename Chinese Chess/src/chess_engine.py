from abc import ABC, abstractmethod

class TurnManager:
    """輪次管理器 - 遵循 OCP 原則的擴展組件"""
    
    def __init__(self):
        self.current_turn = 'Red'  # 紅方先手
        self.last_moved = None
    
    def is_valid_turn(self, color):
        """檢查是否輪到指定顏色行棋"""
        return self.current_turn == color
    
    def switch_turn(self):
        """切換輪次"""
        self.current_turn = 'Black' if self.current_turn == 'Red' else 'Red'
        self.last_moved = 'Black' if self.last_moved == 'Red' else 'Red'
    
    def record_move(self, color):
        """記錄移動並切換輪次"""
        self.last_moved = color
        self.switch_turn()

class CheckmateDetector:
    """將死檢查器 - 遵循 OCP 原則的擴展組件"""
    
    def __init__(self, engine):
        self.engine = engine
    
    def is_in_check(self, color):
        """檢查指定顏色是否被將軍"""
        # 找到該顏色的將軍位置
        general_pos = None
        for pos, piece in self.engine.board.items():
            if piece['type'] == 'General' and piece['color'] == color:
                general_pos = pos
                break
        
        if general_pos is None:
            return False
        
        # 檢查是否有對方棋子可以攻擊到將軍
        opponent_color = 'Black' if color == 'Red' else 'Red'
        for pos, piece in self.engine.board.items():
            if piece['color'] == opponent_color:
                # 檢查這個對方棋子是否可以移動到將軍位置
                validator = self.engine.validators.get(piece['type'])
                if validator and validator.is_valid_move(
                    self.engine.board, pos[0], pos[1], 
                    general_pos[0], general_pos[1], piece
                ):
                    return True
        
        return False
    
    def has_legal_moves(self, color):
        """檢查指定顏色是否還有合法移動"""
        for pos, piece in self.engine.board.items():
            if piece['color'] == color:
                # 嘗試該棋子的所有可能移動
                for target_row in range(1, 11):
                    for target_col in range(1, 10):
                        if (target_row, target_col) != pos:
                            # 模擬移動並檢查是否合法且不會讓自己被將軍
                            if self._is_move_safe(pos, (target_row, target_col), piece):
                                return True
        return False
    
    def _is_move_safe(self, from_pos, to_pos, piece):
        """檢查移動是否安全（移動後不會被將軍）"""
        # 備份原始狀態
        original_board = self.engine.board.copy()
        original_game_result = self.engine.game_result
        
        try:
            # 嘗試移動
            move_successful = self.engine.move_piece(
                from_pos[0], from_pos[1], to_pos[0], to_pos[1]
            )
            
            if not move_successful:
                return False
            
            # 檢查移動後是否被將軍
            is_safe = not self.is_in_check(piece['color'])
            
            return is_safe
        finally:
            # 恢復原始狀態
            self.engine.board = original_board
            self.engine.game_result = original_game_result
    
    def detect_checkmate(self, color):
        """檢查是否為將死"""
        return self.is_in_check(color) and not self.has_legal_moves(color)

class MoveValidator(ABC):
    """移動驗證器的抽象基類"""
    
    @abstractmethod
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        """驗證移動是否合法"""
        pass

class CannonMoveValidator(MoveValidator):
    """炮的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否為直線移動（橫向或縱向）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 必須是純橫向或純縱向移動
        if not ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)):
            return False
        
        # 檢查目標位置是否有棋子
        target_has_piece = (to_row, to_col) in board
        
        if target_has_piece:
            # 攻擊模式：必須跳過恰好一個炮台
            return self._is_valid_attack(board, from_row, from_col, to_row, to_col)
        else:
            # 移動模式：路徑必須暢通（像車一樣）
            return self._is_path_clear(board, from_row, from_col, to_row, to_col)
    
    def _is_path_clear(self, board, from_row, from_col, to_row, to_col):
        """檢查路徑上是否有棋子阻擋（移動模式）"""
        # 計算移動方向
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        # 檢查路徑上的每一格（不包括起點和終點）
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while (current_row, current_col) != (to_row, to_col):
            if (current_row, current_col) in board:
                return False  # 路徑被阻擋
            current_row += row_step
            current_col += col_step
        
        return True  # 路徑暢通
    
    def _is_valid_attack(self, board, from_row, from_col, to_row, to_col):
        """檢查是否為有效的攻擊（必須跳過恰好一個炮台）"""
        # 計算移動方向
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        # 計算路徑上的棋子數量
        screen_count = 0
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while (current_row, current_col) != (to_row, to_col):
            if (current_row, current_col) in board:
                screen_count += 1
            current_row += row_step
            current_col += col_step
        
        # 攻擊時必須跳過恰好一個炮台
        return screen_count == 1

class ElephantMoveValidator(MoveValidator):
    """象的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否為「田」字形移動（恰好對角線2格）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 必須是恰好2x2的對角線移動
        if row_diff != 2 or col_diff != 2:
            return False
        
        # 檢查不能過河（紅方象不能超過第5行）
        color = piece['color']
        if color == 'Red' and to_row > 5:
            return False  # 紅方象不能過河
        if color == 'Black' and to_row < 6:
            return False  # 黑方象不能過河
        
        # 檢查中心點是否被阻擋（田字的中心）
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        
        if (mid_row, mid_col) in board:
            return False  # 中心點被阻擋
        
        return True

class SoldierMoveValidator(MoveValidator):
    """兵/卒的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        color = piece['color']
        
        # 計算移動距離
        row_diff = to_row - from_row
        col_diff = abs(to_col - from_col)
        
        # 只能移動一格：縱向一格或橫向一格，但不能斜行
        if not ((abs(row_diff) == 1 and col_diff == 0) or (abs(row_diff) == 0 and col_diff == 1)):
            return False
        
        # 檢查是否已過河
        has_crossed_river = self._has_crossed_river(from_row, color)
        
        if not has_crossed_river:
            # 過河前：只能向前移動，不能橫移
            if col_diff != 0:
                return False  # 不能橫移
            
            # 檢查是否向前移動
            if color == 'Red':
                return row_diff == -1  # 紅方向上（減少行數）
            else:
                return row_diff == 1   # 黑方向下（增加行數）
        else:
            # 過河後：可以向前或橫移，但不能後退
            if col_diff > 1:
                return False  # 橫移只能一格
            
            if col_diff == 0:
                # 縱向移動：必須向前
                if color == 'Red':
                    return row_diff == -1  # 紅方向上
                else:
                    return row_diff == 1   # 黑方向下
            else:
                # 橫向移動：不能有縱向移動
                return row_diff == 0
    
    def _has_crossed_river(self, row, color):
        """檢查兵是否已過河"""
        if color == 'Red':
            return row >= 6  # 紅方：6行以上算過河
        else:
            return row <= 5  # 黑方：5行以下算過河

class HorseMoveValidator(MoveValidator):
    """馬的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否為「日」字型移動
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 必須是 2+1 或 1+2 的 L 形移動
        if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
            return False
        
        # 檢查是否被腳點阻擋（蹩馬腳）
        return self._is_not_blocked(board, from_row, from_col, to_row, to_col)
    
    def _is_not_blocked(self, board, from_row, from_col, to_row, to_col):
        """檢查馬腳是否被阻擋"""
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        # 確定腳點位置
        if abs(row_diff) == 2:
            # 水平移動2格，腳點在水平方向
            leg_row = from_row + (1 if row_diff > 0 else -1)
            leg_col = from_col
        else:
            # 垂直移動2格，腳點在垂直方向
            leg_row = from_row
            leg_col = from_col + (1 if col_diff > 0 else -1)
        
        # 檢查腳點是否有棋子
        return (leg_row, leg_col) not in board

class RookMoveValidator(MoveValidator):
    """車的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否為直線移動（橫向或縱向）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 必須是純橫向或純縱向移動
        if not ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)):
            return False
        
        # 檢查路徑上是否有棋子阻擋
        return self._is_path_clear(board, from_row, from_col, to_row, to_col)
    
    def _is_path_clear(self, board, from_row, from_col, to_row, to_col):
        """檢查路徑上是否有棋子阻擋"""
        # 計算移動方向
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        # 檢查路徑上的每一格（不包括起點和終點）
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while (current_row, current_col) != (to_row, to_col):
            if (current_row, current_col) in board:
                return False  # 路徑被阻擋
            current_row += row_step
            current_col += col_step
        
        return True  # 路徑暢通

class GuardMoveValidator(MoveValidator):
    """士/仕的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否在九宮格內
        if piece['color'] == 'Red':
            # 紅方九宮格：行 1-3，列 4-6
            if not (1 <= to_row <= 3 and 4 <= to_col <= 6):
                return False
        else:
            # 黑方九宮格：行 8-10，列 4-6
            if not (8 <= to_row <= 10 and 4 <= to_col <= 6):
                return False
        
        # 檢查移動距離（只能移動一格對角線）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 只能斜行移動一格
        if row_diff == 1 and col_diff == 1:
            return True
        
        return False

class GeneralMoveValidator(MoveValidator):
    """將/帥的移動驗證器"""
    
    def is_valid_move(self, board, from_row, from_col, to_row, to_col, piece):
        # 檢查是否在九宮格內
        if piece['color'] == 'Red':
            # 紅方九宮格：行 1-3，列 4-6
            if not (1 <= to_row <= 3 and 4 <= to_col <= 6):
                return False
        else:
            # 黑方九宮格：行 8-10，列 4-6
            if not (8 <= to_row <= 10 and 4 <= to_col <= 6):
                return False
        
        # 檢查移動距離（只能移動一格）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # 只能直行或直列移動一格
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
        
        # 檢查將帥照面規則：模擬移動後檢查是否會造成將帥照面
        if self._would_cause_generals_face_to_face(board, from_row, from_col, to_row, to_col, piece):
            return False
        
        return True
    
    def _would_cause_generals_face_to_face(self, board, from_row, from_col, to_row, to_col, piece):
        """檢查移動後是否會造成將帥照面"""
        # 建立移動後的臨時棋盤狀態
        temp_board = board.copy()
        
        # 移除原位置的棋子
        if (from_row, from_col) in temp_board:
            del temp_board[(from_row, from_col)]
        
        # 在新位置放置棋子
        temp_board[(to_row, to_col)] = piece
        
        # 找到兩個將帥的位置
        red_general_pos = None
        black_general_pos = None
        
        for pos, p in temp_board.items():
            if p['type'] == 'General':
                if p['color'] == 'Red':
                    red_general_pos = pos
                elif p['color'] == 'Black':
                    black_general_pos = pos
        
        # 如果沒有找到兩個將帥，就不會照面
        if red_general_pos is None or black_general_pos is None:
            return False
        
        red_row, red_col = red_general_pos
        black_row, black_col = black_general_pos
        
        # 檢查是否在同一列
        if red_col != black_col:
            return False
        
        # 檢查同一列中間是否有其他棋子
        start_row = min(red_row, black_row) + 1
        end_row = max(red_row, black_row)
        
        for check_row in range(start_row, end_row):
            if (check_row, red_col) in temp_board:
                return False  # 中間有棋子，不會照面
        
        return True  # 會照面

class ChessEngine:
    def __init__(self):
        self.board = {}
        self.game_result = "Continue"
        self.validators = {
            'General': GeneralMoveValidator(),
            'Guard': GuardMoveValidator(),
            'Rook': RookMoveValidator(),
            'Horse': HorseMoveValidator(),
            'Cannon': CannonMoveValidator(),
            'Elephant': ElephantMoveValidator(),
            'Soldier': SoldierMoveValidator()
        }
        # OCP 擴展：組合將死檢查器和輪次管理器
        self.checkmate_detector = CheckmateDetector(self)
        self.turn_manager = TurnManager()
        
    def setup_empty_board(self):
        """設置空棋盤"""
        self.board = {}
        
    def place_piece(self, color, piece_type, row, col):
        """在指定位置放置棋子"""
        self.board[(row, col)] = {'color': color, 'type': piece_type}
        
    def move_piece(self, from_row, from_col, to_row, to_col):
        """移動棋子，使用策略模式驗證移動合法性"""
        # 檢查起始位置是否有棋子
        if (from_row, from_col) not in self.board:
            return False
        
        piece = self.board[(from_row, from_col)]
        piece_type = piece['type']
        piece_color = piece['color']
        
        # OCP 擴展：檢查輪次
        if not self.turn_manager.is_valid_turn(piece_color):
            return False  # 不是該顏色的回合
        
        # 檢查目標位置是否有自己的棋子（不能吃自己的棋子）
        captured_piece = None
        if (to_row, to_col) in self.board:
            target_piece = self.board[(to_row, to_col)]
            if target_piece['color'] == piece['color']:
                return False  # 不能吃自己的棋子
            captured_piece = target_piece
        
        # 獲取對應的驗證器
        if piece_type in self.validators:
            validator = self.validators[piece_type]
            is_valid = validator.is_valid_move(self.board, from_row, from_col, to_row, to_col, piece)
            
            if is_valid:
                # 執行移動
                self._execute_move(from_row, from_col, to_row, to_col, captured_piece)
                # OCP 擴展：記錄移動並切換輪次
                self.turn_manager.record_move(piece_color)
                return True
            else:
                return False
        
        # 如果沒有對應的驗證器，返回 False 確保我們必須實現每個棋子的規則
        return False
    
    def _execute_move(self, from_row, from_col, to_row, to_col, captured_piece):
        """執行移動並檢查勝利條件"""
        # 移動棋子
        piece = self.board[(from_row, from_col)]
        del self.board[(from_row, from_col)]
        self.board[(to_row, to_col)] = piece
        
        # 檢查勝利條件
        if captured_piece and captured_piece['type'] == 'General':
            self.game_result = f"{piece['color']} wins"
        else:
            self.game_result = "Continue" 