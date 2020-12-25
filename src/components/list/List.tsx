import React, { useContext } from 'react';
import { TodoResponse } from '@ashishdotme/sdk/todo';
import TodosContext from '../../common/todosContext';
import { useTodos } from '../../hooks/useTodos';
import TodoItem from './TodoItem';

interface Props {}

const List: React.FC<Props> = () => {
    const { currentMenu } = useContext(TodosContext);
    let { todos } = useTodos();
    todos =
        currentMenu === 'INCOMPLETE'
            ? todos?.filter((todo) => !todo.completed)
            : todos?.filter((todo) => todo.completed);
    return (
        <div className="container">
            <div className="panel is-primary">
                <ul>
                    {todos &&
                        todos.map((todo: TodoResponse, i: number) => (
                            <label className="panel-block">
                                <TodoItem key={i} todo={todo} />
                            </label>
                        ))}
                </ul>
            </div>
        </div>
    );
};

export default List;
