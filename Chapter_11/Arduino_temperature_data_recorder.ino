#include <Wire.h>
#include <Adafruit_MLX90614.h> // Import thermometer library
Adafruit_MLX90614 mlx = Adafruit_MLX90614(); // Specify thermometer type
void setup() {
    Serial.begin(9600);
    mlx.begin(); // Initialize temperature sensor
}
void loop() {
    Serial.println(mlx.readAmbientTempC()); // Read and transfer temperature data
    delay(1000);
}
