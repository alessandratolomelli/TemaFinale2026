%====================================================================================
% cargosystem description   
%====================================================================================
mqttBroker("localhost", "1883", "sprint2").
request( load_request, loadRequest(none) ).
reply( load_accepted, loadAccepted(SLOTID) ).  %%for load_request
reply( load_retrylater, loadRetryLater(none) ).  %%for load_request
reply( load_refused, loadRefused(none) ).  %%for load_request
event( container_detected, containerDetected(none) ).
event( sonar_fault, sonarFault(none) ).
event( sonar_recovered, sonarRecovered(none) ).
request( find_slot_position, findSlotPosition(SLOTID) ).
reply( slot_position, slotPosition(POSX,POSY) ).  %%for find_slot_position
request( robot_to_ioport, robotToIoport(none) ).
reply( robot_ioport_done, robotIoportDone(none) ).  %%for robot_to_ioport
reply( robot_ioport_failed, robotIoportFailed(ARG) ).  %%for robot_to_ioport
request( robot_to_slot5, robotToSlot5(none) ).
reply( robot_slot5_done, robotSlot5Done(none) ).  %%for robot_to_slot5
reply( robot_slot5_failed, robotSlot5Failed(ARG) ).  %%for robot_to_slot5
request( robot_to_slot, robotToSlot(SLOT) ).
reply( robot_slot_done, robotSlotDone(none) ).  %%for robot_to_slot
reply( robot_slot_failed, robotSlotFailed(ARG) ).  %%for robot_to_slot
request( do_marking, doMarking(none) ).
reply( marking_done, markingDone(none) ).  %%for do_marking
request( find_free_slot, findFreeSlot(none) ).
reply( slot_found, slotFound(SLOTID) ).  %%for find_free_slot
reply( slot_full, slotFull(none) ).  %%for find_free_slot
request( find_occupy, occupySlot(SLOTID) ).
reply( occupy_done, occupySlotDone(none) ).  %%for find_occupy
request( find_release, releaseSlot(SLOTID) ).
reply( release_done, releaseSlotDone(none) ).  %%for find_release
dispatch( do_blink, do_blink(none) ).
dispatch( sensor_data, sensorData(DISTANCE) ).
dispatch( led_blink, ledBlink(STATE) ).
event( robot_complete_notification, robotCompleteNotif(FINALSLOT) ).
dispatch( slot_is_free, slot_is_free(none) ).
dispatch( slot_is_full, slot_is_full(none) ).
request( moverobot, moverobot(TARGETX,TARGETY,STEPTIME) ).
reply( moverobotdone, moverobotdone(ARG) ).  %%for moverobot
reply( moverobotfailed, moverobotfailed(PLANDONE,PLANTODO) ).  %%for moverobot
%====================================================================================
context(ctxcargo, "localhost",  "TCP", "8050").
context(ctxrobotsmart, "127.0.0.1",  "TCP", "8020").
 qactor( robotsmart, ctxrobotsmart, "external").
  qactor( hold, ctxcargo, "it.unibo.hold.Hold").
 static(hold).
  qactor( cargoservice, ctxcargo, "it.unibo.cargoservice.Cargoservice").
 static(cargoservice).
  qactor( cargorobot, ctxcargo, "it.unibo.cargorobot.Cargorobot").
 static(cargorobot).
  qactor( led, ctxcargo, "it.unibo.led.Led").
 static(led).
  qactor( markerdevice, ctxcargo, "it.unibo.markerdevice.Markerdevice").
 static(markerdevice).
  qactor( sonar, ctxcargo, "it.unibo.sonar.Sonar").
 static(sonar).
