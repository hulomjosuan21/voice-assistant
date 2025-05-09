#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";
const int ledPin = 2;

WebServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/led", HTTP_POST, handleLEDControl);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body><h1>ESP32 LED Control</h1>";
  html += "<p>POST to /led with either:</p>";
  html += "<ul><li>{\"status\":\"on\"}</li><li>on</li><li>off</li></ul>";
  html += "<p>LED is currently: " + String(digitalRead(ledPin) ? "ON" : "OFF") + "</p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleLEDControl() {
  Serial.println("\n=== New Request ===");

  String body = server.arg("plain");
  Serial.println("Body: " + body);
  body.trim();
  body.toLowerCase();

  DynamicJsonDocument doc(256);
  DeserializationError error = deserializeJson(doc, body);

  String status = "";

  if (!error && doc.containsKey("status")) {
    status = doc["status"].as<String>();
    status.toLowerCase();
  } else {
    status = body;
  }

  if (status == "on") {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED turned ON");
    server.send(200, "application/json", "{\"message\":\"LED ON\",\"status\":\"on\"}");
  } else if (status == "off") {
    digitalWrite(ledPin, LOW);
    Serial.println("LED turned OFF");
    server.send(200, "application/json", "{\"message\":\"LED OFF\",\"status\":\"off\"}");
  } else {
    Serial.println("Invalid status value");
    server.send(400, "text/plain", "Status must be 'on' or 'off'");
  }
}

void handleNotFound() {
  server.send(404, "text/plain", "Endpoint not found");
}
