import React, { useContext } from 'react';
import { AppContext } from '../AppContext';
import { TextField } from '@material-ui/core';
import './Chat.css';

function Chat(): JSX.Element {
    const { state, setState } = useContext(AppContext);

    return (
        <div className="chat_container">
            <TextField id="outlined-basic" label="Outlined" variant="outlined" />
        </div>
    );
}

export default Chat;
