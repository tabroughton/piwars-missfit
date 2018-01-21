#! /bin/bash
echo "Updating atmega328 with to latest slave firmware"
echo "============================="
echo " http://www.digitalpolymath.co.uk "
echo " Run this program: "
echo " sudo ./atmegaupdate.sh"
echo " "
echo " you need to have arduino, arduino-mk and avrdude to run this script"
echo "============================="

echo "ARDUINO_DIR  = /usr/share/arduino" >> Makefile
echo "BOARD_TAG    = atmega328" >> Makefile
echo "include /usr/share/arduino/Arduino.mk" >> Makefile
make
rm Makefile
echo "Make complete"

read -n1 -p "Do you want to update the slave firmware? [y,n]" input
if [[ $input == "Y" || $input == "y" ]]; then
       	printf "\nMake sure that the atmega is connected to Raspberry Pi"
else
        printf "\nExiting..."
	exit 0
fi
if [ $(find build-atmega328 -name "atmegaslave.hex") ]; then
	printf "\nFirmware found"
else
	printf "\nFirmware not found\nCheck if firmware is there or run again\nPress any key to exit"
 	read
	exit 0
fi

printf "\nPress any key to start firmware update\n. . .";
read -n1
avrdude -C avrdude_gpio.conf -c missfit -p atmega328p -v -U flash:w:build-atmega328/atmegaslave.hex:i

read -n1 -p "Do you want to clean up the files? [y,n]" input
if [[ $input == "Y" || $input == "y" ]]; then
       	printf "\nRemoving build files"
        rm -rf build-atmega328
fi
printf "\nFirmware updated"
