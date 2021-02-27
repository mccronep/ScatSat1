#! /bin/ksh
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATION:  @(#)$Id$
#
#::::::::::::::::::::::::::::::
# scatsat_knmi_process_ncdf.ksh
#::::::::::::::::::::::::::::::
#
#--------------------------------------------------------------
# Written by Paul McCrone
# Processes ScatSat-1 NETCDF data files from KNMI
#           [that is, the Royal Dutch Meteorological Institute]
#           and converts to ASCII as per the QuikScat
#           standard as required by FNMOC Modellers.
#           [see the python code for details]
#--------------------------------------------------------------
#
#### RECORD OF CHANGES:
#------------------------------------------------------------------------------
#    Version 3.0.0
#------------------------------------------------------------------------------
#    Nov.  25, 2015  Paul McCrone, x4403 Release Version V2.4.0
#                    Modified to use more of the standard system variables.
#------------------------------------------------------------------------------
#    Dec.  09, 2015  Paul McCrone, x4403 Release Version V2.4.3
#                    Additional Modifications to use more of the standard system variables.
#------------------------------------------------------------------------------
#    Sep.  15, 2017  Paul McCrone, x1503 Release Version V3.0.0
#                    Modify the older RapidScat Code to work for ScatSat-1
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
if [[ -d ${XFER_BASEPATH} && -n ${XFER_BASEPATH} ]]
then
        echo ${XFER_BASEPATH}_EXISTS_and_IS_DEFINED_AS_XFER_BASEPATH_.
else
        echo XFER_BASEPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export XFER_BASEPATH=/satdat/curr/scatsat_knmi
        #export XFER_BASEPATH=/satdat/curr/rscat_knmi
        echo XFER_BASEPATH_IS_NOW_${XFER_BASEPATH}_.
fi
#=============================================================
##--
#
export RSCAT_BASEPATH=$XFER_BASEPATH/../ScatSat1
#export RSCAT_BASEPATH=$XFER_BASEPATH/../RapidScat
#
export KNMI_BASEPATH=$RSCAT_BASEPATH/KNMI
#

###typeset EXECDIR=/satdat/bin/
typeset EXECDIR=${OPSBIN}/
###typeset ROOTDATADIR=/satdat/curr/rscat_knmi/
###typeset ROOTDATADIR=/satdat/curr/scatsat_knmi/
typeset ROOTDATADIR=${XFER_BASEPATH}/
##ALTDIR=/satdat/curr/rscat_knmi
ALTDIR=/satdat/curr/scatsat_knmi
ALTDIR=${XFER_BASEPATH}
##ALT2DIR=/satdat/curr/RapidScat/KNMI
ALT2DIR=/satdat/curr/ScatSat1/KNMI
ALT2DIR=${KNMI_BASEPATH}

#--------------------------------------------------------
#
if [[ $envir == "d" || $envir == "a" ]]; then
   ###typeset EXECDIR=/satdat/bin/
   typeset EXECDIR=${OPSBIN}/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   typeset PYTHONDIR=/satdat/python/sata/bin/
   #ALTDIR=/satdat/alpha/RapidScat/nrt
   #ALTDIR=/satdat/alpha/ScatSat1/nrt
fi
#
#--------------------------------------------------------
#
if [[ $envir == "b" || $envir == "o" ]]; then
   typeset EXECDIR=${OPSBIN}/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   typeset PYTHONDIR=/satdat/python/sata/bin/
   #ALTDIR=/satdat/beta/RapidScat/nrt
   #ALTDIR=/satdat/beta/ScatSat1/nrt
fi
#--------------------------------------------------------
#
if [ $envir == "o" ]; then
   typeset PYTHONDIR=/satdat/python/sata/bin/
   typeset EXECDIR=${OPSBIN}/
   typeset ROOTDATADIR=${XFER_BASEPATH}/
   #ALTDIR=/satdat/ops/RapidScat/nrt
   #ALTDIR=/satdat/ops/ScatSat1/nrt
fi
#
#--------------------------------------------------------

JDAY=$(date +%j)

DDMMYY=$(date +%F)

HH=$(date +%H)

MM=$(date +%M)

LOGPATH=${XFER_BASEPATH}/

LOGFILE=${LOGPATH}log.scatsat_knmi.netcdf.scatsat.log

DASHES=----------------------------------------------------
ZEROFILES=___NO_SCATSAT_files_from_KNMI_were__processed______
SOMEFILES=___SCATSAT_files_from_KNMI_were_processed__________
SCRIPTBEGINS=___The_Script_-scatsat_knmi_process_ncdf.ksh-__BEGINS_at_
SCRIPTENDS=___The_Script_-scatsat_knmi_process_ncdf.ksh-__ENDED_at_


echo ${DASHES} >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}
echo ${SCRIPTBEGINS} >> ${LOGFILE}
date           >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}

###
###
###
cd ${ROOTDATADIR}

LOGDIR=${ALT2DIR}/Nlog/

PROCDATADIR=${ALT2DIR}/Nprocessed/

cd ${EXECDIR}

###python -W ignore ${EXECDIR}rscat_wind_convert_Rscat_nCDF_2_Qscat_ASCII.py  >> ${LOGFILE}
###python -W ignore ${EXECDIR}rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py  >> ${LOGFILE}
${PYTHONDIR}python -W ignore ${EXECDIR}scatsat_knmi_convert_rscat_ncdf_2_qscat_ASCII3.py  >> ${LOGFILE}

echo ${SOMEFILES} >> ${LOGFILE}

echo ${DASHES} >> ${LOGFILE}
echo ${SCRIPTENDS} >> ${LOGFILE}
date           >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}

###mv ${LOGPATH}rapid_*.nc* ${ALT2DIR}/NETCDF
###rm -rf ${LOGPATH}rapid_*.nc*
rm -rf ${LOGPATH}oscat_*.nc*

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
################################################################################
#
# END SCRIPT
#
################################################################################

