#include <WiFi.h>
#include <PubSubClient.h>


// Set the network SSID/Password
const char* ssid = "steren_2_4G";
const char* password = "password";

// Add mosquitto MQTT Broker IP address
const char* mqtt_server = "192.168.1.7";

//Define
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
float num = 0.0;
const int green1 = 14;
const int red1 = 12;
const int green2 = 27;
const int red2 = 26;
const int green3 = 33;
const int red3 = 32;
const int green4 = 15;
const int red4 = 2;


const int sw1 = 13;
const int sw2 = 25;
const int sw3 = 16;
const int sw4 = 4;

String alarm1 = "off";

//Set-up configurations
void setup() {
  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(sw1, INPUT_PULLUP);
  pinMode(green1, OUTPUT);
  pinMode(red1, OUTPUT);
  pinMode(sw2, INPUT_PULLUP);
  pinMode(green2, OUTPUT);
  pinMode(red2, OUTPUT);
  pinMode(sw3, INPUT_PULLUP);
  pinMode(green3, OUTPUT);
  pinMode(red3, OUTPUT);
  pinMode(sw4, INPUT_PULLUP);
  pinMode(green4, OUTPUT);
  pinMode(red4, OUTPUT);
}

//Connecting to WiFi network
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//Callback for MQTT received messages
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // If a message is received on the topic esp32/LED, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == "esp32/green1") {
    Serial.print("Changing LED to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(green1, HIGH);
      digitalWrite(red1, LOW);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(green1, LOW);
      digitalWrite(red1, HIGH);
    }
  }

  if (String(topic) == "esp32/green2") {
    Serial.print("Changing LED to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(green2, HIGH);
      digitalWrite(red2, LOW);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(green2, LOW);
      digitalWrite(red2, HIGH);
    }
  }

  if (String(topic) == "esp32/green3") {
    Serial.print("Changing LED to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(green3, HIGH);
      digitalWrite(red3, LOW);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(green3, LOW);
      digitalWrite(red3, HIGH);
    }
  }

  if (String(topic) == "esp32/green4") {
    Serial.print("Changing LED to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(green4, HIGH);
      digitalWrite(red4, LOW);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(green4, LOW);
      digitalWrite(red4, HIGH);
    }
  }
}

//Connecting to MQTT broker
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe to topics
      client.subscribe("esp32/green1");
      client.subscribe("esp32/green2");
      client.subscribe("esp32/green3");
      client.subscribe("esp32/green4");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;

    
    if (digitalRead(sw1) == 0){
      client.publish("esp32/alarm1", "on");
      while (digitalRead(sw1) == 0);
      client.publish("esp32/alarm1", "off");
    }

    if (digitalRead(sw2) == 0){
      client.publish("esp32/alarm2", "on");
      while (digitalRead(sw2) == 0);
      client.publish("esp32/alarm2", "off");
    }

    if (digitalRead(sw3) == 0){
      client.publish("esp32/alarm3", "on");
      while (digitalRead(sw3) == 0);
      client.publish("esp32/alarm3", "off");
    }

    if (digitalRead(sw4) == 0){
      client.publish("esp32/alarm4", "on");
      while (digitalRead(sw4) == 0);
      client.publish("esp32/alarm4", "off");
    }
    

    /*
    //Preparingn data to send
    num++;
    if (num>100) num=0;   
    
    // Convert the value to a char array
    char numString[8];
    dtostrf(num, 1, 2, numString);
    Serial.println("Sending message on topic: esp32/num");
    client.publish("esp32/num", numString);
    */
  }
}
