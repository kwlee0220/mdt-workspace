#!	/bin/bash

mdt add test $MDT_HOME/models/test

mdt add welder $MDT_HOME/models/welder

mdt add inspector $MDT_HOME/models/innercase/inspector
mdt add heater $MDT_HOME/models/innercase/heater
mdt add trimmer $MDT_HOME/models/innercase//trimmer
mdt add former $MDT_HOME/models/innercase/former
mdt add innercase $MDT_HOME/models/innercase/innercase

mdt add panda $MDT_HOME/models/panda
mdt add opcua $MDT_HOME/models/opcua
mdt add tp-75 $MDT_HOME/models/tp-75

mdt add cnc ./cnc -p 19008
mdt add ktech_inspector ./ktech/inspector -p 19009

# 성균관대 삼천산업 라인
mdt add NozzleAssemblyLine $MDT_HOME/models/skku/NozzleAssemblyLine
mdt add InjectionMouldingProcess $MDT_HOME/models/skku/InjectionMouldingProcess
mdt add InjectionMoulding $MDT_HOME/models/skku/InjectionMoulding
mdt add WeldingProcess $MDT_HOME/models/skku/WeldingProcess
mdt add Welder $MDT_HOME/models/skku/Welder
mdt add FlatnessTestProcess $MDT_HOME/models/skku/FlatnessTestProcess
mdt add FlatnessTest $MDT_HOME/models/skku/FlatnessTest
mdt add AssemblyProcess $MDT_HOME/models/skku/AssemblyProcess
mdt add Assembly $MDT_HOME/models/skku/Assembly
mdt add RotationTorqueInspectionProcess $MDT_HOME/models/skku/RotationTorqueInspectionProcess
mdt add RotationTorqueInspection $MDT_HOME/models/skku/RotationTorqueInspection
mdt add VisionInspectionProcess $MDT_HOME/models/skku/VisionInspectionProcess
mdt add VisionInspection $MDT_HOME/models/skku/VisionInspection
mdt add PackagingProcess $MDT_HOME/models/skku/PackagingProcess
mdt add Packaging $MDT_HOME/models/skku/Packaging

mdt add skku_innercase $MDT_HOME/models/skku/innercase
mdt add skku_inspector $MDT_HOME/models/skku/inspector
mdt add skku_crf $MDT_HOME/models/skku/crf




# LG 냉장고 생산 공정
## CRF 공정
mdt add 01ECEM001 $MDT_HOME/models/lg-fridge/CRF_공정/01ECEM001 -p 19122
mdt add 01ECEM002 $MDT_HOME/models/lg-fridge/CRF_공정/01ECEM002 -p 19123
mdt add 01ECEM003 $MDT_HOME/models/lg-fridge/CRF_공정/01ECEM003 -p 19124
mdt add 01ECON027 $MDT_HOME/models/lg-fridge/CRF_공정/01ECON027 -p 19125
mdt add 01ECON028 $MDT_HOME/models/lg-fridge/CRF_공정/01ECON028 -p 19126
mdt add 01ECON029 $MDT_HOME/models/lg-fridge/CRF_공정/01ECON029 -p 19127
mdt add 01EETC025 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC025 -p 19128
mdt add 01EETC026 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC026 -p 19129
mdt add 01EETC027 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC027 -p 19130
mdt add 01EETC028 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC028 -p 19131
mdt add 01EETC029 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC029 -p 19132
mdt add 01EETC030 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC030 -p 19133
mdt add 01EETC031 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC031 -p 19134
mdt add 01EETC032 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC032 -p 19135
mdt add 01EETC033 $MDT_HOME/models/lg-fridge/CRF_공정/01EETC033 -p 19136
mdt add 01EINP001 $MDT_HOME/models/lg-fridge/CRF_공정/01EINP001 -p 19137
mdt add 01EINP002 $MDT_HOME/models/lg-fridge/CRF_공정/01EINP002 -p 19138
mdt add 01EPRF010 $MDT_HOME/models/lg-fridge/CRF_공정/01EPRF010 -p 19139
mdt add 01EPRF011 $MDT_HOME/models/lg-fridge/CRF_공정/01EPRF011 -p 19140
mdt add 01EPRF012 $MDT_HOME/models/lg-fridge/CRF_공정/01EPRF012 -p 19141
mdt add 01EROB045 $MDT_HOME/models/lg-fridge/CRF_공정/01EROB045 -p 19142
mdt add 01ESUU001 $MDT_HOME/models/lg-fridge/CRF_공정/01ESUU001 -p 19143
mdt add 01ESUU002 $MDT_HOME/models/lg-fridge/CRF_공정/01ESUU002 -p 19144
mdt add 01ESUU003 $MDT_HOME/models/lg-fridge/CRF_공정/01ESUU003 -p 19145
mdt add 01ESUU004 $MDT_HOME/models/lg-fridge/CRF_공정/01ESUU004 -p 19146
mdt add 01ESUU005 $MDT_HOME/models/lg-fridge/CRF_공정/01ESUU005 -p 19147
mdt add CRFProcess $MDT_HOME/models/lg-fridge/CRF_공정/CRFProcess -p 19148

## Cycle 조립
mdt add 01EATT018 $MDT_HOME/models/lg-fridge/Cycle_조립/01EATT018 -p 19100
mdt add 01EATT019 $MDT_HOME/models/lg-fridge/Cycle_조립/01EATT019 -p 19101
mdt add 01EETC048 $MDT_HOME/models/lg-fridge/Cycle_조립/01EETC048 -p 19102
mdt add 01EETC050 $MDT_HOME/models/lg-fridge/Cycle_조립/01EETC050 -p 19103
mdt add 01EETC051 $MDT_HOME/models/lg-fridge/Cycle_조립/01EETC051 -p 19104
mdt add 01EETC078 $MDT_HOME/models/lg-fridge/Cycle_조립/01EETC078 -p 19105
mdt add 01ELAB005 $MDT_HOME/models/lg-fridge/Cycle_조립/01ELAB005 -p 19106
mdt add 01ELAB006 $MDT_HOME/models/lg-fridge/Cycle_조립/01ELAB006 -p 19107
mdt add 01ELAB008 $MDT_HOME/models/lg-fridge/Cycle_조립/01ELAB008 -p 19108
mdt add 01ELAB009 $MDT_HOME/models/lg-fridge/Cycle_조립/01ELAB009 -p 19109
mdt add 01ELAM011 $MDT_HOME/models/lg-fridge/Cycle_조립/01ELAM011 -p 19110
mdt add 01EROB049 $MDT_HOME/models/lg-fridge/Cycle_조립/01EROB049 -p 19111
mdt add 01EROB050 $MDT_HOME/models/lg-fridge/Cycle_조립/01EROB050 -p 19112
mdt add 01EROB051 $MDT_HOME/models/lg-fridge/Cycle_조립/01EROB051 -p 19113
mdt add 01EWEM013 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM013 -p 19114
mdt add 01EWEM015 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM015 -p 19115
mdt add 01EWEM016 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM016 -p 19116
mdt add 01EWEM020 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM020 -p 19117
mdt add 01EWEM021 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM021 -p 19118
mdt add 01EWEM022 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM022 -p 19119
mdt add 01EWEM023 $MDT_HOME/models/lg-fridge/Cycle_조립/01EWEM023 -p 19120
mdt add CycleAssembly $MDT_HOME/models/lg-fridge/Cycle_조립/CycleAssembly -p 19121


mdt get element welder:WelderAmpereLog:Segments.Tail -r 100ms
(cd $MDT_HOME/models/test; java -cp $JAR $MAIN_CLASS --loglevel-external INFO endpoints[0].port=19000)
(cd $MDT_HOME/models/innercase; java -cp $JAR $MAIN_CLASS --loglevel-external INFO endpoints[0].port=19005)

mdt set element param:inspector:UpperImage --file /home/kwlee/mdt/models/innercase/inspector/test_images/Innercase05-5.jpg


mosquitto_sub -t mdt/#

mdt run http --endpoint http://localhost:12987 --opId test/AddAndSleep --poll 1s --loglevel info \
			--in.Data param:test:Data:ParameterValue --in.IncAmount 3 --in.SleepTime 0.5 --out.Output param:test:Data
mdt run http --endpoint http://localhost:12987 --opId test/AddAndSleep --poll 1s \
			--in.Data param:test:Data:ParameterValue \
			--in.IncAmount param:test:IncAmount:ParameterValue \
			--in.SleepTime param:test:SleepTime:ParameterValue \
			--out.Output param:test:Data:ParameterValue
			
mdt run program /home/kwlee/mdt/mdt-operation-server/test/AddAndSleep/operation.json --workingDir /home/kwlee/mdt/mdt-operation-server/test/AddAndSleep \
			--in.Data 7 --in.IncAmount 3 --in.SleepTime 0.5 --out.Output param:test:Data:ParameterValue
mdt run program /home/kwlee/mdt/mdt-operation-server/test/AddAndSleep/operation.json --workingDir /home/kwlee/mdt/mdt-operation-server/test/AddAndSleep \
			--in.Data param:test:Data:ParameterValue \
			--in.IncAmount param:test:IncAmount:ParameterValue \
			--in.SleepTime param:test:SleepTime:ParameterValue \
			--out.Output param:test:Data:ParameterValue
			

mdt run http --server http://localhost:12987 --opid inspector/ThicknessInspection --poll 1s --timeout 1m \
	--in.UpperImage param:inspector:UpperImage \
	--out.Defect inspector:ThicknessInspection:AIInfo.Outputs[0].OutputValue \
	--loglevel info

mdt run task inspector:ThicknessInspection \
	--in.UpperImage param:inspector:UpperImage:ParameterValue \
	--out.Defect oparg:inspector:ThicknessInspection:out:Defect \
	--loglevel info

mdt run task inspector:ThicknessInspection:Operation \
	--in.UpperImage param:inspector:UpperImage:ParameterValue \
	--out.Defect oparg:inspector:ThicknessInspection:out:Defect \
	--loglevel info
	
mdt run aas --operation welder:ProductivityPrediction:Operation \
			--in.NozzleProduction param:welder:NozzleProduction \
			--out.TotalThroughput param:welder:TotalThroughput
	
mdt run aas --operation inspector:ThicknessInspection:Operation \
	--in.UpperImage param:inspector:UpperImage \
	--out.Defect inspector:ThicknessInspection:AIInfo.Outputs[0].OutputValue \
	--loglevel info

mdt run aas --operation innercase:ProcessOptimization:Operation \
--in.HTCycleTime param:heater:CycleTime:ParameterValue \
--in.VFCycleTime param:heater:CycleTime:ParameterValue \
--in.PTCycleTime param:heater:CycleTime:ParameterValue \
--in.QICycleTime param:heater:CycleTime:ParameterValue \
--out.TotalThroughput param:innercase:CycleTime \
--loglevel info

Line (라인)
ItemMaster (자재)
BOM (자재)
Routing (공정순서)
Operation (공정)
Equipment (설비)
Component (설비)
ProductionOrder (생산지시)
ProductionPerformance (생산실적)
ProductionDefect (불량생산)
ProductionPersonnelPerform (생산인력)
Perseonnel (사람)
Repair (수리이력)
Andon (안돈)

---------------------------------------------------------------------------------------------------------
# 올라온 컨트롤러 확인
ros2 control list_controllers

# joint_state_broadcaster 비활성화
ros2 control switch_controllers --deactivate joint_state_broadcaster

# 이제 당신이 지속적으로 joint_states 퍼블리시 (예: 30Hz)
ros2 topic pub -r 30 /joint_states sensor_msgs/msg/JointState "{
  name: ['panda_joint1','panda_joint2','panda_joint3','panda_joint4','panda_joint5','panda_joint6','panda_joint7'],
  position: [0.0,-0.5,0.0,-2.0,0.0,1.5,0.7]
}"
--------------------------------------------------------------------------------------------------------------

AASOperationTask인 경우 option에 operation 추가
timeout이 지정되지 않은 경우에는 timeout 자체를 생략함
