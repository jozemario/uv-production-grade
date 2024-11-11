import React, { useEffect, useState } from "react";
import { useWebSocket } from "../contexts/WebSocketContext";
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
} from "@mui/material";

interface FeedItem {
  id: string;
  type: string;
  timestamp: string;
  data: any;
}

interface LiveFeedProps {
  onNewMessage?: () => void;
}

export const LiveFeed: React.FC<LiveFeedProps> = ({ onNewMessage }) => {
  const [feedItems, setFeedItems] = useState<FeedItem[]>([]);
  const { lastMessage, connected } = useWebSocket();
  const availableEventsColors: any = {
    "todo.created": "primary",
    "todo.updated": "secondary",
    "todo.deleted": "error",
    "webhook.notification": "success",
  };
  useEffect(() => {
    if (lastMessage) {
      const newItem: FeedItem = {
        id: crypto.randomUUID(),
        type: lastMessage.type || "event",
        timestamp: new Date().toISOString(),
        data: lastMessage.data,
      };

      setFeedItems((prev) => [newItem, ...prev].slice(0, 50));
      onNewMessage?.();
    }
  }, [lastMessage, onNewMessage]);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Live Feed{" "}
        {connected && (
          <Chip label="Connected" color="success" size="small" sx={{ ml: 1 }} />
        )}
      </Typography>
      <Paper sx={{ maxHeight: "fit-content", overflow: "auto" }}>
        <List>
          {feedItems.length === 0 ? (
            <ListItem>
              <ListItemText
                primary="No events yet"
                secondary="Events will appear here in real-time"
              />
            </ListItem>
          ) : (
            feedItems.map((item) => (
              <ListItem key={item.id} divider>
                <ListItemText
                  disableTypography
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Chip
                        label={item.type}
                        color={availableEventsColors[item.type]}
                        size="small"
                      />
                      <Typography variant="caption">
                        {new Date(item.timestamp).toLocaleString()}
                      </Typography>
                    </Box>
                  }
                  secondary={
                    <pre style={{ margin: 0, overflow: "auto" }}>
                      {JSON.stringify(item.data, null, 2)}
                    </pre>
                  }
                />
              </ListItem>
            ))
          )}
        </List>
      </Paper>
    </Box>
  );
};
