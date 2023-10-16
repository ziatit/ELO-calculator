# ELO-calculator
ELO calculator that I created for Krakowska Szkoła Fechtunku.
Krakowska Szkoła Fechtunku is a fencing school based in Kraków. The school holds a monthly league meetings for its pupils so they can practice in turnament like conditions. These events generate data that can be used to create elo ranking which is interesting from analytical point of view, and usefull in training process as an aditional source of insight into fencers developement.
The code is an implementation of standard ELO used in chess. 
new fencers are assigned ELO of 1200. The higher the ELO difference between two given fencers, the more lower ranked one can gain (and higher ranked one loose).
Code generates both current ranking with placements as of last league meeting, as well as data frame with figth results that can be used to trace ELO changes after every single bout.
