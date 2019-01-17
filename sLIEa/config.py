# -*- coding: utf-8 -*-
import re

class Config(object):
    
    KOMOE_HTTP_UA_DROID = "Mozilla/5.0 KomoeSDK"
    
    # GVG API URL
    ChangeAiModeUrl = "/api/gvg/change_ai_mode";
    ChangeDeckPlayerUrl = "/api/gvg/change_deck_player";
    GetArtListUrl = "/api/gvg/get_art_list";
    GetBattleHistoryUrl = "/api/gvg/get_battle_history";
    GetCurrentDeckDataUrl = "/api/gvg/get_current_deck_data";
    GetDeckListUrl = "/api/gvg/get_deck_list";
    GetPartySequenceChangeMemberListUrl = "/api/gvg/get_party_sequence_change_member_list";
    GetInfoUrl = "/api/gvg/get_info";
    ReloadDeckUrl = "/api/gvg/reload_deck";
    GetSpRecoverWaveInfoUrl = "/api/gvg/get_sp_recovery_wave_info";
    StartSpRecoveryUrl = "/api/gvg/start_sp_recovery";
    EndSpRecoveryUrl = "/api/gvg/end_sp_recovery";
    SendNotificationToGuildMemberUrl = "/api/gvg/send_notification_to_guild_member";
    
    # Quest Battle Api
    ChangeAiModeUrl = "/api/quest_battle/change_ai_mode";
    GetArtListUrl = "/api/quest_battle/get_art_list";
    GetCurrentDeckDataUrl = "/api/quest_battle/get_current_deck_data";
    GetInfoUrl = "/api/quest_battle/get_info";
    InitializeStageUrl = "/api/quest_battle/initialize_stage";
    JoinStageUrl = "/api/quest_battle/join_stage";
    ReloadDeckUrl = "/api/quest_battle/reload_deck";
    QuestContinueUrl = "/api/quest_battle/quest_continue";
    FinalizeStageForUserUrl = "/api/quest_battle/finalize_stage_for_user";
    WaveClearUrl = "/api/quest_battle/wave_clear";
    WaveStartUrl = "/api/quest_battle/wave_start";
    GetPlayerMemberInfoUrl = "/api/quest_battle/get_player_member_info";
    
    
    CryptKey = 'ABCDEFGHIJKLMNOP'
    CryptKey_req = "DW0-KLO-C7"
    
    
    Service = {
        'SrvVERSION': '', #maskWordVersion
        'checkFilterWords': '' #checkMaskWord
    }

    
    payloads = {
      "payload": None,
      "requestid": None,
      "uuid": None,
      "userId": None,
      "sessionId": None,
      "actionToken": None,
      "access_token": None,
      "ctag": None,
      "actionTime": 131917203325430000
    }
    
    def __init__(self):
        pass