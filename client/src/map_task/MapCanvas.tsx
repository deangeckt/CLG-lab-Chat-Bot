import React, { useContext, useEffect } from 'react';
import { AppContext } from '../AppContext';
import { useMapCanvas } from './useMapCanvas';
import './MapCanvas.css';

function MapCanvas() {
    const { state } = useContext(AppContext);
    const { canvasRef, canvas_width, canvas_height, init_navigator, init_instructor, onMouseClick, onKeyClick } =
        useMapCanvas();

    const init_func = state.game_config.game_role == 1 ? init_instructor : init_navigator;

    useEffect(() => {
        if (state.game_state.end) return;
        init_func();
    }, []);

    return (
        <div className="map_container">
            <canvas
                tabIndex={0}
                ref={canvasRef}
                width={canvas_width}
                height={canvas_height}
                className={'map_canvas'}
                onKeyDown={state.game_config.game_role == 0 ? onKeyClick : () => null}
                onMouseDown={state.game_config.game_role == 0 ? onMouseClick : () => null}
            />
        </div>
    );
}

export default MapCanvas;
