from behave import given, when, then
from src.chess_engine import ChessEngine

@given('the board is empty except for a Red General at {position}')
def step_given_board_with_red_general(context, position):
    # 解析位置字符串 "(1, 5)"
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'General', row, col)

@given('the board is empty except for a Red Guard at {position}')
def step_given_board_with_red_guard(context, position):
    # 解析位置字符串 "(1, 4)"
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Guard', row, col)

@given('the board is empty except for a Red Rook at {position}')
def step_given_board_with_red_rook(context, position):
    # 解析位置字符串 "(4, 1)"
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Rook', row, col)

@given('the board is empty except for a Red Horse at {position}')
def step_given_board_with_red_horse(context, position):
    # 解析位置字符串 "(3, 3)"
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Horse', row, col)

@given('the board is empty except for a Red Cannon at {position}')
def step_given_board_with_red_cannon(context, position):
    # 解析位置字符串 "(6, 2)"
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Cannon', row, col)

@given('the board is empty except for a Red Elephant at {position}')
def step_given_board_with_red_elephant(context, position):
    # 解析位置字符串，支持多種位置
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Elephant', row, col)

@given('the board is empty except for a Red Soldier at {position}')
def step_given_board_with_red_soldier(context, position):
    # 解析位置字符串，支持多種位置
    row, col = eval(position)
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    context.chess_engine.place_piece('Red', 'Soldier', row, col)

@given('the board has')
def step_given_board_has_pieces(context):
    # 建立空棋盤
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    
    # 處理表格中的每一行
    for row in context.table:
        piece_info = row['Piece'].strip()
        position = row['Position'].strip()
        
        # 解析棋子資訊 "Red General" -> color="Red", type="General"
        parts = piece_info.split()
        color = parts[0]  # "Red" or "Black"
        piece_type = parts[1]  # "General", "Rook", etc.
        
        # 解析位置 "(2, 4)" -> row=2, col=4
        pos_row, pos_col = eval(position)
        
        # 放置棋子
        context.chess_engine.place_piece(color, piece_type, pos_row, pos_col)

@when('Red moves the General from {from_pos} to {to_pos}')
def step_when_red_moves_general(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Guard from {from_pos} to {to_pos}')
def step_when_red_moves_guard(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Rook from {from_pos} to {to_pos}')
def step_when_red_moves_rook(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Horse from {from_pos} to {to_pos}')
def step_when_red_moves_horse(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Cannon from {from_pos} to {to_pos}')
def step_when_red_moves_cannon(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Elephant from {from_pos} to {to_pos}')
def step_when_red_moves_elephant(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@when('Red moves the Soldier from {from_pos} to {to_pos}')
def step_when_red_moves_soldier(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

@then('the move is legal')
def step_then_move_is_legal(context):
    assert context.move_result == True, "Expected move to be legal"

@then('the move is illegal')
def step_then_move_is_illegal(context):
    assert context.move_result == False, "Expected move to be illegal"

@then('Red wins immediately')
def step_then_red_wins_immediately(context):
    # 檢查移動結果是否包含勝利信息
    assert hasattr(context.chess_engine, 'game_result'), "Expected game result to be set"
    assert context.chess_engine.game_result == 'Red wins', "Expected Red to win immediately"

@then('the game is not over just from that capture')
def step_then_game_continues(context):
    # 檢查遊戲是否繼續進行
    assert hasattr(context.chess_engine, 'game_result'), "Expected game result to be set"
    assert context.chess_engine.game_result == 'Continue', "Expected game to continue"

# =================================================================
# 新增：黑方移動步驟定義
# =================================================================
@when('Black moves the General from {from_pos} to {to_pos}')
def step_when_black_moves_general(context, from_pos, to_pos):
    from_row, from_col = eval(from_pos)
    to_row, to_col = eval(to_pos)
    context.move_result = context.chess_engine.move_piece(from_row, from_col, to_row, to_col)

# =================================================================
# 新增：將死判斷步驟定義
# =================================================================
@when('Black has no legal move to resolve the check')
def step_when_black_has_no_legal_move(context):
    """檢查黑方是否無法擺脫將軍"""
    # 使用 CheckmateDetector 檢查將死
    is_checkmate = context.chess_engine.checkmate_detector.detect_checkmate('Black')
    if is_checkmate:
        context.chess_engine.game_result = 'Red wins'
    context.checkmate_verified = is_checkmate

@then('Red wins by checkmate')
def step_then_red_wins_by_checkmate(context):
    """驗證紅方通過將死獲勝"""
    assert hasattr(context.chess_engine, 'game_result'), "Expected game result to be set"
    assert context.chess_engine.game_result == 'Red wins', "Expected Red to win by checkmate"
    assert context.checkmate_verified, "Expected checkmate to be verified"

# =================================================================
# 新增：輪次控制步驟定義
# =================================================================
@given("it is Red's turn")
def step_given_red_turn(context):
    """設定當前輪到紅方"""
    context.chess_engine = ChessEngine()
    context.chess_engine.setup_empty_board()
    # 設定當前輪次為紅方（預設就是紅方先手）
    context.chess_engine.turn_manager.current_turn = 'Red'

@given('Red just moved a Rook')
def step_given_red_just_moved_rook(context):
    """紅方剛剛移動了車"""
    # 設置一個簡單的棋盤狀態，表示紅方剛剛移動過
    context.chess_engine.place_piece('Red', 'Rook', 3, 3)
    context.chess_engine.place_piece('Red', 'Cannon', 4, 4)
    # 標記紅方剛移動過，現在應該輪到黑方
    context.chess_engine.turn_manager.last_moved = 'Red'
    context.chess_engine.turn_manager.current_turn = 'Black'

@when('Red tries to move a Cannon')
def step_when_red_tries_move_cannon(context):
    """紅方試圖移動炮"""
    # 嘗試移動炮（應該失敗，因為現在是黑方回合）
    context.move_result = context.chess_engine.move_piece(4, 4, 4, 5)

@then("the move is illegal because it's Black's turn")
def step_then_illegal_because_black_turn(context):
    """驗證移動非法，因為輪到黑方"""
    assert context.move_result == False, "Expected move to be illegal due to turn violation" 