#! /bin/ksh
#
#
#------------------------------------------
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATION:  @(#)$Id$
# Programmer, Paul McCrone, N38DI
#             x1503
#             Original: November  10, 2015
#             Re_used : September 15, 2017
#------------------------------------------
#
#------------------------------------------------------------------------------
####
####    --scatsat_knmi_direxist.ksh--
####
####    Functions for an PBS task that processes the ISRO SCATSAT-1 data for
####    coverting the ISRO SCATSAT-1 NETCDF files (from KNMI) to ASCII [FGGE] data
####
####    This script will check for the existence of key
####    subdirectories needed by rscat_knmi and will
####    re-create the subdirectories if they do not exist.
####
####
#------------------------------------------------------------------------------
#
# Version 2.4.3, 2015-Dec-09 - Altered PATH definitions to use more of the
#                              system variables. PJM
#------------------------------------------------------------------------------

#### RECORD OF CHANGES:
#------------------------------------------------------------------------------
#
#    Nov.  24, 2015  Paul McCrone, x1503 Release Version V2.4.0
#                    Modified to use more of the standard system variables.
#------------------------------------------------------------------------------
#
#    Dec.  09, 2015  Paul McCrone, x1503 Release Version V2.4.3
#                    Additional modifications to use more of the standard system variables.
#
#------------------------------------------------------------------------------
#
#    Sep.  15, 2017  Paul McCrone, x1503 Release Version V3.0.0
#                    Modified to run for ISRO SCATSAT-1 data from KNMI
#
#------------------------------------------------------------------------------
#
#################################################
#
#--------------------------
date
echo ..........The Script ---scatsat_knmi_direxist.ksh--- BEGINS:
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
#export RSCAT_BASEPATH=$XFER_BASEPATH/../RapidScat
export RSCAT_BASEPATH=$XFER_BASEPATH/../ScatSat1
#
export KNMI_BASEPATH=$RSCAT_BASEPATH/KNMI
#

#
GRAPHICPATH=$KNMI_BASEPATH/graphic/
#
ASCIIPATH=$KNMI_BASEPATH/ascii/
#
#
ASCIIPATHORIG=$KNMI_BASEPATH/ascii/
#
#ASCIIPATHTEMP=/satdat/curr/RapidScat/KNMI/ascii_temp/
ASCIIPATHTEMP=$KNMI_BASEPATH/ascii_temp/
#
## /u/beta/etc/dynamic/obs_data/met/cqc/scatsat
##ASCIIPATHAA=/u/beta/etc/dynamic/obs_data/met/cqc/rscat_a/
ASCIIPATHAA=$BETAPATH/etc/dynamic/obs_data/met/cqc/scatsat_a/
#
##ASCIIPATHBB=/u/beta/etc/dynamic/obs_data/met/cqc/rscat/
##ASCIIPATHBB=$BETAPATH/etc/dynamic/obs_data/met/cqc/rscat/
ASCIIPATHBB=$BETAPATH/etc/dynamic/obs_data/met/cqc/scatsat/
#
##ASCIIPATHOO=/u/ops/etc/dynamic/obs_data/met/cqc/rscat/
ASCIIPATHOO=$OPSPATH/etc/dynamic/obs_data/met/cqc/rscat/
ASCIIPATHOO=$OPSPATH/etc/dynamic/obs_data/met/cqc/scatsat/
#
#ASCIIPATHISIS=/satdat/curr/RapidScat/KNMI/ascii_2_isis/
#ASCIIPATHISIS=/satdat/curr/ScatSat1/KNMI/ascii_2_isis/
ASCIIPATHISIS=$KNMI_BASEPATH/ascii_2_isis/
#
##DATAPATH=/satdat/curr/rscat_knmi/
##DATAPATH=/satdat/curr/scatsat_knmi/
DATAPATH=$XFER_BASEPATH/
#
##BINPATH=/u/ops/bin/
BINPATH=$OPSBIN/
#
UTILPATH=$KNMI_BASEPATH/Nutil/
#
PROCPATH=$KNMI_BASEPATH/Nprocessed/
#

#=============================================================


if [ -d ${GRAPHICPATH} ]
then
        echo ${GRAPHICPATH}_EXISTS
else
        echo ${GRAPHICPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir graphic
fi

#=============================================================


if [ -d ${ASCIIPATH} ]
then
        echo ${ASCIIPATH}_EXISTS
else
        echo ${ASCIIPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        #cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir ascii
fi

#=============================================================

if [ -d ${ASCIIPATHTEMP} ]
then
        echo ${ASCIIPATHTEMP}_EXISTS
else
        echo ${ASCIIPATHTEMP}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        #cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
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
                #mkdir rscat_a
                mkdir scatsat_a
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
                #mkdir rscat
                mkdir scatsat
        fi
fi

#=============================================================

if [ -d ${ASCIIPATHOO} ]
then
        echo ${ASCIIPATHOO}_EXISTS
else
        echo ${ASCIIPATHOO}_NOT_AVAILABLE._PLEASE_RECREATE.
        cd /u/ops/etc/dynamic/obs_data/met/cqc/
        #mkdir rscat
        mkdir scatsat
fi

#=============================================================

if [ -d ${ASCIIPATHISIS} ]
then
        echo ${ASCIIPATHISIS}_EXISTS
else
        echo ${ASCIIPATHISIS}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        ##cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
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
        ##mkdir rscat_knmi
        mkdir scatsat_knmi
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
        ##cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir Nutil
fi

#=============================================================

if [ -d ${PROCPATH} ]
then
        echo ${PROCPATH}_EXISTS
else
        echo ${PROCPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        ##cd /satdat/curr/ScatSat1/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir Nprocessed
fi

#=============================================================

echo --
echo --
echo --

#--------------------------
echo ---------------------------------------------------------------------
echo ..........The Script -rscat_knmi_direxist.ksh- ENDS:
date
echo ---------------------------------------------------------------------
#--------------------------

#
################################################
######   END
################################################

