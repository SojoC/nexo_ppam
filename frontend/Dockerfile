FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json /app/
# Asegura herramientas básicas y usa el lockfile
RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates git \
	&& rm -rf /var/lib/apt/lists/* \
	&& npm ci --no-audit --no-fund

COPY . /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
