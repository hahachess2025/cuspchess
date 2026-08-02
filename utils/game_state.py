import logging
import time
from tkinter import *

import chess
import pygame

logger = logging.getLogger(__name__)

def initalize_basic_setting(cusp_app):
    logger.info("initalize_basic_setting")
    # UI board
    # default language: English
    cusp_app.current_lang = "en"
    cusp_app.board = chess.Board()

    # chess board canvas
    cusp_app.canvas_size = 744
    cusp_app.editor_canvas_size = 680
    cusp_app.blindfold_canvas_size = 352
    # for playing blindfold chess

    cusp_app.img = {}
    for i in range(80):
        cusp_app.img[i] = None
    cusp_app.editor_img = {}        
    for i in range(80):
        cusp_app.editor_img[i] = None
    cusp_app.piece_images = {}         
    cusp_app.play_one_logo = PhotoImage(file="assets/PlayerOne.gif")
    cusp_app.play_one_logo = cusp_app.play_one_logo.subsample(5, 5)

    cusp_app.play_two_logo = PhotoImage(file="assets/PlayTwo.gif")
    cusp_app.play_two_logo = cusp_app.play_two_logo.subsample(5, 5)

    # draw move arrows on board
    cusp_app.transparent_arrows = {}    
    for i in range(2):
        cusp_app.transparent_arrows[i] = None
        
    cusp_app.arrow_img = {}
    cusp_app.arrow_img[0] = None
    cusp_app.arrow_img[1] = None

    # draw a rectangle when a piece removed
    cusp_app.board_remove_piece_rectangle = None
    # blindfold chess
    cusp_app.blindfold_mode = False
    cusp_app.blindfold_arrow = None
    cusp_app.blindfold_board_remove_piece_rectangle = None

    # dragging to move a piece
    cusp_app.mouse_drag = False
    cusp_app.piece_move_start_square = -1
    # If a human player make a move, he/she can't choose a color directly this round.
    cusp_app.human_no_move_this_round = True

    # UI setting
    cusp_app.player_one_name = "Player One"
    cusp_app.player_two_name = "Player Two"
    cusp_app.player_one_name_engine = "AI one"
    cusp_app.player_two_name_engine = "AI two"
    cusp_app.player_one = ""
    cusp_app.player_two = ""
    
    # When a human player sets up a fight starting position, color-must-win and color-to-move must be set.
    # Then his/her opponent will choose a color. The game enters 'Fight' phase.
    cusp_app.Human_setup_color_to_move = ""
    cusp_app.Human_setup_color_must_win = ""
    cusp_app.color_must_win_in_cusp_chess = ""
    cusp_app.color_recommended_for_opponent = ""
    # When a human player made a One Free Move (an illegal safe move, but a legal setup move), 
    # he/she must set up a fight starting position.
    # He/she can't move a piece now, but he/she can to set color-must-win and (color-to-move in engine-test mode).
    cusp_app.Human_must_set_up = False
    cusp_app.Human_setup = False

    # For updating widgets
    # see details in ui.language
    cusp_app.player_one_label_state = "player_one_board_label_default"
    cusp_app.player_two_label_state = "player_two_board_label_default"
    cusp_app.game_status_label_state = "game_status_label_ready"
    cusp_app.result_str = ''
    cusp_app.color_to_move_label_state=''
    cusp_app.editor_color_to_move_label_state=''
    cusp_app.game_status_label_player_name=''
    cusp_app.pgn_auto_play_label_state='auto_play_PGN_button'
    cusp_app.blindfold_label_state='empty'   
    
    # When changing a language, we need to update the spinboxes
    cusp_app.player_one_spinbox_chosen=0
    cusp_app.player_two_spinbox_chosen=0
    cusp_app.color_to_move_spinbox_chosen=0
    cusp_app.color_must_win_spinbox_chosen=0
                                
    # chess game
    cusp_app.game_in_progress = False
    # the first player vs the second player
    # Human players or Engine players
    # cusp_app.game_player_mode='AvA': AI vs AI
    # 'AvH': AI vs Human
    # 'HvA': Human vs AI
    # 'HvH': Human vs Human
    cusp_app.game_player_mode = ""    
            
    # cusp_app.chess_game_variant_mode='Normal'
    # 'Normal' means standard chess, "CuspChess" means Cusp Chess
    cusp_app.chess_game_variant_mode = "Normal"
    cusp_app.chess_game_variant_mode_saved = ""
    """    
    In Cusp Chess, there are three phases: Safe Move Phase, Decision Phase, and Fight Phase.
    In Safe Move phase, a human player must press a button to confirm his/her move is finished. So his opponent can play.
    Players just play standard chess move.
    For OTB games, players can just press timers.
    A player can choose a color directly in Safe Move phase, 
    In Decision Phase, a player can set up a fight starting position,  
    If a player made a one-free-move, he/she must set up a fight starting position.
    Then his/her opponent will choose a color. The game enters 'Fight' phase.
    'Fight': , Fight phase. Both players have their own colors now. For a color, draw means loss.
    """
    cusp_app.cusp_chess_phase = "SafeMove"    
    # For move notation in the Decision Phase: CC prefix notation. Choosing a color directly, 
    # is also a kind of setup for a fight starting position.
    cusp_app.setting_up_in_cusp_chess = False
    # move notation in Cusp Chess, or in standard chess
    cusp_app.move_str = ""
    # the tentative player who sets up a fight starting position: white or black.
    cusp_app.active_color_in_cusp_setup = ""
    # if a player choose a color directly, he/she must win with that color.
    # So, the color-must-win is the color he/she chose.
    cusp_app.choose_color_directly = False
    # Pie rule. After a player set up a fight starting position, the other player
    # chooses a color.
    cusp_app.color_chosen_in_setup_phase = ""
    # the color of pieces to make the first move in Fight phase
    cusp_app.color_to_move_in_fight_phase = ""    
    # When setting up a fight starting position, a player must calculate the score of the candidate position, 
    # so he/she can evaluate whether it is a good fight starting position.
    # The other player must calculate score too, so he/she can decide which color to choose.
    # The best fight starting position (cusp position) means a color's win rate in the position is around 50% 
    # based on a perfect chess engine, or based on the player's calculation.
    cusp_app.player_one_value_on_the_cusp = 0
    cusp_app.player_two_value_on_the_cusp = 0
    # True when a value is set. It is used to draw a mark on the eval bar.
    cusp_app.player_one_score_on_the_cusp_set = False
    cusp_app.player_two_score_on_the_cusp_set = False
    # when a player chooses a color directly, the score of his/her opponent's
    # previous move is critical when review the game. It could mean the opponent made a mistake.
    cusp_app.set_cusp_value = False
    cusp_app.previous_move_score = 0

    # When a player set a fight starting position, another player can choose any color
    # he/she wants, so it is possible for tentative players to swap sides.
    # Player_swap_side can be used to decide which AI player is playing
    cusp_app.player_swap_side = False
    # to draw pieces
    cusp_app.flip_board_enable = False
    # to set board image
    cusp_app.rotate_board = False
    
    # results
    cusp_app.game_result = "*"
    # An user can set a result on UI
    cusp_app.user_adjudicator_result = "*"
    # based on an ajdudicator engine or endgame table base.
    cusp_app.engine_adjudicator_result = "*"
    cusp_app.time_out_result = "*"

    # PGN
    cusp_app.pgn_auto_game_variant_detection= True    
    cusp_app.PGN_header = False
    cusp_app.auto_play_PGN = True
    cusp_app.reload_PGN = False
    cusp_app.pgn_movestack=None
    cusp_app.pgn_move_history_stack=None

    # threads for chess engine search
    cusp_app.engine_one = None
    cusp_app.engine_two = None
    
    cusp_app.search_for_best_move_thread = None
    cusp_app.safe_move_or_setup_thread = None
    cusp_app.update_editor_score_thread = None
    cusp_app.search_for_all_cusps_for_CC_thread = None

    # engine score    
    cusp_app.move_score = 0
    cusp_app.move_score_set = False

    # set timer
    cusp_app.player_one_timer_on = True
    # seconds
    cusp_app.time_for_each_player = 300
    cusp_app.player_one_start_time = 0
    cusp_app.player_two_start_time = 0


    # tournament
    cusp_app.tournament_game_number = 10
    cusp_app.tournament_game_number_started = 0
    cusp_app.player_one_tournament_score = 0
    cusp_app.player_two_tournament_score = 0
    cusp_app.tournament_start = False

    # Game early stop, for one game or tournament. It can save some time.
    # For details, check utils.game_results.check_early_stop_results
    cusp_app.game_early_stop = False
    cusp_app.game_early_stop_score_difference = 0.5
    # Check starts from the minimum move.
    # In Cusp Chess, check only starts in Fight phase
    cusp_app.game_early_stop_minimum_moves = 0

    # If a game is likely to end in a draw, we can stop the game early based on a few results.
    cusp_app.game_early_stop_draw_enable = False
    # If a color is likely to win a game, we can stop the game early based on a few results.
    cusp_app.game_early_stop_win_enable = False
    cusp_app.tournament_white_active_count = 0
    # On white's turn, and white's score is smaller than 1 - game_early_stop_score_difference, increase the count. 
    cusp_app.game_early_stop_white_count_minimum = 0
    # On white's turn, and white's score is bigger than 1 + game_early_stop_score_difference + engine_score_difference_maximum, increase the count
    cusp_app.game_early_stop_white_count_maximum_positive = 0
    # On white's turn, and white's score is bigger than -1 - game_early_stop_score_difference - engine_score_difference_maximum, increase the count
    cusp_app.game_early_stop_white_count_maximum_negative = 0

    cusp_app.game_early_stop_black_count_minimum = 0
    cusp_app.game_early_stop_black_count_maximum_positive = 0
    cusp_app.game_early_stop_black_count_maximum_negative = 0
    
    # a result of a early-stopped game
    cusp_app.early_stop_game_draw = False
    cusp_app.early_stop_game_win_white = False
    cusp_app.early_stop_game_win_black = False

    # adjudicator engine for early stop
    # note all games decided by adjudicator engines
    cusp_app.game_early_stop_count_adjudicator = []    
    cusp_app.adjudicator_engine_enable = False
    cusp_app.adjudicator_engine = None
    cusp_app.adjudicator_engine_last_time = time.time()
    cusp_app.endgame_tablebase_enable = False
    cusp_app.Syzygy_tablebases_path = '' 

    # A good fight starting position found
    cusp_app.cusp_position_fen = ""
    # for move history scrolltext
    cusp_app.move_history_text_number = 0

    # editor setting
    cusp_app.editor_engine = None
    cusp_app.editor_engine_analyse_enable = False
    cusp_app.editor_engine_exist = False
    cusp_app.editor_engine_evaluation_limit = 0.3
    cusp_app.editor_engine_multipv=0
    cusp_app.editor_auto_turn_rotation=False
    # the number of all good fight starting positions 
    cusp_app.searching_cusps_count = 0
    cusp_app.FEN_checked = []
    
    cusp_app.sound_path = "assets/sound/move.mp3"
    pygame.mixer.init()
    cusp_app.move_sound = pygame.mixer.Sound(cusp_app.sound_path)

    
def user_setting_initialization(cusp_app):
    logger.info("user_setting_initialization")
    # user can set some parameters at setting section
    cusp_app.engine_one_path = ""
    cusp_app.engine_two_path = ""
    cusp_app.editor_engine_path = ""
    cusp_app.engine_adjudicator_path = ""
    
    cusp_app.maximum_ply_before_setup = 11

    """    
    In stockfish engine, 1 and -1 are cusp scores.
    It is hard to find a FEN whoes score is exactly 1 or -1, so we need to relax the cusp restriction a little bit.
    Score difference = abs(abs(score)-1).     
    engine_score_difference_maximum  must be bigger than engine_score_difference_minimum
    score interval of a fight starting position
    (1 - cusp_app.engine_score_difference_maximum < score <= 1-cusp_app.engine_score_difference_minimum
    or 1 + cusp_app.engine_score_difference_minimum <= score < 1 + cusp_app.engine_score_difference_maximum
    or -1 - cusp_app.engine_score_difference_maximum < score <= -1-cusp_app.engine_score_difference_minimum
    or -1 + cusp_app.engine_score_difference_minimum <= score < < -1 + cusp_app.engine_score_difference_maximum)
    """
    # See details in ai.ai_utils.check_fen_cusp

    cusp_app.engine_score_difference_maximum = 0.1
    cusp_app.engine_score_difference_minimum = 0
    cusp_app.engine_safe_move_score_maximum=0.8
    # The outer range and inner range is necessary when engine_score_difference_maximum is big.
    # See details in ai.ai_utils.check_fen_cusp
    cusp_app.engine_score_cusp_outer_range_enable = True
    cusp_app.engine_score_cusp_inner_range_enable = True
    cusp_app.only_engine_one_setup_enable = False
    cusp_app.choose_the_recommended_color_enable = False
    cusp_app.no_choosing_color_directly_enable = False
    # False means Human-Level-Mode, a simplified version, best for human players
    cusp_app.engine_test_mode_enable=False
    # in Decision Phase, search for a fight starting position in real time
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate = 2
    # in fight phase or standard chess
    cusp_app.engine_one_searching_limit_for_best_move = 2
    cusp_app.engine_two_searching_limit_for_best_move = 2
    cusp_app.engine_time_limit_enable = True
    cusp_app.legacy_engine_mode = False

    cusp_app.play_sound_enable = False
    cusp_app.output_PGN_enable = False
    cusp_app.eval_show_enable = True

    cusp_app.player_one_name_input = ''
    cusp_app.player_two_name_input = ''
    cusp_app.adjudicator_name_input = ''
    cusp_app.PGN_folder_path = ""
