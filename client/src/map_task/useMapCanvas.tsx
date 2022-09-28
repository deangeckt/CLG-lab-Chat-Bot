import { useContext, useRef, useState } from 'react';
import { notifyHumanEnd } from '../api';
import { AppContext } from '../AppContext';
import { path_cell_color, next_cells_color } from '../common/colors';
import { MapCellIdx } from '../Wrapper';
import { useApp } from './useApp';

const get_canvas_size = (im_width: number, im_height: number) => {
    // map canvas is 75% width, the app container is 90% width
    const container_width = 0.75 * 0.9 * window.innerWidth;
    const container_height = 0.75 * 0.9 * window.innerHeight;

    const ratio_w = container_width / im_width;
    const ratio_h = container_height / im_height;

    const ratio = ratio_w < ratio_h ? ratio_w : ratio_h;

    let canvas_width = im_width;
    let canvas_height = im_height;

    if (ratio < 1) {
        canvas_width *= ratio;
        canvas_height *= ratio;
    }
    return { canvas_width, canvas_height };
};

export function useMapCanvas() {
    const { open_ending_modal } = useApp();
    const { state, setState } = useContext(AppContext);
    const [matrix, setMatrix] = useState(Array<Array<Path2D>>);
    const [neighbors, setNeighbors] = useState<Set<string>>(new Set());
    const { canvas_width, canvas_height } = get_canvas_size(state.map_metadata.im_width, state.map_metadata.im_height);
    const canvasRef = useRef(null);
    const [im, setIm] = useState<HTMLImageElement>();
    const radius = canvas_width / 65;

    const draw = (on_draw_cb: Function) => {
        const canvas = canvasRef.current as any;
        if (!canvas) {
            return;
        }
        const context = canvas.getContext('2d');
        const image = new Image();
        image.onload = function () {
            setIm(image);
            context.drawImage(image, 0, 0, canvas_width, canvas_height);
            on_draw_cb();
        };
        image.onerror = function (err) {
            console.log('err', err);
        };

        image.src = require(`./maps/${state.map_metadata.im_src}`);
    };

    const init_navigator = () => {
        draw(init_matrix);
    };

    const init_instructor = () => {
        draw(() => null);
    };

    const init_matrix = () => {
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');

        const rows = state.map_metadata.rows;
        const columns = state.map_metadata.cols;

        const col_step = canvas_width / columns;
        const row_step = canvas_height / rows;

        const new_mat: Array<Array<Path2D>> = [];
        const curr_map_cell: MapCellIdx = state.user_map_path[0];
        const new_neighbors = get_neighbors(curr_map_cell);

        for (let row = 0; row < rows; row++) {
            const new_col: Array<Path2D> = [];
            for (let col = 0; col < columns; col++) {
                const curr: MapCellIdx = { r: row, c: col };
                if (curr.c == curr_map_cell.c && curr.r == curr_map_cell.r) {
                    context.fillStyle = path_cell_color;
                } else if (new_neighbors.has(`${curr.r}_${curr.c}`)) context.fillStyle = next_cells_color;
                else context.fillStyle = 'transparent';

                const circle = new Path2D();
                circle.arc(col_step * col + radius * 1.5, row_step * row + radius * 1.5, radius, 0, 2 * Math.PI);
                context.fill(circle);
                new_col.push(circle);
            }
            new_mat.push(new_col);
        }
        setMatrix(new_mat);
        setNeighbors(new_neighbors);
    };

    const neighbor_str_to_cell = (neighbor: string): MapCellIdx => {
        const splited = neighbor.split('_');
        return { r: Number(splited[0]), c: Number(splited[1]) };
    };

    const get_neighbors = (curr: MapCellIdx): Set<string> => {
        const row = curr.r;
        const col = curr.c;

        const new_neighbors = new Set<string>();
        if (row - 1 > 0) new_neighbors.add(`${row - 1}_${col}`);
        if (row + 1 < state.map_metadata.rows - 1) new_neighbors.add(`${row + 1}_${col}`);
        if (col - 1 > 0) new_neighbors.add(`${row}_${col - 1}`);
        if (col + 1 < state.map_metadata.cols - 1) new_neighbors.add(`${row}_${col + 1}`);
        return new_neighbors;
    };

    const color_change = (cells: MapCellIdx[], color: string) => {
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');

        for (const cell of cells) {
            const path_obj = matrix[cell.r][cell.c];
            context.fillStyle = color;
            context.fill(path_obj);
        }
    };

    const is_finish = (cell: MapCellIdx): boolean => {
        return (
            Math.sqrt((cell.r - state.map_metadata.end_cell.r) ** 2 + (cell.c - state.map_metadata.end_cell.c) ** 2) < 2
        );
    };

    const next_move = (new_cell: MapCellIdx) => {
        if (is_finish(new_cell)) {
            open_ending_modal('Felicidades! you found the treasue');
            if (state.game_config.game_mode == 'human')
                notifyHumanEnd(state.game_config.guid, state.game_config.game_role);
        }

        const new_neighbors = get_neighbors(new_cell);
        setNeighbors(new_neighbors);

        const curr_map_cell: MapCellIdx = state.user_map_path[state.user_map_path.length - 1];

        const ui_new_neighbors = new Set(new_neighbors);
        ui_new_neighbors.delete(`${curr_map_cell.r}_${curr_map_cell.c}`);
        const ui_new_neighbors_list = Array.from(new_neighbors).map((n) => neighbor_str_to_cell(n));

        // clean the canvas
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');
        context.clearRect(0, 0, canvas_width, canvas_height);
        context.drawImage(im, 0, 0, canvas_width, canvas_height);

        // color the circle object after image
        const user_map_path = [...state.user_map_path].concat(new_cell);
        color_change(ui_new_neighbors_list, next_cells_color);
        color_change(user_map_path, path_cell_color);

        setState({ ...state, user_map_path: user_map_path });
    };

    const onKeyClick = (e: any) => {
        const curr_map_cell: MapCellIdx = state.user_map_path[state.user_map_path.length - 1];
        let row = curr_map_cell.r;
        let col = curr_map_cell.c;

        const cols = state.map_metadata.cols;
        const rows = state.map_metadata.rows;

        if (e.keyCode == 37) {
            // console.log('left');
            col = col > 0 ? col - 1 : 0;
        } else if (e.keyCode == 39) {
            // console.log('right');
            col = col < cols - 1 ? col + 1 : cols - 1;
        } else if (e.keyCode == 40) {
            // console.log('down');
            row = row < rows - 1 ? row + 1 : rows - 1;
        } else if (e.keyCode == 38) {
            // console.log('up');
            row = row > 0 ? row - 1 : 0;
        } else {
            return;
        }
        const new_cell: MapCellIdx = { r: row, c: col };
        next_move(new_cell);
    };

    const onMouseClick = (e: any) => {
        // console.log(e.nativeEvent.offsetX / canvas_width, e.nativeEvent.offsetY / canvas_height);
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');
        for (const neighbor_str of neighbors) {
            const neighbor = neighbor_str_to_cell(neighbor_str);
            const cell = matrix[neighbor.r][neighbor.c];
            if (context.isPointInPath(cell, e.nativeEvent.offsetX, e.nativeEvent.offsetY)) {
                next_move(neighbor);
                break;
            }
        }
    };

    return {
        canvasRef,
        matrix,
        canvas_width,
        canvas_height,
        neighbor_str_to_cell,
        get_neighbors,
        init_matrix,
        onMouseClick,
        onKeyClick,
        init_navigator,
        init_instructor,
    };
}
