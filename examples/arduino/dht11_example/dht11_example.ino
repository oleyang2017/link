/*
 * 使用DHT11温湿度传感器上传温湿度数据，
 * 演示了如何推送数据到link
 * 开发板为nodemcu
 * 需要安装的库： PubSubClient、SimpleDHT
 * 接线
 * vcc -> 3.3v
 * gnd -> gnd
 * data -> D4(GPIO2)
 * 设备登录名等信息需要通过link客户端获取，按需更改
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SimpleDHT.h>


const char* ssid = "your wifi ssid";
const char* pwd = "your wifi password";
const char* server_host = "127.0.0.1";   // mqtt服务器地址
const int   port = 1883;  // mqtt服务端口号
const char* username = "your device username";  // mqtt登录名
const char* password = "your device password";  // mqtt登录密码
const char* client_id = "your device client_id"; // mqtt设备client_id
const char* tem_topic = "your publish topic";   // 温度topic
const char* hum_topic = "your publish topic";   // 湿度topic
const int pinDHT11 = 2;  // DHT11 DATA引脚


WiFiClient espClient;
PubSubClient client(espClient);
SimpleDHT11 dht11(pinDHT11);

char tem[5];
char hum[5];

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(server_host, port);
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

void reconnect() {
  // 每5秒重新尝试连接直到连接成功
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(client_id, username,password)) {
      Serial.println("connected");
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
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) == SimpleDHTErrSuccess) {
    
    snprintf (tem, 5, "%.2f", float(temperature));
    snprintf (hum, 5, "%.2f", float(humidity));
    client.publish(tem_topic, tem);
    client.publish(hum_topic, hum);
    Serial.println("publish OK: ");
    Serial.print(tem); Serial.print(" ℃, "); 
    Serial.print(hum); Serial.println(" RH");
  }
  
  delay(5000);

}
