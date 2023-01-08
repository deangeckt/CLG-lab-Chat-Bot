import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { game_over_modal_str } from './common/strings';

export interface UserMetadata {
    name: string;
    age: string;
    gender: string;
}

export interface UserSurvey {
    survey_instructions: string;
    survey_bot: string;
}

export interface MapCellIdx {
    r: number;
    c: number;
}

export interface MapMetadata {
    im_width: number;
    im_height: number;
    im_src: string;
    rows: number;
    cols: number;
    end_cell: MapCellIdx;
    start_cell: MapCellIdx;
    bot_support?: boolean;
    map_idx: number;
}

export type gameMode = 'bot' | 'human';
export type gameRegister = 'yes' | 'no' | 'load' | 'choose_map' | 'fill_details' | 'err';
export type gameRole = number;
export interface Dictionary {
    [Key: number]: string;
}
export const role_strings: Dictionary = { 0: 'navigator', 1: 'instructor' };

export interface GameState {
    end: boolean;
    started: boolean;
    end_modal_text: string;
    end_modal_title: string;
    init_time: number;
    game_time: number;
    open_instructions: boolean;
}

export interface GameConfig {
    game_mode?: gameMode;
    game_role: gameRole;
    registerd: gameRegister;
    guid: string;
}

export interface ChatMsg {
    id: gameRole;
    msg: string;
    timestamp: number;
    curr_nav_cell?: MapCellIdx;
}

export interface IAppState {
    chat: ChatMsg[];
    map_metadata: MapMetadata;
    user_map_path: MapCellIdx[];
    user_metadata: UserMetadata;
    user_survey: UserSurvey;
    game_state: GameState;
    game_config: GameConfig;
    clinet_version: string;
    server_version: string;
}

export const maps: MapMetadata[] = [
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map1_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 16, c: 7 },
        start_cell: { r: 2, c: 23 },
        bot_support: true,
        map_idx: 0,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map2_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 12, c: 6 },
        start_cell: { r: 2, c: 20 },
        bot_support: true,
        map_idx: 1,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map3_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 13, c: 9 },
        start_cell: { r: 3, c: 9 },
        bot_support: true,
        map_idx: 2,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map4_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 7, c: 0 },
        start_cell: { r: 3, c: 23 },
        map_idx: 3,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map5_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 16, c: 9 },
        start_cell: { r: 1, c: 1 },
        map_idx: 4,
    },
];

export const init_app_state: IAppState = {
    chat: [],
    user_metadata: { name: '', age: '', gender: 'Male' },
    map_metadata: maps[0],
    user_map_path: [],
    user_survey: { survey_instructions: '', survey_bot: '' },
    game_state: {
        end: false,
        started: false,
        end_modal_text: '',
        end_modal_title: game_over_modal_str,
        init_time: 300,
        game_time: 0,
        open_instructions: true,
    },
    game_config: { game_role: 0, registerd: 'no', guid: '' },
    clinet_version: '1.2.1_e',
    server_version: '',
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(JSON.parse(JSON.stringify(init_app_state)));

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
