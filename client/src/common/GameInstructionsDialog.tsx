import React, { useEffect, useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide } from '@material-ui/core';
import { useContext } from 'react';
import { TransitionProps } from '@material-ui/core/transitions';
import { AppContext } from '../AppContext';
import { role_strings } from '../Wrapper';
import { useGameInstructions } from './useGameInstructions';
import { ins_instructions_str, nav_instructions_str, nav_sub_title_str } from './strings';

const Transition = React.forwardRef(function Transition(
    props: TransitionProps & {
        children: React.ReactElement<any, any>;
    },
    ref: React.Ref<unknown>,
) {
    return <Slide direction="up" ref={ref} {...props} />;
});

interface Dictionary {
    [Key: number]: string[];
}

function GameInstructionsDialog({}): JSX.Element {
    const { state } = useContext(AppContext);
    const [im, setIm] = useState<HTMLImageElement>();

    const { setGameInstructions } = useGameInstructions();

    const role_string = role_strings[state.game_config.game_role];
    const role_instructions_dict: Dictionary = {
        0: nav_instructions_str,
        1: ins_instructions_str,
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

        let img_map_name = '';
        if (state.game_config.game_role == 1) img_map_name = state.map_metadata.im_src;
        else {
            const prefix = state.map_metadata.im_src.split('.jpg')[0];
            img_map_name = prefix + '_nav.jpg';
        }

        image.src = require(`../map_task/maps/${img_map_name}`);
    }, []);

    return (
        <>
            <Dialog
                open={state.game_state.open_instructions}
                TransitionComponent={Transition as any}
                keepMounted
                onClose={() => setGameInstructions(false)}
            >
                <DialogTitle style={{ fontSize: '1.5rem' }}>Game instructions</DialogTitle>
                <DialogContent>
                    <DialogContentText style={{ fontSize: '1.25rem' }}>
                        {nav_sub_title_str} {role_string}.
                    </DialogContentText>
                    {role_instructions.map((e) => (
                        <DialogContentText key={e}>{e}</DialogContentText>
                    ))}

                    <DialogContentText>Enjoy the game!</DialogContentText>

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
