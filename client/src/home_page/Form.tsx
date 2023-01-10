import React from 'react';
import { Button, MenuItem, TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext, useState } from 'react';
import { AppContext } from '../AppContext';
import { gameRegister, UserMetadata } from '../Wrapper';
import { home_page_form_title1 } from '../common/strings';
import './Home.css';

const genders = ['Male', 'Female', 'Other'];

function Form(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [finish, setFinish] = useState(false);

    const simple_set = (e: any, field: keyof UserMetadata) => {
        const user_metadata = state.user_metadata;
        user_metadata[field] = e.target.value.toString();
        setState({ ...state, user_metadata });
        const is_finish = user_metadata.name != '' && user_metadata.age != '';
        setFinish(is_finish);
    };

    const set_register_state = (r: gameRegister = 'choose_map') => {
        const game_config = state.game_config;
        game_config.registerd = r;
        setState({ ...state, game_config });
    };

    return (
        <div className="form">
            <Typography variant="h5">{home_page_form_title1}</Typography>
            <TextField
                id="outlined-basic"
                label="Name"
                variant="outlined"
                onChange={(event) => simple_set(event, 'name')}
            />
            <TextField
                id="outlined-basic"
                label="Age"
                type="number"
                variant="outlined"
                onChange={(event) => simple_set(event, 'age')}
            />
            <TextField
                variant="outlined"
                id="outlined-basic"
                select
                label="Select"
                value={state.user_metadata.gender}
                onChange={(event) => simple_set(event, 'gender')}
            >
                {genders.map((option) => (
                    <MenuItem key={option} value={option}>
                        {option}
                    </MenuItem>
                ))}
            </TextField>
            <Button
                disabled={!finish}
                style={{ textTransform: 'none' }}
                variant="outlined"
                color="primary"
                onClick={() => set_register_state()}
            >
                Start
            </Button>
        </div>
    );
}

export default Form;
