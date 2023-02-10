import React from 'react';
import { TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { IQuestionInterface } from '../Wrapper';

function TextFieldQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);

    const simple_set = (e: any) => {
        const user_survey = state.user_survey;
        user_survey[data.id].answer = e.target.value.toString();
        setState({ ...state, user_survey });
    };

    return (
        <div className="QuestionGroup" style={{ flexDirection: data.meta.isStyleHoriz ? 'row' : 'column' }}>
            <Typography component="legend">{data.meta.question}</Typography>
            {data.meta.questionCont ? <Typography variant="caption">{data.meta.questionCont}</Typography> : null}
            <TextField
                style={{ width: '25%', margin: '8px' }}
                id={data.id}
                label="type here"
                variant="outlined"
                onChange={(event) => simple_set(event)}
                type={data.meta.numberText ? 'number' : undefined}
            />
        </div>
    );
}

export default TextFieldQuestion;
