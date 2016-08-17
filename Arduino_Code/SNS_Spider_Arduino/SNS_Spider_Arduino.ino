/*
 * File: SNS_Spider_Arduino.ino
 * 
 * Author: Jiankai Li
 * Date: 2016-08-11
 * Modify：Jiankai Li
 * In this demo, mt7688Duo spider someone special's sns account such as facebook or twiter, in this demo, we'll spider someone's weibo account. 
 * The message will save to files("/tmp/message") and the printFlag will save to ("/tmp/printFlag")
 *
 * Mertirials: Thermal Printer
 *             mt7688Duo
 *             Breakout for LinkIt Smart 7688Duo
 * 
 */
#include <Process.h>
#include <string.h>
#include <FileIO.h>
#include <avr/wdt.h>
#include <TimerOne.h>

#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"

#define PIXIEL_PIN 6
#define PIXIEL_NUM 6
#define USER_MAXNUM   6

#define INTERVAL      1          // Time interval unit s
#define INTERVAL_DATA 5          // Time interval unit s
#define RELAY_PIN     5          // 

#define TX_PIN 5 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 4 // Arduino receive   GREEN WIRE   labeled TX on printer
SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor


unsigned long previousTime = 0;  // define the last time  unit s
unsigned long previousTimeData = 0;  // define the data last time  unit 

/* Define the state machine status */

enum Status 
{
	UpdatePrinter    =  4,
	Unknow           =  5,
};
typedef enum Status Systemstatus;
Systemstatus WorkingStatus;

#define BUF_SIZE  8
char *g_Buffer;
char buff[30];
int g_BufferIndex;



void setup() {
  Serial.begin(9600);
  Serial.println("power on!");


  // Initialize Bridge
  Bridge.begin();
  // Initialize the FileSystem
  FileSystem.begin();
  // Initialize the HDC1000
  
  // Initialize the printer
  mySerial.begin(19200);
  printer.begin();
  printer.setDefault();
  
  
  previousTime = millis()/1000;
  previousTimeData = millis()/1000 - random(3,10);
  
  delay(1000);
  wdt_enable(WDTO_2S);
 
  Timer1.initialize(1000000); // set a timer of length 1000000 microseconds 1 second
  Timer1.attachInterrupt( timerIsrFeedFog ); // attach the service routine here
  wdt_reset();
}

void loop() {
	unsigned long currentTime = millis()/1000;
	int speed;
	int user_num;
	if (currentTime - previousTime >= INTERVAL) {

		previousTime = currentTime;
		WorkingStatus = UpdatePrinter;
	}

	switch(WorkingStatus){
	case UpdatePrinter:
        uint8_t command;
		command = bridgeGetPrintCom();
        bridgeClearPrintCom();
		if (1 == command) {
            
            printer.wake(); 
			Serial.println("------------------------Open Printer--------------------------");
			// printerTest();
			bridgeGetPrintMessage();
			// bridgeClearPrintCom();
            printer.sleep();
		}
		Serial.println("UpdatePrinter");
		WorkingStatus = Unknow;
        break;
		
	case Unknow:
		break;
	default:
		break; 
	}
	
}

/* Get the printer command from 7688 */
uint8_t bridgeGetPrintCom() {
	Process p;
	String str;
	uint8_t command;
	p.begin("cat");
	p.addParameter("/tmp/printFlag");
	p.run();
	while (p.available() > 0) {
		char c = p.read();
		str += c;
	}
	command = str.toInt();
	return command;
	
}

/* Clear the printer command  */
void bridgeClearPrintCom() {
	File script = FileSystem.open("/tmp/printFlag",FILE_WRITE);
	script.print(0);
	script.close();
}

void bridgeGetPrintMessage() {
	Process p;
	String str;
	p.begin("cat");
	p.addParameter("/tmp/message");
	p.run();
	while (p.available() > 0) {
		char c = p.read();
		str += c;
	}
    Serial.println(str);
    
    printer.setSize('L');        // Set type size, accepts 'S', 'M', 'L'  
    printer.justify('C');
    printer.println("Lambor's SNS");
    printer.setDefault();
    Serial.println("-----------Print the message-----------------");
    Serial.println(str.length());

    printer.print(str);
    printer.feed(4);  

}

void timerIsrFeedFog()
{
    wdt_reset();
    Serial.println("------------Time ISR");
}
