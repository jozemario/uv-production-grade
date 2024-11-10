import React, { useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/20/solid";

const AuthDebug: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const auth = useSelector((state: RootState) => state.auth);

  return (
    <div className="relative">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-700 bg-white rounded-md border border-gray-200 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Auth State
        {isExpanded ? (
          <ChevronUpIcon className="w-4 h-4" />
        ) : (
          <ChevronDownIcon className="w-4 h-4" />
        )}
      </button>

      {isExpanded && (
        <div className="absolute right-0 mt-2 w-96 bg-white rounded-md shadow-lg border border-gray-200 z-50">
          <div className="p-4">
            <div className="overflow-x-auto">
              <pre className="text-xs text-gray-700 whitespace-pre-wrap break-words">
                {JSON.stringify(auth, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthDebug;
