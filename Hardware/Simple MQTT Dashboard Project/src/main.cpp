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
const char* ssid = "realme 8i";
const char* password = "avinavin";

// MQTT Broker Settings
const char *mqtt_broker = "broker.emqx.io";  
const char *mqtt_topic_led = "avinavin/led";     
const char *mqtt_topic_sensor = "avinavin/sensor";
const char *mqtt_username = "emqx";  
const char *mqtt_password = "public";  
const int mqtt_port = 1883;  

// Connection initialization
WiFiClient espClient;
PubSubClient mqtt_client(espClient);

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

  mqtt_client.setServer(mqtt_broker, mqtt_port);
  mqtt_client.setCallback(mqttCallback);

  // Subscribe to MQTT LED topic
  connectToMqttBroker();
}

void loop() {
  // Make sure MQTT LED topic is connected
  if (!mqtt_client.connected()) {
    connectToMqttBroker();
  }

  // Listen to MQTT msg (trigger callback if there's new msg)
  mqtt_client.loop();

  // Gather data & Publish to MQTT every 2 seconds
  if(millis() - lastMsgSent >= 2000) {
    lastMsgSent = millis();

    JsonDocument doc;
    sensors_event_t event;

    // Temperature
    doc["temperature"] = getTemperature(event);

    // Humidity
    doc["humidty"] = getHumidity(event);

    // Serialize json to buffer then send it to MQTT broker
    char buffer[200];
    serializeJson(doc, buffer);
    
    mqtt_client.publish(mqtt_topic_sensor, buffer);
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
  WiFi.begin(ssid, password);

  Serial.print("\nConnecting to WiFi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to the Wifi Network");
}

// Connect and listen to MQTT LED Topic
void connectToMqttBroker() {
  while(!mqtt_client.connected()) {
    String client_id = "esp8266-client" + String(WiFi.macAddress());
    Serial.printf("Connecting to MQTT Broker as %s...\n", client_id.c_str());

    if(mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT Broker");

      // Subscribe to LED topic here
      mqtt_client.subscribe(mqtt_topic_led);  

      // Check connection by publishing a message
      mqtt_client.publish(mqtt_topic_led, "ESP8266 Listening to LED's Topic");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqtt_client.state());
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

  if(data["led_con"]){
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
