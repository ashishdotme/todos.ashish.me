import React, { FormEvent, useContext, useReducer } from 'react';
import Menu from '../components/menu/Menu';
import Form from '../components/form/Form';
import List from '../components/list/List';
import todosReducer from '../common/todosReducer';
import TodosContext from '../common/todosContext';
import '../styles/home.scss';

const Home: React.FC = () => {
    const initialState = useContext(TodosContext);
    const [state, dispatch] = useReducer(todosReducer, initialState);
    return (
        <TodosContext.Provider value={{ ...state, dispatch }}>
            <div className="todo-container">
                <Form
                    addTodo={(
                        event: FormEvent<HTMLFormElement>,
                        inputValue: string,
                    ) => {
                        event.preventDefault();
                        if (inputValue !== '') {
                        }
                    }}
                />
                <div className="box">
                    <Menu />
                    <List />
                </div>
            </div>
        </TodosContext.Provider>
    );
};

export default Home;
