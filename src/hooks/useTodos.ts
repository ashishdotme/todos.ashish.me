import { API } from "@ashishdotme/api-client";
import { TodoResponse } from "@ashishdotme/sdk/todo";
import useSWR, { responseInterface } from "swr";
type todosResponse = responseInterface<TodoResponse[], any>;

interface UseTodosReturn {
  todos?: todosResponse["data"];
  todosError: todosResponse["error"];
  mutateTodos: todosResponse["mutate"];
}

export const useTodos = (): UseTodosReturn => {
  const {
    data: todos,
    error: todosError,
    mutate: mutateTodos
  } = useSWR(`/todos`, async () =>
    API.todos.getAll()
  );

    return { todos, todosError, mutateTodos };
};
