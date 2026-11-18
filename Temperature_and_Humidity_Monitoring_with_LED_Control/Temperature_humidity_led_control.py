#include <WiFi.h>
#include <WebServer.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11
#define LED 2

DHT dht(DHTPIN, DHTTYPE);
WebServer server(80);

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

String webpage = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<title>Temperature and Humidity</title>
<style>
body {
  font-family: Arial;
  text-align: center;
  background-color: #f2f2f2;
}
h1 {
  color: darkblue;
}
a {
  display: block;
  margin: 15px;
  font-size: 20px;
}
</style>
</head>

<body>

<h1>Temperature and Humidity</h1>

<p>Temperature: <span id="temp">--</span> °C</p>
<p>Humidity: <span id="hum">--</span> %</p>

<h1>LED Control</h1>

<a href="/red/on">Turn Red LED ON</a>
<a href="/red/off">Turn Red LED OFF</a>

<script>
function updateData() {
 fetch('/data')
 .then(response => response.json())
 .then(data => {
   document.getElementById("temp").innerHTML = data.temperature;
   document.getElementById("hum").innerHTML = data.humidity;
 });
}
setInterval(updateData, 2000);
updateData();
</script>

</body>
</html>
)rawliteral";

void handleRoot() {
  server.send(200, "text/html", webpage);
}

void handleData() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    server.send(200, "application/json",
                "{\"temperature\":\"Error\",\"humidity\":\"Error\"}");
    return;
  }

  String data = "{\"temperature\":" + String(t) +
                ",\"humidity\":" + String(h) + "}";

  server.send(200, "application/json", data);
}

void handleOn() {
  digitalWrite(LED, HIGH);
  server.sendHeader("Location", "/");
  server.send(303);
}

void handleOff() {
  digitalWrite(LED, LOW);
  server.sendHeader("Location", "/");
  server.send(303);
}

void setup() {
  Serial.begin(115200);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  dht.begin();

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.on("/red/on", handleOn);
  server.on("/red/off", handleOff);

  server.begin();
}

void loop() {
  server.handleClient();
}