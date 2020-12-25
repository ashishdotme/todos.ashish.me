import React, { useContext } from 'react';
import TodosContext from '../../common/todosContext';
import MenuItem from './MenuItem';

interface Props {}

const Menu: React.FC<Props> = () => {
    const { currentMenu, dispatch } = useContext(TodosContext);
    return (
        <div className="tabs is-fullwidth has-text-weight-bold">
            <ul>
                <MenuItem
                    text="Incomplete"
                    count={0}
                    className={currentMenu == 'INCOMPLETE' ? '' : 'is-active'}
                    onClick={() =>
                        dispatch({
                            type: 'CHANGE_CURRENT_MENU',
                            payload: 'INCOMPLETE',
                        })
                    }
                />

                <MenuItem
                    text="Completed"
                    count={0}
                    className={currentMenu == 'COMPLETED' ? '' : 'is-active'}
                    onClick={() =>
                        dispatch({
                            type: 'CHANGE_CURRENT_MENU',
                            payload: 'COMPLETED',
                        })
                    }
                />
            </ul>
        </div>
    );
};

export default Menu;
