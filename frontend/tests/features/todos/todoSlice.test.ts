import todoReducer, {
    addTodo,
    updateTodo,
    removeTodo,
  } from '../../../src/features/todos/todoSlice';
  
  describe('todo reducer', () => {
    const initialState = {
      todos: [],
    };
  
    it('should handle initial state', () => {
      expect(todoReducer(undefined, { type: 'unknown' })).toEqual({
        todos: [],
      });
    });
  
    it('should handle addTodo', () => {
      const actual = todoReducer(initialState, addTodo({ id: 1, title: 'New Todo', completed: false }));
      expect(actual.todos.length).toEqual(1);
    });
  
    it('should handle updateTodo', () => {
      const state = {
        todos: [{ id: 1, title: 'Old Todo', completed: false }],
      };
      const actual = todoReducer(state, updateTodo({ id: 1, title: 'Updated Todo', completed: true }));
      expect(actual.todos[0].title).toEqual('Updated Todo');
      expect(actual.todos[0].completed).toEqual(true);
    });
  
    it('should handle removeTodo', () => {
      const state = {
        todos: [{ id: 1, title: 'Todo', completed: false }],
      };
      const actual = todoReducer(state, removeTodo(1));
      expect(actual.todos.length).toEqual(0);
    });
  });