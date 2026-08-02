"""

the notation for Cusp Setup has two lines at most. If a player chooses a color directly, it has only one line.

All moves are recorded using standard Algebraic Notation (SAN), except in Decision Phase.
All notations in Decision Phase start with “CC”, which means “Cusp Chess”. There are four different notations:
    •Move a piece. For example, in the notation “CC {WS b8d5 BWBN} {0.98}”, 
     “WS b8d5” means tentative white(W) player set(S) up a fight starting position 
     by moving a piece from b8 to d5. “BW” means the black color must win. 
     “BN” means the black color moves next. 
     {0.98} is the score of the current position.
     
    •Remove a piece. For example, in the notation “CC {BS d2xx BWWN} {1.08}”, 
    “BS d2xx” means tentative black(B) player set(S) up a fight starting position 
    by removing a piece at d2 from the chess board. 
    “BW” means the black color must win, 
    and “WN” means the white color moves next.
    
    •Choose a color when the opponent set up a fight starting positions. 
    For example, in the notation “CC {BCBW} {1.11}”, 
    After tentative white player set up a fight starting position, 
    “BCB” means tentative black player chose black color. 
    “BW” means the black color must win. 
    In this example, that the black color must win was set by the tentative white player
    
    •Choose a color directly.  
    For example, in the notation “CC {WC none BWWN} {1.20}”, 
    “WC” means tentative white player chose a color directly. 
    "none" means, the player can't make a move when choosing a color directly. 
    “BW” means the black color must win. 
    Here we know the tentative white player can only choose black color. 
    His/her opponent will play the white color. 
    “WN” means the white color moves next. 

The notation is redundant on purpose. It is clear and intuitive.

"""

import datetime
import logging
import pathlib
import time
from tkinter import *
from tkinter import filedialog, messagebox

import chess
import chess.pgn
from PIL import Image as PILImage

import ui.setting_panel
import ui.ui_utils
import utils.game_results
import utils.tournament

logger = logging.getLogger(__name__)

def save_PGN_and_output_move_history(cusp_app, active=False):
    logger.info("save_PGN_and_output_move_history")
    # this is special notation in Cusp Chess, CC prefix
    if cusp_app.setting_up_in_cusp_chess:
        cusp_app.pgn_one_player_one_line = False
        # a game in Decision Phase.
        if active:
            # it is OK to get into Decision Phase without moving any piece
            if cusp_app.move_str == "":
                move_str = "none"
            else:
                move_str = str( cusp_app.move_str)
            # if a player believes a Color can win now
            if cusp_app.choose_color_directly:
                choose_action = "C"
            # set up a fight starting position
            else:
                choose_action = "S"
            # the first move in Fight Phase. It can be set when setting up a fight starting position
            if cusp_app.color_to_move_in_fight_phase == "W":
                color_to_move = "W"
            elif cusp_app.color_to_move_in_fight_phase == "B":
                color_to_move = "B"
            # a complete example "CC {WS e2e4 WWBN}", white setup, e2e4, 
            # white must win, black is the next to move
            action_str = ( "CC {" + cusp_app.active_color_in_cusp_setup + choose_action + " " + move_str + " " + cusp_app.color_must_win_in_cusp_chess + "W" + color_to_move + "N" + "}" )
        # after one player set up a fight starting position, 
        # the other player choose acolor to play
        else:
            if cusp_app.active_color_in_cusp_setup == "W":
                passive_side_in_cusp_setup = "B"
            elif cusp_app.active_color_in_cusp_setup == "B":
                passive_side_in_cusp_setup = "W"
            # whether the color is a must-win color, or a draw-means-win color
            if cusp_app.color_chosen_in_setup_phase == "W":
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    # white win
                    color_and_result = "WW"
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    # white draw
                    color_and_result = "WD"
            elif cusp_app.color_chosen_in_setup_phase == "B":
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    color_and_result = "BD"
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    color_and_result = "BW"
            # for example, CC {WCBD}  white choose black color, 
            # and draw meanswin for black
            action_str = ( "CC {" + passive_side_in_cusp_setup + "C" + color_and_result + "}")
    # safe move phase, or fight phase, just like standard chess
    else:
        if cusp_app.move_str == "":
            action_str = "none"
        else:
            action_str = str(cusp_app.move_str)

    if cusp_app.blindfold_mode:
        cusp_app.blindfold_move_notice_label["text"] = str(action_str)

    # If a engine is playing, we add the score part
    if cusp_app.move_score_set:
        if cusp_app.eval_show_enable:
            action_str = action_str + " {" + str(cusp_app.move_score) + "}"
    # Check early stop        
    if utils.game_results.check_early_stop_results(cusp_app):
        utils.game_results.check_game_early_stop(cusp_app)
        return
        
    if cusp_app.game_in_progress:    
        write_to_scrolledtext(cusp_app, action_str)

        # output PGN
        # create PGN folder
        pathlib.Path("PGN/").mkdir(parents=True, exist_ok=True)
        if cusp_app.output_PGN_enable:
            # add header to PGN
            if not cusp_app.PGN_header:
                game = chess.pgn.Game()
                game.headers["Event"] = "Example"
                game.headers["Date"] = str( datetime.date.today().strftime("%Y-%m-%d"))

                game.headers["White"] = cusp_app.player_one_name

                game.headers["Black"] = cusp_app.player_two_name
                print(game, file=open(cusp_app.PGN_save_path, "w"), end="\n")

                with open(cusp_app.PGN_save_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                with open(cusp_app.PGN_save_path, "w", encoding="utf-8") as f:
                    f.writelines(lines[:-3])   

                    if cusp_app.adjudicator_engine_enable:
                        if set_adjudicator_engine_name(cusp_app):
                            f.writelines('[Adjudicator Engine "{}"]'.format(str(cusp_app.adjudicator_engine_name)))
                    f.writelines("\n")
                    if cusp_app.chess_game_variant_mode == "CuspChess":
                        f.writelines('[Variant "Cusp Chess"]')
                    f.writelines("\n")

        write_to_PGN(cusp_app, action_str)

        # if there is a new move, then it will be reset.
        cusp_app.move_str = ""
        # if there is a new engine move, then it will be reset.
        cusp_app.move_score_set = False

def set_adjudicator_engine_name(cusp_app):
    logger.info("set_adjudicator_engine_name")
    if cusp_app.adjudicator_name_input == '':
        if cusp_app.engine_adjudicator_path:
            if "/" in cusp_app.engine_adjudicator_path:
                engine_adjudicator_path = cusp_app.engine_adjudicator_path.split("/")[-1]   
            if len(engine_adjudicator_path) > 30:
                engine_adjudicator_path = engine_adjudicator_path[:30]
            if  " " in engine_adjudicator_path: 
                engine_adjudicator_path = engine_adjudicator_path.split(" ")[0]
            if  "-" in engine_adjudicator_path: 
                engine_adjudicator_path = engine_adjudicator_path.split("-")[0]  
            cusp_app.adjudicator_engine_name=engine_adjudicator_path
    else:
        cusp_app.adjudicator_engine_name = cusp_app.adjudicator_name_input
    if cusp_app.adjudicator_engine_name:    
        return True
    
def write_to_scrolledtext(cusp_app, action_str):
    logger.info("write_to_scrolledtext")
    if cusp_app.board.turn:
        cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
        # file is not empty
        if len(cusp_app.move_history_text.get("1.0", END)) > 1:
            cusp_app.move_history_text.insert(
                END, "\n" + str(cusp_app.move_history_text_number) + ". " + action_str
            )
        else:
            cusp_app.move_history_text.insert( END, str(cusp_app.move_history_text_number) + ". " + action_str )
    elif action_str[0:2] == "CC":
        cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
        cusp_app.move_history_text.insert(
            END, "\n" + str(cusp_app.move_history_text_number) + ". " + action_str
        )
    else:
        # black moves first in fight phase
        # or set up a board in board editor and black to move
        last_line = cusp_app.move_history_text.get( "end-1c linestart", "end-1c lineend")
        if ("CC" in last_line) or len( cusp_app.move_history_text.get("1.0", END)) <= 1:
            cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
            cusp_app.move_history_text.insert(
                END,
                "\n" + str(cusp_app.move_history_text_number) + ". ... " + action_str,
            )
        else:
            cusp_app.move_history_text.insert(END, "  " + action_str)
    cusp_app.move_history_text.see("end")


def write_to_PGN(cusp_app, action_str):
    logger.info("write_to_PGN") 
    with open(cusp_app.PGN_save_path, "a", encoding="utf-8") as write_PGN:
        if cusp_app.board.turn:
            print("\n" + str(cusp_app.move_history_text_number) +
                  ". " + action_str, file=write_PGN, end=" ", )

        elif action_str[0:2] == "CC":
            print("\n" + str(cusp_app.move_history_text_number) +
                  ". " + action_str, file=write_PGN, end=" ", )
        else:
            last_line = ""
            with open(cusp_app.PGN_save_path, "r") as file:
                lines = [line.rstrip() for line in file]
                for line in lines:
                    last_line = line
            if ("CC" in last_line) or cusp_app.PGN_header == False:
                print(
                    "\n"
                    + str(cusp_app.move_history_text_number)
                    + ". ... "
                    + action_str,
                    file=write_PGN,
                    end=" ",
                )
            else:
                print(" " + action_str, file=write_PGN, end=" ")
    cusp_app.PGN_header = True

# check game variant automatically based on pgn.
def check_pgn_game_variant(cusp_app):
    logger.info("check_pgn_game_variant")
    if cusp_app.reload_PGN:
        return
    if not cusp_app.PGN_file_path:
        return
    if not cusp_app.pgn_auto_game_variant_detection: return
    cusp_app.chess_game_variant_mode_value.set(1)    
    with open(cusp_app.PGN_file_path) as file:
        lines = [line.rstrip() for line in file]
        for line in lines:        
            if 'Cusp Chess' in line:
                cusp_app.chess_game_variant_mode_value.set(2)
                break
    ui.setting_panel.chess_game_variant_mode_change(cusp_app) 
        
# the GUI can only read the pgn format created by itself.        
def load_PGN(cusp_app):
    logger.info("load_PGN")
    if cusp_app.reload_PGN:
        cusp_app.reset()
        cusp_app.reload_PGN = True
    else:
        cusp_app.reset()
        
    if not cusp_app.reload_PGN:
        cusp_app.PGN_file_path = filedialog.askopenfilename( filetypes=[("PGN files", "*.PGN"), ("All files", "*.*")] )
    if not cusp_app.PGN_file_path:
        return
    check_pgn_game_variant(cusp_app)

    cusp_app.pgn_movestack = []
    cusp_app.pgn_fen_history_stack = []
    cusp_app.pgn_move_history_stack = []

    cusp_app.game_player_mode = "HvH"
    
    try:
        with open(cusp_app.PGN_file_path,"r", encoding="utf-8") as file:
            lines = [line.rstrip() for line in file]
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.exception("PGN file read error")
        messagebox.showerror("PGN Error", f"Could not open file: {e}")
        return None
        
    try:    
        check_pgn(cusp_app,lines )    
    except ValueError as e:   # bad syntax, wrong format
        logger.exception("PGN parse error")
        messagebox.showerror("PGN Error", f"Invalid PGN format: {e}")
        return None
    except Exception as e:    # fallback catch-all
        logger.exception("Unexpected PGN parse error")
        messagebox.showerror("PGN Error", f"Unexpected error: {e}")
        return None

    # reset board

    cusp_app.board = chess.Board()
    ui.ui_utils.update_color_to_move_label(cusp_app)
    # create two fake players
    cusp_app.engine_one = "cusp_app_engine1"
    cusp_app.engine_two = "cusp_app_engine2"
    cusp_app.player_swap_side = False
    # no timer when reading pgn.
    cusp_app.player_one_timer_label.config(text="       ")
    cusp_app.player_two_timer_label.config(text="       ")
    ui.ui_utils.initialize_piece_images( cusp_app, cusp_app.chess_game_variant_mode)

def check_pgn(cusp_app,lines ):    
    for line in lines:
        if "White" in line:
            player_one_string = line.split('"')[1]
            player_one_string = player_one_string.split('"')[0]
            if len(player_one_string) > 40:
                player_one_string = player_one_string[:40]
            cusp_app.player_one_name = player_one_string
        if "Black" in line:
            player_two_string = line.split('"')[1]
            player_two_string = player_two_string.split('"')[0]
            if len(player_two_string) > 40:
                player_two_string = player_two_string[:40]
            cusp_app.player_two_name = player_two_string

        if line[0:1].isdigit():
            # legal move and white moves first
            if "CC" not in line and "..." not in line and "result" not in line:
                split_line = line.split("  ")
                if len(split_line) == 2:
                    move_and_score = split_line[0].split(". ")[1]
                    move = move_and_score.split(" ")[0]

                    cusp_app.board.push_san(move)
                    cusp_app.pgn_movestack.append(move_and_score)

                    move_and_score = split_line[1]
                    move = move_and_score.split(" ")[0]

                    cusp_app.board.push_san(move)
                    cusp_app.pgn_movestack.append(move_and_score)

                else:
                    move_and_score = split_line[0].split(". ")[1]
                    move = move_and_score.split(" ")[0]

                    cusp_app.board.push_san(move)
                    cusp_app.pgn_movestack.append(move_and_score)
            # only black move
            elif "..." in line:
                split_line = line.split(".. ")
                if len(split_line) == 2:
                    move_and_score = split_line[1]
                    move = move_and_score.split(" ")[0]
                    cusp_app.board.push_san(move)
                    cusp_app.pgn_movestack.append(move_and_score)
            # Decision Phase, set up a fight starting position or choose a color directly,
            # without score, minimum length
            elif "CC" in line and len(line.split("}")[0].split("{")[1]) > 8:
                move_and_score = line.split(". ")[1]
                move_and_score_split = move_and_score.split(" ")

                move_part = move_and_score_split[2]

                # no move
                if move_part == "none" or ( len(move_part) == 4 and move_part[0:2] == move_part[2:] ):
                    pass
                # a piece removed
                elif len(move_part) == 4 and move_part[2:] == "xx":
                    chessboard_index = chess.parse_square( move_part[0:2])
                    cusp_app.board.remove_piece_at(chessboard_index)
                # free move
                else:
                    
                    if is_legal_san(cusp_app.board, move_part):
                        cusp_app.board.push_san(move_part)
                    elif is_legal_uci(cusp_app.board, move_part): 
                        cusp_app.board.push(move_part)
                    else:    
                        logger.exception("Cusp chess PGN, check PGN, one free move, push error")
                        move_start_index = chess.parse_square( move_part[0:2])
                        move_end_index = chess.parse_square( move_part[2:4])

                        piece = cusp_app.board.piece_at( move_start_index)
                        cusp_app.board.remove_piece_at( move_start_index)

                        if len(move_part) == 4:
                            cusp_app.board.set_piece_at( move_end_index, piece)

                        elif len(move_part) > 4:
                            # pawn promotion
                            if str(piece) == "p":
                                if move_part[4] == "q":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("q"), )
                                elif move_part[4] == "r":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("r"), )
                                elif move_part[4] == "n":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("n"), )
                                elif move_part[4] == "b":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("b"), )
                            elif str(piece) == "P":
                                if move_part[4] == "q":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("Q"), )
                                elif move_part[4] == "r":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("R"), )
                                elif move_part[4] == "n":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("N"), )
                                elif move_part[4] == "b":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("B"), )
                # when setting up a fight starting position, a player can set
                # board's turn
                if move_and_score_split[3][2] == "W":
                    cusp_app.board.turn = True
                elif move_and_score_split[3][2] == "B":
                    cusp_app.board.turn = False
                cusp_app.pgn_movestack.append(move_and_score)
            else:
                # the other player chooses a color
                move_and_score = line.split(". ")[1]
                cusp_app.pgn_movestack.append(move_and_score)

def is_legal_uci(board, move_str):
    try:
        move = chess.Move.from_uci(move_str)   # only validates format
    except ValueError:
        return False

    return move in board.legal_moves

def is_legal_san(board, move_str):
    try:
        board.parse_san(move_str)   # fails if illegal or invalid
        return True
    except ValueError:
        return False    

def play_PGN_next(cusp_app):
    logger.info("play_PGN_next")
    cusp_app.arrow_start_index = ""
    cusp_app.arrow_end_index = ""
    ui.ui_utils.clear_board_move_history(cusp_app)
    CC_passive = False
    cusp_app.game_in_progress = True
    if cusp_app.pgn_movestack:
        move_and_score = cusp_app.pgn_movestack.pop(0)
        cusp_app.pgn_fen_history_stack.append(cusp_app.board.fen())
        cusp_app.pgn_move_history_stack.append(move_and_score)
        try:
            if cusp_app.board.turn:
                cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                # file is not empty
                if len(cusp_app.move_history_text.get("1.0", END)) > 1:
                    cusp_app.move_history_text.insert(
                        END,
                        "\n"
                        + str(cusp_app.move_history_text_number)
                        + ". "
                        + move_and_score,
                    )
                else:
                    cusp_app.move_history_text.insert( END, str(cusp_app.move_history_text_number) + ". " + move_and_score, )

            elif "CC" in move_and_score or 'result' in move_and_score :
                cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                cusp_app.move_history_text.insert(
                    END,
                    "\n"
                    + str(cusp_app.move_history_text_number)
                    + ". "
                    + move_and_score,
                )
            else:
                # black moves first in fight phase
                # or set up a board in board editor and black to move
                last_line = cusp_app.move_history_text.get( "end-1c linestart", "end-1c lineend" )
                if ( "CC" in last_line or len(cusp_app.move_history_text.get("1.0", END)) <= 1 ):
                    cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                    cusp_app.move_history_text.insert(
                        END,
                        "\n"
                        + str(cusp_app.move_history_text_number)
                        + ". ... "
                        + move_and_score,
                    )
                else:
                    cusp_app.move_history_text.insert( END, "  " + move_and_score)
            cusp_app.move_history_text.see("end")

            # print(move_and_score)
            if "CC" not in move_and_score and "result" not in move_and_score:
                move_and_score_split = move_and_score.split(" ")
                move = move_and_score_split[0]

                # update eval bar
                if len( move_and_score_split) > 1 and move_and_score_split[1] != "":
                    score = float(move_and_score_split[1][1:-1])

                    if cusp_app.board.turn:
                        if not cusp_app.player_swap_side:
                            cusp_app.engine = cusp_app.engine_one
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, score)
                        else:
                            cusp_app.engine = cusp_app.engine_two
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                    else:
                        if cusp_app.player_swap_side:
                            cusp_app.engine = cusp_app.engine_one
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                        else:
                            cusp_app.engine = cusp_app.engine_two
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, score)

                uci_move = cusp_app.board.push_san(move).uci()
                uci_move = str(uci_move)

                move_start_index = chess.parse_square(uci_move[0:2])
                move_end_index = chess.parse_square(uci_move[2:4])

                cusp_app.arrow_start_index = move_start_index
                cusp_app.arrow_end_index = move_end_index

            elif ( "CC" in move_and_score and len(move_and_score.split("}")[0].split("{")[1]) > 8 ):
                cusp_app.cusp_chess_phase = "Decision"
                move_and_score_split = move_and_score.split(" ")

                move_part = move_and_score_split[2]

                # CC {WS c7f4 WWWN} {0.98} or CC {WC none WWWN} {0.2}
                # if a player choose a color directly, he/she can only choose
                # the color-must-win
                if ( move_and_score_split[1][2] == "C" and move_and_score_split[1][1] != move_and_score_split[3][0] ):
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
                if move_and_score_split[3][0] == "W":
                    cusp_app.color_must_win_in_cusp_chess = "W"
                elif move_and_score_split[3][0] == "B":
                    cusp_app.color_must_win_in_cusp_chess = "B"

                # active color means the color set up a fight starting position or chose
                # a color directly
                if move_and_score_split[1][1] == "W":
                    cusp_app.engine = cusp_app.engine_one
                    cusp_app.active_color_in_cusp_setup = "W"
                elif move_and_score_split[1][1] == "B":
                    cusp_app.engine = cusp_app.engine_two
                    cusp_app.active_color_in_cusp_setup = "B"
                # update eval bar
                if move_and_score.count("}") == 2:
                    # print(move_and_score_split[4][1:-1])

                    score = float(move_and_score_split[4][1:-1])
                    # choose a color directly
                    if move_and_score_split[1][2] == "C":
                        cusp_app.cusp_chess_phase = "Fight"
                        cusp_app.choose_color_directly = True

                        if move_and_score_split[1][1] == "W":
                            cusp_app.active_color_in_cusp_setup = "W"
                            cusp_app.player_one_value_on_the_cusp = score
                            cusp_app.player_one_score_on_the_cusp_set = True
                        elif move_and_score_split[1][1] == "B":
                            cusp_app.active_color_in_cusp_setup = "B"
                            cusp_app.player_two_value_on_the_cusp = score
                            cusp_app.player_two_score_on_the_cusp_set = True
                        ui.ui_utils.update_two_player_scores_bar( cusp_app, score)
                    # set up a fight starting position
                    elif move_and_score_split[1][2] == "S":
                        cusp_app.cusp_chess_phase = "Decision"
                        # player one set up a fight starting position
                        if move_and_score_split[1][1] == "W":
                            # white to move
                            if move_and_score_split[3][2] == "W":
                                cusp_app.player_one_value_on_the_cusp = score
                                cusp_app.player_one_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar( cusp_app, score)
                            # black to move
                            elif move_and_score_split[3][2] == "B":
                                cusp_app.player_one_value_on_the_cusp = -score
                                cusp_app.player_one_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                        # player two set up a fight starting position
                        elif move_and_score_split[1][1] == "B":
                            if move_and_score_split[3][2] == "W":
                                cusp_app.player_two_value_on_the_cusp = -score
                                cusp_app.player_two_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                            elif move_and_score_split[3][2] == "B":
                                cusp_app.player_two_value_on_the_cusp = score
                                cusp_app.player_two_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar( cusp_app, score)

                # no move, move_part[0:2]==move_part[2:] is possible, when
                # engine searchs a fight starting position
                if move_part == "none" or move_part[0:2] == move_part[2:]:
                    cusp_app.arrow_start_index = -1
                    cusp_app.arrow_end_index = -1
                # remove one piece to set up a fight starting position
                elif len(move_part) == 4 and move_part[2:] == "xx":
                    chessboard_index = chess.parse_square(move_part[0:2])
                    cusp_app.board.remove_piece_at(chessboard_index)

                    cusp_app.arrow_start_index = chessboard_index
                    cusp_app.arrow_end_index = -1

                else:
                    
                    # if it is a legal move
                    if is_legal_san(cusp_app.board, move_part):
                        uci_move = cusp_app.board.push_san(move_part).uci()
                        move_start_index = chess.parse_square(uci_move[0:2])
                        move_end_index = chess.parse_square(uci_move[2:4])
                        
                    elif is_legal_uci(cusp_app.board, move_part): 
                        cusp_app.board.push(move_part)
                        move_start_index = chess.parse_square(move_part[0:2])
                        move_end_index = chess.parse_square(move_part[2:4])                        
                    else:    
                        # one free move
                        logger.exception("Cusp chess PGN, one free move, push error")
                        
                        move_start_index = chess.parse_square(move_part[0:2])
                        move_end_index = chess.parse_square(move_part[2:4])
                        piece = cusp_app.board.piece_at(move_start_index)
                        cusp_app.board.remove_piece_at(move_start_index)

                        if len(move_part) == 4:
                            cusp_app.board.set_piece_at(move_end_index, piece)
                        # pawn free promotion
                        elif len(move_part) > 4:
                            if str(piece) == "p":
                                if move_part[4] == "q":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("q"))
                                elif move_part[4] == "r":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("r"))
                                elif move_part[4] == "n":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("n"))
                                elif move_part[4] == "b":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("b"))
                            elif str(piece) == "P":
                                if move_part[4] == "q":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("Q"))
                                elif move_part[4] == "r":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("R"))
                                elif move_part[4] == "n":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("N"))
                                elif move_part[4] == "b":
                                    cusp_app.board.set_piece_at( move_end_index, chess.Piece.from_symbol("B"))

                    cusp_app.arrow_start_index = move_start_index
                    cusp_app.arrow_end_index = move_end_index

                if move_and_score_split[3][2] == "W":
                    cusp_app.board.turn = True
                elif move_and_score_split[3][2] == "B":
                    cusp_app.board.turn = False
                cusp_app.update()

            # CC, the other player chose a color
            elif "CC" in move_and_score:
                cusp_app.cusp_chess_phase = "Fight"
                move_and_score_split = move_and_score.split(" ")
                if move_and_score[6] == "W":
                    cusp_app.color_chosen_in_setup_phase = "W"
                elif move_and_score[6] == "B":
                    cusp_app.color_chosen_in_setup_phase = "B"
                if move_and_score[4] != move_and_score[6]:
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
                if ( len(move_and_score.split("}")) > 1 and move_and_score.split("}")[1] != "" ):
                    score = float(move_and_score_split[2][1:-1])

                    if cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.engine = cusp_app.engine_two
                    elif cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.engine = cusp_app.engine_one

                    if cusp_app.board.turn:
                        if cusp_app.engine == cusp_app.engine_one:
                            cusp_app.player_one_value_on_the_cusp = score
                            cusp_app.player_one_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, score)
                        else:
                            cusp_app.player_two_value_on_the_cusp = -score
                            cusp_app.player_two_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                    else:
                        if cusp_app.engine == cusp_app.engine_two:
                            cusp_app.player_two_value_on_the_cusp = score
                            cusp_app.player_two_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, score)
                        else:
                            cusp_app.player_one_value_on_the_cusp = -score
                            cusp_app.player_one_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar( cusp_app, -score)
                CC_passive = True
            # game result
            elif "result" in move_and_score:
                cusp_app.game_in_progress = False
                if ( "adjudicator" not in move_and_score and "time out" not in move_and_score ):
                    PGN_result = move_and_score.split(" ")[1][1:-1]
                    cusp_app.game_result = PGN_result
                else:
                    PGN_result = move_and_score.split(" ")[3][0:-1]
                    cusp_app.game_result = PGN_result
                utils.game_results.show_game_result(cusp_app)
                return                   
        except ValueError as e:   # bad syntax, wrong format
            logger.exception("PGN parse error")
            messagebox.showerror("CC PGN Error", f"Invalid PGN format: {e}")
            return None
        except Exception as e:    # fallback catch-all
            logger.exception("Unexpected PGN parse error")
            messagebox.showerror("CC PGN Error", f"Unexpected error: {e}")
            return None
        
        if CC_passive:
            cusp_app.after( 100, lambda: ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.old_arrow_start_index, cusp_app.old_arrow_end_index, ), )

        else:
            piece = cusp_app.board.piece_at(cusp_app.arrow_end_index)
            ui.ui_utils.animate_piece_move( cusp_app, piece, cusp_app.arrow_start_index, cusp_app.arrow_end_index, )

            cusp_app.old_arrow_start_index = cusp_app.arrow_start_index
            cusp_app.old_arrow_end_index = cusp_app.arrow_end_index
        ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)

        cusp_app.update()

def play_PGN_previous(cusp_app):
    logger.info("play_PGN_previous")
    if cusp_app.pgn_move_history_stack:
        move_and_score = cusp_app.pgn_move_history_stack.pop()
        cusp_app.pgn_movestack.insert(0, move_and_score)
        board_fen = cusp_app.pgn_fen_history_stack.pop()
        cusp_app.board.set_fen(board_fen)
    cusp_app.move_history_text.delete("end-1l linestart", "end")
    ui.ui_utils.clear_board_move_history(cusp_app)
    ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)


# just reload
def PGN_back_to_beginning(cusp_app):
    logger.info("PGN_back_to_beginning")
    try:
        cusp_app.reload_PGN = True
        load_PGN(cusp_app)
        cusp_app.reload_PGN = False
    except Exception as e:
        cusp_app.reload_PGN = False
        logger.exception("PGN_back_to_beginning error")
        messagebox.showerror("Error", f"Reload PGN error: {e}" )


def initialize_auto_play_PGN_button_text(cusp_app):
    logger.info("initialize_auto_play_PGN_button_text")
    if not cusp_app.auto_play_PGN:
        cusp_app.pgn_auto_play_label_state='stop_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)
    else:
        cusp_app.pgn_auto_play_label_state='auto_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)

def auto_play_PGN_function(cusp_app):
    logger.info("auto_play_PGN_function")
    if cusp_app.auto_play_PGN:
        cusp_app.auto_play_PGN = False
        cusp_app.pgn_auto_play_label_state='stop_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)
        play_PGN(cusp_app)
    else:
        cusp_app.auto_play_PGN = True
        cusp_app.pgn_auto_play_label_state='auto_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)
       


def play_PGN(cusp_app):
    logger.info("play_PGN")
    if not cusp_app.auto_play_PGN:
        if cusp_app.pgn_movestack:
            play_PGN_next(cusp_app)
            cusp_app.after(1500, lambda: play_PGN(cusp_app))
        else:
            cusp_app.auto_play_PGN = True
            initialize_auto_play_PGN_button_text(cusp_app)