export const handleApiError = (error: any): string => {
    if (error.status === 'FETCH_ERROR') {
      return 'Network error. Please check your connection.';
    }
    
    if (error.status === 401) {
      return 'Unauthorized. Please login again.';
    }
    
    return error.data?.message || 'An unexpected error occurred.';
  };