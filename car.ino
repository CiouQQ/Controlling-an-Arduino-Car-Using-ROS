/*
AUTHOR: Hazim Bitar (techbitar)
DATE: Aug 29, 2013
LICENSE: Public domain (use at your own risk)
CONTACT: techbitar at gmail dot com (techbitar.com)
*/
#include<ros.h>
#include<std_msgs/String.h>
 
ros::NodeHandle nh;
 


const byte LEFT1 = 8;
const byte LEFT2 = 9;
const byte LEFT_PWM = 10;

const byte RIGHT1 = 7;
const byte RIGHT2 = 6;
const byte RIGHT_PWM = 5;

byte motorSpeed = 130;

void mstop()
{
  analogWrite(LEFT_PWM,0);
  analogWrite(RIGHT_PWM,0);
}
void backward(int Lspeed,int Rspeed)
{
  digitalWrite(LEFT1, LOW); 
  digitalWrite(LEFT2, HIGH);
  analogWrite(LEFT_PWM,Lspeed);
  digitalWrite(RIGHT1, HIGH); 
  digitalWrite(RIGHT2, LOW);
  analogWrite(RIGHT_PWM,Rspeed);
}
void forward(int Lspeed,int Rspeed)
{
  digitalWrite(LEFT1, HIGH); 
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM,Lspeed);
  digitalWrite(RIGHT1, LOW); 
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM,Rspeed);
}
void turnRight()
{
  digitalWrite(LEFT1, HIGH); 
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM,90);
  digitalWrite(RIGHT1, HIGH); 
  digitalWrite(RIGHT2, LOW);
  analogWrite(RIGHT_PWM,110);
}
void turnLeft()
{
  digitalWrite(LEFT1, LOW); 
  digitalWrite(LEFT2, HIGH);
  analogWrite(LEFT_PWM,90);
  digitalWrite(RIGHT1, LOW); 
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM,110);
}

void stopCb(const std_msgs::String &stop){
    turnRight();
    delay(100);
    mstop();
}
void slowCb(const std_msgs::String &slow){
    mstop();
    
    
}
void normalCb(const std_msgs::String &normal){
    forward(80,100);
    delay(100);
    mstop();
    
    
}
void fastCb(const std_msgs::String &fast){
    forward(130,150);
    
    
}
void rightCb(const std_msgs::String &right){
    turnRight();
    delay(100);
    mstop();
}
void leftCb(const std_msgs::String &left){
    turnLeft();
    delay(100);
    mstop();
}
ros::Subscriber<std_msgs::String> sub0("stop", &stopCb);
ros::Subscriber<std_msgs::String> sub1("slow", &slowCb);
ros::Subscriber<std_msgs::String> sub2("normal", &normalCb);
ros::Subscriber<std_msgs::String> sub3("fast", &fastCb);
ros::Subscriber<std_msgs::String> subR("right", &rightCb);
ros::Subscriber<std_msgs::String> subL("left", &leftCb);
void setup()
{
 pinMode(LEFT1, OUTPUT); // this pin will pull the HC-05 pin 34 (key pin) HIGH to switch module to AT mode
 pinMode(LEFT2, OUTPUT);
 pinMode(LEFT_PWM, OUTPUT);
 pinMode(RIGHT1, OUTPUT);
 pinMode(RIGHT2, OUTPUT);
 pinMode(RIGHT_PWM, OUTPUT);
 nh.initNode();
 nh.subscribe(sub0);
 nh.subscribe(sub1);
 nh.subscribe(sub2);
 nh.subscribe(sub3);
 nh.subscribe(subR);
 nh.subscribe(subL);
 

}
void loop()
{
  nh.spinOnce();
  delay(100);

 
}
