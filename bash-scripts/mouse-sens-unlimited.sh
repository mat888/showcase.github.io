#!/bin/bash

#the lower this value the higher the sens
#user-input-inverse-sens=${1}
#inverse-sens="${user-input-inverse-sens:=1}"

inverseSens=${1:-1}

xinput --set-prop 13 "Coordinate Transformation Matrix" 0.2 0 0 0 0.2 0 0 0 $inverseSens
