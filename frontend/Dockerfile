FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json* /app/
RUN rm -rf node_modules package-lock.json && npm ci --no-audit --no-fund

COPY . /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
