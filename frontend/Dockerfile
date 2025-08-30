# Strands Security Analysis Platform - Frontend Application
# This multi-stage Dockerfile builds the Vue.js frontend application and serves
# it using Nginx. Optimized for production deployment with static asset serving.

# Stage 1: Build the Vue.js application
FROM node:18-alpine AS builder

# Set working directory for build stage
WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Clean any existing dependencies and install fresh
RUN rm -rf node_modules package-lock.json
RUN npm install

# Copy source code and build production assets
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built assets from build stage to Nginx html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 3000 for the web application
EXPOSE 3000

# Start Nginx server in foreground mode
CMD ["nginx", "-g", "daemon off;"]