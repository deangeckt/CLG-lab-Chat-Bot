import React from 'react';
import { MenuItem, TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { IQuestionInterface } from '../Wrapper';

function SelectQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);

    const simple_set = (e: any) => {
        const user_survey = state.user_survey;
        user_survey[data.id].answer = e.target.value.toString();
        setState({ ...state, user_survey });
    };

    return (
        <div className="QuestionGroup" style={{ flexDirection: data.meta.isStyleHoriz ? 'row' : 'column' }}>
            <Typography style={{ margin: '8px' }} component="legend">
                {data.meta.question}
            </Typography>
            <TextField
                onChange={(event) => simple_set(event)}
                id={data.id}
                select
                label="Select"
                defaultValue={data.meta.selectOptions![0]}
            >
                {data.meta.selectOptions!.map((option) => (
                    <MenuItem key={option} value={option}>
                        {option}
                    </MenuItem>
                ))}
            </TextField>
        </div>
    );
}

export default SelectQuestion;
