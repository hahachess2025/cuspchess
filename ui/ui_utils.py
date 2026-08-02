import datetime
import logging
import math
import time
from tkinter import *
from tkinter import messagebox

import chess
from PIL import Image as PILImage
from PIL import ImageDraw, ImageTk

import ai.ChessEngine
import ai.stop_threads
import ui.editor
import utils.config
import utils.game_results
import utils.game_state
import utils.pgnhistory as pgnhistory

logger = logging.getLogger(__name__)

def widget_initialization(cusp_app):
    logger.info("widget_initialization")
    clear_scrolltext_move_history(cusp_app)
    update_player_board_label(cusp_app)
    clear_board_move_history(cusp_app)
    cusp_app.Human_setup_confirmation_checkbox_var.set(0)


def draw_pieces(cusp_app, chess_board_variant, sound_play=True):
    logger.info(f"draw_pieces: {chess_board_variant}")
    if chess_board_variant == "Editor":
        canvas = cusp_app.editor_board_canvas
        canvas_size = cusp_app.editor_canvas_size
        piece_id=cusp_app.editor_img
    elif chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        piece_id=cusp_app.img
        
    if chess_board_variant != "Editor":
        update_player_board_label(cusp_app)
        update_game_status_label(cusp_app)
        update_color_to_move_label(cusp_app)
        # When players swap sides, we just rotate the board.
        if cusp_app.rotate_board:
            if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
                img = PILImage.open("assets/chessBoardRotated.png")
                img = img.resize( (canvas_size, canvas_size), PILImage.Resampling.LANCZOS )
            boardImg = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(0, 0, image=boardImg, anchor=NW)
            cusp_app.boardImg = boardImg

            if cusp_app.blindfold_mode:
                img = PILImage.open("assets/chessBoardrotatedNotationsBig.png")
                img = img.resize( (cusp_app.blindfold_canvas_size, cusp_app.blindfold_canvas_size), PILImage.Resampling.LANCZOS, )
                boardImg = ImageTk.PhotoImage(img)
                cusp_app.blindfold_board_canvas.delete("all")
                cusp_app.blindfold_board_canvas.create_image( 0, 0, image=boardImg, anchor=NW )
                cusp_app.blindfold_boardImg = boardImg
            cusp_app.rotate_board = False

    count = 0
    for i in range(64):
        piece = str(cusp_app.board.piece_at(i))
        if piece:
            if chess_board_variant == "Editor":
                piece_draw_x = (i % 8) * (canvas_size / 8)
                piece_draw_y = (8 - i // 8) * (canvas_size / 8)
            elif chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
                if not cusp_app.flip_board_enable:
                    piece_draw_x = (i % 8) * (cusp_app.canvas_size / 8)
                    piece_draw_y = (7 - i // 8) * (cusp_app.canvas_size / 8)
                else:
                    piece_draw_x = (7 - i % 8) * (cusp_app.canvas_size / 8)
                    piece_draw_y = (i // 8) * (cusp_app.canvas_size / 8)

            piece_img = ""

            if piece == "R":
                piece_img = "assets/Pieces/wr.png"
            if piece == "N":
                piece_img = "assets/Pieces/wn.png"
            if piece == "B":
                piece_img = "assets/Pieces/wb.png"
            if piece == "Q":
                piece_img = "assets/Pieces/wq.png"
            if piece == "K":
                piece_img = "assets/Pieces/wk.png"
            if piece == "P":
                piece_img = "assets/Pieces/wp.png"

            if piece == "r":
                piece_img = "assets/Pieces/br.png"
            if piece == "n":
                piece_img = "assets/Pieces/bn.png"
            if piece == "b":
                piece_img = "assets/Pieces/bb.png"
            if piece == "q":
                piece_img = "assets/Pieces/bq.png"
            if piece == "k":
                piece_img = "assets/Pieces/bk.png"
            if piece == "p":
                piece_img = "assets/Pieces/bp.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 8), int(canvas_size / 8)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
        else:
            piece_id[count] = None
        count = count + 1

    if chess_board_variant == "Editor" :
        if chess_board_variant == "Editor":
            extra_pieces = 6
        else:
            extra_pieces = 5
            check_all_pieces_on_board(cusp_app, cusp_app.board)

        for i in range(extra_pieces):
            piece = ""
            piece_draw_x = (i + 1) * (canvas_size / 8)
            piece_draw_y = 9 * (canvas_size / 8)
            if i == 0:
                if ( chess_board_variant == "Editor" or "R" in cusp_app.board_dict_all_available ):
                    piece = "R"
            elif i == 1:
                if ( chess_board_variant == "Editor" or "N" in cusp_app.board_dict_all_available ):
                    piece = "N"
            elif i == 2:
                if ( chess_board_variant == "Editor" or "B" in cusp_app.board_dict_all_available ):
                    piece = "B"
            elif i == 3:
                if ( chess_board_variant == "Editor" or "Q" in cusp_app.board_dict_all_available ):
                    piece = "Q"
            elif i == 4:
                if ( chess_board_variant == "Editor" or "P" in cusp_app.board_dict_all_available ):
                    piece = "P"
            elif i == 5:
                if chess_board_variant == "Editor":
                    piece = "K"

            piece_img = ""
            if piece == "R":
                piece_img = "assets/Pieces/wr.png"
            if piece == "N":
                piece_img = "assets/Pieces/wn.png"
            if piece == "B":
                piece_img = "assets/Pieces/wb.png"
            if piece == "Q":
                piece_img = "assets/Pieces/wq.png"
            if piece == "K":
                piece_img = "assets/Pieces/wk.png"
            if piece == "P":
                piece_img = "assets/Pieces/wp.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 8), int(canvas_size / 8)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
            count = count + 1
        for i in range(extra_pieces):
            piece = ""
            piece_draw_x = (i + 1) * (canvas_size / 8)
            piece_draw_y = 0
            if i == 0:
                if ( chess_board_variant == "Editor" or "r" in cusp_app.board_dict_all_available ):
                    piece = "r"
            elif i == 1:
                if ( chess_board_variant == "Editor" or "n" in cusp_app.board_dict_all_available ):
                    piece = "n"
            elif i == 2:
                if ( chess_board_variant == "Editor" or "b" in cusp_app.board_dict_all_available ):
                    piece = "b"
            elif i == 3:
                if ( chess_board_variant == "Editor" or "q" in cusp_app.board_dict_all_available ):
                    piece = "q"
            elif i == 4:
                if ( chess_board_variant == "Editor" or "p" in cusp_app.board_dict_all_available ):
                    piece = "p"
            elif i == 5:
                if chess_board_variant == "Editor":
                    piece = "k"
            piece_img = ""
            if piece == "r":
                piece_img = "assets/Pieces/br.png"
            if piece == "n":
                piece_img = "assets/Pieces/bn.png"
            if piece == "b":
                piece_img = "assets/Pieces/bb.png"
            if piece == "q":
                piece_img = "assets/Pieces/bq.png"
            if piece == "k":
                piece_img = "assets/Pieces/bk.png"
            if piece == "p":
                piece_img = "assets/Pieces/bp.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 8), int(canvas_size / 8)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
            count = count + 1
    while count < 80:
        piece_id[count] = None
        count = count + 1

    if cusp_app.play_sound_enable and cusp_app.game_in_progress and sound_play:
        cusp_app.move_sound.play()

    cusp_app.update()


# draw a arrow when dragging mouse
def left_button_motion(cusp_app, event, chess_board_variant):
    logger.info("left_button_motion")
    if not cusp_app.mouse_drag:
        return
    mouse_x, mouse_y = event.x, event.y

    if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        if canvas_size < mouse_x or mouse_x < 0 or mouse_y > canvas_size or mouse_y < 0:
            return
    elif chess_board_variant == "Blindfold":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        if ( cusp_app.blindfold_canvas_size < mouse_x or mouse_x < 0 or mouse_y > cusp_app.blindfold_canvas_size or mouse_y < 0 ):
            return
        size_ratio = canvas_size / cusp_app.blindfold_canvas_size
        mouse_x = size_ratio * mouse_x
        mouse_y = size_ratio * mouse_y

    SQUARE_SIZE = int(canvas_size / 8)
    if cusp_app.selected_piece:
        canvas.delete("drag_piece")
        if str(cusp_app.selected_piece).isupper():
            color = "w"
        else:
            color = "b"
        kind = str(cusp_app.selected_piece).lower()
        key = color + kind
        canvas.create_image( mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2, image=cusp_app.piece_images[key], anchor="nw", tags="drag_piece", )


# remove one piece to set up a fight starting position in Cusp Chess
def right_click(cusp_app, event, chess_board_variant):
    logger.info("right_click")
    clear_board_move_history(cusp_app)
    if chess_board_variant != "Editor":
        if not cusp_app.game_in_progress:
            return

    if chess_board_variant == "CuspChess":
        if not cusp_app.human_no_move_this_round:
            return
        canvas_size = cusp_app.canvas_size
    elif chess_board_variant == "Editor":
        ai.stop_threads.stop_editor_threads(cusp_app)
        canvas_size = cusp_app.editor_canvas_size
    elif chess_board_variant == "Blindfold":
        canvas_size = cusp_app.blindfold_canvas_size

    mouse_x, mouse_y = event.x, event.y
    canvas_x = mouse_x // int(canvas_size / 8)
    canvas_y = mouse_y // int(canvas_size / 8)

    chessboard_x = canvas_x

    if mouse_x > canvas_size or mouse_x < 0:
        return
    if chess_board_variant == "CuspChess" or chess_board_variant == "Blindfold":
        if mouse_y < 0 or mouse_y > canvas_size:
            return
        chessboard_y = 7 - canvas_y
    elif  chess_board_variant == "Editor":
        if mouse_y < canvas_size / 8 or mouse_y > canvas_size * 9 / 8:
            return
        chessboard_y = 9 - canvas_y

    if chess_board_variant == "CuspChess":
        chessboard_index = chessboard_x + chessboard_y * 8
        player_one_turn = cusp_app.board.turn
    elif chess_board_variant == "Editor":
        chessboard_index = chessboard_x + chessboard_y * 8 - 8
        player_one_turn = cusp_app.board.turn

    piece = cusp_app.board.piece_at(chessboard_index)
    if not piece:
        if chess_board_variant == "Blindfold":
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
        return

    if ( ( cusp_app.chess_game_variant_mode == "CuspChess" ) and cusp_app.cusp_chess_phase == "SafeMove" and ( (cusp_app.player_one == "Human" and player_one_turn) or (cusp_app.player_two == "Human" and not player_one_turn) ) ) or chess_board_variant == "Editor":
        if chess_board_variant != "Editor":
            cusp_app.Human_must_set_up = True
            if chess_board_variant == "CuspChess" or chess_board_variant == "Blindfold":
                draw_rectangle(cusp_app, canvas_x, canvas_y)
                cusp_app.human_no_move_this_round = False
                cusp_app.move_str = str( chess.square_name(chessboard_index)) + "xx"
            cusp_app.board.remove_piece_at(chessboard_index)
            draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
        else:
            cusp_app.board.remove_piece_at(chessboard_index)
            draw_pieces(cusp_app, "Editor")
            ui.editor.editor_update_player_score_bar(cusp_app)


def draw_all_legal_moves_for_selected_piece( cusp_app, legal_moves, SQUARE_SIZE, RANKS, chess_board_variant ):
    logger.info("draw_all_legal_moves_for_selected_piece")
    if ( chess_board_variant == "Normal" or chess_board_variant == "CuspChess" or chess_board_variant == "Blindfold" ):
        canvas = cusp_app.board_canvas

    for move in legal_moves:
        to_sq = move.to_square
        tf = chess.square_file(to_sq)  # 0 = 'a', 4 = 'e'
        tr = chess.square_rank(to_sq)
        if cusp_app.flip_board_enable:
            tf = 7 - tf
            tr = 7 - tr
        canvas_x0 = tf * SQUARE_SIZE
        canvas_y0 = (RANKS - 1 - tr) * SQUARE_SIZE
        canvas_x1 = canvas_x0 + SQUARE_SIZE
        canvas_y1 = canvas_y0 + SQUARE_SIZE
        canvas.create_oval( canvas_x0 + SQUARE_SIZE // 4, canvas_y0 + SQUARE_SIZE // 4, canvas_x1 - SQUARE_SIZE // 4, canvas_y1 - SQUARE_SIZE // 4, fill="green", outline="", tags="highlight", )


def legal_moves_at(cusp_app, board: chess.Board, square: chess.Square):
    logger.info("legal_moves_at")
    moves = [move for move in board.legal_moves if move.from_square == square]
    return moves


def check_whether_legal_promotion( cusp_app, move, move_start_index, move_end_index):
    logger.info("check_whether_legal_promotion")
    # here legal not only means legal promotion in standard chess, but also
    # means setup-rule without both kings checked
    if chess.Move.from_uci(move):
        uci_move = chess.Move.from_uci(move)
        if uci_move in cusp_app.board.legal_moves:
            cusp_app.Human_must_set_up = False
            cusp_app.move_str = str(cusp_app.board.san(uci_move))
            return True
        else:
            # check if both king are checked
            board = cusp_app.board.copy()
            board.remove_piece_at(move_start_index)
            if str( cusp_app.board.piece_at( cusp_app.piece_move_start_square)) == "p":
                if str(uci_move)[4] == "q":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("q"))
                elif str(uci_move)[4] == "r":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("r"))
                elif str(uci_move)[4] == "n":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("n"))
                elif str(uci_move)[4] == "b":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("b"))

            elif str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P":
                if str(uci_move)[4] == "q":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("Q"))
                elif str(uci_move)[4] == "r":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("R"))
                elif str(uci_move)[4] == "n":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("N"))
                elif str(uci_move)[4] == "b":
                    board.set_piece_at( move_end_index, chess.Piece.from_symbol("B"))

            changed_turn_board = board.copy()
            changed_turn_board.turn = 1 ^ changed_turn_board.turn

            if board.is_check() and changed_turn_board.is_check():
                logger.info("both kings are checked")

            else:
                cusp_app.Human_must_set_up = True
                logger.info("human must check setup checkbox now")
                cusp_app.move_str = str(move)
                return True


# when setup-rule to set up a fight starting position, both kings are checked is
# not allowed.
def both_kings_checked(cusp_app, move_start_index, move_end_index):
    logger.info("both_kings_checked")
    board = cusp_app.board.copy()
    piece = board.piece_at(move_start_index)
    board.remove_piece_at(move_start_index)
    board.set_piece_at(move_end_index, piece)

    changed_turn_board = board.copy()
    changed_turn_board.turn = 1 ^ changed_turn_board.turn

    if board.is_check() and changed_turn_board.is_check():
        return True


def legal_moves_by_human(cusp_app, move, chess_board_variant):
    logger.info("legal_moves_by_human")
    if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
        canvas = cusp_app.board_canvas
        start_index = cusp_app.piece_move_start_square
        end_index = cusp_app.to_sq

    if cusp_app.move_str_legal:
        cusp_app.move_str = str(cusp_app.board.san(move))
        cusp_app.setting_up_in_cusp_chess = False
        # save before pushing a move
        pgnhistory.utils.pgnhistory.save_PGN_and_output_move_history( cusp_app, True)

        cusp_app.board.push(move)
        draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)

        draw_arrows_with_two_indexes(cusp_app, start_index, end_index)

        utils.game_results.check_game_result(cusp_app)
        cusp_app.update()
        
    # check pawn promotion
    elif ( chess.square_rank(end_index) == 7 and str(cusp_app.board.piece_at(start_index)) == "P" ) or ( chess.square_rank(end_index) == 0 and str(cusp_app.board.piece_at(start_index)) == "p" ):
        moveq = str(move) + "q"
        # pawn promotion to queen to test if the promotion is legal.
        if chess.Move.from_uci(moveq):
            moveq = chess.Move.from_uci(moveq)
            if moveq in cusp_app.board.legal_moves:
                # is legal
                logger.info("-------choose pawn promotion option --------------")
                promotion_result = pawn_promotion(
                    cusp_app
                )  # ['queen','rook','knight','bishop']
                if promotion_result == "queen":
                    move = str(move) + "q"
                    move = chess.Move.from_uci(move)
                elif promotion_result == "rook":
                    move = str(move) + "r"
                    move = chess.Move.from_uci(move)
                elif promotion_result == "knight":
                    move = str(move) + "n"
                    move = chess.Move.from_uci(move)
                elif promotion_result == "bishop":
                    move = str(move) + "b"
                    move = chess.Move.from_uci(move)
                else:
                    move = str(move) + "q"
                    move = chess.Move.from_uci(move)

                cusp_app.move_str = str(cusp_app.board.san(move))
                cusp_app.setting_up_in_cusp_chess = False
                pgnhistory.utils.pgnhistory.save_PGN_and_output_move_history( cusp_app, True)
                # save before push move

                cusp_app.board.push(move)
                draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                draw_arrows_with_two_indexes(cusp_app, start_index, end_index)
                utils.game_results.check_game_result(cusp_app)

                cusp_app.update()


def update_color_to_move_label(cusp_app):
    logger.info("update_color_to_move_label")
    if cusp_app.cusp_chess_phase != "Decision":
        if cusp_app.board.turn:
            cusp_app.color_to_move_label_state = "White"  
        else:
            cusp_app.color_to_move_label_state = "Black" 
        ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
    else:
        if cusp_app.active_color_in_cusp_setup == "W":
            cusp_app.color_to_move_label_state = "Black"
            ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
        else:
            cusp_app.color_to_move_label_state = "White"
            ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
    if cusp_app.blindfold_mode:
        ui.language.update_widget(cusp_app, cusp_app.blindfold_color_to_move_label)
    cusp_app.update()


# at the top and bottom of the chess board
def update_player_board_label(cusp_app):
    logger.info("update_player_board_label")

    cusp_app.player_one_board_label.configure(image=cusp_app.play_one_logo)
    cusp_app.player_two_board_label.configure(image=cusp_app.play_two_logo)
    if ( cusp_app.chess_game_variant_mode == "Normal" or cusp_app.cusp_chess_phase == "SafeMove" ):
        cusp_app.player_one_label_state = "player_one_board_label_show_name"
        cusp_app.player_two_label_state = "player_two_board_label_show_name"
        
    elif ( cusp_app.cusp_chess_phase == "Decision" or cusp_app.cusp_chess_phase == "Fight" ):
        if not cusp_app.choose_color_directly:
            if cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_one_label_state = "player_one_board_label_setup"
                cusp_app.player_two_label_state = "player_two_board_label_passively_choose"
            elif cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_two_label_state = "player_two_board_label_setup"
                cusp_app.player_one_label_state = "player_one_board_label_passively_choose"
        else:
            if cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_one_label_state = "player_one_board_label_directly_choose"
                
            elif cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_two_label_state = "player_two_board_label_directly_choose"
                
    ui.language.update_widget(cusp_app, cusp_app.player_one_board_label) 
    ui.language.update_widget(cusp_app, cusp_app.player_two_board_label)
        
    if cusp_app.blindfold_mode:
        cusp_app.blindfold_player_one_board_label.configure( image=cusp_app.play_one_logo )
        cusp_app.blindfold_player_two_board_label.configure( image=cusp_app.play_two_logo )

        ui.language.update_widget(cusp_app, cusp_app.blindfold_player_one_board_label) 
        ui.language.update_widget(cusp_app, cusp_app.blindfold_player_two_board_label)
    cusp_app.update()


def update_game_status_label(cusp_app, RESET=False):
    logger.info("update_game_status_label")

    if RESET:
        cusp_app.game_status_label.config(font=("Arial", 20))
        if cusp_app.chess_game_variant_mode == "CuspChess":
            cusp_app.game_status_label_state = "game_status_label_ready_CC"
        else:
            cusp_app.game_status_label_state = "game_status_label_ready"
    
    elif cusp_app.game_in_progress:
        if cusp_app.chess_game_variant_mode == "CuspChess":
            if cusp_app.Human_must_set_up:
                if cusp_app.board.turn:
                    cusp_app.game_status_label_player_name=cusp_app.player_one_name
                else:
                    cusp_app.game_status_label_player_name=cusp_app.player_two_name
                cusp_app.game_status_label_state = "game_status_label_player_must_setup"
            elif cusp_app.cusp_chess_phase == "SafeMove":
                cusp_app.game_status_label_state = "game_status_label_safe_CC"
            else:
                cusp_app.game_status_label_state = "game_status_label_player_must_win"
        else:
            cusp_app.game_status_label_state = "game_status_label_ready"

    else:
        utils.game_results.show_game_result(cusp_app)
    ui.language.update_widget(cusp_app, cusp_app.game_status_label)    
    cusp_app.update()


def update_two_player_scores_bar(cusp_app, score=0):
    logger.info("update_two_player_scores_bar")

    if cusp_app.flip_board_enable:
        score = -score
    # cusp value is the score of the fight starting position
    # when a player chooses a color directly, the opponent's cusp value is the previous score.
    # so we can see what the opponent missed.
    if cusp_app.choose_color_directly and cusp_app.set_cusp_value == False:
        if cusp_app.active_color_in_cusp_setup == "W":
            cusp_app.player_two_value_on_the_cusp = cusp_app.previous_move_score
            cusp_app.player_two_score_on_the_cusp_set = True
        elif cusp_app.active_color_in_cusp_setup == "B":
            cusp_app.player_one_value_on_the_cusp = cusp_app.previous_move_score
            cusp_app.player_one_score_on_the_cusp_set = True
        cusp_app.set_cusp_value = True
    cusp_app.previous_move_score = score

    if cusp_app.eval_show_enable:
        set_original_score = score
        if cusp_app.engine == cusp_app.engine_one:
            player_one_white_top = convert_score_to_eval_bar( cusp_app, -set_original_score, cusp_app.canvas_size )

            if not cusp_app.flip_board_enable:
                cusp_app.player_one_bar.create_rectangle(
                    0, 0, 20, player_one_white_top, fill="#000000", outline="")
                cusp_app.player_one_bar.create_rectangle(
                    0,
                    player_one_white_top,
                    20,
                    cusp_app.canvas_size,
                    fill="#FFFFFF",
                    outline="",
                )
            else:
                cusp_app.player_one_bar.create_rectangle(
                    0, 0, 20, player_one_white_top, fill="#FFFFFF", outline="")
                cusp_app.player_one_bar.create_rectangle(
                    0,
                    player_one_white_top,
                    20,
                    cusp_app.canvas_size,
                    fill="#000000",
                    outline="",
                )

        elif cusp_app.engine == cusp_app.engine_two:
            player_two_white_top = convert_score_to_eval_bar( cusp_app, set_original_score, cusp_app.canvas_size )

            if not cusp_app.flip_board_enable:
                cusp_app.player_two_bar.create_rectangle(
                    0, 0, 20, player_two_white_top, fill="#000000", outline="")
                cusp_app.player_two_bar.create_rectangle(
                    0,
                    player_two_white_top,
                    20,
                    cusp_app.canvas_size,
                    fill="#FFFFFF",
                    outline="",
                )
            else:
                cusp_app.player_two_bar.create_rectangle(
                    0, 0, 20, player_two_white_top, fill="#FFFFFF", outline="")
                cusp_app.player_two_bar.create_rectangle(
                    0,
                    player_two_white_top,
                    20,
                    cusp_app.canvas_size,
                    fill="#000000",
                    outline="",
                )

        # draw two marks for the two cusp value.
        if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase != "SafeMove" ):
            if cusp_app.engine == cusp_app.engine_one:
                if cusp_app.player_one_score_on_the_cusp_set:
                    mark_player_one_score = cusp_app.player_one_value_on_the_cusp

                    if cusp_app.flip_board_enable:
                        mark_player_one_score = -mark_player_one_score
                    mark_player_one_score = convert_score_to_eval_bar( cusp_app, -mark_player_one_score, cusp_app.canvas_size )

                    if cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.player_one_bar.create_rectangle(
                            0,
                            mark_player_one_score - 2,
                            20,
                            mark_player_one_score + 2,
                            fill="#EF0C0C",
                            outline="",
                        )
                    elif cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.player_one_bar.create_rectangle(
                            0,
                            mark_player_one_score - 2,
                            20,
                            mark_player_one_score + 2,
                            fill="#00FF00",
                            outline="",
                        )
            else:
                if cusp_app.player_two_score_on_the_cusp_set:
                    mark_player_two_score = cusp_app.player_two_value_on_the_cusp
                    if cusp_app.flip_board_enable:
                        mark_player_two_score = -mark_player_two_score
                    mark_player_two_score = convert_score_to_eval_bar( cusp_app, mark_player_two_score, cusp_app.canvas_size )

                    if cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.player_two_bar.create_rectangle(
                            0,
                            mark_player_two_score - 2,
                            20,
                            mark_player_two_score + 2,
                            fill="#EF0C0C",
                            outline="",
                        )
                    elif cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.player_two_bar.create_rectangle(
                            0,
                            mark_player_two_score - 2,
                            20,
                            mark_player_two_score + 2,
                            fill="#00FF00",
                            outline="",
                        )

    cusp_app.update()


def convert_score_to_eval_bar(cusp_app, score_to_be_converted, canvas_size):
    logger.info("convert_score_to_eval_bar")
    # # if score equals to 0, the white mark ends at the center of the chess board.
    # # if score equals to 1, the mark at fifth rank. critical area in Cusp Chess
    # # if score equals to 2, the mark at sixth rank
    # # if score equals to -1, the mark at third rank. critical area in Cusp Chess
    # # if score equals to -2, the mark at second rank
    max_score = 10
    # Adjust maximum score
    if 2 >= score_to_be_converted >= -2:
        eval_bar = canvas_size / 2 + canvas_size / 8 * score_to_be_converted
    elif (max_score > score_to_be_converted > 2) or ( -max_score < score_to_be_converted < -2 ):
        eval_bar = ( canvas_size / 2 + canvas_size / 8 * 2 * math.copysign(1, score_to_be_converted) + math.copysign(1, score_to_be_converted) * (abs(score_to_be_converted) - 2) * canvas_size / 4 / 8 )
    else:
        eval_bar = ( canvas_size / 2 + math.copysign( 1, score_to_be_converted) * canvas_size / 2)
    return eval_bar


def reset_two_player_scores_bar(cusp_app):
    logger.info("reset_two_player_scores_bar")

    cusp_app.player_one_bar.delete("all")
    cusp_app.player_two_bar.delete("all")
    engine_one = cusp_app.engine_one
    engine_two = cusp_app.engine_two
    cusp_app.engine_one = "1"
    cusp_app.engine_two = "2"

    cusp_app.cusp_chess_phase = "SafeMove"

    cusp_app.engine = cusp_app.engine_one
    update_two_player_scores_bar(cusp_app, 0)
    cusp_app.engine = cusp_app.engine_two
    update_two_player_scores_bar(cusp_app, 0)

    cusp_app.engine_one = engine_one
    cusp_app.engine_two = engine_two


def initialize_piece_images(cusp_app, chess_variant):
    logger.info("initialize_piece_images")

    if chess_variant == "Normal" or chess_variant == "CuspChess":
        canvas_size = cusp_app.canvas_size

    for color in ["w", "b"]:
        for kind in ["p", "r", "n", "b", "q", "k"]:
            path = f"assets/Pieces/{color}{kind}.png"
            img = PILImage.open(path).resize( (int(canvas_size / 8), int(canvas_size / 8)), PILImage.Resampling.LANCZOS )
            cusp_app.piece_images[color + kind] = ImageTk.PhotoImage(img)


def animate_piece_move( cusp_app, piece, start_board_index, end_board_index, steps=10, delay=20 ):
    logger.info("animate_piece_move")
    if start_board_index == "":
        return
    if start_board_index == -1:
        return
    if start_board_index == end_board_index:
        return

    if end_board_index == -1:
        draw_arrows_with_two_indexes( cusp_app, start_board_index, end_board_index)
        return
    if not piece:
        return

    chessboard_move_start_x = start_board_index % 8
    chessboard_move_start_y = start_board_index // 8

    canvas_move_start_x = chessboard_move_start_x
    canvas_move_start_y = 7 - chessboard_move_start_y

    chessboard_move_end_x = end_board_index % 8
    chessboard_move_end_y = end_board_index // 8

    canvas_move_end_x = chessboard_move_end_x
    canvas_move_end_y = 7 - chessboard_move_end_y

    if not cusp_app.flip_board_enable:
        start_x = canvas_move_start_x * (cusp_app.canvas_size / 8)
        start_y = canvas_move_start_y * (cusp_app.canvas_size / 8)

        end_x = canvas_move_end_x * (cusp_app.canvas_size / 8)
        end_y = canvas_move_end_y * (cusp_app.canvas_size / 8)
    else:
        start_x = 7 * (cusp_app.canvas_size / 8) - ( canvas_move_start_x * (cusp_app.canvas_size / 8) )
        start_y = 7 * (cusp_app.canvas_size / 8) - ( canvas_move_start_y * (cusp_app.canvas_size / 8) )

        end_x = 7 * (cusp_app.canvas_size / 8) - ( canvas_move_end_x * (cusp_app.canvas_size / 8) )
        end_y = 7 * (cusp_app.canvas_size / 8) - ( canvas_move_end_y * (cusp_app.canvas_size / 8) )

    if str(piece).isupper():
        color = "w"
    else:
        color = "b"
    kind = str(piece).lower()
    key = color + kind

    piece_img = cusp_app.piece_images[key]
    piece_id = cusp_app.board_canvas.create_image( start_x, start_y, image=piece_img, anchor="nw" )

    animate_piece( cusp_app, piece_id, start_x, start_y, end_x, end_y, steps=10, delay=20)
    cusp_app.after( steps * delay * 2, lambda: cusp_app.board_canvas.delete(piece_id) )
    cusp_app.after( steps * delay * 2, lambda: draw_arrows_with_two_indexes( cusp_app, start_board_index, end_board_index ), )


def draw_arrows_with_two_indexes(cusp_app, start_board_index, end_board_index):
    logger.info("draw_arrows_with_two_indexes")
    position_list = []
    position_list.append(start_board_index)
    position_list.append(end_board_index)
    draw_transparent_arrow( cusp_app, position_list, cusp_app.chess_game_variant_mode)


def animate_piece( cusp_app, piece_id, from_x, from_y, to_x, to_y, steps=10, delay=20):
    logger.info("animate_piece")
    dx = (to_x - from_x) / steps
    dy = (to_y - from_y) / steps

    def step(count=0):
        if count < steps:
            cusp_app.board_canvas.move(piece_id, dx, dy)
            cusp_app.board_canvas.after(delay, step, count + 1)
    step()


def draw_transparent_arrow( cusp_app, position_list, chess_board_variant, keep_others=False, arrow_color=(172, 84, 94), alpha=128, ):
    logger.info("draw_transparent_arrow")
    if len(position_list) == 0 or (len(position_list) % 2 != 0):
        return

    if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size

    for i in range(2):
        if cusp_app.transparent_arrows[i]:
            canvas.delete(cusp_app.transparent_arrows[i])


    for index in range(len(position_list) // 2):
        if position_list[index * 2] == position_list[index * 2 + 1]:
            continue
        if position_list[index * 2] == -1:
            continue

        start_board_index = position_list[index * 2]
        end_board_index = position_list[index * 2 + 1]

        chessboard_move_start_x = start_board_index % 8
        chessboard_move_start_y = start_board_index // 8

        canvas_move_start_x = chessboard_move_start_x
        canvas_move_start_y = 7 - chessboard_move_start_y

        if end_board_index == -1:
            draw_rectangle(cusp_app, canvas_move_start_x, canvas_move_start_y)
            return

        chessboard_move_end_x = end_board_index % 8
        chessboard_move_end_y = end_board_index // 8

        canvas_move_end_x = chessboard_move_end_x
        canvas_move_end_y = 7 - chessboard_move_end_y

        if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
            if not cusp_app.flip_board_enable:
                start_x = (canvas_move_start_x * (canvas_size / 8) + (canvas_size / 8) / 2)
                start_y = (canvas_move_start_y * (canvas_size / 8) + (canvas_size / 8) / 2)

                end_x = canvas_move_end_x * \
                    (canvas_size / 8) + (canvas_size / 8) / 2
                end_y = canvas_move_end_y * \
                    (canvas_size / 8) + (canvas_size / 8) / 2
            else:
                start_x = ( 8 * (canvas_size / 8) - (canvas_move_start_x * (canvas_size / 8)) - (canvas_size / 8) / 2 )
                start_y = ( 8 * (canvas_size / 8) - (canvas_move_start_y * (canvas_size / 8)) - (canvas_size / 8) / 2 )

                end_x = ( 8 * (canvas_size / 8) - (canvas_move_end_x * (canvas_size / 8)) - (canvas_size / 8) / 2 )
                end_y = ( 8 * (canvas_size / 8) - (canvas_move_end_y * (canvas_size / 8)) - (canvas_size / 8) / 2 )

        
        # --- compute direction vectors ---
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.hypot(dx, dy)
        if length < 1e-6:
            return None  # nothing to draw
        ux = dx / length
        uy = dy / length
        if cusp_app.cusp_chess_phase == "Decision":
            arrow_color = (255, 0, 0)

        if chess_board_variant == "Normal" or chess_board_variant == "CuspChess":
            w = h = canvas_size
   
        img = PILImage.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.line( ( start_x, start_y, end_x - (canvas_size / 8) / 6 * ux, end_y - (canvas_size / 8) / 6 * uy, ), fill=arrow_color + (alpha,), width=8, )

        # Draw arrowhead (triangle)

        # perpendicular (unit)
        px = -uy
        py = ux

        # --- head / shaft sizing ---

        head_length = max(12, min(length * 0.25, 40))

        head_width = head_length * 0.6

        # base point of the head (where shaft ends)
        bx = end_x - ux * head_length
        by = end_y - uy * head_length

        # head corners (perpendicular offset from base)
        half_w = head_width / 2.0
        corner1 = (bx + px * half_w, by + py * half_w)
        corner2 = (bx - px * half_w, by - py * half_w)
        tip = (end_x, end_y)

        rgba = (arrow_color[0], arrow_color[1], arrow_color[2], int(alpha))
        draw.polygon([tip, corner1, corner2], fill=rgba)

        # Convert to Tk image and display
        arrow_img = ImageTk.PhotoImage(img)
        cusp_app.transparent_arrows[index] = canvas.create_image( 0, 0, image=arrow_img, anchor="nw" )
        cusp_app.arrow_img[index] = arrow_img
        # print('draw arrow')

        if cusp_app.blindfold_mode:
            if cusp_app.blindfold_arrow:
                cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_arrow)
            if cusp_app.blindfold_board_remove_piece_rectangle:
                cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )

            resize_img = img.resize( (cusp_app.blindfold_canvas_size, cusp_app.blindfold_canvas_size), PILImage.Resampling.LANCZOS, )
            arrow_img = ImageTk.PhotoImage(resize_img)
            cusp_app.blindfold_arrow = cusp_app.blindfold_board_canvas.create_image( 0, 0, image=arrow_img, anchor="nw")
            cusp_app.arrow_img[1] = arrow_img

# for a piece removed in Cusp Chess

def draw_rectangle(cusp_app, canvas_x, canvas_y):
    logger.info("draw_rectangle")

    if cusp_app.board_remove_piece_rectangle:
        cusp_app.board_canvas.delete(cusp_app.board_remove_piece_rectangle)

    if cusp_app.flip_board_enable:
        canvas_x = 7 - canvas_x
        canvas_y = 7 - canvas_y
    else:
        canvas_x = canvas_x
        canvas_y = canvas_y

    cusp_app.board_remove_piece_rectangle = cusp_app.board_canvas.create_rectangle(
        canvas_x * (cusp_app.canvas_size / 8),
        canvas_y * (cusp_app.canvas_size / 8),
        (canvas_x * (cusp_app.canvas_size / 8) + (cusp_app.canvas_size / 8)),
        (canvas_y * (cusp_app.canvas_size / 8) + (cusp_app.canvas_size / 8)),
        outline="#FF0000",
        width=6,
    )
    if cusp_app.blindfold_mode:
        if cusp_app.blindfold_arrow:
            cusp_app.blindfold_board_canvas.delete(cusp_app.blindfold_arrow)
        if cusp_app.blindfold_board_remove_piece_rectangle:
            cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )
        resize_coefficient = cusp_app.blindfold_canvas_size / cusp_app.canvas_size
        cusp_app.blindfold_board_remove_piece_rectangle = (
            cusp_app.blindfold_board_canvas.create_rectangle(
                resize_coefficient * canvas_x * (cusp_app.canvas_size / 8),
                resize_coefficient * canvas_y * (cusp_app.canvas_size / 8),
                (
                    resize_coefficient * canvas_x * (cusp_app.canvas_size / 8)
                    + (cusp_app.blindfold_canvas_size / 8)
                ),
                (
                    resize_coefficient * canvas_y * (cusp_app.canvas_size / 8)
                    + (cusp_app.blindfold_canvas_size / 8)
                ),
                outline="#FF0000",
                width=6,
            )
        )


def clear_board_move_history(cusp_app):
    logger.info("clear_board_move_history")
    if cusp_app.blindfold_arrow:
        cusp_app.blindfold_board_canvas.delete(cusp_app.blindfold_arrow)

    if cusp_app.board_remove_piece_rectangle:
        cusp_app.board_canvas.delete(cusp_app.board_remove_piece_rectangle)

    if cusp_app.blindfold_board_remove_piece_rectangle:
        cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )

    cusp_app.update()


def clear_scrolltext_move_history(cusp_app):
    logger.info("clear_scrolltext_move_history")
    cusp_app.move_history_text.delete(1.0, END)


def generate_PGN_path(cusp_app):
    logger.info("generate_PGN_path")
    if cusp_app.chess_game_variant_mode == "Normal":
        cusp_app.PGN_save_path = ( cusp_app.PGN_folder_path + "/chess_" + str(datetime.datetime.now()).replace(":", "") + ".pgn" )
    elif cusp_app.chess_game_variant_mode == "CuspChess":
        cusp_app.PGN_save_path = ( cusp_app.PGN_folder_path + "/cusp_chess_" + str(datetime.datetime.now()).replace(":", "") + ".pgn" )
    utils.config.save_setting_in_config_file(cusp_app)

def confirm_players(cusp_app):
    logger.info("confirm_players")
    if cusp_app.translations[cusp_app.current_lang]["AI"]== cusp_app.player_one_spinbox_var.get():
        cusp_app.player_one = "AI"
        cusp_app.player_one_spinbox_chosen=0
    else:
        cusp_app.player_one = "Human"
        cusp_app.player_one_spinbox_chosen=1
        
    if cusp_app.translations[cusp_app.current_lang]["AI"]== cusp_app.player_two_spinbox_var.get():
        cusp_app.player_two = "AI"
        cusp_app.player_two_spinbox_chosen=0
    else:
        cusp_app.player_two = "Human"
        cusp_app.player_two_spinbox_chosen=1
        
    logger.info( f"---now p1 is {cusp_app.player_one} and p2 is {cusp_app.player_two}")

    if cusp_app.player_one == "AI" and cusp_app.player_two == "AI":
        cusp_app.game_player_mode = "AvA"
        set_engine_one(cusp_app)
        set_engine_two(cusp_app)
    elif cusp_app.player_one == "AI" and cusp_app.player_two == "Human":
        cusp_app.game_player_mode = "AvH"
        set_engine_one(cusp_app)
    elif cusp_app.player_two == "AI" and cusp_app.player_one == "Human":
        cusp_app.game_player_mode = "HvA"
        set_engine_two(cusp_app)
    elif cusp_app.player_one == "Human" and cusp_app.player_two == "Human":
        cusp_app.game_player_mode = "HvH"
 
    if cusp_app.adjudicator_engine_enable and cusp_app.engine_adjudicator_path != "":
        setup_engine( cusp_app, 'adjudicator_engine', cusp_app.engine_adjudicator_path)
    else:
        logger.info('no adjudicator_engine')
            
    set_player_names(cusp_app)
    utils.config.save_setting_in_config_file(cusp_app)


def set_engine_one(cusp_app):
    logger.info('set_engine_one')
    if cusp_app.engine_one_path != "":
        setup_engine(cusp_app, 'engine_one', cusp_app.engine_one_path)
        engine_one_path = cusp_app.engine_one_path
        if "/" in engine_one_path:
            engine_one_path = engine_one_path.split("/")[-1]   
        if len(engine_one_path) > 40:
            engine_one_path = engine_one_path[:40]
            if  " " in engine_one_path: 
                engine_one_path = engine_one_path.split(" ")[0]
            if  "-" in engine_one_path: 
                engine_one_path = engine_one_path.split("-")[0]
            if  "_" in engine_one_path: 
                engine_one_path = engine_one_path.split("_")[0]
        cusp_app.player_one_name_engine = engine_one_path            
    else:
        logger.info("please set engine one path in setting menu")
        return


def set_engine_two(cusp_app):
    logger.info('set_engine_two')
    if cusp_app.engine_two_path != "":
        setup_engine(cusp_app, 'engine_two', cusp_app.engine_two_path)
        engine_two_path = cusp_app.engine_two_path
        if "/" in engine_two_path:
            engine_two_path = engine_two_path.split("/")[-1]   
        if len(engine_two_path) > 40:
            engine_two_path = engine_two_path[:40]
            if  " " in engine_two_path: 
                engine_two_path = engine_two_path.split(" ")[0]
            if  "-" in engine_two_path: 
                engine_two_path = engine_two_path.split("-")[0]
            if  "_" in engine_two_path: 
                engine_two_path = engine_two_path.split("_")[0]
        cusp_app.player_two_name_engine = engine_two_path
    else:
        logger.info("please set engine two path in setting menu")
        return


def set_player_names(cusp_app):
    logger.info('set_player_names')
    if cusp_app.player_one_name_input == '':
        if cusp_app.player_one == "Human":
            cusp_app.player_one_name = "Human player one"
        elif cusp_app.player_one == "AI":
            cusp_app.player_one_name = cusp_app.player_one_name_engine
    else:
        cusp_app.player_one_name = cusp_app.player_one_name_input

    if cusp_app.player_two_name_input == '':
        if cusp_app.player_two == "Human":
            cusp_app.player_two_name = "Human player two"
        elif cusp_app.player_two == "AI":
            cusp_app.player_two_name = cusp_app.player_two_name_engine
    else:
        cusp_app.player_two_name = cusp_app.player_two_name_input


def setup_engine(cusp_app, engine_name, engine_path):
    logger.info('setup_engine')
    try:
        if engine_name == 'engine_one':
            if cusp_app.engine_one:
                cusp_app.engine_one.quit()
            cusp_app.engine_one = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
        elif engine_name == 'engine_two':
            if cusp_app.engine_two:
                cusp_app.engine_two.quit()
            cusp_app.engine_two = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
        elif engine_name == 'adjudicator_engine':
            if cusp_app.adjudicator_engine:
                cusp_app.adjudicator_engine.quit()            
            cusp_app.adjudicator_engine = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
            cusp_app.adjudicator_engine_last_time = time.time()
        elif engine_name == 'editor_engine':
            if cusp_app.editor_engine:
                cusp_app.editor_engine.quit()            
            cusp_app.editor_engine = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
            cusp_app.editor_engine_exist = True
    except Exception as e:
        logger.exception(f'engine {engine_name} setup error')
        messagebox.showerror("Error", f"Engine setup error: {e}" )

def check_all_pieces_on_board(cusp_app, board):
    logger.info('check_all_pieces_on_board') 
    cusp_app.piece_map = board.piece_map()
    cusp_app.board_dict = {
        "p": 0,
        "P": 0,
        "r": 0,
        "R": 0,
        "n": 0,
        "N": 0,
        "b": 0,
        "B": 0,
        "q": 0,
        "Q": 0,
        "k": 0,
        "K": 0,
    }
    cusp_app.board_dict_white_available = {
        "P": 8,
        "N": 2,
        "B": 2,
        "R": 2,
        "Q": 1,
        "K": 1,
    }
    cusp_app.board_dict_black_available = {
        "p": 8,
        "n": 2,
        "b": 2,
        "r": 2,
        "q": 1,
        "k": 1,
    }
    cusp_app.board_dict_all_available = {
        "p": 8,
        "P": 8,
        "n": 2,
        "N": 2,
        "b": 2,
        "B": 2,
        "r": 2,
        "R": 2,
        "q": 1,
        "Q": 1,
        "k": 1,
        "K": 1,
    }

    for index in cusp_app.piece_map:
        cusp_app.board_dict[str(cusp_app.piece_map[index])] += 1
        if str(cusp_app.piece_map[index]).isupper():
            cusp_app.board_dict_white_available[str( cusp_app.piece_map[index])] -= 1
        else:
            cusp_app.board_dict_black_available[str( cusp_app.piece_map[index])] -= 1
        cusp_app.board_dict_all_available[str(cusp_app.piece_map[index])] -= 1
        # no pawn promotion for placement and fight starting position setup
        if cusp_app.board_dict_all_available[str( cusp_app.piece_map[index])] == 0:
            del cusp_app.board_dict_all_available[str( cusp_app.piece_map[index])]
            if str(cusp_app.piece_map[index]).isupper():
                del cusp_app.board_dict_white_available[str( cusp_app.piece_map[index])]
            else:
                del cusp_app.board_dict_black_available[str( cusp_app.piece_map[index])]

# for game early stop.
def count_major_pieces(cusp_app):
    logger.info('count_major_pieces') 
    board_map = cusp_app.board.piece_map()
    cusp_app.major_piece_count = 0
    for index in board_map:
        if ( str(board_map[index]) != "p" and str(board_map[index]) != "P" and str(board_map[index]) != "k" and str(board_map[index]) != "K" ):
            cusp_app.major_piece_count = cusp_app.major_piece_count + 1


def set_timer(cusp_app):
    logger.info('set_timer')
    cusp_app.player_one_remain_time = cusp_app.time_for_each_player
    cusp_app.player_two_remain_time = cusp_app.time_for_each_player
    cusp_app.player_one_new_time = cusp_app.time_for_each_player
    cusp_app.player_two_new_time = cusp_app.time_for_each_player
    initialize_player_time_label(cusp_app)

    cusp_app.start_time = time.time()
    update_timer(cusp_app)


def initialize_player_time_label(cusp_app):
    logger.info('initialize_player_time_label')
    timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.time_for_each_player // 60), int(cusp_app.time_for_each_player % 60), int((cusp_app.time_for_each_player - int(cusp_app.time_for_each_player)) * 100), )

    cusp_app.player_one_timer_label.config(text=timestr)
    cusp_app.player_two_timer_label.config(text=timestr)


def update_timer(cusp_app):
    if cusp_app.game_in_progress:
        if cusp_app.player_one_timer_on:
            cusp_app.player_two_remain_time = cusp_app.player_two_new_time
            cusp_app.player_one_new_time = cusp_app.player_one_remain_time - ( time.time() - cusp_app.start_time )
            if cusp_app.player_one_new_time <= 0:
                if not cusp_app.player_swap_side:
                    cusp_app.time_out_result = "0-1"
                else:
                    cusp_app.time_out_result = "1-0"
                utils.game_results.check_game_result(cusp_app)
                cusp_app.player_one_new_time = 0
            timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.player_one_new_time // 60), int(cusp_app.player_one_new_time % 60), int( (cusp_app.player_one_new_time - int(cusp_app.player_one_new_time)) * 100 ), )

            update_timer_label(cusp_app, timestr)

            if cusp_app.cusp_chess_phase == "Decision":
                if cusp_app.active_color_in_cusp_setup == "W":
                    cusp_app.player_one_timer_on = False
                    cusp_app.start_time = time.time()
            else:
                if not cusp_app.player_swap_side:
                    if not cusp_app.board.turn:
                        cusp_app.player_one_timer_on = False
                        cusp_app.start_time = time.time()
                elif cusp_app.player_swap_side:
                    if cusp_app.board.turn:
                        cusp_app.player_one_timer_on = False
                        cusp_app.start_time = time.time()
        elif not cusp_app.player_one_timer_on:
            cusp_app.player_one_remain_time = cusp_app.player_one_new_time
            cusp_app.player_two_new_time = cusp_app.player_two_remain_time - ( time.time() - cusp_app.start_time )
            if cusp_app.player_two_new_time <= 0:
                if not cusp_app.player_swap_side:
                    cusp_app.time_out_result = "1-0"
                else:
                    cusp_app.time_out_result = "0-1"
                utils.game_results.check_game_result(cusp_app)
                cusp_app.player_two_new_time = 0
            timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.player_two_new_time // 60), int(cusp_app.player_two_new_time % 60), int( (cusp_app.player_two_new_time - int(cusp_app.player_two_new_time)) * 100 ), )
            update_timer_label(cusp_app, timestr)

            if cusp_app.cusp_chess_phase == "Decision":
                if cusp_app.active_color_in_cusp_setup == "B":
                    cusp_app.player_one_timer_on = True
                    cusp_app.start_time = time.time()
            else:
                if not cusp_app.player_swap_side:
                    if cusp_app.board.turn:
                        cusp_app.player_one_timer_on = True
                        cusp_app.start_time = time.time()
                else:
                    if not cusp_app.board.turn:
                        cusp_app.player_one_timer_on = True
                        cusp_app.start_time = time.time()


def update_timer_label(cusp_app, timestr):
    if cusp_app.player_one_timer_on:
        cusp_app.player_one_timer_label.config(text=timestr)
    else:
        cusp_app.player_two_timer_label.config(text=timestr)
    cusp_app.after(50, lambda: update_timer(cusp_app))

def pawn_promotion(cusp_app):
    logger.info('pawn_promotion')
    values = ["queen", "rook", "knight", "bishop"]
    dlg = multiple_options_window( cusp_app, cusp_app, "Dialog", "Select pawn promotion", values )
    return dlg.result


# for pawn promotion
class multiple_options_window(Toplevel):
    def __init__(self, parent, cusp_app, title, question, options):
        super().__init__(parent)
        root_x = parent.winfo_rootx()
        root_y = parent.winfo_rooty()

        if not cusp_app.blindfold_mode:
            win_x = root_x + 300
            win_y = root_y + 300
        else:
            win_x = root_x + 300 + cusp_app.canvas_size
            win_y = root_y + 300

        self.geometry(f"+{win_x}+{win_y}")
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.options = options
        self.result = "_"
        self.createWidgets()
        self.grab_set()
        self.wait_window()

    def createWidgets(self):
        frmQuestion = Frame(self)
        Label(frmQuestion, text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = Button( frmButtons, text=option, command=lambda x=option: self.setOption(x))
            btn.grid(column=column, row=0)
            column += 1

    def setOption(self, optionSelected):
        self.result = optionSelected
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()