import React, { useState } from "react";
import { Box, Button, TextField, Typography, Alert } from "@mui/material";
import { useSelector } from "react-redux";
import { RootState } from "../store";

export const WebhookTester: React.FC = () => {
  const auth = useSelector((state: RootState) => state.auth);
  const [testMessage, setTestMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const sendTestWebhook = async () => {
    try {
      const response = await fetch(
        `${"http://localhost:8000"}/api/v1/notifications/webhook/${
          auth.user?.id
        }`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${auth.token}`,
          },
          body: JSON.stringify({ message: testMessage }),
        }
      );

      if (response.ok) {
        setStatus("success");
        setTestMessage("");
        setErrorMessage("");
      } else {
        const error = await response.json();
        setStatus("error");
        setErrorMessage(error.detail || "Failed to send webhook");
      }
    } catch (error) {
      setStatus("error");
      setErrorMessage("Network error occurred");
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Test Webhook
      </Typography>
      <Box sx={{ display: "flex", gap: 2, alignItems: "flex-start" }}>
        <TextField
          fullWidth
          label="Test Message"
          value={testMessage}
          onChange={(e) => setTestMessage(e.target.value)}
          multiline
          rows={3}
        />
        <Button
          variant="contained"
          onClick={sendTestWebhook}
          disabled={!testMessage.trim()}
        >
          Send Test
        </Button>
      </Box>
      {status === "success" && (
        <Alert severity="success" sx={{ mt: 2 }}>
          Test webhook sent successfully!
        </Alert>
      )}
      {status === "error" && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {errorMessage || "Failed to send test webhook."}
        </Alert>
      )}
    </Box>
  );
};
