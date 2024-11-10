#!/bin/bash
export $(grep -v '^#' ../.env.local | xargs)
npm install
npm start