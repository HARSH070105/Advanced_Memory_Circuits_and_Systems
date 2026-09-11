* AMCAS Lab 6T read, bitline discharge and margin
.include 45nm_bulk.txt

.param VDD=1.1 VBL=1.1
Vdd vdd 0 'VDD'
Vwl wl 0 PWL(0 0 1n 0 1.05n 'VDD')

* cross-coupled pair, Q=0 QB=1
MP1 qb q  vdd vdd pmos W=0.15u L=0.045u
MN1 qb q  0   0   nmos W=0.20u L=0.045u
MP2 q  qb vdd vdd pmos W=0.15u L=0.045u
MN2 q  qb 0   0   nmos W=0.20u L=0.045u

* access devices + bitlines
MA1 bl  wl q  0 nmos W=0.24u L=0.045u
MA2 blb wl qb 0 nmos W=0.24u L=0.045u

Cbl  bl  0 180f IC='VBL'
Cblb blb 0 180f IC='VBL'

.ic v(q)=0 v(qb)='VDD'
* .options temp=85

.control
    tran 5p 4n uic
    let v_diff = v(blb) - v(bl)
    meas tran dv FIND v_diff AT=2.0n
    meas tran qmax MAX v(q) FROM=1n TO=4n
    wrdata read_task2.csv v(bl) v(blb) v(q) v(qb)
    echo "dv = $&dv" >> task_2_results.txt
    echo "qmax = $&qmax" >> task_2_results.txt
    quit
.endc

* .control
*     let v_curr = 1.1
*     let v_stop = 0.1
*     let v_step = 0.05

*     echo "VDD, dv" > vdd_sweep.csv

*     while v_curr >= v_stop
*         * Change VDD, reset the circuit, and run the transient
*         alterparam VDD = $&v_curr
*         reset
*         tran 5p 4n uic

*         * Measure the voltage difference at 2ns
*         let v_diff = v(blb) - v(bl)
*         meas tran current_dv FIND v_diff AT=2.0n

*         * Save the result to our CSV
*         echo "$&v_curr, $&current_dv" >> vdd_sweep.csv

*         * Decrement VDD by 50mV
*         let v_curr = v_curr - v_step
*     end
*     quit
* .endc

.end