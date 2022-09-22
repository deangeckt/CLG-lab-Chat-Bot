import React, { useContext, useEffect } from 'react';
import { AppContext } from '../AppContext';
import { useMapCanvas } from './useMapCanvas';
import './MapCanvas.css';

// TODO: first render fix

function MapCanvas() {
    const { state } = useContext(AppContext);
    const { canvasRef, canvas_width, canvas_height, init_matrix, onMouseClick, onKeyClick } = useMapCanvas();

    useEffect(() => {
        const image = document.getElementById('source');
        const canvas = canvasRef.current as any;
        if (!canvas) {
            return;
        }
        const context = canvas.getContext('2d');
        context.drawImage(image, 0, 0, canvas_width, canvas_height);
        if (state.game_state.end) return;

        init_matrix();
        console.log('init');
    }, []);

    return (
        <div className="map_container">
            <canvas
                tabIndex={0}
                ref={canvasRef}
                width={canvas_width}
                height={canvas_height}
                className={'map_canvas'}
                onKeyDown={onKeyClick}
                onMouseDown={onMouseClick}
            />
            <div className="map_img">
                <img id="source" src={state.map_metadata.im_src} />
            </div>
        </div>
    );
}

export default MapCanvas;
