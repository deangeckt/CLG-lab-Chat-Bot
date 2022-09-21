import React from 'react';
import { Button, MenuItem, TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { UserMetadata } from '../Wrapper';
import Header from '../common/Header';
import './Home.css';

const genders = ['Male', 'Female', 'Other'];

function Home(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();
    const routeChange = () => {
        const path = `map_task`;
        navigate(path);
    };

    const simple_set = (e: any, field: keyof UserMetadata) => {
        const metadata = state.user_metadata;
        metadata[field] = e.target.value.toString();
        setState({ ...state, metadata: metadata });
    };

    return (
        <div className="Home">
            <Header />

            <div className="Home_Container">
                <Typography variant="h4">Welcome to CLG map task</Typography>
                <Typography variant="h5">Fill in your details por favor</Typography>
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
                <Button style={{ textTransform: 'none' }} variant="outlined" color="primary" onClick={routeChange}>
                    Start
                </Button>
            </div>
        </div>
    );
}

export default Home;
