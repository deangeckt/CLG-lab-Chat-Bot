import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { Message } from 'react-chat-ui';

export interface MapCoord {
    x: number;
    y: number;
}

export interface Metadata {
    name: string;
    age: string;
    gender: string;
}

export interface IAppState {
    chat: Message[];
    curr_corrd: MapCoord;
    metadata: Metadata;
}

export const init_app_state: IAppState = {
    chat: [new Message({ id: 1, message: 'Welcome!' })],
    curr_corrd: { x: 0.96, y: 0.091 },
    metadata: { name: '', age: '', gender: 'Male' },
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(init_app_state);

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
