import React, { useContext, useReducer, useState } from 'react';
import Menu from '../components/menu/Menu';
import List from '../components/list/List';
import todosReducer from '../common/todosReducer';
import TodosContext from '../common/todosContext';
import '../styles/home.scss';

const Home: React.FC = () => {
    const [currentPage, setCurrentPage] = useState(0);
    const initialState = useContext(TodosContext);
    const [state, dispatch] = useReducer(todosReducer, initialState);
    return (
        <TodosContext.Provider value={{ ...state, dispatch }}>
            <div className="todo-container">
                <div className="box">
                    <Menu
                        setCurrentPage={(pageNumber: number) =>
                            setCurrentPage(pageNumber)
                        }
                    />
                    <List
                        currentPage={currentPage}
                        setCurrentPage={(pageNumber: number) =>
                            setCurrentPage(pageNumber)
                        }
                    />
                </div>
            </div>
        </TodosContext.Provider>
    );
};

export default Home;
