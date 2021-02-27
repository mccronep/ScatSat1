#! /bin/ksh
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATION:  @(#)$Id$
#
#::::::::::::::::::::::::::::::
# rscat_wind_process_ncdf.ksh
#::::::::::::::::::::::::::::::
#
#--------------------------------------------------------
# Written by Paul McCrone
# Processes RapidScat NETCDF data files from NASA JPL
#           and converts to ASCII as per the QuikScat
#           standard as required by FNMOC Modellers.
#           [see the python code for details]
#
#--------------------------------------------------------
#
#
#### RECORD OF CHANGES:
#------------------------------------------------------------------------------
#    Version 2.4.3A
#------------------------------------------------------------------------------
#
#    Dec.  18, 2015  Paul McCrone, x4403 Release Version V2.4.3A
#                    Additional Modifications to use more of the standard systeam variables.
#
#
#------------------------------------------------------------------------------
#
#################################################
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# Define environment variables
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#

typeset machine=$( uname -n )
typeset envir=$(echo $machine | cut -c 3-3 )

##--
#=============================================================
if [[ -d ${OPSPATH} && -n${OPSPATH} ]]                        
then                                                          
        echo OPSPATH_EXISTS_AND_IS_${OPSPATH}._               
else
        echo OPSPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSPATH=/satdat                       
        if [[ $envir == "b" || $envir == "B" ]]; then
           export OPSPATH=/u/curr                    
        fi
        if [[ $THISHOSTNAME == "a4ou" ]]; then
           export OPSPATH=/u/curr             
        fi
        echo OPSPATH_IS_NOW_${OPSPATH}_.
fi
#=============================================================
if [[ -d ${OPSBIN} && -n${OPSBIN} ]]                          
then
        echo OPSBIN_EXISTS_AND_IS_${OPSBIN}._
        if  [[ $envir == "d" || $envir == "a" ]]
        then
                export OPSBIN=/satdat/bin
                echo FOR_ALPHA_ONLY--OPSBIN_EXISTS_AND_IS_RESET_TO__${OPSBIN}_.
        fi
else
        echo OPSBIN_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSBIN=$OPSPATH/bin                  
        if  [[ $envir == "d" || $envir == "a" ]]    
        then
                export OPSBIN=/satdat/bin
        fi
        echo OPSBIN_IS_NOW_${OPSBIN}_.
fi
#=============================================================

#=============================================================
#=============================================================
if [[ -d ${XFER_BASEPATH} && -n ${XFER_BASEPATH} ]]           
then
        echo ${XFER_BASEPATH}_EXISTS_and_IS_DEFINED_AS_XFER_BASEPATH_.
else
        echo XFER_BASEPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export XFER_BASEPATH=/satdat/curr/rscat_wind       
        echo XFER_BASEPATH_IS_NOW_${XFER_BASEPATH}_.       
fi
#=============================================================
##--
#
export RSCAT_BASEPATH=$XFER_BASEPATH/../RapidScat
#
export NRT_BASEPATH=$RSCAT_BASEPATH/nrt
#






typeset EXECDIR=/satdat/bin/
###typeset ROOTDATADIR=/satdat/alpha/RapidScat/nrt/NETCDF/
typeset ROOTDATADIR=/satdat/curr/rscat_wind/
###ALTDIR=/satdat/curr/RapidScat/nrt
###ALTDIR=/satdat/curr/rscat_wind
###ALT2DIR=/satdat/curr/RapidScat/nrt
ALTDIR=${XFER_BASEPATH}
ALT2DIR=${NRT_BASEPATH}



#--------------------------------------------------------
if [[ $envir == "d" || $envir == "a" ]]; then
   typeset EXECDIR=/satdat/bin/
   typeset ROOTDATADIR=/satdat/alpha/RapidScat/nrt/NETCDF/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   #ALTDIR=/satdat/alpha/RapidScat/nrt
fi
#--------------------------------------------------------
if [[ $envir == "b" || $envir == "o" ]]; then
   typeset EXECDIR=/u/ops/bin/
   typeset ROOTDATADIR=/satdat/beta/RapidScat/nrt/NETCDF/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   #ALTDIR=/satdat/beta/RapidScat/nrt
fi
#--------------------------------------------------------
if [ $envir == "o" ]; then
   typeset EXECDIR=/u/ops/bin/
   typeset ROOTDATADIR=/satdat/ops/RapidScat/nrt/NETCDF/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   #ALTDIR=/satdat/ops/RapidScat/nrt
fi

#--------------------------------------------------------

JDAY=$(date +%j)

DDMMYY=$(date +%F)

HH=$(date +%H)

MM=$(date +%M)

LOGPATH=/satdat/curr/rscat_wind/

LOGFILE=${LOGPATH}rscat_wind.netcdf.rapidscat.log

DASHES=----------------------------------------------------

ZEROFILES=___NO_RAPIDSCAT_files_FROM_NASA-JPL_were__processed______

SOMEFILES=___RAPIDSCAT_files__FROM_NASA-JPL_were_processed__________

SCRIPTBEGINS=___The_Script_-rscat_wind_process_ncdf.ksh-__BEGINS_at_
SCRIPTENDS=___The_Script_-rscat_wind_process_ncdf.ksh-__ENDED_at_


echo ${DASHES} >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}
echo ${SCRIPTBEGINS} >> ${LOGFILE}
date           >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}

###
###--------------------------------
###
###--------------------------------
###

cd ${ROOTDATADIR}

LOGDIR=${ALT2DIR}/Nlog/

PROCDATADIR=${ALT2DIR}/Nprocessed/

cd ${EXECDIR}

python -W ignore ${EXECDIR}rscat_wind_convert_Rscat_nCDF_2_Qscat_ASCII.py  >> ${LOGFILE}

echo ${SOMEFILES} >> ${LOGFILE}

echo ${DASHES} >> ${LOGFILE}
echo ${SCRIPTENDS} >> ${LOGFILE}
date           >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}

##mv ${LOGPATH}rs_l2b_*.nc* ${ALT2DIR}/NETCDF
rm -rf ${LOGPATH}rs_l2b_*.nc*


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
################################################################################
#
# END SCRIPT
#
################################################################################
#
# rs_l2b_v1.1_04917_201508051112.nc.gz
#
