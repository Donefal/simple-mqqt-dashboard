#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

// Alias Declaration
#define DHT_PIN D5
#define LED_PIN D6
#define DHT_TYPE DHT11

// Wifi Settings
const char* SSID = "realme 8i";
const char* PASSWORD = "avinavin";

// MQTT Broker Settings
const char *MQTT_BROKER = "broker.emqx.io";  
const char *MQTT_TOPIC_LED = "avinavin/led";     
const char *MQTT_TOPIC_SENSOR = "avinavin/sensor";
const char *MQTT_USERNAME = "emqx";  
const char *MQTT_PASSWORD = "public";  
const int MQTT_PORT = 1883;  

// Connection initialization
WiFiClient espClient;
PubSubClient mqttc(espClient);

// Global Variable
unsigned long lastMsgSent = 0;

// DHT Object
DHT_Unified dht(DHT_PIN, DHT_TYPE);

// Function Declaration
void connectToWifi();
void connectToMqttBroker();
void mqttCallback(char *topic, byte *payload, unsigned int length);
float getTemperature(sensors_event_t &event);
float getHumidity(sensors_event_t &event);

// -------------------------------------------------------------------------------
// START OF MAIN
// -------------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  dht.begin();

  connectToWifi();

  pinMode(LED_PIN, OUTPUT);

  mqttc.setServer(MQTT_BROKER, MQTT_PORT);
  mqttc.setCallback(mqttCallback);

  // Subscribe to MQTT LED topic
  connectToMqttBroker();
}

void loop() {
  // Make sure MQTT LED topic is connected
  if (!mqttc.connected()) {
    connectToMqttBroker();
  }

  // Listen to MQTT msg (trigger callback if there's new msg)
  mqttc.loop();

  // Gather data & Publish to MQTT every 2 seconds
  if(millis() - lastMsgSent >= 2000) {
    lastMsgSent = millis();

    JsonDocument doc;
    sensors_event_t event;

    // Temperature
    doc["temperature"] = getTemperature(event);

    // Humidity
    doc["humidity"] = getHumidity(event);

    // Serialize json to buffer then send it to MQTT broker
    char buffer[200];
    serializeJson(doc, buffer);
    
    mqttc.publish(MQTT_TOPIC_SENSOR, buffer);
  }
}
// -------------------------------------------------------------------------------
// END OF MAIN
// -------------------------------------------------------------------------------



// -------------------------------------------------------------------------------
// Function Definition
// -------------------------------------------------------------------------------

// Connect to wifi
void connectToWifi() {
  WiFi.begin(SSID, PASSWORD);

  Serial.print("\nConnecting to WiFi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to the Wifi Network");
}

// Connect and listen to MQTT LED Topic
void connectToMqttBroker() {
  while(!mqttc.connected()) {
    String client_id = "esp8266-client" + String(WiFi.macAddress());
    Serial.printf("Connecting to MQTT Broker as %s...\n", client_id.c_str());

    if(mqttc.connect(client_id.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Connected to MQTT Broker");

      // Subscribe to LED topic here
      mqttc.subscribe(MQTT_TOPIC_LED);  

      // Check connection by publishing a message
      mqttc.publish(MQTT_TOPIC_LED, "ESP8266 Listening to LED's Topic");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqttc.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// Callback for for LED Topic (also control the LED itself here)
void mqttCallback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  Serial.print("Message: ");

  String message;
  for(unsigned int i = 0; i < length; i++) {
    message += (char) payload[i];
  }

  JsonDocument data;
  deserializeJson(data, message.c_str());
  serializeJson(data, Serial);
  
  Serial.println();
  Serial.println("------------------");

  if(data["led_state"]){
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}

// Helper function for temperature
float getTemperature(sensors_event_t &event) {
  dht.temperature().getEvent(&event);

  if (isnan(event.temperature)) {
    Serial.println("Error reading temperature!");
  }
  else {
    Serial.print("Temperature:");
    Serial.print(event.temperature);
    Serial.println("°C");

    return event.temperature;
  }

  return -1.0;
}

// Helper function for humidity
float getHumidity(sensors_event_t &event) {  
  dht.humidity().getEvent(&event);

  if (isnan(event.relative_humidity)) {
    Serial1.println("Error reading humidity!");
  } else {
    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");

    return event.relative_humidity;
  }

  return -1.0;
}
