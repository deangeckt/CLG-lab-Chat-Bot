import React, { useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide } from '@material-ui/core';
import { useContext } from 'react';
import { TransitionProps } from '@material-ui/core/transitions';
import { AppContext } from '../AppContext';
import { Dictionary, role_strings } from '../Wrapper';

const Transition = React.forwardRef(function Transition(
    props: TransitionProps & {
        children: React.ReactElement<any, any>;
    },
    ref: React.Ref<unknown>,
) {
    return <Slide direction="up" ref={ref} {...props} />;
});

function GameInstructionsDialog(): JSX.Element {
    const [open, setOpen] = useState(true);
    const { state } = useContext(AppContext);
    const role_string = role_strings[state.game_config.game_role];
    const role_instructions_dict: Dictionary = {
        0: 'you should navigate towrads the treasure',
        1: 'you should instruct the naviagator towrads the treasure',
    };
    const role_instructions = role_instructions_dict[state.game_config.game_role];

    return (
        <>
            <Dialog open={open} TransitionComponent={Transition as any} keepMounted onClose={() => setOpen(false)}>
                <DialogTitle>Your role: {role_string}</DialogTitle>
                <DialogContent>
                    <DialogContentText>{role_instructions}</DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="outlined"
                        color="primary"
                        onClick={() => setOpen(false)}
                    >
                        Start
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default GameInstructionsDialog;
