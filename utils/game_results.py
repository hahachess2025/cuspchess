import logging
import time
from tkinter import END, messagebox

import chess
import chess.syzygy

import ui.language
import ui.ui_utils
import utils.config
import utils.tournament

logger = logging.getLogger(__name__)

def check_game_result(cusp_app):
    logger.info("check_game_result")  
    if cusp_app.game_in_progress and ( cusp_app.board.is_game_over() 
        or cusp_app.user_adjudicator_result != "*" or cusp_app.engine_adjudicator_result != "*" or cusp_app.time_out_result != "*" ):
        cusp_app.game_in_progress = False
        if cusp_app.board.is_game_over():
            cusp_app.game_result = cusp_app.board.result()
        elif cusp_app.user_adjudicator_result != "*":
            cusp_app.game_result = cusp_app.user_adjudicator_result
        elif cusp_app.engine_adjudicator_result != "*":
            cusp_app.game_result = cusp_app.engine_adjudicator_result
        elif cusp_app.time_out_result != "*":
            cusp_app.game_result = cusp_app.time_out_result
            
        show_game_result(cusp_app)
        write_game_result(cusp_app)
        utils.tournament.update_tournament_result(cusp_app)
        utils.tournament.check_tournament_result(cusp_app)
        cusp_app.update()
        return True


def show_game_result(cusp_app):
    logger.info("show_game_result")    
    result_str = ""
    if cusp_app.chess_game_variant_mode == "Normal":
        if cusp_app.game_result == "1-0":
            result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
        elif cusp_app.game_result == "0-1":
            result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
        elif cusp_app.game_result == "1/2-1/2":
            result_str = cusp_app.translations[cusp_app.current_lang]['draw']
    else:
        # In Cusp Chess, we need to know the color-must-win.
        if cusp_app.color_must_win_in_cusp_chess == "W":
            if cusp_app.game_result == "1-0":
                if not cusp_app.player_swap_side:
                    result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
                else:
                    result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
            elif cusp_app.game_result == "0-1":
                if not cusp_app.player_swap_side:
                    result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
                else:
                    result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
            elif cusp_app.game_result == "1/2-1/2":
                if not cusp_app.player_swap_side:
                    result_str = ( cusp_app.translations[cusp_app.current_lang]['Draw_means_Black_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won'])
                else:
                    result_str = ( cusp_app.translations[cusp_app.current_lang]['Draw_means_Black_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won'])
        elif cusp_app.color_must_win_in_cusp_chess == "B":
            if cusp_app.game_result == "1-0":
                if not cusp_app.player_swap_side:
                    result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
                else:
                    result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
            elif cusp_app.game_result == "0-1":
                if not cusp_app.player_swap_side:
                    result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
                else:
                    result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
            elif cusp_app.game_result == "1/2-1/2":
                if not cusp_app.player_swap_side:
                    result_str = ( cusp_app.translations[cusp_app.current_lang]['Draw_means_White_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won'])
                else:
                    result_str = ( cusp_app.translations[cusp_app.current_lang]['Draw_means_White_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won'])
        else:
            # no one sets up a fight starting position. draw means loss for the first player.
            if cusp_app.game_result == "1-0":
                result_str = cusp_app.translations[cusp_app.current_lang]['White_won'] + cusp_app.player_one_name + cusp_app.translations[cusp_app.current_lang]['won']
            elif cusp_app.game_result == "0-1":
                result_str = cusp_app.translations[cusp_app.current_lang]['Black_won'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won']
            if cusp_app.game_result == "1/2-1/2" :
                result_str = ( cusp_app.translations[cusp_app.current_lang]['No_one_set_up_a_cusp_position'] + cusp_app.player_two_name + cusp_app.translations[cusp_app.current_lang]['won'] )

    if result_str:
        if len(result_str) > 40:
            font_size = 20 - (len(result_str) - 40) // 3
            font_size = max(10, font_size)
        else:
            font_size = 20
        cusp_app.result_str = result_str

        cusp_app.game_status_label_state = "game_status_label_final_result"
        ui.language.update_widget(cusp_app, cusp_app.game_status_label)
        cusp_app.game_status_label.config(font=("Arial", font_size))


    # write game result to PGN and to GUI
def write_game_result(cusp_app):
    logger.info("write_game_result")  
    result_str = ""
    if cusp_app.board.is_game_over():
        result_str = cusp_app.board.result()
    elif cusp_app.user_adjudicator_result != "*":
        result_str = 'user adjudicator ' + cusp_app.user_adjudicator_result
    elif cusp_app.engine_adjudicator_result != "*":
        result_str = 'engine adjudicator '  + cusp_app.engine_adjudicator_result    
    elif cusp_app.time_out_result != "*":
        result_str = 'time out ' + cusp_app.time_out_result
    if result_str != "":
        result_str = 'result ' + "{" + result_str + "}"
        logger.info("{result_str}")
        if cusp_app.blindfold_mode:
            cusp_app.blindfold_move_notice_label["text"] = str(result_str)

        cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1

        cusp_app.move_history_text.insert(
            END, "\n" + str(cusp_app.move_history_text_number) + ". " + result_str
        )
        cusp_app.move_history_text.see("end")

        if cusp_app.output_PGN_enable:
            with open(cusp_app.PGN_save_path, "a") as write_PGN:
                print("\n" + str(cusp_app.move_history_text_number) +
                      ". " + result_str, file=write_PGN, end=" ", )
                      

def check_early_stop_results(cusp_app):
    logger.info("check_early_stop_results")     
    if cusp_app.move_score_set:
        if (  (cusp_app.game_early_stop_draw_enable or cusp_app.game_early_stop_win_enable) and cusp_app.game_early_stop == False ):            
            if  ( cusp_app.game_early_stop_minimum_moves < cusp_app.board.fullmove_number ):
                if cusp_app.chess_game_variant_mode != "Normal" and cusp_app.cusp_chess_phase == "Fight":
                    if cusp_app.board.turn:
                        if cusp_app.color_must_win_in_cusp_chess == "W":
                            # minimum for draw calculation, maximum positive for win, maximum negative for lose
                            # In Cusp Chess, draw means win for a color, so sometimes draw is enough.
                            if ( cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum ):
                                cusp_app.game_early_stop_white_count_maximum_positive += 1
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                                cusp_app.game_early_stop_white_count_minimum = 0
                              
                            elif cusp_app.move_score < -(1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum):
                                cusp_app.game_early_stop_white_count_minimum = 0
                                cusp_app.game_early_stop_white_count_maximum_negative += 1
                                cusp_app.game_early_stop_white_count_maximum_positive = 0
                            # It is possible to end in draw for white.    
                            elif (abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference):
                                cusp_app.game_early_stop_white_count_minimum += 1
                                cusp_app.game_early_stop_white_count_maximum_positive = 0
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                            # uncertainty. We reset the count, because we need the score to be stable.   
                            else:
                                cusp_app.game_early_stop_white_count_maximum_positive = 0
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                                cusp_app.game_early_stop_white_count_minimum = 0
                                
                        elif cusp_app.color_must_win_in_cusp_chess == "B":
                            if ( -cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum ):
                                cusp_app.game_early_stop_white_count_maximum_negative += 1
                                cusp_app.game_early_stop_white_count_maximum_positive = 0
                                cusp_app.game_early_stop_white_count_minimum = 0
                            elif cusp_app.move_score >(1 + cusp_app.game_early_stop_score_difference+ cusp_app.engine_score_difference_maximum):
                                cusp_app.game_early_stop_white_count_minimum = 0
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                                cusp_app.game_early_stop_white_count_maximum_positive += 1                                
                            elif (abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference):
                                cusp_app.game_early_stop_white_count_minimum += 1
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                                cusp_app.game_early_stop_white_count_maximum_positive = 0        
                            else:
                                cusp_app.game_early_stop_white_count_maximum_positive = 0
                                cusp_app.game_early_stop_white_count_maximum_negative = 0
                                cusp_app.game_early_stop_white_count_minimum = 0
                    else:
                        if cusp_app.color_must_win_in_cusp_chess == "B":
                            if ( cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum ):
                                cusp_app.game_early_stop_black_count_maximum_positive += 1
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                                cusp_app.game_early_stop_black_count_minimum = 0
                            elif cusp_app.move_score < -(1 + cusp_app.game_early_stop_score_difference+ cusp_app.engine_score_difference_maximum):
                                cusp_app.game_early_stop_black_count_minimum = 0
                                cusp_app.game_early_stop_black_count_maximum_negative += 1
                                cusp_app.game_early_stop_black_count_maximum_positive = 0
                                
                            elif (abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference):
                                cusp_app.game_early_stop_black_count_minimum += 1
                                cusp_app.game_early_stop_black_count_maximum_positive = 0
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                            else:
                                cusp_app.game_early_stop_black_count_maximum_positive = 0
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                                cusp_app.game_early_stop_black_count_minimum = 0
                        elif cusp_app.color_must_win_in_cusp_chess == "W":
                            if ( -cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum ):
                                cusp_app.game_early_stop_black_count_maximum_negative += 1
                                cusp_app.game_early_stop_black_count_maximum_positive = 0
                                cusp_app.game_early_stop_black_count_minimum = 0
                            elif cusp_app.move_score >(1 + cusp_app.game_early_stop_score_difference+ cusp_app.engine_score_difference_maximum):
                                cusp_app.game_early_stop_black_count_minimum = 0
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                                cusp_app.game_early_stop_black_count_maximum_positive += 1                                
                            elif (abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference):
                                cusp_app.game_early_stop_black_count_minimum += 1
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                                cusp_app.game_early_stop_black_count_maximum_positive = 0        
                            else:
                                cusp_app.game_early_stop_black_count_maximum_positive = 0
                                cusp_app.game_early_stop_black_count_maximum_negative = 0
                                cusp_app.game_early_stop_black_count_minimum = 0
                # For standard chess, there is no color-must-win.
                elif cusp_app.chess_game_variant_mode == "Normal" :
                    if cusp_app.board.turn:
                        if  cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference:
                            cusp_app.game_early_stop_white_count_maximum_positive += 1
                            cusp_app.game_early_stop_white_count_maximum_negative = 0
                            cusp_app.game_early_stop_white_count_minimum = 0
                        elif cusp_app.move_score < -(1 + cusp_app.game_early_stop_score_difference):
                            cusp_app.game_early_stop_white_count_minimum = 0
                            cusp_app.game_early_stop_white_count_maximum_negative += 1
                            cusp_app.game_early_stop_white_count_maximum_positive = 0
                            
                        elif (abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference):
                            cusp_app.game_early_stop_white_count_minimum += 1
                            cusp_app.game_early_stop_white_count_maximum_positive = 0
                            cusp_app.game_early_stop_white_count_maximum_negative = 0
                        else:
                            cusp_app.game_early_stop_white_count_maximum_positive = 0
                            cusp_app.game_early_stop_white_count_maximum_negative = 0
                            cusp_app.game_early_stop_white_count_minimum = 0
                    else:
                        # win
                        if  cusp_app.move_score > 1 + cusp_app.game_early_stop_score_difference:
                            cusp_app.game_early_stop_black_count_maximum_positive += 1
                            cusp_app.game_early_stop_black_count_maximum_negative = 0
                            cusp_app.game_early_stop_black_count_minimum = 0
                        # loss    
                        elif cusp_app.move_score < -(1 + cusp_app.game_early_stop_score_difference):
                            cusp_app.game_early_stop_black_count_minimum = 0
                            cusp_app.game_early_stop_black_count_maximum_negative += 1
                            cusp_app.game_early_stop_black_count_maximum_positive = 0
                        # draw    
                        elif abs(cusp_app.move_score) < 1 - cusp_app.game_early_stop_score_difference:
                            cusp_app.game_early_stop_black_count_minimum += 1
                            cusp_app.game_early_stop_black_count_maximum_positive = 0
                            cusp_app.game_early_stop_black_count_maximum_negative = 0
                        # uncertainty, reset
                        else:
                            cusp_app.game_early_stop_black_count_maximum_positive = 0
                            cusp_app.game_early_stop_black_count_maximum_negative = 0
                            cusp_app.game_early_stop_black_count_minimum = 0          
                logger.info(f'cusp_app.game_early_stop_white_count_maximum_positive: {cusp_app.game_early_stop_white_count_maximum_positive}') 
                logger.info(f'cusp_app.game_early_stop_white_count_maximum_negative: {cusp_app.game_early_stop_white_count_maximum_negative}')
                logger.info(f'cusp_app.game_early_stop_white_count_minimum: {cusp_app.game_early_stop_white_count_minimum}') 
                
                logger.info(f'cusp_app.game_early_stop_black_count_maximum_positive: {cusp_app.game_early_stop_black_count_maximum_positive}') 
                logger.info(f'cusp_app.game_early_stop_black_count_maximum_negative: {cusp_app.game_early_stop_black_count_maximum_negative}') 
                logger.info(f'cusp_app.game_early_stop_black_count_minimum: {cusp_app.game_early_stop_black_count_minimum}') 
                
                # When we check the result, we don't care it is Cusp Chess or standard chess,
                # because here we only check the result for a color not for two players.
                adjudicator_threshold=10 
                # Check if early stop for draw is enabled.
                if cusp_app.game_early_stop_draw_enable:
                    # check endgame tablebase
                    if check_endgame_tablebase(cusp_app):
                        logger.info(f'cusp_app.game_early_stop {cusp_app.game_early_stop}')
                        return True
                    # If both scores from two AI players are below the draw threshold for five consecutive moves, 
                    # and the number of major pieces is less than 6, we believe the game will end in draw.  
                    if ( cusp_app.game_early_stop_white_count_minimum > adjudicator_threshold/2 and cusp_app.game_early_stop_black_count_minimum > adjudicator_threshold/2 ):
                        ui.ui_utils.count_major_pieces(cusp_app)
                        logger.info( f"major_piece_count { cusp_app.major_piece_count}")
                        if cusp_app.major_piece_count < 6:
                            cusp_app.game_early_stop = True
                            cusp_app.early_stop_game_draw = True
                            return True
                    # If both scores are below the draw threshold for 10 consecutive moves, we believe the game will end in draw.        
                    if ( cusp_app.game_early_stop_white_count_minimum > adjudicator_threshold and cusp_app.game_early_stop_black_count_minimum > adjudicator_threshold ):
                        cusp_app.game_early_stop = True
                        cusp_app.early_stop_game_draw = True
                        return True
                    # If only one player's score is below the draw threshold for 10 consecutive moves, we can start an Adjudicator Engine to check the score.
                    # It is necessary for two different AI players, such as Stockfish 17.1 vs 1.0.
                    # Usually I take Leela Chess Zero engine as the adjudicator.
                    if ( cusp_app.game_early_stop_white_count_minimum > adjudicator_threshold or cusp_app.game_early_stop_black_count_minimum > adjudicator_threshold ):
                        if cusp_app.adjudicator_engine_enable:
                            check_adjudicator_engine(cusp_app)
                            try:
                                if cusp_app.engine_time_limit_enable:
                                    info = cusp_app.adjudicator_engine.go( cusp_app.board, limit=1 )
                                else:
                                    info = cusp_app.adjudicator_engine.go( cusp_app.board, limit=20 )
                                cusp_app.judicator_score = info["score"].relative.score( mate_score=10000)
                                cusp_app.judicator_score = cusp_app.judicator_score / 100
                            except Exception as e:
                                logger.exception('adjudicator engine error')
                                messagebox.showerror("Error", f"Adjudicator engine error: {e}" )
                                return
                            logger.info( "------------adjudicator engine is working -----------------------" )
                            logger.info( f"cusp_app.judicator_score { cusp_app.judicator_score}")
                            if abs( cusp_app.judicator_score) < min( 0.5, 1 - cusp_app.game_early_stop_score_difference + 0.2, ):
                                logger.info( "------------adjudicator engine is working --------draw---------------" )
                                cusp_app.game_early_stop_count_adjudicator.append( cusp_app.tournament_game_number_started + 1)
                                cusp_app.game_early_stop = True
                                cusp_app.early_stop_game_draw = True
                                return True
                # a color can win
                # Check if early stop for win is enabled.
                if cusp_app.game_early_stop_win_enable:
                    if check_endgame_tablebase(cusp_app):
                        print('cusp_app.game_early_stop ',cusp_app.game_early_stop)
                        return True
                    # If white score indicates win and black score indicates loss, we believe white will win.    
                    if ( cusp_app.game_early_stop_white_count_maximum_positive > 5 
                        and cusp_app.game_early_stop_black_count_maximum_negative > 5 ):
                        cusp_app.early_stop_game_win_white = True
                        cusp_app.game_early_stop = True
                        return True
                    # If black score indicates win and white score indicates loss, we believe black will win.    
                    if ( cusp_app.game_early_stop_white_count_maximum_negative > 5 
                        and cusp_app.game_early_stop_black_count_maximum_positive > 5 ):
                        cusp_app.early_stop_game_win_black = True
                        cusp_app.game_early_stop = True
                        return True
                    # We need an adjudicator engine to check the position if only one color indicates either win or loss.    
                    if ( cusp_app.game_early_stop_white_count_maximum_positive > adjudicator_threshold 
                        or cusp_app.game_early_stop_white_count_maximum_negative > adjudicator_threshold 
                        or cusp_app.game_early_stop_black_count_maximum_positive > adjudicator_threshold 
                        or cusp_app.game_early_stop_black_count_maximum_negative > adjudicator_threshold ):
                        if cusp_app.adjudicator_engine_enable:
                            check_adjudicator_engine(cusp_app)
                            try:
                                if cusp_app.engine_time_limit_enable:
                                    info = cusp_app.adjudicator_engine.go( cusp_app.board, limit=1 )
                                else:
                                    info = cusp_app.adjudicator_engine.go( cusp_app.board, limit=20 )
                                cusp_app.judicator_score = info["score"].relative.score( mate_score=10000)
                                cusp_app.judicator_score = cusp_app.judicator_score / 100
                            except Exception as e:
                                logger.exception('adjudicator engine error')
                                messagebox.showerror("Error", f"Adjudicator engine error: {e}" )
                                return
                            logger.info( "------------adjudicator engine is working -----------------------" )
                            logger.info( f"cusp_app.judicator_score { cusp_app.judicator_score}")
                            if (abs(cusp_app.judicator_score) > 1 + cusp_app.game_early_stop_score_difference + cusp_app.engine_score_difference_maximum * 2):
                                if cusp_app.judicator_score > 0:
                                    if cusp_app.board.turn:
                                        if ( cusp_app.game_early_stop_white_count_maximum_positive > adjudicator_threshold 
                                            or cusp_app.game_early_stop_black_count_maximum_negative > adjudicator_threshold ):
                                            logger.info( "------------adjudicator engine is working ---------- white win -------------" )
                                            cusp_app.game_early_stop_count_adjudicator.append( cusp_app.tournament_game_number_started + 1)
                                            cusp_app.early_stop_game_win_white = True
                                            cusp_app.game_early_stop = True
                                            return True
                                    else:
                                        if ( cusp_app.game_early_stop_white_count_maximum_negative > adjudicator_threshold 
                                            or cusp_app.game_early_stop_black_count_maximum_positive > adjudicator_threshold ):
                                            logger.info( "------------adjudicator engine is working --------- black win --------------" )
                                            cusp_app.game_early_stop_count_adjudicator.append( cusp_app.tournament_game_number_started + 1)
                                            cusp_app.early_stop_game_win_black = True
                                            cusp_app.game_early_stop = True
                                            return True
                                else:
                                    if cusp_app.board.turn:
                                        if ( cusp_app.game_early_stop_white_count_maximum_negative > adjudicator_threshold 
                                            or cusp_app.game_early_stop_black_count_maximum_positive > adjudicator_threshold ):
                                            logger.info( "------------adjudicator engine is working ----------- black win ------------" )
                                            cusp_app.game_early_stop_count_adjudicator.append( cusp_app.tournament_game_number_started + 1)
                                            cusp_app.early_stop_game_win_black = True
                                            cusp_app.game_early_stop = True
                                            return True
                                    else:
                                        if ( cusp_app.game_early_stop_white_count_maximum_positive > adjudicator_threshold 
                                            or cusp_app.game_early_stop_black_count_maximum_negative > adjudicator_threshold ):
                                            logger.info( "------------adjudicator engine is working ---------- white win -------------" )
                                            cusp_app.game_early_stop_count_adjudicator.append( cusp_app.tournament_game_number_started + 1)
                                            cusp_app.early_stop_game_win_white = True
                                            cusp_app.game_early_stop = True
                                            return True



def check_adjudicator_engine(cusp_app):
    logger.info("check_adjudicator_engine")
    # In case time out problem.
    if time.time() - cusp_app.adjudicator_engine_last_time > 300:
        if cusp_app.adjudicator_engine:
            cusp_app.adjudicator_engine.quit()
        if cusp_app.engine_adjudicator_path != "":
            ui.ui_utils.setup_engine( cusp_app, 'adjudicator_engine', cusp_app.engine_adjudicator_path)
        else:
            logger.info('no adjudicator_engine')


def check_endgame_tablebase(cusp_app):
    logger.info("check_endgame_tablebase") 

    if cusp_app.endgame_tablebase_enable and cusp_app.Syzygy_tablebases_path:
        try:
            with chess.syzygy.open_tablebase(cusp_app.Syzygy_tablebases_path) as tablebase:
                tablebase_result=tablebase.get_wdl(cusp_app.board)
                if tablebase_result is not None:
                    # only check draw
                    if cusp_app.game_early_stop_draw_enable and int(tablebase_result)==0:
                        cusp_app.game_early_stop = True
                        cusp_app.early_stop_game_draw = True
                        logger.info(f'endgame tablebase, cusp_app.early_stop_game_draw: {cusp_app.early_stop_game_draw}')
                        return True 
                    # only check win    
                    elif cusp_app.game_early_stop_win_enable and int(tablebase_result)>0 :
                        if cusp_app.board.turn:
                            cusp_app.early_stop_game_win_white = True
                            cusp_app.game_early_stop = True
                            logger.info(f'endgame tablebase, cusp_app.early_stop_game_win_white: {cusp_app.early_stop_game_win_white}')
                            return True 
                        else:
                            cusp_app.early_stop_game_win_black = True
                            cusp_app.game_early_stop = True
                            logger.info(f'endgame tablebase, cusp_app.early_stop_game_win_black: {cusp_app.early_stop_game_win_black}')
                            return True
                    # only check win         
                    elif cusp_app.game_early_stop_win_enable and int(tablebase_result)<0:
                        if not cusp_app.board.turn:
                            cusp_app.early_stop_game_win_white = True
                            cusp_app.game_early_stop = True
                            logger.info(f'endgame tablebase, cusp_app.early_stop_game_win_white: {cusp_app.early_stop_game_win_white}')
                            return True 
                        else:
                            cusp_app.early_stop_game_win_black = True
                            cusp_app.game_early_stop = True
                            logger.info(f'endgame tablebase, cusp_app.early_stop_game_win_black: {cusp_app.early_stop_game_win_black}')
                            return True              
        except Exception as e:
            logger.exception('check endgame tablebase error')            
            messagebox.showerror("Error", f"check endgame tablebase error: {e}" )
#  Based on an Endgame table base or adjudicator engine.            
def check_game_early_stop(cusp_app): 
    logger.info("check_game_early_stop")    
    if cusp_app.game_early_stop:
        if cusp_app.early_stop_game_draw:
            cusp_app.engine_adjudicator_result = "1/2-1/2"
        elif cusp_app.early_stop_game_win_white:
            cusp_app.engine_adjudicator_result = "1-0"
        elif cusp_app.early_stop_game_win_black:
            cusp_app.engine_adjudicator_result = "0-1"
        check_game_result(cusp_app)

                      