#include <WiFi.h>
#include <WebServer.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

#define LIGHT1 16
#define LIGHT2 17
#define LIGHT3 18
#define FAN1 19

DHT dht(DHTPIN, DHTTYPE);
WebServer server(80);

const char* ssid = "SmartRoom";
const char* password = "12345678";

bool l1 = false;
bool l2 = false;
bool l3 = false;
bool fan = false;

void updateDevices() {
  digitalWrite(LIGHT1, l1 ? LOW : HIGH);
  digitalWrite(LIGHT2, l2 ? LOW : HIGH);
  digitalWrite(LIGHT3, l3 ? LOW : HIGH);
  digitalWrite(FAN1, fan ? LOW : HIGH);
}

String page = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart Room</title>

<style>
body {
  font-family: Arial;
  background: #eaf2ff;
  text-align: center;
  margin: 0;
}
h1 {
  background: #243b70;
  color: white;
  padding: 20px;
}
.box {
  background: white;
  padding: 20px;
  margin: 15px;
  border-radius: 15px;
}
button {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  background: #2864dc;
  color: white;
  font-size: 16px;
}
p {
  font-size: 20px;
}
</style>
</head>

<body>

<h1>🏠 My Smart Room</h1>

<div class="box">
<h2>💡 Light Controls</h2>
<p>Light 1 <button onclick="toggle('l1')">ON / OFF</button></p>
<p>Light 2 <button onclick="toggle('l2')">ON / OFF</button></p>
<p>Light 3 <button onclick="toggle('l3')">ON / OFF</button></p>
</div>

<div class="box">
<h2>🌀 Fan Control</h2>
<button onclick="toggle('fan')">ON / OFF</button>
</div>

<div class="box">
<h2>🌡️ Room Temperature</h2>
<p id="temp">Loading...</p>
<h2>💧 Room Humidity</h2>
<p id="hum">Loading...</p>
</div>

<script>
function toggle(device) {
  fetch('/toggle?device=' + device);
}

function updateData() {
  fetch('/data')
  .then(response => response.json())
  .then(data => {
    document.getElementById("temp").innerHTML =
      data.temperature + " °C";

    document.getElementById("hum").innerHTML =
      data.humidity + " %";
  });
}

setInterval(updateData, 2000);
updateData();
</script>

</body>
</html>
)rawliteral";

void handleRoot() {
  server.send(200, "text/html", page);
}

void handleToggle() {
  String device = server.arg("device");

  if (device == "l1") l1 = !l1;
  if (device == "l2") l2 = !l2;
  if (device == "l3") l3 = !l3;
  if (device == "fan") fan = !fan;

  updateDevices();
  server.send(200, "text/plain", "OK");
}

void handleData() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    server.send(200, "application/json",
                "{\"temperature\":\"Error\",\"humidity\":\"Error\"}");
    return;
  }

  String data = "{\"temperature\":" +
                String(temperature) +
                ",\"humidity\":" +
                String(humidity) + "}";

  server.send(200, "application/json", data);
}

void setup() {
  Serial.begin(115200);

  pinMode(LIGHT1, OUTPUT);
  pinMode(LIGHT2, OUTPUT);
  pinMode(LIGHT3, OUTPUT);
  pinMode(FAN1, OUTPUT);

  updateDevices();

  dht.begin();

  WiFi.softAP(ssid, password);

  Serial.println("Smart Room Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/toggle", handleToggle);
  server.on("/data", handleData);

  server.begin();
}

void loop() {
  server.handleClient();
}
