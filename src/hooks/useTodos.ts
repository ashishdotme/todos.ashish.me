import { API } from "@ashishdotme/api-client";
import { TodoResponse } from "@ashishdotme/sdk/todo";
import useSWR, { responseInterface } from "swr";
// import { database } from "../firebase/config";
// import { DataSnapshot } from "../interfaces/FirebaseTypes";
// import { UserContext } from "../contexts/Contexts";
type todosResponse = responseInterface<TodoResponse[], any>;

interface UseTodosReturn {
  todos?: todosResponse["data"];
  todosError: todosResponse["error"];
}

export const useTodos = (): UseTodosReturn => {
  const {
    data: todos,
    error: todosError,
  } = useSWR(`/todos`, async () =>
    API.todos.getAll()
  );

    return { todos, todosError };
};
