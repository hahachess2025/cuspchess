"""
In Cusp Chess, if it is in Safe Move Phase or Decision Phase, 
the player need to press the "move finished" or "choose directly" button after each move.

The "move finished" button can tell your opponent 
whether you  want to set up a fight starting Position or not, especially after a legal safe move

If you made a move which is a legal safe move, and you don't want to set a fight starting position,
you uncheck the setup checkbox, and press the "move finished" button.

If you made a move (a legal safe move or a legal setup move) 
and want to set the board position as a fight starting position,
you set the must-win color, and check the setup checkbox, 
and then press the "move finished" button.

If you made a move which is an illegal safe move but a legal setup move, 
you must set the position as a fight starting position.

If you want to choose a color directly, you can't make a move on board in this tur.
You can set the must-color and hit "choose directly" button. 
Then your color is the must-win color, and you must win with the color.
 
"""

import logging
from tkinter import *
from tkinter import ttk

import chess
from PIL import Image as PILImage
from PIL import ImageTk

import ui.language

import ui.ui_utils
import utils.config
import utils.game_results
import utils.pgnhistory

logger = logging.getLogger(__name__)

# Cusp Chess board
def create_cusp_chess_UI(cusp_app):
    logger.info("create_cusp_chess_UI")
    board_frame_rowspan = 12
    player_one_board_label_row = 9
    game_status_label_row = 10
    color_to_move_label_row = 11
    player_one_timer_label_row = 8
    player_one_bar_label_row = 9

    cusp_app.board_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.board_frame.grid( column=0, row=0, rowspan=board_frame_rowspan, sticky="wens" )

    cusp_app.board_frame.grid_columnconfigure(0, weight=1)
    cusp_app.board_frame.grid_columnconfigure(1, weight=1)
    cusp_app.board_frame.grid_columnconfigure(2, weight=8)
    cusp_app.board_frame.grid_columnconfigure(3, weight=1)

    cusp_app.player_two_board_label = ttk.Label( cusp_app.board_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_two_logo, font=("Times", 15), )
    ui.language.register_widget(cusp_app, cusp_app.player_two_board_label, key=lambda:ui.language.player_two_label_dynamic_key(cusp_app), **ui.language.player_two_label_dynamic_kwargs(cusp_app) )
    cusp_app.player_two_board_label.grid(column=2, row=0)
    cusp_app.player_two_board_label.image = cusp_app.play_two_logo

    cusp_app.player_one_board_label = ttk.Label( cusp_app.board_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_one_logo, font=("Times", 15), )
    ui.language.register_widget(cusp_app, cusp_app.player_one_board_label, key=lambda:ui.language.player_one_label_dynamic_key(cusp_app), **ui.language.player_one_label_dynamic_kwargs(cusp_app) )
    cusp_app.player_one_board_label.grid( column=2, row=player_one_board_label_row)
    cusp_app.player_one_board_label.image = cusp_app.play_one_logo

    cusp_app.game_status_label = ttk.Label( cusp_app.board_frame, font=("Arial", 20) )
    ui.language.register_widget(cusp_app, cusp_app.game_status_label, key=lambda:ui.language.game_status_label_dynamic_key(cusp_app), **ui.language.game_status_label_dynamic_kwargs(cusp_app) )
    cusp_app.game_status_label.grid(column=2, row=game_status_label_row)

    cusp_app.color_to_move_label = ttk.Label(cusp_app.board_frame, font=("Times", 12))  
    ui.language.register_widget(cusp_app, cusp_app.color_to_move_label, "color_to_move_label", **ui.language.color_to_move_label_dynamic_kwargs(cusp_app))
    cusp_app.color_to_move_label.grid( column=0, row=color_to_move_label_row, columnspan=3, padx=5, pady=5, sticky="W")
    ui.ui_utils.update_color_to_move_label(cusp_app)

    cusp_app.player_one_timer_label = ttk.Label( cusp_app.board_frame, text="00:00:00", font=("Times", 15) )
    cusp_app.player_one_timer_label.grid( column=3, row=player_one_timer_label_row, padx=5, sticky="wens" )

    cusp_app.player_two_timer_label = ttk.Label( cusp_app.board_frame, text="00:00:00",font=("Times", 15) )
    cusp_app.player_two_timer_label.grid( column=3, row=1, padx=5, sticky="wens")

    cusp_app.board_canvas = Canvas( cusp_app.board_frame, width=cusp_app.canvas_size, height=cusp_app.canvas_size)
    cusp_app.board_canvas.grid(column=2, row=1, rowspan=8, sticky="news")

    cusp_app.board_canvas.bind( "<Button-1>", lambda event: left_click( cusp_app, event))
    cusp_app.board_canvas.bind( "<B1-Motion>", lambda event: ui.ui_utils.left_button_motion( cusp_app, event, cusp_app.chess_game_variant_mode ), )
    cusp_app.board_canvas.bind( "<ButtonRelease-1>", lambda event: left_button_release(cusp_app, event) )
    # remove pieces when in Cusp Chess
    cusp_app.board_canvas.bind( "<Button-3>", lambda event: ui.ui_utils.right_click( cusp_app, event, cusp_app.chess_game_variant_mode), )

    cusp_app.player_one_bar = Canvas(
        cusp_app.board_frame,
        width=20,
        height=cusp_app.canvas_size,
        bg="#808080")
    cusp_app.player_one_bar.grid(row=1, column=0, rowspan=8, padx=5)

    cusp_app.player_two_bar = Canvas(
        cusp_app.board_frame,
        width=20,
        height=cusp_app.canvas_size,
        bg="#808080")
    cusp_app.player_two_bar.grid(row=1, column=1, rowspan=8, padx=5)
    ui.ui_utils.initialize_piece_images( cusp_app, cusp_app.chess_game_variant_mode)
    draw_chess_board(cusp_app)
    # lable for two eval bars
    ttk.Label( cusp_app.board_frame, text="p1", font=("Times", 12) ).grid(row=player_one_bar_label_row, column=0, padx=2)
    ttk.Label( cusp_app.board_frame, text="p2", font=("Times", 12) ).grid(row=player_one_bar_label_row, column=1, padx=2)

    cusp_app.board_frame.bind( "<Configure>", lambda event: resize_chess_board(cusp_app, event) )
    cusp_app.update()


def draw_chess_board(cusp_app):
    logger.info("draw_chess_board")

    img = PILImage.open("assets/chessBoardNormal.png")
    img = img.resize( (cusp_app.canvas_size, cusp_app.canvas_size), PILImage.Resampling.LANCZOS)
    boardImg = ImageTk.PhotoImage(img)

    cusp_app.board_canvas.delete("all")
    cusp_app.board_canvas.create_image(0, 0, image=boardImg, anchor=NW)
    cusp_app.boardImg = boardImg


def resize_chess_board(cusp_app, event):
    logger.info("resize_chess_board")
    if cusp_app.resizing_enabled == True:
        redraw_chess_board(cusp_app)


def redraw_chess_board(cusp_app):
    logger.info("redraw_chess_board")
    board_frame_height = cusp_app.board_frame.winfo_height()
    board_frame_width = cusp_app.board_frame.winfo_width()

    cusp_app.canvas_size = board_frame_height * 86 / 100
    cusp_app.canvas_size = int(cusp_app.canvas_size / 8) * 8

    cusp_app.board_canvas.config( width=cusp_app.canvas_size, height=cusp_app.canvas_size )
    cusp_app.player_one_bar.config(width=20, height=cusp_app.canvas_size)
    cusp_app.player_two_bar.config(width=20, height=cusp_app.canvas_size)

    ui.ui_utils.initialize_piece_images( cusp_app, cusp_app.chess_game_variant_mode)
    draw_chess_board(cusp_app)
    ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode, False)

    utils.config.save_setting_in_config_file(cusp_app)

    cusp_app.update()


# human player
def left_click(cusp_app, event):
    logger.info("left_click")
    if cusp_app.game_in_progress and ( ( cusp_app.chess_game_variant_mode == "Normal" and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.chess_game_variant_mode == "CuspChess" and ( ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "Human" and not cusp_app.board.turn) or (cusp_app.player_two == "Human" and cusp_app.board.turn) ) ) ) ) ):
        if utils.game_results.check_game_result(cusp_app):
            return
        if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
            return

        ui.ui_utils.clear_board_move_history(cusp_app)
        cusp_app.setting_up_in_cusp_chess = False

        mouse_x, mouse_y = event.x, event.y
        canvas_x = mouse_x // (cusp_app.canvas_size / 8)
        canvas_y = mouse_y // (cusp_app.canvas_size / 8)
        canvas_x = int(canvas_x)
        canvas_y = int(canvas_y)

        if not cusp_app.flip_board_enable:
            chessboard_x = canvas_x
            chessboard_y = 7 - canvas_y
        else:
            chessboard_x = 7 - canvas_x
            chessboard_y = canvas_y

        chessboard_index = chessboard_x + chessboard_y * 8

        piece = cusp_app.board.piece_at(chessboard_index)

        if piece:
           
            if not cusp_app.engine_test_mode_enable:    
                if (cusp_app.board.turn and str(piece).islower()) or ( (not cusp_app.board.turn) and str(piece).isupper()):
                    return
            cusp_app.piece_move_start_square = chessboard_index
            cusp_app.mouse_drag = True

            cusp_app.selected_piece = piece
            cusp_app.board_canvas.delete("highlight")
            legal_moves = ui.ui_utils.legal_moves_at( cusp_app, cusp_app.board, chessboard_index)
            SQUARE_SIZE = int(cusp_app.canvas_size / 8)
            RANKS = 8
            ui.ui_utils.draw_all_legal_moves_for_selected_piece( cusp_app, legal_moves, SQUARE_SIZE, RANKS, cusp_app.chess_game_variant_mode, )


def left_button_release(cusp_app, event):
    logger.info("left_button_release")
    cusp_app.board_canvas.delete("highlight")
    cusp_app.board_canvas.delete("drag_piece")
    if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
        return

    if not cusp_app.mouse_drag:
        return
    cusp_app.mouse_drag = False
    ui.ui_utils.clear_board_move_history(cusp_app)
    mouse_x, mouse_y = event.x, event.y
    if ( mouse_x >= cusp_app.canvas_size or mouse_x < 0 or mouse_y >= cusp_app.canvas_size or mouse_y < 0 ):
        return
    canvas_x = mouse_x // (cusp_app.canvas_size / 8)
    canvas_y = mouse_y // (cusp_app.canvas_size / 8)
    canvas_x = int(canvas_x)
    canvas_y = int(canvas_y)

    if not cusp_app.flip_board_enable:
        chessboard_x = canvas_x
        chessboard_y = 7 - canvas_y
    else:
        chessboard_x = 7 - canvas_x
        chessboard_y = canvas_y
    chessboard_index = chessboard_x + chessboard_y * 8
    if cusp_app.piece_move_start_square == chessboard_index:
        return
    cusp_app.to_sq = chessboard_index

    move = chess.Move( from_square=cusp_app.piece_move_start_square, to_square=chessboard_index)
    if move in cusp_app.board.legal_moves:
        cusp_app.move_str_legal = True
    else:
        cusp_app.move_str_legal = False
    # legal chess move
    if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "Fight" ) or cusp_app.chess_game_variant_mode == "Normal":
        ui.ui_utils.legal_moves_by_human( cusp_app, move, cusp_app.chess_game_variant_mode)

    # Cusp Chess and cusp_app.cusp_chess_phase=="SafeMove", one free move is allowed
    elif ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" ):
        # legal move except pawn promotion
        if cusp_app.move_str_legal:
            cusp_app.Human_must_set_up = False
            cusp_app.move_str = str(cusp_app.board.san(move))
            cusp_app.move_str_uci = str(move)
            cusp_app.board.push(move)
            # keeping board's turn unchanged is easier to process some parameters in Safe Move Phase in Cusp Chess.
            # we will set the right "color to move" when press the move finished confirmation button
            cusp_app.board.turn = 1 ^ cusp_app.board.turn
            # if a player has made a move, he/she can't choose color directly
            # to get into Fight Phase in this round anymore.
            cusp_app.human_no_move_this_round = False
            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)

            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cusp_app.to_sq )
            utils.game_results.check_game_result(cusp_app)

        elif ( str(cusp_app.board.piece_at(chessboard_index)) != "k" and str(cusp_app.board.piece_at(chessboard_index)) != "K" ):
            # pawn promotion
            if cusp_app.piece_move_start_square != chessboard_index:
                if ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" and chessboard_index < 8 ) or ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" and chessboard_index > 55 ):
                    # no promotion in simplified one free move
                    if not cusp_app.engine_test_mode_enable:  return
                    logger.info("-------choose pawn promotion option --------------")
                    promotion_result = ui.ui_utils.pawn_promotion(
                        cusp_app
                    )  # ['queen','rook','knight','bishop']
                    pawn_promotion = False
                    if (str(cusp_app.board.piece_at( cusp_app.piece_move_start_square)) == "p"):
                        if promotion_result == "queen":
                            move = str(move) + "q"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("q"))
                                pawn_promotion = True
                        elif promotion_result == "rook":
                            move = str(move) + "r"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("r"))
                                pawn_promotion = True
                        elif promotion_result == "knight":
                            move = str(move) + "n"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("n"))
                                pawn_promotion = True
                        elif promotion_result == "bishop":
                            move = str(move) + "b"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("b"))
                                pawn_promotion = True
                        else:
                            move = str(move) + "q"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("q"))
                                pawn_promotion = True
                    else:
                        if promotion_result == "queen":
                            move = str(move) + "q"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("Q"))
                                pawn_promotion = True
                        elif promotion_result == "rook":
                            move = str(move) + "r"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("R"))
                                pawn_promotion = True
                        elif promotion_result == "knight":
                            move = str(move) + "n"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("N"))
                                pawn_promotion = True
                        elif promotion_result == "bishop":
                            move = str(move) + "b"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("B"))
                                pawn_promotion = True
                        else:
                            move = str(move) + "q"
                            if ui.ui_utils.check_whether_legal_promotion( cusp_app, move, cusp_app.piece_move_start_square, chessboard_index, ):
                                cusp_app.board.set_piece_at( chessboard_index, chess.Piece.from_symbol("Q"))
                                pawn_promotion = True
                    if pawn_promotion:
                        cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square)
                        cusp_app.human_no_move_this_round = False
                        ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)

                        ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cusp_app.to_sq)
                # move a pawn to back rank is not allowed
                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" and chessboard_index > 55 ) or ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" and chessboard_index < 8 ):
                    return
                # one free move, but both king are not allowed to checked at
                # the same time
                elif not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, chessboard_index ):
                    # one free move, must setup a fight starting position, and let the
                    # opponent choose a color
                    cusp_app.Human_must_set_up = True
                    logger.info("human must check setup checkbox now")
                    cusp_app.human_no_move_this_round = False
                    cusp_app.move_str_uci = str(move)

                    piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square)
                    cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square)
                    cusp_app.board.set_piece_at(chessboard_index, piece)
                    ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)
                    ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cusp_app.to_sq)
                    # timer is set when a confirmation button is pressed in
                    # Safe Move Phase

    cusp_app.piece_move_start_square = -1
    # In Cusp Chess, when cusp_chess_phase=="SafeMove", it is Safe Move Phase, human players need to
    # click move-finished button every time.
    if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
        if cusp_app.chess_game_variant_mode == "Normal":
            if (cusp_app.player_one == "AI" and cusp_app.board.turn) or ( cusp_app.player_two == "AI" and not cusp_app.board.turn ):
                cusp_app.AI_searching_best_move()
        elif cusp_app.chess_game_variant_mode == "CuspChess":
            if cusp_app.cusp_chess_phase == "Fight":
                if ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "AI" and cusp_app.board.turn) or ( cusp_app.player_two == "AI" and not cusp_app.board.turn))) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "AI" and not cusp_app.board.turn) or ( cusp_app.player_two == "AI" and cusp_app.board.turn))):
                    cusp_app.AI_searching_best_move()