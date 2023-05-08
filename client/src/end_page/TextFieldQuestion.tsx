import React from 'react';
import { TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { IQuestionInterface } from '../Wrapper';

function TextFieldQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const survey = data.survey === 'general' ? state.general_survey : state.games[state.curr_game].map_survey;

    const simple_set = (e: any) => {
        survey[data.id].answer = e.target.value.toString();
        if (data.survey === 'general') setState({ ...state, general_survey: survey });
        else {
            const games = [...state.games];
            games[state.curr_game].map_survey = survey;
            setState({ ...state, games: games });
        }
    };

    return (
        <div className="QuestionGroup">
            <div style={{ width: '50%', display: 'flex', flexDirection: 'column' }}>
                <Typography component="legend" align="left">
                    {data.meta.question}
                </Typography>
                {data.meta.questionCont ? (
                    <Typography variant="caption" align="left">
                        {data.meta.questionCont}
                    </Typography>
                ) : null}
            </div>

            <TextField
                style={{ width: '50%' }}
                id={data.id}
                label="type here"
                variant="outlined"
                onChange={(event) => simple_set(event)}
                type={data.meta.numberText ? 'number' : undefined}
                value={survey[data.id].answer}
            />
        </div>
    );
}

export default TextFieldQuestion;
