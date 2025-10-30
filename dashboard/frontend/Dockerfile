# Step 1: Use official Node image
FROM node:20-alpine AS builder

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package files and install deps
COPY package*.json ./
RUN npm install

# Step 4: Copy rest of the source and build it
COPY . .
RUN npm run build

# Step 5: Use a lightweight web server to serve the build
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# Step 6: Expose the default Nginx port
EXPOSE 80

# Step 7: Start the server
CMD ["nginx", "-g", "daemon off;"]
