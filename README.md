# 🏙️ AIStreetEasy

Welcome to **AIStreetEasy**! This project leverages AI to streamline real estate data analysis and provide actionable insights for users.

---

## ✨ Summary

AIStreetEasy is a multi-component system designed to collect, process, and serve real estate data efficiently. It features a web interface, LLM Data Source Model Context Protocol (MCP) server, and a backend server, each with a specific role in the data pipeline.

---

## 🛠️ Backend Logic

- **Web Server**: Handles user interactions and displays data.
- **MCP Server (Model Context Protocol)**: Serves as the datasource for the LLM, LLM transforms any query into the the input params for the MCP tool, the MCP tool inturns queries StreetEasyAPI to get true live data of rentals, which the LLM formats to the desired format for the backend to process.
- **Backend Server**: Processes data, queries AI models, and manages the database.

---

## 🗺️ Architecture Flowchart

<!-- Add your architecture flowchart here -->

---

## 🎥 Demo Video

<!-- Add your demo video here -->

---


## 🚀 To Dos

- **Backend Caching**: Implement an external caching application on the backend server to enable persistent storage of frequently accessed data, improving performance and reducing redundant processing.
- **MCP Server Query Storage**: Enhance the MCP server to store query results locally, minimizing repeated API calls to StreetEasy endpoints and optimizing response times for recurring queries.


# 📦 Web Server



---

# 🔗 MCP Server



---

# 🧠 Backend Server

