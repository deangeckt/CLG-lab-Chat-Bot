import React from 'react';
import { Button, TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { UserSurvey } from '../Wrapper';
import './EndPage.css';

function EndPage(): JSX.Element {
    const { state, setState } = useContext(AppContext);

    const simple_set = (e: any, field: keyof UserSurvey) => {
        const metadata = state.user_survey;
        metadata[field] = e.target.value.toString();
        setState({ ...state, metadata: metadata });
    };

    const send = () => {
        console.log('send');
    };

    return (
        <div className="End">
            <Header />
            <div className="End_Container">
                <Typography variant="h4">Gracias for participating</Typography>
                <TextField
                    id="outlined-basic"
                    label="What did you think?"
                    variant="outlined"
                    onChange={(event) => simple_set(event, 'free_text')}
                />
                <Button style={{ textTransform: 'none' }} variant="outlined" color="primary" onClick={send}>
                    Send
                </Button>
            </div>
        </div>
    );
}

export default EndPage;
