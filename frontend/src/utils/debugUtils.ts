export const logRequest = async (url: string, options: RequestInit): Promise<any> => {
    console.group('API Request');
    console.log('URL:', url);
    console.log('Options:', {
      ...options,
      headers: Object.fromEntries(
        // @ts-ignore
        [...(options.headers instanceof Headers ? options.headers.entries() : [])]
      ),
    });
    
    try {
      const response = await fetch(url, options);
      const data = await response.clone().json();
      console.log('Response:', {
        status: response.status,
        data,
      });
      console.groupEnd();
      return response;
    } catch (error) {
      console.error('Request Error:', error);
      console.groupEnd();
      throw error;
    }
  };