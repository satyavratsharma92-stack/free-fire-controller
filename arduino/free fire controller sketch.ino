const int LX_PIN  = A0;  // Left Joy X  (WASD left/right)
const int LY_PIN  = A1;  // Left Joy Y  (WASD forward/back)
const int LSW_PIN = 2;   // Left Joy Click → Crouch (C)
const int RX_PIN  = A2;  // Right Joy X (Mouse aim horizontal)
const int RY_PIN  = A3;  // Right Joy Y (Mouse aim vertical)
const int RSW_PIN = 3;   // Right Joy Click → Melee (F)
const int B1_PIN  = 4;   // Button 1 → Fire (Left Mouse)
const int B2_PIN  = 5;   // Button 2 → Jump (Space)
const int B3_PIN  = 6;   // Button 3 → Reload (R)
const int B4_PIN  = 7;   // Button 4 → Scope/ADS (Right Mouse)

void setup() {
  Serial.begin(9600);
  // INPUT_PULLUP: pin is HIGH (1) by default, LOW (0) when button pressed
  pinMode(LSW_PIN, INPUT_PULLUP);
  pinMode(RSW_PIN, INPUT_PULLUP);
  pinMode(B1_PIN,  INPUT_PULLUP);
  pinMode(B2_PIN,  INPUT_PULLUP);
  pinMode(B3_PIN,  INPUT_PULLUP);
  pinMode(B4_PIN,  INPUT_PULLUP);
}

void loop() {
  // ── Read Analog Joysticks (0–1023) ─────────────────────
  int lx  = analogRead(LX_PIN);
  int ly  = analogRead(LY_PIN);
  int rx  = analogRead(RX_PIN);
  int ry  = analogRead(RY_PIN);

  // ── Read Digital (0=pressed, 1=released due to PULLUP) ──
  int lsw = digitalRead(LSW_PIN);
  int rsw = digitalRead(RSW_PIN);
  int b1  = digitalRead(B1_PIN);
  int b2  = digitalRead(B2_PIN);
  int b3  = digitalRead(B3_PIN);
  int b4  = digitalRead(B4_PIN);

  // ── Send 10 values, comma-separated, newline terminated ─
  // Format: lx,ly,lsw,rx,ry,rsw,b1,b2,b3,b4
  Serial.print(lx);  Serial.print(',');
  Serial.print(ly);  Serial.print(',');
  Serial.print(lsw); Serial.print(',');
  Serial.print(rx);  Serial.print(',');
  Serial.print(ry);  Serial.print(',');
  Serial.print(rsw); Serial.print(',');
  Serial.print(b1);  Serial.print(',');
  Serial.print(b2);  Serial.print(',');
  Serial.print(b3);  Serial.print(',');
  Serial.println(b4); // println adds \n at end

  delay(20); // ~50 reads per second — smooth enough for gaming
}