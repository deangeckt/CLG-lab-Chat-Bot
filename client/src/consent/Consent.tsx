import React, { useContext } from 'react';
import { Box, Button, CircularProgress, Typography } from '@material-ui/core';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';
import Header from '../common/Header';
import { main_blue } from '../common/colors';
import { useRegister } from '../useRegister';
import './Consent.css';

const consent_txt1 =
    'The purpose of this research study is to better understand the linguistic properties of written, online conversations. For this reason, we will be asking participants to complete a Map Task that involves giving directions to a conversational partner via a chat interface (20 minutes), followed by a language history questionnaire and exit survey (5-10 minutes). There are no foreseeable risks associated with this project, nor are there any direct benefits to you. However, your participation will allow researchers to better understand how language is used in an informal, written, online setting.';
const consent_txt2 = (amount: string) =>
    `If you choose to participate, your data will be associated only with your Prolific ID, not your real name, making it difficult to link your responses back to you. If you complete the study, you will be paid ${amount} as a token of our appreciation for your participation. Your participation is voluntary, and you may withdraw from the study at any time by simply closing your browser window. If you decide to withdraw after you have submitted responses, your responses will be retained by the researchers along with all other data associated with this project. This study is being conducted by Dr. Shuly Wintner (shuly@cs.haifa.ac.il) and Dr. Melinda Fricke (melinda.fricke@pitt.edu), who can be reached by email if you have any questions.`;

function Conset(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const { register_game } = useRegister();
    const navigate = useNavigate();

    React.useEffect(() => {
        if (state.registerd === 'yes') return;
        register_game(0);
    }, []);

    const onClick = () => {
        setState({ ...state, consent: true });
        navigate('/map_task');
    };

    const redner_conset = () => {
        return (
            <>
                <h6 className="consentText">
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
                {state.registerd === 'err' && (
                    <Typography variant="h5" style={{ margin: '16px' }}>
                        An errur occured, please try again later
                    </Typography>
                )}
                {state.registerd === 'yes' && redner_conset()}
                {state.registerd === 'load' && (
                    <Box sx={{ display: 'flex', margin: '32px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                )}
            </div>
        </div>
    );
}

export default Conset;
