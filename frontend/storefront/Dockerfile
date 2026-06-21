FROM node:22-alpine

WORKDIR /app

# Install dependencies first (cached layer). All packages live inside the image.
COPY package.json ./
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
