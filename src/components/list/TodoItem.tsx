import React from 'react';
import * as _ from 'lodash';
import { DateTime } from 'luxon';
import { TodoResponse } from '@ashishdotme/sdk/todo';

interface Props {
    todo: TodoResponse;
}

const TodoItem: React.FC<Props> = (props) => {
    const formatTag = (completedDate: string) => {
        return (
            <span className="tag is-link is-light">
                {DateTime.fromJSDate(new Date(completedDate!)).toLocaleString(
                    DateTime.DATE_MED,
                )}
            </span>
        );
    };
    return (
        <div>
            {_.capitalize(_.trim(props.todo.content))}{' '}
            {props.todo.completed ? formatTag(props.todo.completedDate!) : ''}
        </div>
    );
};

export default TodoItem;
