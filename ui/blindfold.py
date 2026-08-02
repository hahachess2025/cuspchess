"""
it is a small trick to show your blindfold chess skill to your friends, or for streaming.

"""

import logging
from tkinter import *
from tkinter import ttk

import chess
from PIL import Image as PILImage
from PIL import ImageTk

import ui.language
import ui.normalboard
import ui.ui_utils
import utils.config
import utils.game_results
import utils.pgnhistory

logger = logging.getLogger(__name__)

def create_blindfold_chess_frame(cusp_app):
    logger.info("create_blindfold_chess_frame")
    cusp_app.blindfold_chess_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.blindfold_chess_frame.grid( column=1, row=0, rowspan=10, sticky="wens")
    cusp_app.blindfold_player_two_board_label = ttk.Label( cusp_app.blindfold_chess_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_two_logo, font=("Times", 15), )
    
    ui.language.register_widget(cusp_app, cusp_app.blindfold_player_two_board_label, key=lambda:ui.language.player_two_label_dynamic_key(cusp_app), **ui.language.player_two_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_player_two_board_label.grid(column=0, row=0)
    cusp_app.blindfold_player_two_board_label.image = cusp_app.play_two_logo

    cusp_app.blindfold_player_one_board_label = ttk.Label( cusp_app.blindfold_chess_frame,justify=LEFT, compound=LEFT, image=cusp_app.play_one_logo, font=("Times", 15), )
    ui.language.register_widget(cusp_app,  cusp_app.blindfold_player_one_board_label, key=lambda:ui.language.player_one_label_dynamic_key(cusp_app), **ui.language.player_one_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_player_one_board_label.grid(column=0, row=6)
    cusp_app.blindfold_player_one_board_label.image = cusp_app.play_one_logo

    cusp_app.blindfold_board_canvas = Canvas( cusp_app.blindfold_chess_frame, width=cusp_app.blindfold_canvas_size, height=cusp_app.blindfold_canvas_size, )
    cusp_app.blindfold_board_canvas.grid( column=0, row=1, rowspan=5, sticky="news")

    cusp_app.blindfold_board_canvas.bind( "<Button-1>", lambda event: blindfold_left_click(cusp_app, event) )
    cusp_app.blindfold_board_canvas.bind( "<B1-Motion>", lambda event: ui.ui_utils.left_button_motion( cusp_app, event, "Blindfold"))
    cusp_app.blindfold_board_canvas.bind( "<ButtonRelease-1>", lambda event: blindfold_left_button_release(cusp_app, event), )
    # remove pieces when in Cusp Chess
    cusp_app.blindfold_board_canvas.bind( "<Button-3>", lambda event: ui.ui_utils.right_click( cusp_app, event, "Blindfold"))

    create_blindfold_chess_board(cusp_app)

    cusp_app.blindfold_move_notice_label = ttk.Label( cusp_app.blindfold_chess_frame, font=("Times", 15) )
    ui.language.register_widget(cusp_app, cusp_app.blindfold_move_notice_label, key=lambda:ui.language.blindfold_label_dynamic_key(cusp_app),)
    cusp_app.blindfold_move_notice_label.grid(column=0, row=7)

    cusp_app.blindfold_color_to_move_label = ttk.Label( cusp_app.blindfold_chess_frame, font=("Times", 12) )
    ui.language.register_widget(cusp_app, cusp_app.blindfold_color_to_move_label, "color_to_move_label",**ui.language.color_to_move_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_color_to_move_label.grid( column=0, row=8, padx=5, pady=5, sticky="W" )
    ui.ui_utils.update_color_to_move_label(cusp_app)
    cusp_app.blindfold_chess_frame.bind( "<Configure>", lambda event: resize_blindfold_chess(cusp_app, event) )
    cusp_app.update()


def create_blindfold_chess_board(cusp_app):
    logger.info("create_blindfold_chess_board")
    img = PILImage.open("assets/chessBoardNotationsBig.png")
    img = img.resize( (cusp_app.blindfold_canvas_size, cusp_app.blindfold_canvas_size), PILImage.Resampling.LANCZOS, )
    boardImg = ImageTk.PhotoImage(img)

    cusp_app.blindfold_board_canvas.delete("all")
    cusp_app.blindfold_board_canvas.create_image( 0, 0, image=boardImg, anchor=NW)
    cusp_app.blindfold_boardImg = boardImg


def resize_blindfold_chess(cusp_app, event):
    logger.info("resize_blindfold_chess")
    blindfold_chess_frame_height = cusp_app.blindfold_chess_frame.winfo_height()
    blindfold_chess_frame_width = cusp_app.blindfold_chess_frame.winfo_width()

    cusp_app.blindfold_canvas_size = blindfold_chess_frame_height * 40 / 100

    cusp_app.blindfold_canvas_size = int( cusp_app.blindfold_canvas_size / 8) * 8
    cusp_app.blindfold_board_canvas.config( width=cusp_app.blindfold_canvas_size, height=cusp_app.blindfold_canvas_size)

    create_blindfold_chess_board(cusp_app)
    cusp_app.update()

    utils.config.save_setting_in_config_file(cusp_app)


def blindfold_left_click(cusp_app, event):
    logger.info("blindfold_left_click")
    if cusp_app.game_in_progress and ( ( cusp_app.chess_game_variant_mode == "Normal" and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.chess_game_variant_mode == "CuspChess" and ( ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "Human" and not cusp_app.board.turn) or (cusp_app.player_two == "Human" and cusp_app.board.turn) ) ) ) ) ):
        if utils.game_results.check_game_result(cusp_app):
            return
        if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
            return

        ui.ui_utils.clear_board_move_history(cusp_app)
        cusp_app.setting_up_in_cusp_chess = False

        mouse_x, mouse_y = event.x, event.y
        canvas_x = mouse_x // (cusp_app.blindfold_canvas_size / 8)
        canvas_y = mouse_y // (cusp_app.blindfold_canvas_size / 8)
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
        cusp_app.selected_piece = piece
        if piece:
            cusp_app.piece_move_start_square = chessboard_index
            cusp_app.mouse_drag = True

            cusp_app.board_canvas.delete("highlight")
            legal_moves = ui.ui_utils.legal_moves_at( cusp_app, cusp_app.board, chessboard_index)
            SQUARE_SIZE = int(cusp_app.canvas_size / 8)
            RANKS = 8
            # print(legal_moves)
            ui.ui_utils.draw_all_legal_moves_for_selected_piece( cusp_app, legal_moves, SQUARE_SIZE, RANKS, "Blindfold" )


def blindfold_left_button_release(cusp_app, event):
    logger.info("blindfold_left_button_release")
    cusp_app.board_canvas.delete("drag_piece")
    cusp_app.board_canvas.delete("highlight")
    if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
        return

    if not cusp_app.mouse_drag:
        return
    cusp_app.mouse_drag = False
    ui.ui_utils.clear_board_move_history(cusp_app)
    mouse_x, mouse_y = event.x, event.y
    if ( mouse_x >= cusp_app.blindfold_canvas_size or mouse_x < 0 or mouse_y >= cusp_app.blindfold_canvas_size or mouse_y < 0 ):
        return
    canvas_x = mouse_x // (cusp_app.blindfold_canvas_size / 8)
    canvas_y = mouse_y // (cusp_app.blindfold_canvas_size / 8)
    canvas_x = int(canvas_x)
    canvas_y = int(canvas_y)

    if not cusp_app.flip_board_enable:
        chessboard_x = canvas_x
        chessboard_y = 7 - canvas_y
    else:
        chessboard_x = 7 - canvas_x
        chessboard_y = canvas_y
    chessboard_index = chessboard_x + chessboard_y * 8

    move = chess.Move( from_square=cusp_app.piece_move_start_square, to_square=chessboard_index)
    if move in cusp_app.board.legal_moves:
        cusp_app.move_str_legal = True
    else:
        cusp_app.move_str_legal = False
    # standard chess move
    if ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "Fight" ) or cusp_app.chess_game_variant_mode == "Normal":
        if cusp_app.move_str_legal:
            cusp_app.move_str = str(cusp_app.board.san(move))
            cusp_app.setting_up_in_cusp_chess = False
            utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)
            # save before push move
            cusp_app.board.push(move)
            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, chessboard_index )
            utils.game_results.check_game_result(cusp_app)

        elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" or str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" ):
            moveq = str(move) + "q"
            if chess.Move.from_uci(moveq):
                moveq = chess.Move.from_uci(moveq)
                if moveq in cusp_app.board.legal_moves:
                    # islegal = True
                    logger.info("-------choose pawn promotion option --------------")
                    promotion_result = ui.ui_utils.pawn_promotion(
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
                    utils.pgnhistory.save_PGN_and_output_move_history( cusp_app, True)
                    # save befor push move
                    cusp_app.board.push(move)
                    ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)
                    ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, chessboard_index)
                    utils.game_results.check_game_result(cusp_app)

                else:
                    cusp_app.blindfold_label_state='The_move_is_illegal'
                    ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
            else:
                cusp_app.blindfold_label_state='The_move_is_illegal'
                ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)

        else:
            # output 'The move is illegal'
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)

        cusp_app.update()

    # Cusp Chess and cusp_app.cusp_chess_phase=="SafeMove", legal setup move

    elif ( cusp_app.chess_game_variant_mode == "CuspChess" and cusp_app.cusp_chess_phase == "SafeMove" ):
        # legal move except promotion
        if cusp_app.move_str_legal:
            cusp_app.Human_must_set_up = False
            cusp_app.move_str = str(cusp_app.board.san(move))
            cusp_app.board.push(move)
            cusp_app.board.turn = 1 ^ cusp_app.board.turn
            cusp_app.human_no_move_this_round = False
            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, chessboard_index )

            utils.game_results.check_game_result(cusp_app)

        elif ( str(cusp_app.board.piece_at(chessboard_index)) != "k" and str(cusp_app.board.piece_at(chessboard_index)) != "K" ):
            # pawn promotion
            if cusp_app.piece_move_start_square != chessboard_index:
                if ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" and chessboard_index < 8 ) or ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" and chessboard_index > 55 ):
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
                        ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, chessboard_index)

                    else:
                        # output 'The move is illegal'
                        cusp_app.blindfold_label_state='The_move_is_illegal'
                        ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
                        # utils.game_results.check_game_result(cusp_app)
                # move a pawn to back rank is not allowed
                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" and chessboard_index > 55 ) or ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" and chessboard_index < 8 ):
                    # output 'The move is illegal'
                    cusp_app.blindfold_label_state='The_move_is_illegal'
                    ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
                    # return
                # setup-rule, but both king are not allowed to checked at
                # the same time
                elif not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, chessboard_index ):
                    # setup-rule, must setup
                    logger.info("Human_must_set_up=True")
                    cusp_app.Human_must_set_up = True
                    cusp_app.human_no_move_this_round = False
                    cusp_app.move_str = str(move)

                    piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square)
                    cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square)
                    cusp_app.board.set_piece_at(chessboard_index, piece)
                    ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)
                    ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, chessboard_index)

                else:
                    cusp_app.blindfold_label_state='The_move_is_illegal'
                    ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
        else:
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)

    cusp_app.piece_move_start_square = -1
    # in Safe Move and Decision Phase, human players need to click move-finished button
    # AvH: first player: AI, second player: Human player
    if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
        if cusp_app.chess_game_variant_mode == "Normal":
            if (cusp_app.player_one == "AI" and cusp_app.board.turn) or ( cusp_app.player_two == "AI" and not cusp_app.board.turn ):
                cusp_app.AI_searching_best_move()
        elif cusp_app.chess_game_variant_mode == "CuspChess":
            if cusp_app.cusp_chess_phase == "Fight":
                if ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "AI" and cusp_app.board.turn) or ( cusp_app.player_two == "AI" and not cusp_app.board.turn))) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "AI" and not cusp_app.board.turn) or ( cusp_app.player_two == "AI" and cusp_app.board.turn))):
                    cusp_app.AI_searching_best_move()