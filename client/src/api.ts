import axios, { AxiosResponse } from 'axios';
import { ChatMsg, MapCellIdx } from './Wrapper';

export const baseUrl = 'http://localhost:8080/api/v1/';

export const huamn_to_human_event = async (update: Function) => {
    const evtSource = new EventSource(baseUrl + 'event');
    evtSource.onopen = function () {
        console.log('Connection to event server opened.');
    };
    evtSource.onmessage = function (e) {
        update(e.data);
    };
    evtSource.onerror = function (e) {
        console.log('EventSource failed.', e);
    };
};

export const callBot = async (msg: string, cell: MapCellIdx, update: Function) => {
    try {
        const data = { msg, state: cell };
        const response = (await axios.request({
            url: baseUrl + 'call_bot',
            method: 'POST',
            data: data,
        })) as AxiosResponse;
        update(response.data.res);
    } catch (error: any) {
        update('Bot not connected');
    }
};

export const callHuman = async (msg: ChatMsg) => {
    try {
        (await axios.request({
            url: baseUrl + 'call_human',
            method: 'POST',
            data: msg,
        })) as AxiosResponse;
    } catch (error: any) {
        console.log('Server not connected');
    }
};

export const assign_role = async (update: Function) => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'assign_roles',
            method: 'GET',
        })) as AxiosResponse;
        update(response.data.res);
    } catch (error: any) {
        console.log('Server not connected');
    }
};
