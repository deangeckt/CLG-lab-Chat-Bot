import React, { useState } from 'react';
import { AppContext } from './AppContext';

export interface IAppState {
    a: string;
}

export const init_app_state: IAppState = {
    a: 'first string',
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(init_app_state);

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
