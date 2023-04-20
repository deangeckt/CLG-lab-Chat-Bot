import React, { useState } from 'react';
import { AppContext } from './AppContext';
import { game_over_modal_str } from './common/strings';

export type UserSurveyType = 'rating' | 'textfield' | 'select';

export interface UserSurveyQuestion {
    question: string;
    answer: number | string;
    type: UserSurveyType;
    hintAbove?: string;
    sliderLeftText?: string;
    slideRightText?: string;
    numberText?: boolean;
    selectOptions?: string[];
    isStyleHoriz?: boolean;
    questionCont?: string;
    not_applicable?: boolean;
    question_ref?: string;
}

export type surveyType = 'map' | 'general';

export interface IQuestionInterface {
    meta: UserSurveyQuestion;
    id: string;
    survey: surveyType;
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

export type gameRegister = 'yes' | 'no' | 'load' | 'err';
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
    game_role: gameRole;
    map_index: number;
    //dynamic
    guid: string;
    registerd: gameRegister;
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
    general_survey: UserSurvey;
    map_survey: UserSurvey;
    game_state: GameState;
    game_config: GameConfig;
    clinet_version: string;
    server_version: string;
    consent: boolean;
    uploaded: boolean;
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
    map_metadata: maps[0],
    user_map_path: [],
    general_survey: {
        '14': {
            question: 'Age:',
            answer: '',
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
            answer: '',
            type: 'textfield',
            isStyleHoriz: true,
        },
        '17': {
            question: 'Place of current residence:',
            answer: '',
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
            answer: '',
            type: 'textfield',
            isStyleHoriz: true,
        },
        '20': {
            question: 'Do you speak any other languages?',
            answer: '',
            type: 'textfield',
            questionCont: 'If so, please list',
        },
        '21': {
            question: 'What languages are currently spoken in your home?',
            answer: '',
            type: 'textfield',
        },
        '22': {
            question: 'Have you spent extended time (e.g., more than 6 months) living in another country?',
            questionCont: 'If so, please describe briefly where and for how long',
            answer: '',
            type: 'textfield',
        },
        '23': {
            question: 'Enter your native language, or the language you are providing answers for, here:',
            answer: '',
            type: 'textfield',
        },
        '24': {
            hintAbove: 'How would you rate your fluency in your native language, for each of these categories:',
            question: 'Reading',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '24',
        },
        '25': {
            question: 'Writing',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '24',
        },
        '26': {
            question: 'Speaking',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '24',
        },
        '27': {
            question: 'Listening',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '24',
        },
        '28': {
            hintAbove: 'Please rate how likely you are to use your first language in the following contexts:',
            question: 'At work',
            answer: 50,
            type: 'rating',
            question_ref: '28',
        },
        '29': {
            question: 'At home',
            answer: 50,
            type: 'rating',
            question_ref: '28',
        },
        '30': {
            question: 'Interacting with friends',
            answer: 50,
            type: 'rating',
            question_ref: '28',
        },
        '31': {
            question: 'Interacting with family',
            answer: 50,
            type: 'rating',
            question_ref: '28',
        },
        '32': {
            question: 'Entertainment (TV series, music, etc.)',
            answer: 50,
            type: 'rating',
            question_ref: '28',
        },
        '33': {
            question: 'Enter your most proficient second language here:',
            answer: '',
            type: 'textfield',
        },
        '34': {
            hintAbove: 'How would you rate your fluency in your second language, for each of these categories:',
            question: 'Reading',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '34',
        },
        '35': {
            question: 'Writing',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '34',
        },
        '36': {
            question: 'Speaking',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '34',
        },
        '37': {
            question: 'Listening',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'no knowledge at all',
            slideRightText: 'perfect, like a native speaker',
            question_ref: '34',
        },
        '38': {
            question: 'Approximately what age did you begin learning your second language?',
            questionCont: "If the answer is “since birth”, enter '0'",
            answer: '',
            type: 'textfield',
            numberText: true,
            isStyleHoriz: true,
        },
        '39': {
            hintAbove: 'Please rate how likely you are to use your second language in the following contexts:',
            question: 'At work',
            answer: 50,
            type: 'rating',
            question_ref: '39',
        },
        '40': {
            question: 'At home',
            answer: 50,
            type: 'rating',
            question_ref: '39',
        },
        '41': {
            question: 'Interacting with friends',
            answer: 50,
            type: 'rating',
            question_ref: '39',
        },
        '42': {
            question: 'Interacting with family',
            answer: 50,
            type: 'rating',
            question_ref: '39',
        },
        '43': {
            question: 'Entertainment (TV series, music, etc.)',
            answer: 50,
            type: 'rating',
            question_ref: '39',
        },
        '44': {
            question:
                'Have you ever lived in a home environment or country where your second language was spoken? If so, please explain briefly:',
            answer: '',
            type: 'textfield',
        },
        '45': {
            question:
                'On a day-to-day basis, how likely are you to have a conversation using both your first and second languages?',
            answer: 50,
            type: 'rating',
            not_applicable: true,
        },
        '46': {
            hintAbove: 'How likely would you be to mix languages in the following contexts?',
            question: 'At work',
            answer: 50,
            type: 'rating',
            not_applicable: true,
            question_ref: '46',
        },
        '47': {
            question: 'At home',
            answer: 50,
            type: 'rating',
            not_applicable: true,
            question_ref: '46',
        },
        '48': {
            question: 'Interacting with friends',
            answer: 50,
            type: 'rating',
            not_applicable: true,
            question_ref: '46',
        },
        '49': {
            question: 'Interacting with family',
            answer: 50,
            type: 'rating',
            not_applicable: true,
            question_ref: '46',
        },
        '50': {
            question: 'Using social media',
            answer: 50,
            type: 'rating',
            not_applicable: true,
            question_ref: '46',
        },
        '51': {
            hintAbove: 'When you switch languages, how often is it for the following reasons?',
            question: "To accommodate people who don't share the same language or language fluency.",
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '52': {
            question: 'For social reasons; one language feels more appropriate.',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '53': {
            question: "I can't think of a word in the current language.",
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '54': {
            question: 'The word in the other language just fits better.',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '55': {
            question: "It's an accident, or I don't realize I'm doing it.",
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '56': {
            question: "I'm more comfortable discussing the topic in the other language.",
            answer: 50,
            type: 'rating',
            sliderLeftText: 'never',
            slideRightText: 'always',
            not_applicable: true,
            question_ref: '51',
        },
        '57': {
            question: 'Do you enjoy mixing languages in conversation?',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'yes very much',
            not_applicable: true,
        },
        '58': {
            question: 'What do you think when others mix languages in conversation? Please explain:',
            answer: '',
            type: 'textfield',
            not_applicable: true,
        },
        '59': {
            question: 'Any final comments about your language background?',
            answer: '',
            type: 'textfield',
            not_applicable: true,
        },
    },
    map_survey: {
        '0': {
            question: 'How much did you enjoy the task?',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '1': {
            question: 'How difficult was it to communicate with your partner?',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '2': {
            question: 'How successful do you think you were at completing the task?',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '3': {
            question: "How difficult was it to understand your partner's directions?",
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '4': {
            question: 'How likely is your partner to be a fluent speaker of English?',
            answer: 50,
            type: 'rating',
        },
        '5': {
            question: 'How likely is your partner to be a fluent speaker of Spanish?',
            answer: 50,
            type: 'rating',
        },
        '6': {
            question: 'How likely do you think it is that your partner is bilingual?',
            answer: 50,
            type: 'rating',
        },

        '7': {
            hintAbove: 'Please rate your partner according to the following attributes:',
            question: 'friendly',
            answer: 50,
            type: 'rating',
            question_ref: '7',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '8': {
            question: 'smart',
            answer: 50,
            type: 'rating',
            question_ref: '7',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '9': {
            question: 'collaborative',
            answer: 50,
            type: 'rating',
            question_ref: '7',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '10': {
            question: 'honest',
            answer: 50,
            type: 'rating',
            question_ref: '7',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '11': {
            question: 'funny',
            answer: 50,
            type: 'rating',
            question_ref: '7',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
        },
        '12': {
            question: 'How likely do you think it was that you were talking to a chatbot rather than a human?',
            answer: 50,
            type: 'rating',
        },
        '13': {
            question:
                'If you were communicating with a chat bot, would you want them to communicate in both English and Spanish?',
            answer: 50,
            type: 'rating',
            sliderLeftText: 'not at all',
            slideRightText: 'extremely',
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
    game_config: { game_role: 1, map_index: 0, registerd: 'no', guid: '' },
    clinet_version: '2.1.0_p',
    server_version: '',
    consent: false,
    uploaded: false,
};

const Wrapper = (props: any) => {
    const [state, setState] = useState<IAppState>(JSON.parse(JSON.stringify(init_app_state)));

    return <AppContext.Provider value={{ state, setState }}>{props.children}</AppContext.Provider>;
};

export default Wrapper;
