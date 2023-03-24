const int enc = A0;

void setup()
{
  Serial.begin(9600);
  pinMode(enc, INPUT);
}

void loop() 
{
  int data = analogRead(enc);
  Serial.println(data);
  delay(1);
}
