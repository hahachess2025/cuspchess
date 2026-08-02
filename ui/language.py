import logging

logger = logging.getLogger(__name__)

def inialize_luanguage_setting(cusp_app):
    logger.info("inialize_luanguage_setting")
    cusp_app.translations = {
        "en": {
            "title": "Cusp Chess",
            "menu_Boards":"Boards",
            "menu_B_chess":"Chess",
            "menu_B_editor":"Board editor",
            "menu_B_blindfold":"Blindfold Chess",
            "menu_Setting":"Setting",
            "menu_S_Game_Setting":"Game Setting",
            
            "white": "White",
            "black": "Black",
            "AI": "AI",
            "Human": "Human",

            "player_one_board_label_default": "Player One",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: White or Black?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: I choose {color_must_win} directly",
                
            "player_two_board_label_default": "Player Two",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: White or Black?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: I choose {color_must_win} directly",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Cusp Chess, draw means loss",
            "game_status_label_safe_CC": "Cusp Chess, draw means loss",
            "game_status_label_searching": "Searching for a fight starting position",
            "game_status_label_player_must_setup": "{player_name} must set up now",
            "game_status_label_player_must_win": "Cusp Chess, {color} must win",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Color to move: {color}",
            "editor_color_to_move_label": "Color to move: {color}",
            
            "editor_start_position": "Starting position",
            "editor_clear_board":"Clear board",
            "editor_white_to_move_radio": "White to move",            
            "editor_black_to_move_radio": "Black to move",
            "editor_auto_turn_rotation_checkbox":"Auto turn rotation",
            "editor_engine_path_button": "Set engine path",               
            "editor_engine_analyse_checkbox": "Engine enable?",
            "editor_engine_time_or_depth_label": "Engine search time/depth",
            "editor_engine_top_moves_label": "Top moves",
            "editor_engine_score_label": "Now score is: ",
            "editor_engine_score_and_top_moves_search_button": "Search",   
            
            "editor_engine_search_for_cusps_label": "Search for fight starting positions for Cusp Chess", 
            "editor_search_for_cusps_for_CC_confirm_button": "Search",            

            "editor_cusp_stop_button": "Stop",
            "editor_editor_export_board_fen_button": "Export board FEN",
            "editor_clear_fen_history_button": "Clear history",
            "editor_set_board_fen_button": "Set board FEN",
                     
            "engine_one_path_button": "Engine player one",
            "engine_two_path_button": "Engine player two",
            "engine_adjudicator_path_button": "Adjudicator Engine",            
            "PGN_path_button": "PGN folder",
            "Syzygy_tablebases_path_button": "Syzygy tablebase folder",
                      
            "maximum_ply_before_setup_label": "Maximum plies before setup for an AI player",
            "engine_score_difference_maximum_label": "Engine maximum score difference for a Cusp",
            "engine_score_difference_minimum_label": "Engine minimum score difference for a Cusp",  
            "engine_safe_move_score_maximum_label": "Engine maximum absolute score for a safe move",
            "engine_cusp_outer_range_checkbox": "Cusp outer range, away from 0",
            "engine_cusp_inner_range_checkbox": "Cusp inner range, closer to 0",      
            "only_engine_one_setup_checkbox": "Only engine one sets up?",
            "the_other_engine_chooses_recommended_color_checkbox": "Recommended color for the other engine?",
            "no_choosing_color_directly_enable_checkbox": "No choosing color directly?", 
            "engine_test_mode_enable_checkbox": "Engine test mode",
         

            
            "time_limit_radio": "Time",
            "depth_limit_radio": "Depth",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Engine evaluation time/depth for a Cusp candidate",
            "engine_one_searching_limit_for_best_move_label": "Time/depth per move for engine one",   
            "engine_two_searching_limit_for_best_move_label": "Time/depth per move for engine two",
            "time_for_each_player_label": "Time for each player (seconds)",
            "reset_setting_button": "reset all",
            
            "modern_engine_mode_radio": "Modern engine",   
            "legacy_engine_mode_radio": "Legacy engine",
            "output_PGN_checkbox": "Output PGN?",
            "pgn_auto_game_variant_detection_checkbox":"change UI based on PGN",
            "play_sound_checkbox": "Play sound?",
            "eval_bar_checkbox": "Show eval?",   
            "endgame_tablebase_checkbox": "Endgame tablebase?",
            "player_one_name_label": "Set player one name",      
            "player_two_name_label": "Set player two name",
            "adjudicator_name_label": "Set adjudicator engine name",
            "setting_ok_button": "Save", 

            "tournament_game_number_label": "Tournament game number",
            "game_early_stop_draw_checkbox": "Early stop if draw?", 
            "game_early_stop_win_checkbox": "Early stop if win?",
            "game_early_stop_label": "Early stop score difference",   
            "game_early_stop_minimum_moves_label": "Early stop minimum moves",
            "adjudicator_engine_enable_checkbox": "Adjudicator engine?",      
            "tournament_start_button": "Start tournament",
            "stop_tournament": "Stop tournament", 
            
            "start_game_button": "Start game",
            "stop_game_button": "Stop game",     
            "reset_game_button": "Reset",
            "chess_radio": "Chess", 
            "cusp_chess_radio": "Cusp Chess",

            "player_one_label": "Player One",
            "player_two_label": "Player Two",  
            
            "load_PGN_button": "Load PGN",
            "play_PGN_previous_button": "Previous",   
            "play_PGN_next_button": "Next",
            "beginning_PGN_button": "Beginning",  
            "auto_play_PGN_button": "Auto play",
            "stop_play_PGN_button": "Stop play",
            "clear_history_button": "Clear history", 
            
            "move_history_label": "Move history",
            
            "setup_label_CC": "Setup for Cusp Chess",   
            "setup_CC_color_to_move": "Color to move",
            "setup_CC_color_must_win": "Color must win",      
            "Human_setup_confirmation_checkbox": "Set up?",
            "Human_move_finished_button": "Move finished",   
            "Human_directly_choose_button": "Choose directly",

            "Tournament_score":"Tournament score",
            "Now_Score_is":"Now Score is",

            "White_won":"White won. ",
            "Black_won":"Black won. ",
            "won":" won. ",
            "draw":"draw",
            "Draw_means_White_won":"Draw means White won. ",
            "Draw_means_Black_won":"Draw means Black won. ",
            "No_one_set_up_a_cusp_position":"No one set up a fight starting position. ",
            "The_move_is_illegal":"The move is illegal",
            "empty":"",    
            
        },
        
        "cn": {
            "title": "奇点象棋",
            
            "menu_Boards":"棋盘",
            "menu_B_chess":"国际象棋",
            "menu_B_editor":"棋盘编辑",
            "menu_B_blindfold":"盲棋",
            "menu_Setting":"设置",
            "menu_S_Game_Setting":"游戏设置",

            "white": "白方",
            "black": "黑方",
            "AI": "引擎",
            "Human": "人类玩家",
            
            "player_one_board_label_default": "玩家一",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: 白方还是黑方?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: 我直接选择 {color_must_win}",
                
            "player_two_board_label_default": "玩家二",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: 白方还是黑方?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: 我直接选择 {color_must_win}",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "奇点象棋, 和棋算输",
            "game_status_label_safe_CC": "奇点象棋, 和棋算输",
            "game_status_label_searching": "正在搜索奇点",
            "game_status_label_player_must_setup": "{player_name} 现在必须设置奇点局面",
            "game_status_label_player_must_win": "奇点象棋, {color} 必须赢",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "下一步: {color}",
            "editor_color_to_move_label": "下一步: {color}",            
            "editor_start_position": "开始局面",
            "editor_clear_board":"清空棋盘",
            "editor_white_to_move_radio": "白方走",            
            "editor_black_to_move_radio": "黑方走",
            "editor_auto_turn_rotation_checkbox":"自动换边",
            "editor_engine_path_button": "设置引擎路径",               
            "editor_engine_analyse_checkbox": "使用引擎?",
            "editor_engine_top_moves_label": "最佳走子选项",
            "editor_engine_time_or_depth_label": "引擎搜索 时间/深度",            
            "editor_engine_score_label": "当前分数是: ",
            "editor_engine_score_and_top_moves_search_button": "搜索",   
            
            "editor_engine_search_for_cusps_label": "搜索奇点象棋当前局面存在的所有奇点", 
            "editor_search_for_cusps_for_CC_confirm_button": "搜索",            
  
            "editor_cusp_stop_button": "停止",
            "editor_editor_export_board_fen_button": "输出当前局面 FEN",
            "editor_clear_fen_history_button": "清除输出",
            "editor_set_board_fen_button": "设置棋盘 FEN",
                     
            "engine_one_path_button": "引擎一路径",
            "engine_two_path_button": "引擎二路径",
            "engine_adjudicator_path_button": "裁判引擎路径",            
            "PGN_path_button": "PGN文件夹路径",
            "Syzygy_tablebases_path_button": "Syzygy 残局库",
                      
            "maximum_ply_before_setup_label": "引擎设置奇点之前的步数最大值",
            "engine_score_difference_maximum_label": "引擎搜索的奇点，其绝对值分数与1的差值上限",
            "engine_score_difference_minimum_label": "引擎搜索的奇点，其绝对值分数与1的差值下限",
            "engine_safe_move_score_maximum_label": "引擎安全走子，绝对值分数的上限",            
            "engine_cusp_outer_range_checkbox": "非0方向的取值",
            "engine_cusp_inner_range_checkbox": "靠近0方向的取值",      
            "only_engine_one_setup_checkbox": "只有引擎一设置奇点?",
            "the_other_engine_chooses_recommended_color_checkbox": "接受推荐的颜色?",
            "no_choosing_color_directly_enable_checkbox": "禁止引擎直接选择某方?",  
            "engine_test_mode_enable_checkbox": "引擎测试模式",
         

            
            "time_limit_radio": "搜索时间/秒",
            "depth_limit_radio": "搜索深度",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "引擎评估某候选奇点的搜索时间/深度",
            "engine_one_searching_limit_for_best_move_label": "引擎一每步搜索时间/深度",   
            "engine_two_searching_limit_for_best_move_label": "引擎二每步搜索时间/深度",
            "time_for_each_player_label": "每个玩家的总时间(秒)",
            "reset_setting_button": "恢复默认设置",
                      
            "modern_engine_mode_radio": "现代引擎",   
            "legacy_engine_mode_radio": "老版引擎",
            "output_PGN_checkbox": "输出PGN?",
            "pgn_auto_game_variant_detection_checkbox":"读取PGN时自动调整UI",
            "play_sound_checkbox": "走子声音?",
            "eval_bar_checkbox": "显示AI打分?",   
            "endgame_tablebase_checkbox": "使用残局库?",
            "player_one_name_label": "设置玩家一的用户名",      
            "player_two_name_label": "设置玩家二的用户名",
            "adjudicator_name_label": "设置仲裁引擎的用户名",
            "setting_ok_button": "保存", 
            
            "tournament_game_number_label": "锦标赛总盘数",
            "game_early_stop_draw_checkbox": "可能和棋，是否提前结束?", 
            "game_early_stop_win_checkbox": "可能赢棋，是否提前结束?",
            "game_early_stop_label": "提前结束的分差",   
            "game_early_stop_minimum_moves_label": "提前结束的最少步数",
            "adjudicator_engine_enable_checkbox": "使用裁判引擎仲裁?",      
            "tournament_start_button": "开始锦标赛",
            "stop_tournament": "停止锦标赛", 
            
            "start_game_button": "开始",
            "stop_game_button": "结束",     
            "reset_game_button": "重置",
            "chess_radio": "国际象棋", 
            "cusp_chess_radio": "奇点象棋",

            "player_one_label": "玩家一",
            "player_two_label": "玩家二",  
            
            "load_PGN_button": "载入PGN",
            "play_PGN_previous_button": "上一步",   
            "play_PGN_next_button": "下一步",
            "beginning_PGN_button": "初始局面",  
            "auto_play_PGN_button": "自动播放",
            "stop_play_PGN_button": "停止",
            "clear_history_button": "清除输出", 
            
            "move_history_label": "棋谱",
            
            "setup_label_CC": "设置奇点局面",   
            "setup_CC_color_to_move": "下一步",
            "setup_CC_color_must_win": "必须赢的颜色",      
            "Human_setup_confirmation_checkbox": "设置奇点?",
            "Human_move_finished_button": "完成",   
            "Human_directly_choose_button": "直接选赢的颜色",
            "Tournament_score":"锦标赛比分", 
            "Now_Score_is":"当前分数是",

            "White_won":"白方赢. ",
            "Black_won":"黑方赢. ",
            "won":" 赢. ",
            "draw":"和棋",
            "Draw_means_White_won":"和棋算白棋赢. ",
            "Draw_means_Black_won":"和棋算黑棋赢. ",
            "No_one_set_up_a_cusp_position":"无人设置奇点局面. ",   
            "The_move_is_illegal":"非法走子",
            "empty":"",    
        },
        "de": {
            "title": "Cusp Chess",
            "menu_Boards":"Bretter",
            "menu_B_chess":"Schach",
            "menu_B_editor":"Brett-Editor",
            "menu_B_blindfold":"Blindschach",
            "menu_Setting":"Einstellung",
            "menu_S_Game_Setting":"Spieleinstellung",
            
            "white": "Weiß",
            "black": "Schwarz",
            "AI": "KI",
            "Human": "Mensch",

            "player_one_board_label_default": "Spieler Eins",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: Weiß oder Schwarz?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: Ich wähle {color_must_win} direkt",
                
            "player_two_board_label_default": "Spieler Zwei",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: Weiß oder Schwarz?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: Ich wähle {color_must_win} direkt",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Singularität Schach, Remis bedeutet Niederlage",

            "game_status_label_safe_CC": "Singularität Schach, Remis bedeutet Niederlage",

            "game_status_label_searching": "Suche nach Singularitätsposition",
            "game_status_label_player_must_setup": "{player_name} muss jetzt aufstellen",
            "game_status_label_player_must_win": "Singularität Schach, {color} muss gewinnen",

            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Farbe am Zug: {color}",
            "editor_color_to_move_label": "Farbe am Zug: {color}",
            "editor_start_position": "Startposition",
            "editor_clear_board":"Brett löschen",
            "editor_white_to_move_radio": "Weiß am Zug",            
            "editor_black_to_move_radio": "Schwarz am Zug",
            "editor_auto_turn_rotation_checkbox":"Automatisches Drehen der Turniereihenfolge",
            "editor_engine_path_button": "Engine-Pfad setzen",               
            "editor_engine_analyse_checkbox": "Engine aktivieren?",
            "editor_engine_top_moves_label": "Höhepunkt-Züge",
            "editor_engine_time_or_depth_label": "Engine-Suchzeit/-tiefe",            
            "editor_engine_score_label": "Aktueller Stand: ",
            "editor_engine_score_and_top_moves_search_button": "Suche",   
            
            "editor_engine_search_for_cusps_label": "Suche nach Singularitätspositionen für Singularität Schach", 
            "editor_search_for_cusps_for_CC_confirm_button": "Suchen",            
  
            "editor_cusp_stop_button": "Stop",
            "editor_editor_export_board_fen_button": "Brett-FEN exportieren",
            "editor_clear_fen_history_button": "Verlauf löschen",
            "editor_set_board_fen_button": "Brett-FEN setzen",
                        
            "engine_one_path_button": "Engine Spieler Eins Pfad",
            "engine_two_path_button": "Engine Spieler Zwei Pfad",
            "engine_adjudicator_path_button": "Schiedsrichter-Engine-Pfad",            
            "PGN_path_button": "PGN-Ordnerpfad",
            "Syzygy_tablebases_path_button": "Syzygy-Tablebase-Ordnerpfad",
                       
            "maximum_ply_before_setup_label": "Maximale Züge vor Einrichtung für KI",
            "engine_score_difference_maximum_label": "Obere Grenze der Engine-Punktdifferenz für eine Singularität",
            "engine_score_difference_minimum_label": "Untere Grenze der Engine-Punktdifferenz für eine Singularität ",   
            "engine_safe_move_score_maximum_label": "Maschine maximale absoluter Score für eine sichere Zug",
            "engine_cusp_outer_range_checkbox": "Äußerer Bereich?",
            "engine_cusp_inner_range_checkbox": "Innerer Bereich?",      
            "only_engine_one_setup_checkbox": "Nur Engine Eins richtet auf?",
            "the_other_engine_chooses_recommended_color_checkbox": "Empfohlene Farbe für die andere Maschine?",
            "no_choosing_color_directly_enable_checkbox": "Keine direkte Farbauswahl?",
            "engine_test_mode_enable_checkbox": "Maschinentestmodus",
       
            
            "time_limit_radio": "Zeit",
            "depth_limit_radio": "Tiefe",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Engine-Bewertungszeit/Tiefe für Singularitätskandidat",
            "engine_one_searching_limit_for_best_move_label": "Zeit/Tiefe pro Zug für Engine Eins",   
            "engine_two_searching_limit_for_best_move_label": "Zeit/Tiefe pro Zug für Engine Zwei",
            "time_for_each_player_label": "Zeit für jeden Spieler (Sekunden))",
            "reset_setting_button": "Alles zurücksetzen",
            
            "modern_engine_mode_radio": "Moderner Engine",   
            "legacy_engine_mode_radio": "Legacy engine",
            "output_PGN_checkbox": "PGN ausgeben?",
            "pgn_auto_game_variant_detection_checkbox":"Benutzeroberfläche basierend auf PGN ändern",
            "play_sound_checkbox": "Ton abspielen?",
            "eval_bar_checkbox": "Bewertung anzeigen?",   
            "endgame_tablebase_checkbox": "Endspiel-Datenbank?",
            "player_one_name_label": "Spieler Eins Name setzen",      
            "player_two_name_label": "Spieler Zwei Name setzen",
            "adjudicator_name_label": "Adjudikationsmaschine-Name setzen",
            "setting_ok_button": "Speichern", 

            "tournament_game_number_label": "Turnierspielnummer",
            "game_early_stop_draw_checkbox": "Früher Stopp bei Remis?", 
            "game_early_stop_win_checkbox": "Früher Stopp bei Sieg?",
            "game_early_stop_label": "Punktedifferenz für früher Stopp",   

            "adjudicator_engine_enable_checkbox": "Schiedsrichter-Engine?",      
            "tournament_start_button": "Turnier starten",
            "stop_tournament": "Turnier stoppen", 
            
            "start_game_button": "Spiel starten",
            "stop_game_button": "Spiel stoppen",     
            "reset_game_button": "Zurücksetzen",
            "chess_radio": "Schach", 
            "cusp_chess_radio": "Singularität Schach",

            "player_one_label": "Spieler Eins",
            "player_two_label": "Spieler Zwei",  
            
            "load_PGN_button": "PGN laden",
            "play_PGN_previous_button": "Vorherige",   
            "play_PGN_next_button": "Nächste",
            "beginning_PGN_button": "Anfang",  
            "auto_play_PGN_button": "Automatische Wiedergabe",
            "stop_play_PGN_button": "Wiedergabe stoppen",
            "clear_history_button": "Verlauf löschen", 
            
            "move_history_label": "Zugverlauf",
            
            "setup_label_CC": "Setup für Singularität Schach",   
            "setup_CC_color_to_move": "Farbe am Zug",
            "setup_CC_color_must_win": "Farbe muss gewinnen",      
            "Human_setup_confirmation_checkbox": "Aufstellen?",
            "Human_move_finished_button": "Zug beendet",   
            "Human_directly_choose_button": "Direkt wählen",

            "Tournament_score":"Turnierstand",
            "Now_Score_is":"Aktueller Stand",

            "White_won":"Weiß hat gewonnen. ",
            "Black_won":"Schwarz hat gewonnen. ",
            "won":" hat gewonnen. ",
            "draw":"Unentschieden",
            "Draw_means_White_won":"Unentschieden bedeutet Weiß hat gewonnen. ",
            "Draw_means_Black_won":"Unentschieden bedeutet Schwarz hat gewonnen. ",
            "No_one_set_up_a_cusp_position":"Niemand hat eine Singularitätsposition aufgestellt. ",
            "The_move_is_illegal":"Der Zug ist illegal.",
            "empty":"",    
            
        },        
        "fr": {
            "title": "Cusp Chess",
            "menu_Boards":"Plateaux",
            "menu_B_chess":"Échecs",
            "menu_B_editor":"Éditeur de plateau",
            "menu_B_blindfold":"Échecs à l’aveugle",
            "menu_Setting":"Paramètre",
            "menu_S_Game_Setting":"Paramètres de partie",
            
            "white": "Blanc",
            "black": "Noir",
            "AI": "IA",
            "Human": "Humain",

            "player_one_board_label_default": "Joueur Un ",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: Blanc ou Noir?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: Je choisis {color_must_win} directement",
                
            "player_two_board_label_default": "Joueur Deux",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: Blanc ou Noir?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: Je choisis {color_must_win} directement",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Échecs singularité, Le nul signifie défaite",
            "game_status_label_safe_CC": "Échecs singularité, Le nul signifie défaite",
            "game_status_label_searching": "Recherche d'une position de singularité",
            "game_status_label_player_must_setup": "{player_name} doit se mettre en place maintenant",
            "game_status_label_player_must_win": "Échecs singularité, {color} doit gagner",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Couleur à jouer: {color}",
            "editor_color_to_move_label": "Couleur à jouer: {color}",
            "editor_start_position": "Position de départ",
            "editor_clear_board":"Effacer le plateau",
            "editor_white_to_move_radio": "Blanc à jouer",            
            "editor_black_to_move_radio": "Noir à jouer",
            "editor_auto_turn_rotation_checkbox":"Rotation automatique des tours",
            "editor_engine_path_button": "Définir le chemin du moteur",               
            "editor_engine_analyse_checkbox": "Activer le moteur?",
            "editor_engine_time_or_depth_label": "Temps/profondeur de recherche du moteur", 
            "editor_engine_top_moves_label": "Meilleurs coups",
            "editor_engine_score_label": "Score actuel: ",
            "editor_engine_score_and_top_moves_search_button": "Recherche",   
            
            "editor_engine_search_for_cusps_label": "Rechercher des positions de singularité pour Échecs singularité", 
            "editor_search_for_cusps_for_CC_confirm_button": "Rechercher",            

            "editor_cusp_stop_button": "Arrêter",
            "editor_editor_export_board_fen_button": "Exporter le FEN du plateau",
            "editor_clear_fen_history_button": "Effacer l'historique",
            "editor_set_board_fen_button": "Définir FEN du plateau",

            "engine_one_path_button": "Chemin moteur joueur un",
            "engine_two_path_button": "Chemin moteur joueur deux",
            "engine_adjudicator_path_button": "Chemin moteur d'arbitre",            
            "PGN_path_button": "Chemin du dossier PGN",
            "Syzygy_tablebases_path_button": "Chemin du dossier tablebase Syzygy",
           
            "maximum_ply_before_setup_label": "Nombre maximum de demi-coups avant configuration pour IA",
            "engine_score_difference_maximum_label": "Limite supérieure de différence de score du moteur",
            "engine_score_difference_minimum_label": "Limite inférieure de différence de score du moteur",   
            "engine_safe_move_score_maximum_label": "Score maximum absolu de la machine pour un mouvement sûr",
            "engine_cusp_outer_range_checkbox": "Plage externe?",
            "engine_cusp_inner_range_checkbox": "Plage interne?",      
            "only_engine_one_setup_checkbox": "Seul le moteur un s'installe?",
            "the_other_engine_chooses_recommended_color_checkbox": "Couleur recommandée pour l'autre machine?",
            "no_choosing_color_directly_enable_checkbox": "Pas de choix direct de couleur?",
            "engine_test_mode_enable_checkbox": "Mode de test de la machine",
          
            
            "time_limit_radio": "Temps",
            "depth_limit_radio": "Profondeur",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Temps/profondeur d'évaluation pour un candidat singularité",
            "engine_one_searching_limit_for_best_move_label": "Temps/profondeur par coup pour moteur un",   
            "engine_two_searching_limit_for_best_move_label": "Temps/profondeur par coup pour moteur deux",
            "time_for_each_player_label": "Temps pour chaque joueur (secondes)",
            "reset_setting_button": "Réinitialiser tout",
            
            "modern_engine_mode_radio": "Moteur moderne",   
            "legacy_engine_mode_radio": "Moteur hérité",
            "output_PGN_checkbox": "Exporter PGN?",
            "pgn_auto_game_variant_detection_checkbox":"Changer l’interface selon le PGN",
            "play_sound_checkbox": "Jouer le son?",
            "eval_bar_checkbox": "Montrer l'évaluation?",   
            "endgame_tablebase_checkbox": "Table de fin de partie?",
            "player_one_name_label": "Définir le nom du joueur un",      
            "player_two_name_label": "Définir le nom du joueur deux",
            "adjudicator_name_label": "Définir le nom de la machine arbitre",
            "setting_ok_button": "Sauvegarder", 

            "tournament_game_number_label": "Numéro de partie du tournoi",
            "game_early_stop_draw_checkbox": "Arrêt anticipé si nul?", 
            "game_early_stop_win_checkbox": "Arrêt anticipé si victoire?",
            "game_early_stop_label": "Différence de score pour arrêt anticipé",   
            "game_early_stop_minimum_moves_label": "Nombre minimum de coups pour arrêt anticipé",
            "adjudicator_engine_enable_checkbox": "Moteur arbitre?",      
            "tournament_start_button": "Démarrer le tournoi",
            "stop_tournament": "Arrêter le tournoi", 
            
            "start_game_button": "Démarrer la partie",
            "stop_game_button": "Arrêter la partie",     
            "reset_game_button": "Réinitialiser",
            "chess_radio": "Échecs", 
            "cusp_chess_radio": "Échecs singularité",

            "player_one_label": "Joueur Un",
            "player_two_label": "Joueur Deux",  
            
            "load_PGN_button": "Charger PGN",
            "play_PGN_previous_button": "Précédent",   
            "play_PGN_next_button": "Suivant",
            "beginning_PGN_button": "Début",  
            "auto_play_PGN_button": "Lecture automatique",
            "stop_play_PGN_button": "Arrêter lecture",
            "clear_history_button": "Effacer l'historique", 
            
            "move_history_label": "Historique des coups",
            
            "setup_label_CC": "Configuration pour Échecs singularité",   
            "setup_CC_color_to_move": "Couleur à jouer",
            "setup_CC_color_must_win": "Couleur doit gagner",      
            "Human_setup_confirmation_checkbox": "Configurer?",
            "Human_move_finished_button": "Coup terminé",   
            "Human_directly_choose_button": "Choisir directement",

            "Tournament_score":"Score du tournoi",
            "Now_Score_is":"Score actuel",

            "White_won":"Blancs ont gagné. ",
            "Black_won":"Noirs ont gagné. ",
            "won":" a gagné. ",
            "draw":"Nul",
            "Draw_means_White_won":"Nul signifie que Blancs ont gagné. ",
            "Draw_means_Black_won":"Nul signifie que Noirs ont gagné. ",
            "No_one_set_up_a_cusp_position":"Personne n'a configuré de position de singularité. ",
            "The_move_is_illegal":"Le coup est illégal.",
            "empty":"",    
            
        },        

        "es": {
            "title": "Cusp Chess",
            "menu_Boards":"Tableros",
            "menu_B_chess":"Ajedrez",
            "menu_B_editor":"Editor de tablero",
            "menu_B_blindfold":"Ajedrez a ciegas",
            "menu_Setting":"Ajuste",
            "menu_S_Game_Setting":"Configuración del juego",
            
            "white": "Blancas",
            "black": "Negras",
            "AI": "IA",
            "Human": "Humano",

            "player_one_board_label_default": "Jugador Uno",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: ¿Blancas o Negras?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: Elijo {color_must_win} directamente",
                
            "player_two_board_label_default": "Jugador Dos",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: ¿Blancas o Negras?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: Elijo {color_must_win} directamente",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Ajedrez singularidad, empate significa derrota",
            "game_status_label_safe_CC": "Ajedrez singularidad, empate significa derrota",
            "game_status_label_searching": "Buscando una posición de singularidad",
            "game_status_label_player_must_setup": "{player_name} debe colocarse ahora",
            "game_status_label_player_must_win": "Ajedrez singularidad, {color} debe ganar",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Color en turno: {color}",
            "editor_color_to_move_label": "Color en turno: {color}",
            "editor_start_position": "Posición inicial",
            "editor_clear_board":"Limpiar tablero",
            "editor_white_to_move_radio": "Juegan blancas",            
            "editor_black_to_move_radio": "Juegan negras",
            "editor_auto_turn_rotation_checkbox":"Rotación automática del turno",
            "editor_engine_path_button": "Establecer ruta del motor",               
            "editor_engine_analyse_checkbox": "¿Activar motor?",
            "editor_engine_time_or_depth_label": "Tiempo/profundidad de búsqueda del motor",
            "editor_engine_top_moves_label": "Mejores movimientos",
            "editor_engine_score_label": "Puntuación actual: ",
            "editor_engine_score_and_top_moves_search_button": "Buscar",   
            
            "editor_engine_search_for_cusps_label": "Buscar posiciones de singularidad para Ajedrez singularidad", 
            "editor_search_for_cusps_for_CC_confirm_button": "Buscar",            

            "editor_cusp_stop_button": "Detener",
            "editor_editor_export_board_fen_button": "Exportar FEN del tablero",
            "editor_clear_fen_history_button": "Limpiar historial",
            "editor_set_board_fen_button": "Establecer FEN del tablero",
            
            "engine_one_path_button": "Ruta del motor jugador uno",
            "engine_two_path_button": "Ruta del motor jugador dos",
            "engine_adjudicator_path_button": "Ruta del motor árbitro",            
            "PGN_path_button": "Ruta de carpeta PGN",
            "Syzygy_tablebases_path_button": "Ruta de carpeta de tablebase Syzygy",
                      
            "maximum_ply_before_setup_label": "Máximo de medias jugadas antes de configurar IA",
            "engine_score_difference_maximum_label": "mite superior de diferencia de puntuación del motor para una singularidad",
            "engine_score_difference_minimum_label": "Límite inferior de diferencia de puntuación del motor para una singularidad",   
            "engine_safe_move_score_maximum_label": "Puntuación máxima absoluta para un movimiento seguro",
            "engine_cusp_outer_range_checkbox": "Rango exterior?",
            "engine_cusp_inner_range_checkbox": "Rango interior?",      
            "only_engine_one_setup_checkbox": "¿Solo el motor uno se configura?",
            "the_other_engine_chooses_recommended_color_checkbox": "Color recomendado para la otra máquina?",
            "no_choosing_color_directly_enable_checkbox": "¿No elegir color directamente?", 
            "engine_test_mode_enable_checkbox": "Modo de prueba de la máquina",
        
            
            "time_limit_radio": "Tiempo",
            "depth_limit_radio": "Profundidad",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Tiempo/profundidad de evaluación para candidato singularidad",
            "engine_one_searching_limit_for_best_move_label": "Tiempo/profundidad por jugada para motor uno",   
            "engine_two_searching_limit_for_best_move_label": "Tiempo/profundidad por jugada para motor dos",
            "time_for_each_player_label": "Tiempo para cada jugador (segundos)",
            "reset_setting_button": "Reiniciar todo",
            
            "modern_engine_mode_radio": "Motor moderno",   
            "legacy_engine_mode_radio": "Motor legado",
            "output_PGN_checkbox": "¿Exportar PGN?",
            "pgn_auto_game_variant_detection_checkbox":"Cambiar la interfaz según el PGN",
            "play_sound_checkbox": "¿Reproducir sonido?",
            "eval_bar_checkbox": "¿Mostrar evaluación?",   
            "endgame_tablebase_checkbox": "¿Tabla de finales?",
            "player_one_name_label": "Establecer nombre jugador uno",      
            "player_two_name_label": "Establecer nombre jugador dos",
            "adjudicator_name_label": "Establecer nombre de la máquina árbitro",
            "setting_ok_button": "Guardar", 

            "tournament_game_number_label": "Número de juego del torneo",
            "game_early_stop_draw_checkbox": "Parada temprana si empate?", 
            "game_early_stop_win_checkbox": "Parada temprana si victoria?",
            "game_early_stop_label": "Diferencia de puntuación para parada temprana",   
            "game_early_stop_minimum_moves_label": "Movimientos mínimos para parada temprana",
            "adjudicator_engine_enable_checkbox": "¿Motor árbitro?",      
            "tournament_start_button": "Iniciar torneo",
            "stop_tournament": "Detener torneo", 
            
            "start_game_button": "Iniciar juego",
            "stop_game_button": "Detener juego",     
            "reset_game_button": "Reiniciar",
            "chess_radio": "Ajedrez", 
            "cusp_chess_radio": "Ajedrez singularidad",

            "player_one_label": "Jugador Uno",
            "player_two_label": "Jugador Dos",  
            
            "load_PGN_button": "Cargar PGN",
            "play_PGN_previous_button": "Anterior",   
            "play_PGN_next_button": "Siguiente",
            "beginning_PGN_button": "Principio",  
            "auto_play_PGN_button": "Reproducción automática",
            "stop_play_PGN_button": "Detener reproducción",
            "clear_history_button": "Limpiar historial", 
            
            "move_history_label": "Historial de jugadas",
            
            "setup_label_CC": "Configuración para Ajedrez singularidad",   
            "setup_CC_color_to_move": "Color en turno",
            "setup_CC_color_must_win": "El color debe ganar",      
            "Human_setup_confirmation_checkbox": "Configurar?",
            "Human_move_finished_button": "Jugada terminada",   
            "Human_directly_choose_button": "Elegir directamente",

            "Tournament_score":"Puntuación del torneo",
            "Now_Score_is":"La puntuación actual es",

            "White_won":"Blancas ganaron. ",
            "Black_won":"Negras ganaron. ",
            "won":" ganó. ",
            "draw":"Empate",
            "Draw_means_White_won":"Empate significa que Blancas ganaron. ",
            "Draw_means_Black_won":"Empate significa que Negras ganaron. ",
            "No_one_set_up_a_cusp_position":"Nadie configuró una posición de singularidad. ",
            "The_move_is_illegal":"La jugada es ilegal.",
            "empty":"",    
            
        },

        "ukr": {
            "title": "Cusp Chess",
            "menu_Boards":"Дошки",
            "menu_B_chess":"Шахи",
            "menu_B_editor":"Редактор дошки",
            "menu_B_blindfold":"Шахи в сліпу",
            "menu_Setting":"Налаштування",
            "menu_S_Game_Setting":"Налаштування гри",
            
            "white": "Білі",
            "black": "Чорні",
            "AI": "ШІ",
            "Human": "Людина",

            "player_one_board_label_default": "Гравець Один",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: Білі чи Чорні?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: Я обираю {color_must_win} безпосередньо",
                
            "player_two_board_label_default": "Гравець Два",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: Білі чи Чорні?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: Я обираю {color_must_win} безпосередньо",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Шахи сингулярності, нічия означає поразку",
            "game_status_label_safe_CC": "Шахи сингулярності, нічия означає поразку",
            "game_status_label_searching": "Пошук сингулярної позиції",
            "game_status_label_player_must_setup": "{player_name} має зараз встановити",
            "game_status_label_player_must_win": "Шахи сингулярності, {color} має виграти",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Хід кольору: {color}",
            "editor_color_to_move_label": "Хід кольору: {color}",
            "editor_start_position": "Початкова позиція",
            "editor_clear_board":"Очистити дошку",
            "editor_white_to_move_radio": "Хід білих",            
            "editor_black_to_move_radio": "Хід чорних",
            "editor_auto_turn_rotation_checkbox":"Автоматичний обертання шахівниці",
            "editor_engine_path_button": "Встановити шлях до движка",               
            "editor_engine_analyse_checkbox": "Активувати движок?",
            "editor_engine_time_or_depth_label": "Час/глибина пошуку движка",
            "editor_engine_top_moves_label": "Найкращі ходи",
            "editor_engine_score_label": "Поточний рахунок: ",
            "editor_engine_score_and_top_moves_search_button": "Пошук",   
            
            "editor_engine_search_for_cusps_label": "Пошук сингулярних позицій для шахів сингулярності", 
            "editor_search_for_cusps_for_CC_confirm_button": "Пошук",            

            "editor_cusp_stop_button": "Зупинити",
            "editor_editor_export_board_fen_button": "Експорт FEN дошки",
            "editor_clear_fen_history_button": "Очистити історію",
            "editor_set_board_fen_button": "Встановити FEN дошки",
                     
            "engine_one_path_button": "Шлях до движка гравця один",
            "engine_two_path_button": "Шлях до движка гравця два",
            "engine_adjudicator_path_button": "Шлях до движка арбітра",            
            "PGN_path_button": "Шлях до папки PGN",
            "Syzygy_tablebases_path_button": "Шлях до бази Syzygy",
                      
            "maximum_ply_before_setup_label": "Максимальна кількість ходів перед налаштуванням для ШІ",
            "engine_score_difference_maximum_label": "Верхня межа різниці оцінки движка для сингулярності",
            "engine_score_difference_minimum_label": "Нижня межа різниці оцінки движка для сингулярності",   
            "engine_safe_move_score_maximum_label": "Максимальна абсолютна оцінка для безпеки руху",            
            "engine_cusp_outer_range_checkbox": "зовнішній діапазон?",
            "engine_cusp_inner_range_checkbox": "внутрішній діапазон?",      
            "only_engine_one_setup_checkbox": "Тільки движок один встановлює?",
            "the_other_engine_chooses_recommended_color_checkbox": "Рекомендована кольорова схема іншої машини?",
            "no_choosing_color_directly_enable_checkbox": "Не можна обирати колір безпосередньо?",
            "engine_test_mode_enable_checkbox": "Режим перевірки машини",
        
            
            "time_limit_radio": "Час",
            "depth_limit_radio": "Глибина",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Час/глибина оцінки движка для кандидата в сингулярність",
            "engine_one_searching_limit_for_best_move_label": "Час/глибина на хід для движка один",   
            "engine_two_searching_limit_for_best_move_label": "Час/глибина на хід для движка два",
            "time_for_each_player_label": "Час для кожного гравця (секунди)",
            "reset_setting_button": "Скинути все",
            
            "modern_engine_mode_radio": "Сучасний движок",   
            "legacy_engine_mode_radio": "Старий движок",
            "output_PGN_checkbox": "Вивід PGN?",
            "pgn_auto_game_variant_detection_checkbox":"Змінити інтерфейс на основі PGN",
            "play_sound_checkbox": "Відтворювати звук?",
            "eval_bar_checkbox": "Показувати оцінку?",   
            "endgame_tablebase_checkbox": "Ендшпільна таблиця?",
            "player_one_name_label": "Встановити ім’я гравця один",      
            "player_two_name_label": "Встановити ім’я гравця два",
            "adjudicator_name_label": "Встановлення імені машини судді",
            "setting_ok_button": "Зберегти", 

            "tournament_game_number_label": "Номер гри турніру",
            "game_early_stop_draw_checkbox": "Раннє завершення при нічиї?", 
            "game_early_stop_win_checkbox": "Раннє завершення при перемозі?",
            "game_early_stop_label": "Різниця оцінок для раннього завершення",   
            "game_early_stop_minimum_moves_label": "Мінімальна кількість ходів для раннього завершення",
            "adjudicator_engine_enable_checkbox": "Движок арбітра?",      
            "tournament_start_button": "Почати турнір",
            "stop_tournament": "Зупинити турнір", 
            
            "start_game_button": "Почати гру",
            "stop_game_button": "Зупинити гру",     
            "reset_game_button": "Скинути",
            "chess_radio": "Шахи", 
            "cusp_chess_radio": "Шахи сингулярності",

            "player_one_label": "Гравець Один",
            "player_two_label": "Гравець Два",  
            
            "load_PGN_button": "Завантажити PGN",
            "play_PGN_previous_button": "Попередній",   
            "play_PGN_next_button": "Наступний",
            "beginning_PGN_button": "Початок",  
            "auto_play_PGN_button": "Авто-гру",
            "stop_play_PGN_button": "Зупинити гру",
            "clear_history_button": "Очистити історію", 
            
            "move_history_label": "Історія ходів",
            
            "setup_label_CC": "Налаштування для шахів сингулярності",   
            "setup_CC_color_to_move": "Хід кольору",
            "setup_CC_color_must_win": "Колір має виграти",      
            "Human_setup_confirmation_checkbox": "Налаштувати?",
            "Human_move_finished_button": "Хід завершено",   
            "Human_directly_choose_button": "Обрати безпосередньо",

            "Tournament_score":"Рахунок турніру",
            "Now_Score_is":"Поточний рахунок",

            "White_won":"Перемогли Білі. ",
            "Black_won":"Перемогли Чорні. ",
            "won":" виграв. ",
            "draw":"Нічия",
            "Draw_means_White_won":"Нічия означає, що перемогли Білі. ",
            "Draw_means_Black_won":"Нічия означає, що перемогли Чорні. ",
            "No_one_set_up_a_cusp_position":"Ніхто не встановив сингулярну позицію. ",
            "The_move_is_illegal":"Хід заборонено.",
            "empty":"",    
            
        },
        
        "ru": {
            "title": "Cusp Chess",
            "menu_Boards":"Доски",
            "menu_B_chess":"Шахматы",
            "menu_B_editor":"Редактор доски",
            "menu_B_blindfold":"Шахматы вслепую",
            "menu_Setting":"Настройка",
            "menu_S_Game_Setting":"Настройки игры",
            
            "white": "Белые",
            "black": "Чёрные",
            "AI": "ИИ",
            "Human": "Человек",

            "player_one_board_label_default": "Игрок Один",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: Белые или Чёрные?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: Я выбираю {color_must_win} напрямую",
                
            "player_two_board_label_default": "Игрок Два",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: Белые или Чёрные?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: Я выбираю {color_must_win} напрямую",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Шахматы сингулярность, Ничья означает поражение",
            "game_status_label_safe_CC": "Шахматы сингулярность, Ничья означает поражение",
            "game_status_label_searching": "Поиск позиции сингулярности",
            "game_status_label_player_must_setup": "{player_name} должен установить сейчас",
            "game_status_label_player_must_win": "Шахматы сингулярность, {color} должен выиграть",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Ходят: {color}",
            "editor_color_to_move_label": "Ходят: {color}",
            "editor_start_position": "Начальная позиция",
            "editor_clear_board":"Очистить доску",
            "editor_white_to_move_radio": "Белые ходят",            
            "editor_black_to_move_radio": "Чёрные ходят",
            "editor_auto_turn_rotation_checkbox":"Автоматическое поворачивание доски",
            "editor_engine_path_button": "Задать путь движка",               
            "editor_engine_analyse_checkbox": "Включить движок?",
            "editor_engine_time_or_depth_label": "Время/глубина поиска движка",
            "editor_engine_top_moves_label": "Лучшие ходы",
            "editor_engine_score_label": "Текущий счёт: ",
            "editor_engine_score_and_top_moves_search_button": "Поиск",   
            
            "editor_engine_search_for_cusps_label": "Поиск позиций сингулярности для шахмат сингулярность", 
            "editor_search_for_cusps_for_CC_confirm_button": "Искать",            

            "editor_cusp_stop_button": "Стоп",
            "editor_editor_export_board_fen_button": "Экспортировать FEN доски",
            "editor_clear_fen_history_button": "Очистить историю",
            "editor_set_board_fen_button": "Задать FEN доски",
            
            "engine_one_path_button": "Путь движка игрока один",
            "engine_two_path_button": "Путь движка игрока два",
            "engine_adjudicator_path_button": "Путь движка арбитра",            
            "PGN_path_button": "Путь к папке PGN",
            "Syzygy_tablebases_path_button": "Путь к папке таблиц Syzygy",
           
            "maximum_ply_before_setup_label": "Максимум полуходов перед настройкой ИИ",
            "engine_score_difference_maximum_label": "Верхняя граница разницы оценок движка для сингулярности",
            "engine_score_difference_minimum_label": "Нижняя граница разницы оценок движка для сингулярности", 
            "engine_safe_move_score_maximum_label": "Максимум абсолютной оценки для безопасного хода",            
            "engine_cusp_outer_range_checkbox": "Внешний диапазон?",
            "engine_cusp_inner_range_checkbox": "Внутренний диапазон?",      
            "only_engine_one_setup_checkbox": "Только движок один расставляет?",
            "the_other_engine_chooses_recommended_color_checkbox": "Рекомендуемая цветовая схема другой машины?",
            "no_choosing_color_directly_enable_checkbox": "Нельзя выбрать цвет напрямую?",
            "engine_test_mode_enable_checkbox": "Режим тестирования машины",
           
            
            "time_limit_radio": "Время",
            "depth_limit_radio": "Глубина",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Время/глубина оценки для кандидата сингулярности",
            "engine_one_searching_limit_for_best_move_label": "Время/глубина на ход для движка один",   
            "engine_two_searching_limit_for_best_move_label": "Время/глубина на ход для движка два",
            "time_for_each_player_label": "Время для каждого игрока (секунды)",
            "reset_setting_button": "Сбросить всё",
            
            "modern_engine_mode_radio": "Современный движок",   
            "legacy_engine_mode_radio": "Старый движок",
            "output_PGN_checkbox": "Вывод PGN?",
            "pgn_auto_game_variant_detection_checkbox":"Изменить интерфейс на основе PGN",
            "play_sound_checkbox": "Воспроизвести звук?",
            "eval_bar_checkbox": "Показать оценку?",   
            "endgame_tablebase_checkbox": "Эндшпильная база?",
            "player_one_name_label": "Задать имя игрока один",      
            "player_two_name_label": "Задать имя игрока два",
            "adjudicator_name_label": "Установка имени машиной арбитра",
            "setting_ok_button": "Сохранить", 

            "tournament_game_number_label": "Номер партии турнира",
            "game_early_stop_draw_checkbox": "Раннее окончание при ничьей?", 
            "game_early_stop_win_checkbox": "Раннее окончание при победе?",
            "game_early_stop_label": "Разница очков для раннего окончания",   
            "game_early_stop_minimum_moves_label": "Минимум ходов для раннего окончания",
            "adjudicator_engine_enable_checkbox": "Движок арбитр?",      
            "tournament_start_button": "Начать турнир",
            "stop_tournament": "Остановить турнир", 
            
            "start_game_button": "Начать игру",
            "stop_game_button": "Остановить игру",     
            "reset_game_button": "Сброс",
            "chess_radio": "Шахматы", 
            "cusp_chess_radio": "Шахматы сингулярность",

            "player_one_label": "Игрок Один",
            "player_two_label": "Игрок Два",  
            
            "load_PGN_button": "Загрузить PGN",
            "play_PGN_previous_button": "Предыдущий",   
            "play_PGN_next_button": "Следующий",
            "beginning_PGN_button": "Начало",  
            "auto_play_PGN_button": "Автовоспроизведение",
            "stop_play_PGN_button": "Остановить воспроизведение",
            "clear_history_button": "Очистить историю", 
            
            "move_history_label": "История ходов",
            
            "setup_label_CC": "Настройка для шахмат сингулярности",   
            "setup_CC_color_to_move": "Ходят",
            "setup_CC_color_must_win": "Цвет должен выиграть",      
            "Human_setup_confirmation_checkbox": "Настроить?",
            "Human_move_finished_button": "Ход завершён",   
            "Human_directly_choose_button": "Выбрать напрямую",

            "Tournament_score":"Турнирный счёт",
            "Now_Score_is":"Текущий счёт",

            "White_won":"Белые выиграли. ",
            "Black_won":"Чёрные выиграли. ",
            "won":" выиграл. ",
            "draw":"Ничья",
            "Draw_means_White_won":"Ничья означает, что выиграли Белые. ",
            "Draw_means_Black_won":"Ничья означает, что выиграли Чёрные. ",
            "No_one_set_up_a_cusp_position":"Никто не установил позицию сингулярности. ",
            "The_move_is_illegal":"Ход недопустим.",
            "empty":"",    
            
        },        
    }

def register_widget(cusp_app, widget, key, **kwargs):
    logger.info("register_widget")
    """
    key may be a string (translation key) or a callable returning the key.
    kwargs values may be plain values or callables returning the value.
    """
    cusp_app.widget_registry[widget] = (key, kwargs)
    update_widget(cusp_app, widget)

def resolve( maybe_callable):
    return maybe_callable() if callable(maybe_callable) else maybe_callable

def update_widget(cusp_app, widget):
    """Update just one registered widget"""
    # for widget in list(cusp_app.widget_registry.keys()):
        # if not widget.winfo_exists():
            # cusp_app.widget_registry.pop(widget)
        
    if widget not in cusp_app.widget_registry:
        logger.info('no widget now')
        return
    if widget is None or not widget.winfo_exists():
        logger.info('widget does not exist anymore')
        return
    key_or_callable, kwargs = cusp_app.widget_registry[widget]
    key = resolve(key_or_callable)
    lang_dict = cusp_app.translations[cusp_app.current_lang]
    template = lang_dict.get(key, f"[{key}]")
    resolved_kwargs = {k: resolve(v) for k, v in kwargs.items()}
    try:
        widget.config(text=template.format(**resolved_kwargs))
    except KeyError as e:
        logger.exception(f"update_widget, [Missing {e.args[0]}]")
        widget.config(text=f"[Missing {e.args[0]}]")
        
def update_texts(cusp_app):
    logger.info("update_texts")
    """Refresh all registered widgets"""
    cusp_app.title(cusp_app.translations[cusp_app.current_lang]["title"])
    update_menus(cusp_app)
    update_spinboxes(cusp_app)       
           
    for widget in cusp_app.widget_registry.keys():
        update_widget(cusp_app, widget)
        #print(cusp_app.widget_registry[widget])

def update_menus(cusp_app):
    logger.info("update_menus")
    cusp_app.menubar.entryconfig(1, label=cusp_app.translations[cusp_app.current_lang]["menu_Boards"])
    cusp_app.menubar.entryconfig(2, label=cusp_app.translations[cusp_app.current_lang]["menu_Setting"])

    cusp_app.Boards_menu.entryconfig(0, label=cusp_app.translations[cusp_app.current_lang]["menu_B_chess"])
    cusp_app.Boards_menu.entryconfig(1, label=cusp_app.translations[cusp_app.current_lang]["menu_B_editor"])
    cusp_app.Boards_menu.entryconfig(2, label=cusp_app.translations[cusp_app.current_lang]["menu_B_blindfold"])

    cusp_app.setting_menu.entryconfig(0, label=cusp_app.translations[cusp_app.current_lang]["menu_S_Game_Setting"])

def update_spinboxes(cusp_app):
    logger.info("update_spinboxes")
    players=(cusp_app.translations[cusp_app.current_lang]["AI"],cusp_app.translations[cusp_app.current_lang]["Human"])
    cusp_app.player_one_spinbox.config(values=players)
    cusp_app.player_two_spinbox.config(values=players)
    p=players[cusp_app.player_one_spinbox_chosen]
    cusp_app.player_one_spinbox_var.set(p)
    
    p=players[cusp_app.player_two_spinbox_chosen]
    cusp_app.player_two_spinbox_var.set(p)

    side=(cusp_app.translations[cusp_app.current_lang]["white"],cusp_app.translations[cusp_app.current_lang]["black"])
    cusp_app.color_to_move_spinbox.config(values=side)
    cusp_app.color_must_win_spinbox.config(values=side)
    
    v = side[cusp_app.color_to_move_spinbox_chosen]
    cusp_app.color_to_move_spinbox_var.set(v)
    
    v = side[cusp_app.color_must_win_spinbox_chosen]
    cusp_app.color_must_win_spinbox_var.set(v)
    
def player_one_label_dynamic_key(cusp_app):
    logger.info("player_one_label_dynamic_key")
    return cusp_app.player_one_label_state

            
def player_one_label_dynamic_kwargs(cusp_app):
    logger.info("player_one_label_dynamic_kwargs")
    return{"player_one_name":lambda:cusp_app.player_one_name,
            "color_chosen": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_chosen_in_setup_phase == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_chosen_in_setup_phase == "B" else None ),
            "color_must_win": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_must_win_in_cusp_chess == "B" else None)
            }

def player_two_label_dynamic_key(cusp_app):
    logger.info("player_two_label_dynamic_key")
    return cusp_app.player_two_label_state
    
def player_two_label_dynamic_kwargs(cusp_app):
    logger.info("player_two_label_dynamic_kwargs")
    return{"player_two_name":lambda:cusp_app.player_two_name,
        "color_chosen": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_chosen_in_setup_phase == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_chosen_in_setup_phase == "B" else None ),
        "color_must_win": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_must_win_in_cusp_chess == "B" else None )
    }
  
def game_status_label_dynamic_key(cusp_app):
    logger.info("game_status_label_dynamic_key")
    return cusp_app.game_status_label_state

def game_status_label_dynamic_kwargs(cusp_app):
    logger.info("game_status_label_dynamic_kwargs")
    return {"player_name": lambda:cusp_app.game_status_label_player_name,
            "color" : lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else cusp_app.translations[cusp_app.current_lang]["black"],
            "result": lambda: cusp_app.result_str
    }
   
def color_to_move_label_dynamic_kwargs(cusp_app):
    logger.info("color_to_move_label_dynamic_kwargs")
    return{"color":lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_to_move_label_state=='White' else (cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_to_move_label_state=='Black' else None)}
    
def editor_color_to_move_label_dynamic_kwargs(cusp_app):
    logger.info("editor_color_to_move_label_dynamic_kwargs")
    return{"color":lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.editor_color_to_move_label_state=='White' else (cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.editor_color_to_move_label_state=='Black' else None)}
        
def pgn_auto_play_label_dynamic_key(cusp_app):
    logger.info("pgn_auto_play_label_dynamic_key")
    return cusp_app.pgn_auto_play_label_state
    
def blindfold_label_dynamic_key(cusp_app):
    logger.info("blindfold_label_dynamic_key")
    return cusp_app.blindfold_label_state    