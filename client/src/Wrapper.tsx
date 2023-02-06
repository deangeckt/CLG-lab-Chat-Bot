import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { game_over_modal_str } from './common/strings';

export interface UserMetadata {
    name: string;
    age: string;
    gender: string;
}

export type UserSurveyType = 'rating' | 'textfield' | 'select';

export interface UserSurveyQuestion {
    question: string;
    answer: number | null | string;
    type: UserSurveyType;
    hintAbove?: string;
    sliderLeftText?: string;
    slideRightText?: string;
    numberText?: boolean;
    selectOptions?: string[];
    isStyleHoriz?: boolean;
    questionCont?: string;
}

export interface IQuestionInterface {
    meta: UserSurveyQuestion;
    id: string;
}

export interface UserSurvey {
    [Key: string]: UserSurveyQuestion;
}

export interface MapCellIdx {
    r: number;
    c: number;
}

export interface MapMetadata {
    im_width: number;
    im_height: number;
    im_src: string;
    rows: number;
    cols: number;
    end_cell: MapCellIdx;
    start_cell: MapCellIdx;
    bot_support?: boolean;
    map_idx: number;
}

export type gameMode = 'bot' | 'human';
export type gameRegister = 'yes' | 'no' | 'load' | 'choose_map' | 'fill_details' | 'err';
export type gameRole = number;
export interface Dictionary {
    [Key: number]: string;
}
export const role_strings: Dictionary = { 0: 'navigator', 1: 'instructor' };

export interface GameState {
    end: boolean;
    started: boolean;
    end_modal_text: string;
    end_modal_title: string;
    init_time: number;
    game_time: number;
    open_instructions: boolean;
}

export interface GameConfig {
    game_mode?: gameMode;
    game_role: gameRole;
    registerd: gameRegister;
    guid: string;
}

export interface ChatMsg {
    id: gameRole;
    msg: string;
    timestamp: number;
    curr_nav_cell?: MapCellIdx;
}

export interface IAppState {
    chat: ChatMsg[];
    map_metadata: MapMetadata;
    user_map_path: MapCellIdx[];
    user_metadata: UserMetadata;
    user_survey: UserSurvey;
    game_state: GameState;
    game_config: GameConfig;
    clinet_version: string;
    server_version: string;
}

export const maps: MapMetadata[] = [
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map1_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 16, c: 7 },
        start_cell: { r: 2, c: 23 },
        map_idx: 0,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map2_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 12, c: 6 },
        start_cell: { r: 2, c: 20 },
        map_idx: 1,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map3_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 13, c: 9 },
        start_cell: { r: 3, c: 9 },
        map_idx: 2,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map4_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 7, c: 0 },
        start_cell: { r: 3, c: 23 },
        map_idx: 3,
    },
    {
        im_width: 2304,
        im_height: 1728,
        im_src: 'map5_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 16, c: 9 },
        start_cell: { r: 1, c: 1 },
        map_idx: 4,
    },
    {
        im_width: 1754,
        im_height: 1226,
        im_src: 'map6_0.jpg',
        rows: 18,
        cols: 24,
        end_cell: { r: 6, c: 2 },
        start_cell: { r: 8, c: 7 },
        map_idx: 5,
    },
];

export const init_app_state: IAppState = {
    chat: [],
    user_metadata: { name: '', age: '', gender: 'Male' },
    map_metadata: maps[0],
    user_map_path: [],
    user_survey: {
        '0': { question: 'How much did you enjoy the task?', answer: null, type: 'rating' },
        '1': { question: 'How difficult was it to communicate with your partner?', answer: null, type: 'rating' },
        '2': {
            question: 'How successful do you think you were at completing the task?',
            answer: null,
            type: 'rating',
        },
        '3': {
            question: "How difficult was it to understand your partner's directions?",
            answer: null,
            type: 'rating',
        },
        '4': {
            question: 'How likely is your partner to be a fluent speaker of English?',
            answer: null,
            type: 'rating',
        },
        '5': {
            question: 'How likely is your partner to be a fluent speaker of Spanish?',
            answer: null,
            type: 'rating',
        },
        '6': {
            question: 'How likely do you think it is that your partner is bilingual?',
            answer: null,
            type: 'rating',
        },

        '7': {
            hintAbove: 'Please rate your partner according to the following attributes:',
            question: 'friendly',
            answer: null,
            type: 'rating',
        },
        '8': {
            question: 'smart',
            answer: null,
            type: 'rating',
        },
        '9': {
            question: 'collaborative',
            answer: null,
            type: 'rating',
        },
        '10': {
            question: 'honest',
            answer: null,
            type: 'rating',
        },
        '11': {
            question: 'funny',
            answer: null,
            type: 'rating',
        },
        '12': {
            question: 'How likely do you think it was that you were talking to a chatbot rather than a human?',
            answer: null,
            type: 'rating',
        },
        '13': {
            question:
                'If you were communicating with a chat bot, would you want them to communicate in both English and Spanish?',
            answer: null,
            type: 'rating',
        },
        '14': {
            question: 'Age:',
            answer: null,
            type: 'textfield',
            numberText: true,
            isStyleHoriz: true,
        },
        '15': {
            question: 'Gender:',
            selectOptions: ['male', 'female', 'non-binary', 'prefer not to answer'],
            answer: 'male',
            type: 'select',
            isStyleHoriz: true,
        },
        '16': {
            question: 'Place of birth:',
            answer: null,
            type: 'textfield',
            isStyleHoriz: true,
        },
        '17': {
            question: 'Place of current resident:',
            answer: null,
            type: 'textfield',
            isStyleHoriz: true,
        },
        '18': {
            question: 'Highest level of education received:',
            selectOptions: [
                'less than high school',
                'high school',
                'trade school',
                'some college',
                'college',
                'graduate school',
                'some graduate school',
                'MA',
                'PhD',
                'other',
            ],
            answer: 'less than high school',
            type: 'select',
            isStyleHoriz: true,
        },
        '19': {
            question: 'Native language(s):',
            answer: null,
            type: 'textfield',
            isStyleHoriz: true,
        },
        '20': {
            question: 'Do you speak any other languages?',
            answer: null,
            type: 'textfield',
            questionCont: 'If so, please list',
        },
        '21': {
            question: 'What languages are currently spoken in your home?',
            answer: null,
            type: 'textfield',
        },
        '22': {
            question: 'Have you spent extended time (e.g., more than 6 months) living in another country?',
            questionCont: 'If so, please describe briefly where and for how long',
            answer: null,
            type: 'textfield',
        },
        '23': {
            question: 'Enter your native language, or the language you are providing answers for, here:',
            answer: null,
            type: 'textfield',
        },
        '24': {
            hintAbove: 'How would you rate your fluency in your native language, for each of these categories:',
            question: 'Reading',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '25': {
            question: 'Writing',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '26': {
            question: 'Speaking',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '27': {
            question: 'Listening',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '28': {
            hintAbove: 'Please rate how likely you are to use your first language in the following contexts:',
            question: 'At work',
            answer: null,
            type: 'rating',
        },
        '29': {
            question: 'At home',
            answer: null,
            type: 'rating',
        },
        '30': {
            question: 'Interacting with friends',
            answer: null,
            type: 'rating',
        },
        '31': {
            question: 'Interacting with family',
            answer: null,
            type: 'rating',
        },
        '32': {
            question: 'Entertainment (TV series, music, etc.)',
            answer: null,
            type: 'rating',
        },
        '33': {
            question: 'Enter your most proficient second language here:',
            answer: null,
            type: 'textfield',
        },
        '34': {
            hintAbove: 'How would you rate your fluency in your second language, for each of these categories:',
            question: 'Reading',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '35': {
            question: 'Writing',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '36': {
            question: 'Speaking',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '37': {
            question: 'Listening',
            answer: null,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
        },
        '38': {
            question: 'Approximately what age did you begin learning your second language?',
            answer: null,
            type: 'textfield',
            numberText: true,
            isStyleHoriz: true,
        },
        '39': {
            hintAbove: 'Please rate how likely you are to use your second language in the following contexts:',
            question: 'At work',
            answer: null,
            type: 'rating',
        },
        '40': {
            question: 'At home',
            answer: null,
            type: 'rating',
        },
        '41': {
            question: 'Interacting with friends',
            answer: null,
            type: 'rating',
        },
        '42': {
            question: 'Interacting with family',
            answer: null,
            type: 'rating',
        },
        '43': {
            question: 'Entertainment (TV series, music, etc.)',
            answer: null,
            type: 'rating',
        },
        '44': {
            question:
                'Have you ever lived in a home environment or country where your second language was spoken? If so, please explain briefly:',
            answer: null,
            type: 'textfield',
        },
    },
    game_state: {
        end: false,
        started: false,
        end_modal_text: '',
        end_modal_title: game_over_modal_str,
        init_time: 300,
        game_time: 0,
        open_instructions: true,
    },
    game_config: { game_role: 0, registerd: 'no', guid: '' },
    clinet_version: '1.4.0_e',
    server_version: '',
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(JSON.parse(JSON.stringify(init_app_state)));

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
