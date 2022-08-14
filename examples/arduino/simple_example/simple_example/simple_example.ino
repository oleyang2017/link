/*
 * 这是最简单的连接link的arudino示例，
 * 演示了如何推送数据到link，以及接收并处理link发送的指令控制板载LED灯
 * 开发板为nodemcu
 * 设备登录名等信息需要通过link客户端获取，按需更改
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your wifi ssid";
const char* pwd = "your wifi password";
const char* server_host = "127.0.0.1";   // mqtt服务器地址
const int   port = 1883;  // mqtt服务端口号
const char* username = "your device username"  // mqtt登录名
const char* password = "your device password"  // mqtt登录密码
const char* client_id = "your device client_id" // mqtt设备client_id
const char* pub_topic = "your publish topic"   // mqtt推送topic名称
const char* sub_topic = "your publish topic"   // mqtt订阅topic名称


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int randNum;

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(server_host, port);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, pwd);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(client_id, username,password)) {
      Serial.println("connected");
      client.publish(pub_topic, "1");
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      Serial.print("client_id:");
      Serial.print(client_id);
      Serial.print("  username:");
      Serial.print(username);
      Serial.print("  password:");
      Serial.println(password);
      Serial.println("try again in 5 seconds");
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
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(pub_topic, msg);
  }
}
