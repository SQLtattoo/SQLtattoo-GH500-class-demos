/**
 * GHAS Demo App — Frontend (Express)
 * Deliberately vulnerable for GH-500 training.
 * DO NOT deploy to production.
 */

const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// ---------------------------------------------------------------------------
// VULNERABILITY: Reflected XSS — Demo 4.3 (code scanning in PR)
// ---------------------------------------------------------------------------
app.get("/greet", (req, res) => {
  const name = req.query.name || "World";
  // BAD: user input reflected directly into HTML without escaping
  res.send(`<html><body><h1>Hello, ${name}!</h1></body></html>`);
});

// ---------------------------------------------------------------------------
// VULNERABILITY: Path Traversal — code scanning alert
// ---------------------------------------------------------------------------
app.get("/file", (req, res) => {
  const filename = req.query.name;
  if (!filename) {
    return res.status(400).send("Missing filename");
  }
  // BAD: user-controlled path with no sanitisation
  const filePath = path.join(__dirname, "public", filename);
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      return res.status(404).send("File not found");
    }
    res.send(data);
  });
});

// ---------------------------------------------------------------------------
// VULNERABILITY: Command Injection — code scanning alert
// ---------------------------------------------------------------------------
const { exec } = require("child_process");

app.get("/ping", (req, res) => {
  const host = req.query.host;
  if (!host) {
    return res.status(400).send("Missing host parameter");
  }
  // BAD: user input passed directly to shell command
  exec(`ping -c 2 ${host}`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).send(stderr);
    }
    res.type("text").send(stdout);
  });
});

// ---------------------------------------------------------------------------
// SAFE version of search (for demonstrating the fix)
// ---------------------------------------------------------------------------
app.get("/greet/safe", (req, res) => {
  const name = req.query.name || "World";
  // SAFE: HTML-encode the user input
  const escaped = name
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
  res.send(`<html><body><h1>Hello, ${escaped}!</h1></body></html>`);
});

// ---------------------------------------------------------------------------
// Healthcheck
// ---------------------------------------------------------------------------
app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`Frontend running on http://localhost:${PORT}`);
});
