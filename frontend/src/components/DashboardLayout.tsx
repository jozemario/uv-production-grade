import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Container,
  SwipeableDrawer,
  IconButton,
  Badge,
  Fab,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { LiveFeed } from "./LiveFeed";
import { WebhookTester } from "./WebhookTester";
import { useWebSocket } from "../contexts/WebSocketContext";
import NotificationsIcon from "@mui/icons-material/Notifications";
import CloseIcon from "@mui/icons-material/Close";

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const { lastMessage } = useWebSocket();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const handleNewMessage = useCallback(() => {
    if (!isDrawerOpen) {
      setUnreadCount((prev) => prev + 1);
    }
  }, [isDrawerOpen]);

  useEffect(() => {
    if (lastMessage) {
      handleNewMessage();
    }
  }, [lastMessage]);

  const handleDrawerOpen = () => {
    setIsDrawerOpen(true);
    setUnreadCount(0);
  };

  const handleDrawerClose = () => {
    setIsDrawerOpen(false);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {children}

      <Fab
        color="primary"
        sx={{
          position: "fixed",
          bottom: 16,
          right: 16,
          zIndex: theme.zIndex.drawer - 1,
        }}
        onClick={handleDrawerOpen}
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </Fab>

      <SwipeableDrawer
        anchor={isMobile ? "bottom" : "right"}
        open={isDrawerOpen}
        onClose={handleDrawerClose}
        onOpen={handleDrawerOpen}
        swipeAreaWidth={20}
        ModalProps={{ keepMounted: true }}
        sx={{
          "& .MuiDrawer-paper": {
            width: isMobile ? "100%" : "400px",
            height: isMobile ? "80vh" : "100%",
            overflow: "hidden",
          },
        }}
      >
        <Box
          sx={{
            p: 2,
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 1 }}>
            <IconButton onClick={handleDrawerClose}>
              <CloseIcon />
            </IconButton>
          </Box>

          <Box
            sx={{
              flex: 1,
              overflow: "auto",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            <WebhookTester />
            <LiveFeed />
          </Box>
        </Box>
      </SwipeableDrawer>
    </Container>
  );
};

export default DashboardLayout;
