import React, { useState } from "react";
import {
  useGetWebhooksQuery,
  useCreateWebhookMutation,
} from "../features/api/apiSlice";
import { XCircleIcon, PlusIcon } from "@heroicons/react/24/outline";
import { useSelector } from "react-redux";
import { RootState } from "../store";

const WebhookManager: React.FC = () => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [url, setUrl] = useState("");
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
  const { data: webhooks = [], isLoading } = useGetWebhooksQuery({});
  const [createWebhook] = useCreateWebhookMutation();
  const auth = useSelector((state: RootState) => state.auth);

  const availableEvents = ["todo.created", "todo.updated", "todo.deleted"];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createWebhook({
        url,
        events: selectedEvents,
      }).unwrap();
      setUrl("");
      setSelectedEvents([]);
      setShowAddForm(false);
    } catch (error) {
      console.error("Failed to create webhook:", error);
    }
  };

  const generateNotificationUrl = () => {
    const baseUrl = "http://localhost:8000";
    return `${baseUrl}/api/v1/notifications/webhook/${auth.user?.id}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold text-gray-900">Webhooks</h2>
        <div className="flex gap-2">
          <button
            onClick={() => {
              navigator.clipboard.writeText(generateNotificationUrl());
            }}
            className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Copy Notification URL
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Add Webhook
          </button>
        </div>
      </div>

      {showAddForm && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium">Add Webhook</h3>
              <button onClick={() => setShowAddForm(false)}>
                <XCircleIcon className="h-6 w-6 text-gray-400" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Webhook URL
                </label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Events
                </label>
                <div className="mt-2 space-y-2">
                  {availableEvents.map((event) => (
                    <label key={event} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedEvents.includes(event)}
                        onChange={(e) => {
                          setSelectedEvents(
                            e.target.checked
                              ? [...selectedEvents, event]
                              : selectedEvents.filter((e) => e !== event)
                          );
                        }}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-600">
                        {event}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700"
                >
                  Add Webhook
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white shadow rounded-lg">
        {isLoading ? (
          <div className="p-4 text-center">Loading...</div>
        ) : webhooks.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            No webhooks configured
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {webhooks.map((webhook) => (
              <li key={webhook.url} className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {webhook.url}
                    </p>
                    <div className="mt-1 flex flex-wrap gap-2">
                      {webhook.events.map((event) => (
                        <span
                          key={event}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {event}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default WebhookManager;
