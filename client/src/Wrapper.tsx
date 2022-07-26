import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { Message } from 'react-chat-ui';

export interface IAppState {
    chat: Message[];
}

export const init_app_state: IAppState = {
    chat: [new Message({ id: 1, message: 'Welcome!' })],
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(init_app_state);

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
