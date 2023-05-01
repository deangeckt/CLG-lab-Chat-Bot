import React, { useContext } from 'react';
import { Box, Button, CircularProgress, Typography } from '@material-ui/core';
import { AppContext } from '../AppContext';
import { maps } from '../Wrapper';
import { bot_welcome_str } from '../common/strings';
import { useNavigate } from 'react-router-dom';
import { register } from '../api';
import Header from '../common/Header';
import { main_blue } from '../common/colors';
import './Consent.css';

const consent_txt1 =
    'The purpose of this research study is to better understand the linguistic properties of written, online conversations. For this reason, we will be asking participants to complete a Map Task that involves giving directions to a conversational partner via a chat interface (20 minutes), followed by a language history questionnaire and exit survey (5-10 minutes). There are no foreseeable risks associated with this project, nor are there any direct benefits to you. However, your participation will allow researchers to better understand how language is used in an informal, written, online setting.';
const consent_txt2 = (amount: string) =>
    `If you choose to participate, your data will be associated only with your Prolific ID, not your real name, making it difficult to link your responses back to you. If you complete the study, you will be paid ${amount} as a token of our appreciation for your participation. Your participation is voluntary, and you may withdraw from the study at any time by simply closing your browser window. If you decide to withdraw after you have submitted responses, your responses will be retained by the researchers along with all other data associated with this project. This study is being conducted by Dr. Shuly Wintner (shuly@cs.haifa.ac.il) and Dr. Melinda Fricke (melinda.fricke@pitt.edu), who can be reached by email if you have any questions.`;

function Conset(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    React.useEffect(() => {
        const game_config = state.game_config;
        if (game_config.registerd === 'yes') return;
        register(game_config.map_index, game_config.game_role, register_cb);

        game_config.registerd = 'load';
        setState({ ...state, game_config });
    }, []);

    const register_cb = (data: any) => {
        const game_config = state.game_config;
        const map_index = game_config.map_index;
        const map_metadata = maps[map_index];

        let server_version = '';
        game_config.registerd = 'yes';

        if (data) {
            server_version = data.version;
            game_config.guid = data.guid;
            const map = map_metadata.im_src.split('_')[0];
            map_metadata.im_src = `${map}_${game_config.game_role}.jpg`;
        } else {
            game_config.registerd = 'err';
        }
        let chat = [...state.chat];
        chat = chat.concat([{ id: 1 - state.game_config.game_role, msg: bot_welcome_str, timestamp: Date.now() }]);

        setState({
            ...state,
            game_config,
            chat,
            map_metadata,
            user_map_path: [maps[map_index].start_cell],
            server_version,
        });
    };

    const onClick = () => {
        setState({ ...state, consent: true });
        navigate('/map_task');
    };

    const redner_conset = () => {
        return (
            <>
                <h6 style={{ margin: '2em', textAlign: 'start', fontSize: 18, fontWeight: 400 }}>
                    {consent_txt1} <br /> <br /> {consent_txt2('5$')}
                </h6>
                <Button
                    className="register_btn"
                    style={{ textTransform: 'none' }}
                    variant="outlined"
                    color="primary"
                    onClick={() => onClick()}
                >
                    Accept
                </Button>
            </>
        );
    };

    return (
        <div className="conset">
            <Header />
            <div className="conset_container">
                {state.game_config.registerd === 'err' && (
                    <Typography variant="h5" style={{ margin: '16px' }}>
                        An errur occured, please try again later
                    </Typography>
                )}
                {state.game_config.registerd === 'yes' && redner_conset()}
                {state.game_config.registerd === 'load' && (
                    <Box sx={{ display: 'flex', margin: '32px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                )}
            </div>
        </div>
    );
}

export default Conset;
