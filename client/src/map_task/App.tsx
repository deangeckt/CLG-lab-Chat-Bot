import React from 'react';
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Slide,
    Typography,
} from '@material-ui/core';
import Timer from './Timer';
import { useContext } from 'react';
import { TransitionProps } from '@material-ui/core/transitions';
import { AppContext } from '../AppContext';
import { useApp } from './useApp';
import Header from '../common/Header';
import './App.css';
import { role_strings } from '../Wrapper';

const Transition = React.forwardRef(function Transition(
    props: TransitionProps & {
        children: React.ReactElement<any, any>;
    },
    ref: React.Ref<unknown>,
) {
    return <Slide direction="up" ref={ref} {...props} />;
});

function App(): JSX.Element {
    const { state } = useContext(AppContext);
    const { navigate_to_end_page } = useApp();
    const role_string = role_strings[state.game_config.game_role];

    return (
        <div className="App">
            <Header />
            <Dialog
                open={state.game_state.end}
                TransitionComponent={Transition as any}
                keepMounted
                onClose={navigate_to_end_page}
            >
                <DialogTitle>{state.game_state.end_modal_title}</DialogTitle>
                <DialogContent>
                    <DialogContentText>{state.game_state.end_modal_text}</DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="outlined"
                        color="primary"
                        onClick={navigate_to_end_page}
                    >
                        Next
                    </Button>
                </DialogActions>
            </Dialog>

            <div className="App_Header">
                <Typography variant="h4">Your role: {role_string}</Typography>
                {state.game_config.game_mode == 'bot' ? <Timer /> : null}
            </div>
            <div className="App_Container">
                <MapCanvas />
                <Chat />
            </div>
        </div>
    );
}

export default App;
