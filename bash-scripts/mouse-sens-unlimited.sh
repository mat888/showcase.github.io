#!/bin/bash

#script allows changing of mouse sensitivity outside range normally allowed

#the lower the input value the higher the sens

#defaults to 1
inverseSens=${1:-1}

xinput --set-prop 13 "Coordinate Transformation Matrix" 0.2 0 0 0 0.2 0 0 0 $inverseSens
