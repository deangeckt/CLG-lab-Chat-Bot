import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './map_task/App';
import Wrapper from './Wrapper';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Home from './home_page/Home';
import SurveyGeneral from './end_page/SurveyGeneral';
import './index.css';
import SurveyMap from './end_page/SurveyMap';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
    <Wrapper>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="general_survey" element={<SurveyGeneral />} />
                <Route path="map_task" element={<App />} />
                <Route path="map_survey" element={<SurveyMap />} />
            </Routes>
        </BrowserRouter>
    </Wrapper>,
);
