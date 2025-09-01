#!	/bin/bash

python3 estimate_throughput.py --nozzleProduction '{"AvgDefectRate":0.0108585,"AvgWaitingTime":"PT20.038S","QuantityProduced":3005,"AvgProcessingTime":"PT14.526S","Timestamp":"2023-05-25T23:58:25","DefectVolume":32}' --outputFile /home/kwlee/mdt/models/welder/ProductivityPrediction/TotalThroughput

	
mdt run aas --operation welder:ProductivityPrediction:Operation \
			--in.NozzleProduction param:welder:NozzleProduction \
			--out.TotalThroughput param:welder:TotalThroughput
