#! /bin/ksh
#
#
#----------------------------------
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATIO
# Programmer, Paul McCrone, N38DI
#             x4403
#             December 18, 2015
#----------------------------------
#
#------------------------------------------------------------------------------
####    --rscat_wind_direxist.ksh--
####
####    Functions for an PBS task that processes the NASA RAPIDSCAT data for
####    coverting the NASA RAPIDSCAT NETCDF files (from NASA JPL) to ASCII [FGGE] data
####
####    This script will check for the existence of key
####    subdirectories needed by rscat_knmi and will
####    re-create the subdirectories if they do not exist.
####
####
#
#------------------------------------------------------------------------------
#
# Version 2.4.3A, 2015-Dec-18 - Altered PATH definitions to use more of the
#                               system variables. PJM
#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
#
# Version 2.4.3B, 2016-Jan-11 - Altered PATH definitions to use more of the
#                               system variables. PJM
#------------------------------------------------------------------------------
#
#
#### RECORD OF CHANGES:
#
#------------------------------------------------------------------------------
#
#    Dec.  18, 2015  Paul McCrone, x4403 Release Version V2.4.3A
#                    Modified to use more of the standard system variables.
#------------------------------------------------------------------------------
#    Jan.  11, 2016  Paul McCrone, x4403 Release Version V2.4.3B
#                    Modified to use more of the standard system variables.
#
#
#------------------------------------------------------------------------------
#
#################################################
#
#--------------------------
date
echo ---------------------------------------------------------------------
echo ..........The Script -rscat_wind_direxist.ksh- BEGINS:
echo ---------------------------------------------------------------------

#--------------------------
#--------------------------
#--------------------------
#
# Define environment variables
#
#

typeset ENDINGF=_alpha_

typeset machine=$( uname -n )
typeset envir=$(echo $machine | cut -c 3-3 )
typeset THISHOSTNAME=$(echo $machine | cut -c 1-4)

#
if [[ $envir == "d" || $envir == "a" ]]; then
   typeset ENDINGF=_alpha_
fi
#
if [[ $envir == "b" || $envir == "B" ]]; then
   typeset ENDINGF=_beta_
fi
#
if [[ $THISHOSTNAME == "a4ou" ]]; then
   typeset ENDINGF=_OPS_
fi
#
#
#--------------------------
#--------------------------
#--------------------------

echo --
echo --
echo --

echo Running_on_HOSTNAME_${THISHOSTNAME}
echo Current_Running_Environment_is_${ENDINGF}


echo --
echo --
echo --

###--export OPSPATH=/satdat
###--export OPSBIN=$OPSPATH/bin
###--export OPSFCN=$OPSPATH/job/bin
###--export XFER_BASEPATH=/satdat/alpha/rscat_knmi

export BETAPATH=/u/beta

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
if [[ -d ${OPSFCN} && -n${OPSFCN} ]]
then
        echo OPSFCN_EXISTS_AND_IS_${OPSFCN}._
else
        echo OPSFCN_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSFCN=$OPSPATH/job/bin
        echo OPSFCN_IS_NOW_${OPSFCN}_.
fi
#=============================================================
if [[ -d ${XFER_BASEPATH} && -n ${XFER_BASEPATH} ]]
then
        echo ${XFER_BASEPATH}_EXISTS
else
        echo XFER_BASEPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export XFER_BASEPATH=/satdat/curr/rscat_knmi
        echo XFER_BASEPATH_IS_NOW_${XFER_BASEPATH}_.
fi
#=============================================================

#
export RSCAT_BASEPATH=$XFER_BASEPATH/../RapidScat
#
export NRT_BASEPATH=$RSCAT_BASEPATH/nrt
#export KNMI_BASEPATH=$RSCAT_BASEPATH/nrt
#

#
GRAPHICPATH=$NRT_BASEPATH/graphic/
#
ASCIIPATH=$NRT_BASEPATH/ascii/
#
#
ASCIIPATHORIG=$NRT_BASEPATH/ascii/
#
#ASCIIPATHTEMP=/satdat/curr/RapidScat/KNMI/ascii_temp/
ASCIIPATHTEMP=$NRT_BASEPATH/ascii_temp/
#
##ASCIIPATHAA=/u/beta/etc/dynamic/obs_data/met/cqc/rscat_a/
ASCIIPATHAA=$BETAPATH/etc/dynamic/obs_data/met/cqc/rscat_a/
#
##ASCIIPATHBB=/u/beta/etc/dynamic/obs_data/met/cqc/rscat/
ASCIIPATHBB=$BETAPATH/etc/dynamic/obs_data/met/cqc/rscat/
#
##ASCIIPATHOO=/u/ops/etc/dynamic/obs_data/met/cqc/rscat/
ASCIIPATHOO=$OPSPATH/etc/dynamic/obs_data/met/cqc/rscat/
#
#ASCIIPATHISIS=/satdat/curr/RapidScat/KNMI/ascii_2_isis/
ASCIIPATHISIS=$NRT_BASEPATH/ascii_2_isis/
#
##DATAPATH=/satdat/curr/rscat_knmi/
DATAPATH=$XFER_BASEPATH/
#
##BINPATH=/u/ops/bin/
BINPATH=$OPSBIN/
#
UTILPATH=$NRT_BASEPATH/Nutil/
#
PROCPATH=$NRT_BASEPATH/Nprocessed/
#

#=============================================================


if [ -d ${GRAPHICPATH} ]
then
        echo ${GRAPHICPATH}_EXISTS
else
        echo ${GRAPHICPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        cd ${NRT_BASEPATH}/
        mkdir graphic
fi

#=============================================================


if [ -d ${ASCIIPATH} ]
then
        echo ${ASCIIPATH}_EXISTS
else
        echo ${ASCIIPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        cd ${NRT_BASEPATH}/
        mkdir ascii
fi

#=============================================================

if [ -d ${ASCIIPATHTEMP} ]
then
        echo ${ASCIIPATHTEMP}_EXISTS
else
        echo ${ASCIIPATHTEMP}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        cd ${NRT_BASEPATH}/
        mkdir ascii_temp
fi

#=============================================================

if [[ $envir == "d" || $envir == "a" ]]; then

        if [ -d ${ASCIIPATHAA} ]
        then
                echo ${ASCIIPATHAA}_EXISTS
        else
                echo ${ASCIIPATHAA}_NOT_AVAILABLE._PLEASE_RECREATE.
                ##cd /u/beta/etc/dynamic/obs_data/met/cqc/
                cd $BETAPATH/etc/dynamic/obs_data/met/cqc/
                mkdir rscat_a
        fi
fi

#=============================================================

if [[ $envir == "b" || $envir == "B" ]]; then

        if [ -d ${ASCIIPATHBB} ]
        then
                echo ${ASCIIPATHBB}_EXISTS
        else
                echo ${ASCIIPATHBB}_NOT_AVAILABLE._PLEASE_RECREATE.
                ##cd /u/beta/etc/dynamic/obs_data/met/cqc/
                cd $BETAPATH/etc/dynamic/obs_data/met/cqc/
                mkdir rscat
        fi
fi

#=============================================================

if [ -d ${ASCIIPATHOO} ]
then
        echo ${ASCIIPATHOO}_EXISTS
else
        echo ${ASCIIPATHOO}_NOT_AVAILABLE._PLEASE_RECREATE.
        cd /u/ops/etc/dynamic/obs_data/met/cqc/
        mkdir rscat
fi

#=============================================================

if [ -d ${ASCIIPATHISIS} ]
then
        echo ${ASCIIPATHISIS}_EXISTS
else
        echo ${ASCIIPATHISIS}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        cd ${N_BASEPATH}/
        mkdir ascii_2_isis
fi

#=============================================================

if [ -d ${DATAPATH} ]
then
        echo ${DATAPATH}_EXISTS
else
        echo ${DATAPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/
        cd $XFER_BASEPATH/..
        mkdir rscat_knmi
fi

#=============================================================
###
###if [ -d ${BINPATH} ]
###then
###        echo ${BINPATH}_EXISTS
###else
###        echo ${BINPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
###        cd /satdat/curr/RapidScat/KNMI/
###        mkdir ascii_temp
###fi
###
#=============================================================

if [ -d ${UTILPATH} ]
then
        echo ${UTILPATH}_EXISTS
else
        echo ${UTILPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        cd ${NRT_BASEPATH}/
        mkdir Nutil
fi

#=============================================================

if [ -d ${PROCPATH} ]
then
        echo ${PROCPATH}_EXISTS
else
        echo ${PROCPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        cd ${NRT_BASEPATH}/
        mkdir Nprocessed
fi

#=============================================================

echo --
echo --
echo --

#--------------------------
echo ---------------------------------------------------------------------
echo ..........The Script -rscat_wind_direxist.ksh- ENDS:
date
echo ---------------------------------------------------------------------
#--------------------------

#
################################################
######   END
################################################

