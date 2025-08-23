#include <Servo.h>
Servo motor;
String input;
int target_speed;
void setup() {
    motor.attach(3);
    Serial.begin(9600);
}
void loop()
{
  if(Serial.available()) // Check if data available in serial port
    {
    input = Serial.readStringUntil('\n'); // Read data until newline
    target_speed = input.toInt();
    motor.write(target_speed);    // Move motor at target speed
    }
}
