/* 
***DOCUMENTATION SHEET***

this code makes a motor controller for eight (number can be modified using NUM_MOTORS constant) afro 30A ESCs. it 
can be interacted with through pins 0 and 1 (default rx and tx), so it can also be tested with the IDE monitor. on startup, if all goes well, 
you should hear a beep from each ESC, then five seconds later each motor will spin at 10% power for 500 ms, one at a time. this startup
sequence can be disabled by setting the constant STARTING_SEQUENCE to 0 (1 is enabled, 0 is disabled). obviously, make sure you have it disabled
when you actually go into the water. if instead you start hearing frequent beeps after eight seconds, refer to the ESC's manual, 
as it means it's not receiving any signals. also keep in mind they need to receive this signal immediatly after their startup, 
so you should reset them and the arduino at the same time when starting.

there is a debug constant named SEND_RESPONSE; if set to 1, it will send a 0 for an invalid motor, a 1 for an out of bounds speed, and
a 2 for a success. if set to 2, it will give all above data, as well as echo the full buffer minus the colon once it has fully processed it,
("Full input: (your string here)") and all data it parses ("Parsed data: (speed, motor)"). keep in mind that if either data point is
invalid, it will be parsed as 0. otherwise, it will not send any data back

the format is as follows:
(speed as float from -1 to 1, works as a percentage. max two decimal points),(motor as int from 2-9):
eg. 0.5,3:
this turns the second motor at 50%. also, the colon is REQUIRED, and keep in mind the motors start at 2, not 0.
commands can also be chained,
eg. 0.5,3:0.1,4:0.6,7:
keep in mind the motor will always keep whatever its previous command is until it gets a new one, so to turn it off you need to send 0 to
all motors.

the code isn't too complicated, so for any questions/problems, you should be able to look over the code and find the answer. there are also
comments which should hopefully explain anything you don't understand


in case of a bad speed input, the speed will be set to 0, so the motor you are trying to set will be stopped (assuming a valid motor). if the motor
is invalid, the motor number will be set to 0, and as the motor numbers begin at 2, nothing will happen
*/


/*
TODO
- out of bounds speed fix, not just set to 0 (not sure how to do this but its prob possible)
- config about starting pin
- more responses/data
- document all responses better
*/




// ### CONFIG BEGIN ###

#define NUM_MOTORS 8
#define STARTUP_SEQUENCE 0
// 0 off, 1 on
#define SEND_RESPONSE 1
// 0 no response, 1 end status response, 2 full data

// changing these variables (especially INVALID_MOTOR_RESPONSE) may cause issues, use with caution
#define INVALID_MOTOR_RESPONSE 0
#define OUT_OF_BOUNDS_SPEED_RESPONSE 1
#define SUCCESS_RESPONSE 2

// ### CONFIG END ###






#define MAXBUF 256 // maximum size for the buffer


#include <Servo.h>


Servo motors[NUM_MOTORS];


void forward(int speed, int motor) {
  if(speed >= 0 && speed <= 180) {
    motors[motor].write(speed);
  }
}


void setup() {
  Serial.begin(9600); // default serial opens on pins 0 and 1, you can also use the serial monitor
  for(int i = 0; i < NUM_MOTORS; i++) {
    motors[i].attach(i+2, 1000, 2000); // we start at two because pins 0 and 1 are used for serial
    forward(90, i); // send neutral signal to motors, required for the afro 30A ESC startup- this needs to be modified for different ESCs
  }
  delay(5000); // wait five seconds to give time for ESC startup
  if(STARTUP_SEQUENCE == 1) {
    for(int i = 0; i < NUM_MOTORS; i++) {
      forward(100, i);
      delay(500);
      forward(90, i); // turn motor on, wait 500ms, turn off
    }
  }
}

char buf[MAXBUF];
int charsinbuf = 0;

void loop() {

  charsinbuf = 0; // reset buffer

  // the point of having a custom buffer is that if you were to try to read character-by-character from the serial, you would read 
  // faster than it is sent, and the code would think halfway through is the whole command; this way, we can reliably 
  // get the entire command as one string

  while((charsinbuf == 0) || (buf[charsinbuf-1] != ':')) { 
    // until we find a colon (end character), we also ignore the first time because it would try to read out-of-bounds (index -1)
    if(Serial.available() > 0) {
      buf[charsinbuf] = Serial.read();
      charsinbuf++;
    }
    if (charsinbuf == MAXBUF) { // reset if it hits the max
      charsinbuf = 0;
    }
  }

  buf[charsinbuf-1] = '\0'; // get rid of the colon, and replace it with the string end character
  if(SEND_RESPONSE == 2) {
    Serial.print("Full input: ");
    Serial.println(buf);
  }


  char *spd = strtok(buf, ","); // get the speed as a string from everything up to the first comma
  float speed = atof(spd); // try to turn it into a float, if it isn't numerical it becomes 0.0
  char *mtr = strtok(NULL, ","); // using NULL finds the next number
  int motor = atoi(mtr); // parse int, otherwise 0

  if(SEND_RESPONSE == 2) {
    Serial.print("Parsed data: ")
    Serial.print(speed);
    Serial.print(", ");
    Serial.println(motor);
  }

  if(speed > 1.0 || speed < -1.0) {
    if(SEND_RESPONSE > 0) {
      Serial.println(OUT_OF_BOUNDS_SPEED_RESPONSE);
    }
    return;
  }

  if(motor < 2 || motor >= 2 + NUM_MOTORS) {
    if(SEND_RESPONSE > 0) {
      Serial.println(INVALID_MOTOR_RESPONSE);
    }
    return;
  }

  // two decimal places of accuracy
  // we multiply by 100 and floor it because the map function only accepts ints, so we set the bounds to -100 to 100
  forward(map(floor(speed*100.0), -100, 100, 0, 180), motor-2);
  // motor is subtracted by two to bring it back to 0. the only reason to have it at 2 in the first place is to be able to differentiate from
  // the first motor (would be index 0) and the output of the atoi function given an invalid motor (would also be 0)
  // one advantage is that with this the number you send should be the same as the pin numbers of the motors
    if(SEND_RESPONSE > 0) {
      Serial.println(SUCCESS_RESPONSE);
    }
  }
    
    