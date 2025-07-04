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