import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UiState {
  isLoading: boolean;
  error: string | null;
  successMessage: string | null;
  theme: 'light' | 'dark';
}

const initialState: UiState = {
  isLoading: false,
  error: null,
  successMessage: null,
  theme: (localStorage.getItem('theme') as UiState['theme']) || 'light',
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.successMessage = null;
    },
    setSuccessMessage: (state, action: PayloadAction<string | null>) => {
      state.successMessage = action.payload;
      state.error = null;
    },
    setTheme: (state, action: PayloadAction<UiState['theme']>) => {
      state.theme = action.payload;
      localStorage.setItem('theme', action.payload);
    },
    clearMessages: (state) => {
      state.error = null;
      state.successMessage = null;
    },
  },
});

export const { 
  setLoading, 
  setError, 
  setSuccessMessage, 
  setTheme,
  clearMessages 
} = uiSlice.actions;
export default uiSlice.reducer;