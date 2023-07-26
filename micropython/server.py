import max30102
import ssd1306
from machine import Pin, I2C
import time
import requests
import smtplib

# Initialize OLED display
i2c = I2C(-1, Pin(22), Pin(21))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Initialize MAX30102 sensor
sensor = max30102.MAX30102()

# Set LED brightness, sample rate, and number of samples to average
sensor.set_led_pulse_amplitude(0x1F)
sensor.set_sample_rate(max30102.SAMPLE_RATE_100)
sensor.set_pulse_width(max30102.PULSE_WIDTH_160)
sensor.set_finger_threshold(750)
sensor.set_finger_threshold(100)
sensor.enable_spo2()

# Display startup message on OLED display
display.fill(0)
display.text('MAX30102 & ESP32', 0, 0)
display.text('Pulse Oximeter', 0, 10)
display.show()

# Set alert threshold and email configuration
alert_threshold = 80  # Set your desired heart rate alert threshold
email_sender = 'sender@example.com'  # Sender's email address
email_password = 'password'  # Sender's email password
email_receiver = 'receiver@example.com'  # Receiver's email address

# Read heart rate and oxygen saturation values and display on OLED display
while True:
    red, ir, spo2 = sensor.read_sensor()
    bpm = sensor.calculate_heart_rate(ir)
    display.fill(0)
    display.text('BPM: {}'.format(bpm), 0, 0)
    display.text('SpO2: {}%'.format(spo2), 0, 10)
    display.show()

    if bpm >= alert_threshold:
        # Send email notification
        subject = 'Heart Rate Alert'
        body = 'Heart rate exceeded the threshold: {}'.format(bpm)
        message = 'Subject: {}\n\n{}'.format(subject, body)

        try:
            server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your email server and port
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message)
            server.quit()
            print('Email notification sent')
        except Exception as e:
            print('Failed to send email notification:', e)

    time.sleep_ms(10)