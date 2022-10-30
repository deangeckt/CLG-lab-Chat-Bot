import React, { useEffect, useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide } from '@material-ui/core';
import { useContext } from 'react';
import { TransitionProps } from '@material-ui/core/transitions';
import { AppContext } from '../AppContext';
import { Dictionary, role_strings } from '../Wrapper';
import { useGameInstructions } from './useGameInstructions';

const Transition = React.forwardRef(function Transition(
    props: TransitionProps & {
        children: React.ReactElement<any, any>;
    },
    ref: React.Ref<unknown>,
) {
    return <Slide direction="up" ref={ref} {...props} />;
});

function GameInstructionsDialog({}): JSX.Element {
    const { state } = useContext(AppContext);
    const [im, setIm] = useState<HTMLImageElement>();

    const { setGameInstructions } = useGameInstructions();

    const role_string = role_strings[state.game_config.game_role];
    const role_instructions_dict: Dictionary = {
        0: 'You should navigate towrads some object in the map in a specific path. to learn the path chat with the game instructor. to navigate on the map you can either use the keyboard or the mouse - click on the green dots',
        1: 'You should instruct the naviagator to follow the path via the chat. the path is only visable to you.',
    };
    const role_instructions = role_instructions_dict[state.game_config.game_role];

    useEffect(() => {
        const image = new Image();
        image.onload = function () {
            setIm(image);
        };
        image.onerror = function (err) {
            console.log('img load err', err);
        };

        image.src = require(`../map_task/maps/${state.map_metadata.im_src}`);
    }, []);

    return (
        <>
            <Dialog
                open={state.game_state.open_instructions}
                TransitionComponent={Transition as any}
                keepMounted
                onClose={() => setGameInstructions(false)}
            >
                <DialogTitle>Game instructions</DialogTitle>
                <DialogContent>
                    <DialogContentText>Your role is the {role_string}.</DialogContentText>
                    <DialogContentText>{role_instructions}</DialogContentText>
                    <img
                        src={im?.src}
                        width={state.map_metadata.im_width / 5}
                        height={state.map_metadata.im_height / 5}
                    />
                </DialogContent>
                <DialogActions>
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="outlined"
                        color="primary"
                        onClick={() => setGameInstructions(false)}
                    >
                        Ok
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default GameInstructionsDialog;
