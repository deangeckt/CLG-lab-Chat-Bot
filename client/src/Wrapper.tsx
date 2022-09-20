import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { Message } from 'react-chat-ui';

export interface UserMetadata {
    name: string;
    age: string;
    gender: string;
}

export interface MapCoord {
    x: number;
    y: number;
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
    start_cell: MapCellIdx;
}

export interface IAppState {
    chat: Message[];
    map_metadata: MapMetadata;
    curr_map_cell: MapCellIdx;
    user_map_path: MapCellIdx[];
    user_metadata: UserMetadata;
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
        start_cell: { r: 2, c: 23 },
    },
    curr_map_cell: { r: 2, c: 23 },
    user_map_path: [{ r: 2, c: 23 }],
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(init_app_state);

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
