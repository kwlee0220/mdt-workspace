#!	/bin/bash

python3 read_nozzle_audit.py --quantityProduced 1789 --avgProcessingTime 3555 --avgWaitingTime 3999 --defectVolume 21 --avgDefectRate 0.012131716 --outputFile output

mdt run aas --operation welder:ProductivityPrediction:Operation \
          --in.Timestamp param:welder:NozzleProduction:EventDateTime \
          --in.NozzleProduction param:welder:NozzleProduction:ParameterValue \
          --out.TotalThroughput param:welder:TotalThroughput
