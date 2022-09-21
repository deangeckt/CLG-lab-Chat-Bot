import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './map_task/App';
import Wrapper from './Wrapper';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Home from './home_page/Home';
import EndPage from './end_page/EndPage';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
    <Wrapper>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="map_task" element={<App />} />
                <Route path="map_task/survey" element={<EndPage />} />
            </Routes>
        </BrowserRouter>
    </Wrapper>,
);
