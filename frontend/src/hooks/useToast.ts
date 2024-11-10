import { useCallback } from 'react';
import { useAppDispatch } from './useAppDispatch';
import { setError, setSuccessMessage, clearMessages } from '../features/ui/uiSlice';

export const useToast = () => {
  const dispatch = useAppDispatch();

  const showError = useCallback((message: string) => {
    dispatch(setError(message));
    setTimeout(() => dispatch(clearMessages()), 5000);
  }, [dispatch]);

  const showSuccess = useCallback((message: string) => {
    dispatch(setSuccessMessage(message));
    setTimeout(() => dispatch(clearMessages()), 5000);
  }, [dispatch]);

  return { showError, showSuccess };
};
