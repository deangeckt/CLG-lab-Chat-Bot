import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { Message } from 'react-chat-ui';

export interface UserMetadata {
    name: string;
    age: string;
    gender: string;
}

export interface UserSurvey {
    free_text: string;
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
}

export interface GameState {
    end: boolean;
    end_modal_text: string;
    end_modal_title: string;
    init_time: number;
}

export interface IAppState {
    chat: Message[];
    map_metadata: MapMetadata;
    user_map_path: MapCellIdx[];
    user_metadata: UserMetadata;
    user_survey: UserSurvey;
    game_state: GameState;
}

export const init_app_state: IAppState = {
    chat: [new Message({ id: 1, message: 'Welcome!' })],
    user_metadata: { name: '', age: '', gender: 'Male' },
    map_metadata: {
        im_width: 1413,
        im_height: 1052,
        im_src: 'map1.png',
        rows: 18,
        cols: 24,
        end_cell: { r: 16, c: 7 },
    },
    user_map_path: [{ r: 2, c: 23 }],
    user_survey: { free_text: '' },
    game_state: { end: false, end_modal_text: '', end_modal_title: 'Game is over', init_time: 300 },
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(init_app_state);

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
