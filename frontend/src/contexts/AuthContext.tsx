import React, { createContext, useContext } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";

interface AuthContextType {
  token: string | null;
  user: any;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  user: null,
  isAuthenticated: false,
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const auth = useSelector((state: RootState) => state.auth);

  return (
    <AuthContext.Provider
      value={{
        token: auth.token,
        user: auth.user,
        isAuthenticated: auth.isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
