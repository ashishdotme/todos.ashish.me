import React from 'react';
import { TodoResponse } from '@ashishdotme/sdk/todo';

interface Props {
    todo: TodoResponse;
}

const TodoItem: React.FC<Props> = (props) => (
    <div>
        <label className="checkbox mr-3">
            <input type="checkbox" />
        </label>
        {props.todo.content}
    </div>
);

export default TodoItem;
