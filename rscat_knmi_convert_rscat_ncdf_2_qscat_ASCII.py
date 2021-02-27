#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#==============================================================
# 
#==============================================================
#
#
#==-FNMOC/N38DI PYTHON PROGRAM DEFINITION-==========================================
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py
# :::::::::::::::::::::::::::::::::::::::::::::::
#
#  PROGRAM OVERVIEW:
#  	(1) This program reads in the RAPIDSCAT data from Royal Netherlands Meteorological Institute (KNMI).
#	(2) The input file is in netCDF4 format. 
#	(3) The output file is an ASCII file in column format.
#	(4) There are several functions, -Print_Current_Time(now)- and -Get_Converted_Time90(spacecrafttime)-
#		-a- -Print_Current_Time- simply prints the current time.
#		-b- --Get_Converted_Time90- reads in the time from the netCDF4 file in megaseconds
#		    (such as 500000000 seconds) since January 1st, 1990, at 0000UTC, then 
#		    converts the numerical value into a calendar readable year-month-date-time.
#
#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
#
# I/O		NAME         	TYPE		FUNCTION
#--------------------------------------------------------------------------------------------------
#  I          	netCDF4 file 	input 		INPUT RAPIDSCAT DATA FROM NASA JPL. 
#  O            ASCII file      output          Converted FGGE RAPIDSCAT DATA for use by modelers.
#                                               Internally at FNMOC, see:	
#                                               http://a4au-a002/fgge_format/scatq_2.html
#_________________________________________________________________________________________________
#=================================================================================================
#
#=================================================================================================
#-
#
# Programmer: Mr. Paul McCrone     02 February 2015
#
# Modification  : BELOW
#========================================================================================
#  Version 2.3  , Dated 2015-Nov-19
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  Version 2.4  , Dated 2015-Nov-26
#                                 Modified to use more of the standard system variables.
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Version 2.4.9, Dated 2016-April-29
#                                 Modified to send netCDF file on to rscat_satfocus.
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  Version 2.5.0,  Dated 2016-Jul-20
#                                 Adding a capability to save the same data set to
#                                 ascii_bb [beta] that will store using a more
#                                 descriptive filename that currently used by the NWP group.
#
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 2.6.6 for RHEL.
#---------------------------------------------------------------
#  PYTHON MODULES USED: numpy, scipy, matplotlib, netCDF4, datetime 	
#---------------------------------------------------------------
#
#  This code reads and converts data for the ISS-RapidScat Level 2B 12.5km 
#  science-quality netCDF dataset. 
#
#  Dataset description [quoted from NASA JPL]:
#  "This dataset contains the ISS-RapidScat Level 2B 12.5km science-quality ocean 
#  surface wind vectors. The Level 2B wind vectors are binned on a 12.5 km Wind 
#  Vector Cell (WVC) grid and processed using the Level 2A Sigma-0 dataset. Unlike 
#  QuikSCAT, the International Space Station (ISS) is not in sun-synchronous orbit 
#  and flies at roughly half the altitude with a low inclination angle that restricts 
#  data coverage to the tropics and mid-latitude regions; the extent of latitudinal 
#  coverage stretches from approximately 60 degrees North to 60 degrees South. 
#  Furthermore, there is no consistent local time of day retrieval. This dataset is 
#  provided in netCDF-4 "classic" format and made avaialble via FTP and OPeNDAP."
#
#----------------------------------------------------------------------------------------
#  Please note the following caveat(s) with this current release [quoted from NASA JPL]: 
#
#  "[Quote]
#  1) This dataset has gone through an expedited public release, and although this dataset 
#     has completed cal/val through the RapidScat science team, the PO.DAAC is not prepared 
#     to provide full user support until the completion of a user guide, which will provide 
#     details on any known issues and caveats with the dataset. The user guide is expected 
#     to be released by January 2015."
#
#  2) The data fields containing the number of measurements of each type for each wind vector 
#     cell are currently zero filled. These fields include number_in_aft, number_in_fore, 
#     number_out_aft, and number_out_fore. In the next release the correct number of 
#     measurements will be included, but for now these fields are zeroed out. Until the next 
#     data release, please ignore these data fields.
#
#  3) The wind_obj data field that is supposed to contain the likelihood value of the DIRTH 
#     wind vector is also not properly set. For now this field is filled with -Inf values. 
#     This will be corrected in a future release. Until that time, users interested in the 
#     likelihood values for the solution are encouraged to use the values for the 4 peaks 
#     of the likelihood function contained in the ambiguity_obj data field.
#     "[End Quote]
#
#========================================================================================
#
# Data file contents: RapidScat L2B data files 
#
# NASA JPL File naming convention:
# rs_l2b_v1_RRRRR_YYYYMMDDHHmm.nc.gz
# 
# rs_l2b	Instrument/Level Identifier: RapidScat Level 2B
# RRRRR	5-digit orbital revolution number
# v1	Version ID: v1 = version 1
# YYYY	4-digit year of data file creation date
# MM	2-digit month of data file creation date
# DD	2-digit day of month of data file creation date
# HH	2-digit hour of 24-hour day of data file creation time
# mm	2-digit minute of hour of data file creation time
# nc	File extension: nc = netCDF
# gz	GNU Zip file extension
# 
# Please send any comments or questions to podaac@podaac.jpl.nasa.gov.
#
#========================================================================================
#
#
#========================================================================================
#
# Data file contents: RapidScat L2 NETCDF data files
#
#  KNMI File naming convention:
#
#  rapid_YYYYMMDD_HHmmSS_iss____RRRRR_2hr_o_EEE_1903_ovw_l2.nc
#  
#  WHERE:
#  ======
#  rapid_       Instrument/Level Identifier: RapidScat Level 2
#  YYYY         4-digit year of data file creation date
#  MM           2-digit month of data file creation date
#  DD           2-digit day of month of data file creation date
#  HH           2-digit hour of 24-hour day of data file creation time
#  mm           2-digit minute of hour of data file creation time
#  SS           2-digit Seconds of minute of  hour of data file creation time
#  iss          The International Space Station (ISS)
#  RRRRR        5-digit orbital revolution number
#  EEE          Spatial Resolution (250-25km and 500 - 50 km)
#  ovw          Ocean Vector Winds
#  l2           Level 2
#  nc           File extension: nc = netCDF
#  gz           GNU Zip file extension
#
#  EXAMPLE:
#  rapid_20160721_121748_iss____10375_2hr_o_500_1903_ovw_l2.nc
#
#
#========================================================================================
#
#
#
import numpy as N
import scipy as S
import matplotlib as M
import netCDF4 as NCF
import datetime
import os as OS
import sys as SYS
import math as MATH
import warnings as WARNINGS
import socket
import commands
#
#
#
#
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#  LIST OF PYTHON FUNCTIONS:
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#
#  ==> fxn()
#	--> Eliminate python warnings.
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Determine_mndate_from_leapjday(jday)
#	--> Determine the month and date from Julian day (on leap years)
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Determine_mndate_from_jday(jday)
#	--> Determine the month and date from Julian day (on non-leap years)
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Determine_Wind_SPEED(data_from_netcdf)
#	--> data_from_netcdf:Float, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Determine_Wind_Direction(data_from_file)
#	--> data_from_file:Float, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Compute_MLE_STRNG(datafromfile, MAX_data_Value)
#	--> datafromfile:Float, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Print_Current_Time(now)
#	--> now:String, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Access_Current_Time(now)
#       --> now:String, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Get_Converted_Time90(spacecrafttime):
#	--> spacecrafttime:Integer or Float, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> main()
#       --> This is the -MAIN- program  
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#
#
#
dadots=".  .  .  .  .  .  .  .  .  .  .  .  ."
dadash="-------------------------------------"
#
NOT_A_NUMBER=float('nan')
#  MATH.isnan(NOT_A_NUMBER)
#
#import warnings
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function fxn
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def fxn():
    WARNINGS.warn("nan", DeprecationWarning)
    #WARNINGS.warn("deprecated", DeprecationWarning)
    #WARNINGS.warn("Warning: converting a masked element to nan.", DeprecationWarning)
#######  END OF Function fxn


with WARNINGS.catch_warnings():
    WARNINGS.simplefilter("ignore")
    fxn()

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Determine_mndate_from_leapjday
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Determine_mndate_from_leapjday(jday):
    #
    #-----#-----#-----#-----#-----
    #
    #

    month_n_date="0000"

    if jday < 1:
        print("ERROR==>Input Jday cannot be less than 0.")
        return month_n_date
        #
        #----------------------------------------------------
        # End of if block
        #----------------------------------------------------

    if jday > 366:
        print("ERROR==>Input Jday cannot exceed 366.")
        return month_n_date
        #
        #----------------------------------------------------
        # End of if block
        #----------------------------------------------------


    if jday == 1:
        month_n_date="0101"
    elif jday == 2:
        month_n_date="0102"
    elif jday == 3:
        month_n_date="0103"
    elif jday == 4:
        month_n_date="0104"
    elif jday == 5:
        month_n_date="0105"
    elif jday == 6:
        month_n_date="0106"
    elif jday == 7:
        month_n_date="0107"
    elif jday == 8:
        month_n_date="0108"
    elif jday == 9:
        month_n_date="0109"
    elif jday == 10:
        month_n_date="0110"
    elif jday == 11:
        month_n_date="0111"
    elif jday == 12:
        month_n_date="0112"
    elif jday == 13:
        month_n_date="0113"
    elif jday == 14:
        month_n_date="0114"
    elif jday == 15:
        month_n_date="0115"
    elif jday == 16:
        month_n_date="0116"
    elif jday == 17:
        month_n_date="0117"
    elif jday == 18:
        month_n_date="0118"
    elif jday == 19:
        month_n_date="0119"
    elif jday == 20:
        month_n_date="0120"
    elif jday == 21:
        month_n_date="0121"
    elif jday == 22:
        month_n_date="0122"
    elif jday == 23:
        month_n_date="0123"
    elif jday == 24:
        month_n_date="0124"
    elif jday == 25:
        month_n_date="0125"
    elif jday == 26:
        month_n_date="0126"
    elif jday == 27:
        month_n_date="0127"
    elif jday == 28:
        month_n_date="0128"
    elif jday == 29:
        month_n_date="0129"
    elif jday == 30:
        month_n_date="0130"
    elif jday == 31:
        month_n_date="0131"
        #--------------------------
    elif jday == 32:
        month_n_date="0201"
    elif jday == 33:
        month_n_date="0202"
    elif jday == 34:
        month_n_date="0203"
    elif jday == 35:
        month_n_date="0204"
    elif jday == 36:
        month_n_date="0205"
    elif jday == 37:
        month_n_date="0206"
    elif jday == 38:
        month_n_date="0207"
    elif jday == 39:
        month_n_date="0208"
    elif jday == 40:
        month_n_date="0209"
    elif jday == 41:
        month_n_date="0210"
    elif jday == 42:
        month_n_date="0211"
    elif jday == 43:
        month_n_date="0212"
    elif jday == 44:
        month_n_date="0213"
    elif jday == 45:
        month_n_date="0214"
    elif jday == 46:
        month_n_date="0215"
    elif jday == 47:
        month_n_date="0216"
    elif jday == 48:
        month_n_date="0217"
    elif jday == 49:
        month_n_date="0218"
    elif jday == 50:
        month_n_date="0219"
    elif jday == 51:
        month_n_date="0220"
    elif jday == 52:
        month_n_date="0221"
    elif jday == 53:
        month_n_date="0222"
    elif jday == 54:
        month_n_date="0223"
    elif jday == 55:
        month_n_date="0224"
    elif jday == 56:
        month_n_date="0225"
    elif jday == 57:
        month_n_date="0226"
    elif jday == 58:
        month_n_date="0227"
    elif jday == 59:
        month_n_date="0228"
    elif jday == 60:
        month_n_date="0229"
        #--------------------------
    elif jday == 61:
        month_n_date="0301"
    elif jday == 62:
        month_n_date="0302"
    elif jday == 63:
        month_n_date="0303"
    elif jday == 64:
        month_n_date="0304"
    elif jday == 65:
        month_n_date="0305"
    elif jday == 66:
        month_n_date="0306"
    elif jday == 67:
        month_n_date="0307"
    elif jday == 68:
        month_n_date="0308"
    elif jday == 69:
        month_n_date="0309"
    elif jday == 70:
        month_n_date="0310"
    elif jday == 71:
        month_n_date="0311"
    elif jday == 72:
        month_n_date="0312"
    elif jday == 73:
        month_n_date="0313"
    elif jday == 74:
        month_n_date="0314"
    elif jday == 75:
        month_n_date="0315"
    elif jday == 76:
        month_n_date="0316"
    elif jday == 77:
        month_n_date="0317"
    elif jday == 78:
        month_n_date="0318"
    elif jday == 79:
        month_n_date="0319"
    elif jday == 80:
        month_n_date="0320"
    elif jday == 81:
        month_n_date="0321"
    elif jday == 82:
        month_n_date="0322"
    elif jday == 83:
        month_n_date="0323"
    elif jday == 84:
        month_n_date="0324"
    elif jday == 85:
        month_n_date="0325"
    elif jday == 86:
        month_n_date="0326"
    elif jday == 87:
        month_n_date="0327"
    elif jday == 88:
        month_n_date="0328"
    elif jday == 89:
        month_n_date="0329"
    elif jday == 90:
        month_n_date="0330"
    elif jday == 91:
        month_n_date="0331"
        #--------------------------
        #--------------------------
    elif jday == 92:
        month_n_date="0401"
    elif jday == 93:
        month_n_date="0402"
    elif jday == 94:
        month_n_date="0403"
    elif jday == 95:
        month_n_date="0404"
    elif jday == 96:
        month_n_date="0405"
    elif jday == 97:
        month_n_date="0406"
    elif jday == 98:
        month_n_date="0407"
    elif jday == 99:
        month_n_date="0408"
    elif jday == 100:
        month_n_date="0409"
    elif jday == 101:
        month_n_date="0410"
    elif jday == 102:
        month_n_date="0411"
    elif jday == 103:
        month_n_date="0412"
    elif jday == 104:
        month_n_date="0413"
    elif jday == 105:
        month_n_date="0414"
    elif jday == 106:
        month_n_date="0415"
    elif jday == 107:
        month_n_date="0416"
    elif jday == 108:
        month_n_date="0417"
    elif jday == 109:
        month_n_date="0418"
    elif jday == 110:
        month_n_date="0419"
    elif jday == 111:
        month_n_date="0420"
    elif jday == 112:
        month_n_date="0421"
    elif jday == 113:
        month_n_date="0422"
    elif jday == 114:
        month_n_date="0423"
    elif jday == 115:
        month_n_date="0424"
    elif jday == 116:
        month_n_date="0425"
    elif jday == 117:
        month_n_date="0426"
    elif jday == 118:
        month_n_date="0427"
    elif jday == 119:
        month_n_date="0428"
    elif jday == 120:
        month_n_date="0429"
    elif jday == 121:
        month_n_date="0430"
    #--------------------------
    elif jday == 122:
        month_n_date="0501"
    elif jday == 123:
        month_n_date="0502"
    elif jday == 124:
        month_n_date="0503"
    elif jday == 125:
        month_n_date="0504"
    elif jday == 126:
        month_n_date="0505"
    elif jday == 127:
        month_n_date="0506"
    elif jday == 128:
        month_n_date="0507"
    elif jday == 129:
        month_n_date="0508"
    elif jday == 130:
        month_n_date="0509"
    elif jday == 131:
        month_n_date="0510"
    elif jday == 132:
        month_n_date="0511"
    elif jday == 133:
        month_n_date="0512"
    elif jday == 134:
        month_n_date="0513"
    elif jday == 135:
        month_n_date="0514"
    elif jday == 136:
        month_n_date="0515"
    elif jday == 137:
        month_n_date="0516"
    elif jday == 138:
        month_n_date="0517"
    elif jday == 139:
        month_n_date="0518"
    elif jday == 140:
        month_n_date="0519"
    elif jday == 141:
        month_n_date="0520"
    elif jday == 142:
        month_n_date="0521"
    elif jday == 143:
        month_n_date="0522"
    elif jday == 144:
        month_n_date="0523"
    elif jday == 145:
        month_n_date="0524"
    elif jday == 146:
        month_n_date="0525"
    elif jday == 147:
        month_n_date="0526"
    elif jday == 148:
        month_n_date="0527"
    elif jday == 149:
        month_n_date="0528"
    elif jday == 150:
        month_n_date="0529"
    elif jday == 151:
        month_n_date="0530"
    elif jday == 152:
        month_n_date="0531"
        #--------------------------
    elif jday == 153:
        month_n_date="0601"
    elif jday == 154:
        month_n_date="0602"
    elif jday == 155:
        month_n_date="0603"
    elif jday == 156:
        month_n_date="0604"
    elif jday == 157:
        month_n_date="0605"
    elif jday == 158:
        month_n_date="0606"
    elif jday == 159:
        month_n_date="0607"
    elif jday == 160:
        month_n_date="0608"
    elif jday == 161:
        month_n_date="0609"
    elif jday == 162:
        month_n_date="0610"
    elif jday == 163:
        month_n_date="0611"
    elif jday == 164:
        month_n_date="0612"
    elif jday == 165:
        month_n_date="0613"
    elif jday == 166:
        month_n_date="0614"
    elif jday == 167:
        month_n_date="0615"
    elif jday == 168:
        month_n_date="0616"
    elif jday == 169:
        month_n_date="0617"
    elif jday == 170:
        month_n_date="0618"
    elif jday == 171:
        month_n_date="0619"
    elif jday == 172:
        month_n_date="0620"
    elif jday == 173:
        month_n_date="0621"
    elif jday == 174:
        month_n_date="0622"
    elif jday == 175:
        month_n_date="0623"
    elif jday == 176:
        month_n_date="0624"
    elif jday == 177:
        month_n_date="0625"
    elif jday == 178:
        month_n_date="0626"
    elif jday == 179:
        month_n_date="0627"
    elif jday == 180:
        month_n_date="0628"
    elif jday == 181:
        month_n_date="0629"
    elif jday == 182:
        month_n_date="0630"
        #--------------------------
    elif jday == 183:
        month_n_date="0701"
    elif jday == 184:
        month_n_date="0702"
    elif jday == 185:
        month_n_date="0703"
    elif jday == 186:
        month_n_date="0704"
    elif jday == 187:
        month_n_date="0705"
    elif jday == 188:
        month_n_date="0706"
    elif jday == 189:
        month_n_date="0707"
    elif jday == 190:
        month_n_date="0708"
    elif jday == 191:
        month_n_date="0709"
    elif jday == 192:
        month_n_date="0710"
    elif jday == 193:
        month_n_date="0711"
    elif jday == 194:
        month_n_date="0712"
    elif jday == 195:
        month_n_date="0713"
    elif jday == 196:
        month_n_date="0714"
    elif jday == 197:
        month_n_date="0715"
    elif jday == 198:
        month_n_date="0716"
    elif jday == 199:
        month_n_date="0717"
    elif jday == 200:
        month_n_date="0718"
    elif jday == 201:
        month_n_date="0719"
    elif jday == 202:
        month_n_date="0720"
    elif jday == 203:
        month_n_date="0721"
    elif jday == 204:
        month_n_date="0722"
    elif jday == 205:
        month_n_date="0723"
    elif jday == 206:
        month_n_date="0724"
    elif jday == 207:
        month_n_date="0725"
    elif jday == 208:
        month_n_date="0726"
    elif jday == 209:
        month_n_date="0727"
    elif jday == 210:
        month_n_date="0728"
    elif jday == 211:
        month_n_date="0729"
    elif jday == 212:
        month_n_date="0730"
    elif jday == 213:
        month_n_date="0731"
        #--------------------------
    elif jday == 214:
        month_n_date="0801"
    elif jday == 215:
        month_n_date="0802"
    elif jday == 216:
        month_n_date="0803"
    elif jday == 217:
        month_n_date="0804"
    elif jday == 218:
        month_n_date="0805"
    elif jday == 219:
        month_n_date="0806"
    elif jday == 220:
        month_n_date="0807"
    elif jday == 221:
        month_n_date="0808"
    elif jday == 222:
        month_n_date="0809"
    elif jday == 223:
        month_n_date="0810"
    elif jday == 224:
        month_n_date="0811"
    elif jday == 225:
        month_n_date="0812"
    elif jday == 226:
        month_n_date="0813"
    elif jday == 227:
        month_n_date="0814"
    elif jday == 228:
        month_n_date="0815"
    elif jday == 229:
        month_n_date="0816"
    elif jday == 230:
        month_n_date="0817"
    elif jday == 231:
        month_n_date="0818"
    elif jday == 232:
        month_n_date="0819"
    elif jday == 233:
        month_n_date="0820"
    elif jday == 234:
        month_n_date="0821"
    elif jday == 235:
        month_n_date="0822"
    elif jday == 236:
        month_n_date="0823"
    elif jday == 237:
        month_n_date="0824"
    elif jday == 238:
        month_n_date="0825"
    elif jday == 239:
        month_n_date="0826"
    elif jday == 240:
        month_n_date="0827"
    elif jday == 241:
        month_n_date="0828"
    elif jday == 242:
        month_n_date="0829"
    elif jday == 243:
        month_n_date="0830"
    elif jday == 244:
        month_n_date="0831"
        #--------------------------
    elif jday == 245:
        month_n_date="0901"
    elif jday == 246:
        month_n_date="0902"
    elif jday == 247:
        month_n_date="0903"
    elif jday == 248:
        month_n_date="0904"
    elif jday == 249:
        month_n_date="0905"
    elif jday == 250:
        month_n_date="0906"
    elif jday == 251:
        month_n_date="0907"
    elif jday == 252:
        month_n_date="0908"
    elif jday == 253:
        month_n_date="0909"
    elif jday == 254:
        month_n_date="0910"
    elif jday == 255:
        month_n_date="0911"
    elif jday == 256:
        month_n_date="0912"
    elif jday == 257:
        month_n_date="0913"
    elif jday == 258:
        month_n_date="0914"
    elif jday == 259:
        month_n_date="0915"
    elif jday == 260:
        month_n_date="0916"
    elif jday == 261:
        month_n_date="0917"
    elif jday == 262:
        month_n_date="0918"
    elif jday == 263:
        month_n_date="0919"
    elif jday == 264:
        month_n_date="0920"
    elif jday == 265:
        month_n_date="0921"
    elif jday == 266:
        month_n_date="0922"
    elif jday == 267:
        month_n_date="0923"
    elif jday == 268:
        month_n_date="0924"
    elif jday == 269:
        month_n_date="0925"
    elif jday == 270:
        month_n_date="0926"
    elif jday == 271:
        month_n_date="0927"
    elif jday == 272:
        month_n_date="0928"
    elif jday == 273:
        month_n_date="0929"
    elif jday == 274:
        month_n_date="0930"
        #--------------------------
    elif jday == 275:
        month_n_date="1001"
    elif jday == 276:
        month_n_date="1002"
    elif jday == 277:
        month_n_date="1003"
    elif jday == 278:
        month_n_date="1004"
    elif jday == 279:
        month_n_date="1005"
    elif jday == 280:
        month_n_date="1006"
    elif jday == 281:
        month_n_date="1007"
    elif jday == 282:
        month_n_date="1008"
    elif jday == 283:
        month_n_date="1009"
    elif jday == 284:
        month_n_date="1010"
    elif jday == 285:
        month_n_date="1011"
    elif jday == 286:
        month_n_date="1012"
    elif jday == 287:
        month_n_date="1013"
    elif jday == 288:
        month_n_date="1014"
    elif jday == 289:
        month_n_date="1015"
    elif jday == 290:
        month_n_date="1016"
    elif jday == 291:
        month_n_date="1017"
    elif jday == 292:
        month_n_date="1018"
    elif jday == 293:
        month_n_date="1019"
    elif jday == 294:
        month_n_date="1020"
    elif jday == 295:
        month_n_date="1021"
    elif jday == 296:
        month_n_date="1022"
    elif jday == 297:
        month_n_date="1023"
    elif jday == 298:
        month_n_date="1024"
    elif jday == 299:
        month_n_date="1025"
    elif jday == 300:
        month_n_date="1026"
    elif jday == 301:
        month_n_date="1027"
    elif jday == 302:
        month_n_date="1028"
    elif jday == 303:
        month_n_date="1029"
    elif jday == 304:
        month_n_date="1030"
    elif jday == 305:
        month_n_date="1031"
        #--------------------------
    elif jday == 306:
        month_n_date="1101"
    elif jday == 307:
        month_n_date="1102"
    elif jday == 308:
        month_n_date="1103"
    elif jday == 309:
        month_n_date="1104"
    elif jday == 310:
        month_n_date="1105"
    elif jday == 311:
        month_n_date="1106"
    elif jday == 312:
        month_n_date="1107"
    elif jday == 313:
        month_n_date="1108"
    elif jday == 314:
        month_n_date="1109"
    elif jday == 315:
        month_n_date="1110"
    elif jday == 316:
        month_n_date="1111"
    elif jday == 317:
        month_n_date="1112"
    elif jday == 318:
        month_n_date="1113"
    elif jday == 319:
        month_n_date="1114"
    elif jday == 320:
        month_n_date="1115"
    elif jday == 321:
        month_n_date="1116"
    elif jday == 322:
        month_n_date="1117"
    elif jday == 323:
        month_n_date="1118"
    elif jday == 324:
        month_n_date="1119"
    elif jday == 325:
        month_n_date="1120"
    elif jday == 326:
        month_n_date="1121"
    elif jday == 327:
        month_n_date="1122"
    elif jday == 328:
        month_n_date="1123"
    elif jday == 329:
        month_n_date="1124"
    elif jday == 330:
        month_n_date="1125"
    elif jday == 331:
        month_n_date="1126"
    elif jday == 332:
        month_n_date="1127"
    elif jday == 333:
        month_n_date="1128"
    elif jday == 334:
        month_n_date="1129"
    elif jday == 335:
        month_n_date="1130"
        #--------------------------
    elif jday == 336:
        month_n_date="1201"
    elif jday == 337:
        month_n_date="1202"
    elif jday == 338:
        month_n_date="1203"
    elif jday == 339:
        month_n_date="1204"
    elif jday == 340:
        month_n_date="1205"
    elif jday == 341:
        month_n_date="1206"
    elif jday == 342:
        month_n_date="1207"
    elif jday == 343:
        month_n_date="1208"
    elif jday == 344:
        month_n_date="1209"
    elif jday == 345:
        month_n_date="1210"
    elif jday == 346:
        month_n_date="1211"
    elif jday == 347:
        month_n_date="1212"
    elif jday == 348:
        month_n_date="1213"
    elif jday == 349:
        month_n_date="1214"
    elif jday == 350:
        month_n_date="1215"
    elif jday == 351:
        month_n_date="1216"
    elif jday == 352:
        month_n_date="1217"
    elif jday == 353:
        month_n_date="1218"
    elif jday == 354:
        month_n_date="1219"
    elif jday == 355:
        month_n_date="1220"
    elif jday == 356:
        month_n_date="1221"
    elif jday == 357:
        month_n_date="1222"
    elif jday == 358:
        month_n_date="1223"
    elif jday == 359:
        month_n_date="1224"
    elif jday == 360:
        month_n_date="1225"
    elif jday == 361:
        month_n_date="1226"
    elif jday == 362:
        month_n_date="1227"
    elif jday == 363:
        month_n_date="1228"
    elif jday == 364:
        month_n_date="1229"
    elif jday == 365:
        month_n_date="1230"
    elif jday == 366:
        month_n_date="1231"
        #--------------------------
        #--------------------------
    #-=-=-=-=-=-=-=-=-=-=-=-=-=
    else:
    #-=-=-=-=-=-=-=-=-=-=-=-=-=
        month_n_date="0000"
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
    #
    #
    return month_n_date
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Determine_mndate_from_leapjday
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Determine_mndate_from_jday
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Determine_mndate_from_jday(jday):
    #
    #-----#-----#-----#-----#-----
    #

    month_n_date="0000"

    if jday < 1:
        print("ERROR==>Input Jday cannot be less than 0.")
        return month_n_date
        #
        #----------------------------------------------------
        # End of if block
        #----------------------------------------------------

    if jday > 365:
        print("ERROR==>Input Jday cannot exceed 365.")
        return month_n_date
        #
        #----------------------------------------------------
        # End of if block
        #----------------------------------------------------

    if jday == 1:
        month_n_date="0101"
    elif jday == 2:
        month_n_date="0102"
    elif jday == 3:
        month_n_date="0103"
    elif jday == 4:
        month_n_date="0104"
    elif jday == 5:
        month_n_date="0105"
    elif jday == 6:
        month_n_date="0106"
    elif jday == 7:
        month_n_date="0107"
    elif jday == 8:
        month_n_date="0108"
    elif jday == 9:
        month_n_date="0109"
    elif jday == 10:
        month_n_date="0110"
    elif jday == 11:
        month_n_date="0111"
    elif jday == 12:
        month_n_date="0112"
    elif jday == 13:
        month_n_date="0113"
    elif jday == 14:
        month_n_date="0114"
    elif jday == 15:
        month_n_date="0115"
    elif jday == 16:
        month_n_date="0116"
    elif jday == 17:
        month_n_date="0117"
    elif jday == 18:
        month_n_date="0118"
    elif jday == 19:
        month_n_date="0119"
    elif jday == 20:
        month_n_date="0120"
    elif jday == 21:
        month_n_date="0121"
    elif jday == 22:
        month_n_date="0122"
    elif jday == 23:
        month_n_date="0123"
    elif jday == 24:
        month_n_date="0124"
    elif jday == 25:
        month_n_date="0125"
    elif jday == 26:
        month_n_date="0126"
    elif jday == 27:
        month_n_date="0127"
    elif jday == 28:
        month_n_date="0128"
    elif jday == 29:
        month_n_date="0129"
    elif jday == 30:
        month_n_date="0130"
    elif jday == 31:
        month_n_date="0131"
        #--------------------------
    elif jday == 32:
        month_n_date="0201"
    elif jday == 33:
        month_n_date="0202"
    elif jday == 34:
        month_n_date="0203"
    elif jday == 35:
        month_n_date="0204"
    elif jday == 36:
        month_n_date="0205"
    elif jday == 37:
        month_n_date="0206"
    elif jday == 38:
        month_n_date="0207"
    elif jday == 39:
        month_n_date="0208"
    elif jday == 40:
        month_n_date="0209"
    elif jday == 41:
        month_n_date="0210"
    elif jday == 42:
        month_n_date="0211"
    elif jday == 43:
        month_n_date="0212"
    elif jday == 44:
        month_n_date="0213"
    elif jday == 45:
        month_n_date="0214"
    elif jday == 46:
        month_n_date="0215"
    elif jday == 47:
        month_n_date="0216"
    elif jday == 48:
        month_n_date="0217"
    elif jday == 49:
        month_n_date="0218"
    elif jday == 50:
        month_n_date="0219"
    elif jday == 51:
        month_n_date="0220"
    elif jday == 52:
        month_n_date="0221"
    elif jday == 53:
        month_n_date="0222"
    elif jday == 54:
        month_n_date="0223"
    elif jday == 55:
        month_n_date="0224"
    elif jday == 56:
        month_n_date="0225"
    elif jday == 57:
        month_n_date="0226"
    elif jday == 58:
        month_n_date="0227"
    elif jday == 59:
        month_n_date="0228"
        #--------------------------
    elif jday == 60:
        month_n_date="0301"
    elif jday == 61:
        month_n_date="0302"
    elif jday == 62:
        month_n_date="0303"
    elif jday == 63:
        month_n_date="0304"
    elif jday == 64:
        month_n_date="0305"
    elif jday == 65:
        month_n_date="0306"
    elif jday == 66:
        month_n_date="0307"
    elif jday == 67:
        month_n_date="0308"
    elif jday == 68:
        month_n_date="0309"
    elif jday == 69:
        month_n_date="0310"
    elif jday == 70:
        month_n_date="0311"
    elif jday == 71:
        month_n_date="0312"
    elif jday == 72:
        month_n_date="0313"
    elif jday == 73:
        month_n_date="0314"
    elif jday == 74:
        month_n_date="0315"
    elif jday == 75:
        month_n_date="0316"
    elif jday == 76:
        month_n_date="0317"
    elif jday == 77:
        month_n_date="0318"
    elif jday == 78:
        month_n_date="0319"
    elif jday == 79:
        month_n_date="0320"
    elif jday == 80:
        month_n_date="0321"
    elif jday == 81:
        month_n_date="0322"
    elif jday == 82:
        month_n_date="0323"
    elif jday == 83:
        month_n_date="0324"
    elif jday == 84:
        month_n_date="0325"
    elif jday == 85:
        month_n_date="0326"
    elif jday == 86:
        month_n_date="0327"
    elif jday == 87:
        month_n_date="0328"
    elif jday == 88:
        month_n_date="0329"
    elif jday == 89:
        month_n_date="0330"
    elif jday == 90:
        month_n_date="0331"
        #--------------------------
    elif jday == 91:
        month_n_date="0401"
    elif jday == 92:
        month_n_date="0402"
    elif jday == 93:
        month_n_date="0403"
    elif jday == 94:
        month_n_date="0404"
    elif jday == 95:
        month_n_date="0405"
    elif jday == 96:
        month_n_date="0406"
    elif jday == 97:
        month_n_date="0407"
    elif jday == 98:
        month_n_date="0408"
    elif jday == 99:
        month_n_date="0409"
    elif jday == 100:
        month_n_date="0410"
    elif jday == 101:
        month_n_date="0411"
    elif jday == 102:
        month_n_date="0412"
    elif jday == 103:
        month_n_date="0413"
    elif jday == 104:
        month_n_date="0414"
    elif jday == 105:
        month_n_date="0415"
    elif jday == 106:
        month_n_date="0416"
    elif jday == 107:
        month_n_date="0417"
    elif jday == 108:
        month_n_date="0418"
    elif jday == 109:
        month_n_date="0419"
    elif jday == 110:
        month_n_date="0420"
    elif jday == 111:
        month_n_date="0421"
    elif jday == 112:
        month_n_date="0422"
    elif jday == 113:
        month_n_date="0423"
    elif jday == 114:
        month_n_date="0424"
    elif jday == 115:
        month_n_date="0425"
    elif jday == 116:
        month_n_date="0426"
    elif jday == 117:
        month_n_date="0427"
    elif jday == 118:
        month_n_date="0428"
    elif jday == 119:
        month_n_date="0429"
    elif jday == 120:
        month_n_date="0430"
    #--------------------------
    elif jday == 121:
        month_n_date="0501"
    elif jday == 122:
        month_n_date="0502"
    elif jday == 123:
        month_n_date="0503"
    elif jday == 124:
        month_n_date="0504"
    elif jday == 125:
        month_n_date="0505"
    elif jday == 126:
        month_n_date="0506"
    elif jday == 127:
        month_n_date="0507"
    elif jday == 128:
        month_n_date="0508"
    elif jday == 129:
        month_n_date="0509"
    elif jday == 130:
        month_n_date="0510"
    elif jday == 131:
        month_n_date="0511"
    elif jday == 132:
        month_n_date="0512"
    elif jday == 133:
        month_n_date="0513"
    elif jday == 134:
        month_n_date="0514"
    elif jday == 135:
        month_n_date="0515"
    elif jday == 136:
        month_n_date="0516"
    elif jday == 137:
        month_n_date="0517"
    elif jday == 138:
        month_n_date="0518"
    elif jday == 139:
        month_n_date="0519"
    elif jday == 140:
        month_n_date="0520"
    elif jday == 141:
        month_n_date="0521"
    elif jday == 142:
        month_n_date="0522"
    elif jday == 143:
        month_n_date="0523"
    elif jday == 144:
        month_n_date="0524"
    elif jday == 145:
        month_n_date="0525"
    elif jday == 146:
        month_n_date="0526"
    elif jday == 147:
        month_n_date="0527"
    elif jday == 148:
        month_n_date="0528"
    elif jday == 149:
        month_n_date="0529"
    elif jday == 150:
        month_n_date="0530"
    elif jday == 151:
        month_n_date="0531"
        #--------------------------
        #--------------------------
    elif jday == 152:
        month_n_date="0601"
    elif jday == 153:
        month_n_date="0602"
    elif jday == 154:
        month_n_date="0603"
    elif jday == 155:
        month_n_date="0604"
    elif jday == 156:
        month_n_date="0605"
    elif jday == 157:
        month_n_date="0606"
    elif jday == 158:
        month_n_date="0607"
    elif jday == 159:
        month_n_date="0608"
    elif jday == 160:
        month_n_date="0609"
    elif jday == 161:
        month_n_date="0610"
    elif jday == 162:
        month_n_date="0611"
    elif jday == 163:
        month_n_date="0612"
    elif jday == 164:
        month_n_date="0613"
    elif jday == 165:
        month_n_date="0614"
    elif jday == 166:
        month_n_date="0615"
    elif jday == 167:
        month_n_date="0616"
    elif jday == 168:
        month_n_date="0617"
    elif jday == 169:
        month_n_date="0618"
    elif jday == 170:
        month_n_date="0619"
    elif jday == 171:
        month_n_date="0620"
    elif jday == 172:
        month_n_date="0621"
    elif jday == 173:
        month_n_date="0622"
    elif jday == 174:
        month_n_date="0623"
    elif jday == 175:
        month_n_date="0624"
    elif jday == 176:
        month_n_date="0625"
    elif jday == 177:
        month_n_date="0626"
    elif jday == 178:
        month_n_date="0627"
    elif jday == 179:
        month_n_date="0628"
    elif jday == 180:
        month_n_date="0629"
    elif jday == 181:
        month_n_date="0630"
        #--------------------------
    elif jday == 182:
        month_n_date="0701"
    elif jday == 183:
        month_n_date="0702"
    elif jday == 184:
        month_n_date="0703"
    elif jday == 185:
        month_n_date="0704"
    elif jday == 186:
        month_n_date="0705"
    elif jday == 187:
        month_n_date="0706"
    elif jday == 188:
        month_n_date="0707"
    elif jday == 189:
        month_n_date="0708"
    elif jday == 190:
        month_n_date="0709"
    elif jday == 191:
        month_n_date="0710"
    elif jday == 192:
        month_n_date="0711"
    elif jday == 193:
        month_n_date="0712"
    elif jday == 194:
        month_n_date="0713"
    elif jday == 195:
        month_n_date="0714"
    elif jday == 196:
        month_n_date="0715"
    elif jday == 197:
        month_n_date="0716"
    elif jday == 198:
        month_n_date="0717"
    elif jday == 199:
        month_n_date="0718"
    elif jday == 200:
        month_n_date="0719"
    elif jday == 201:
        month_n_date="0720"
    elif jday == 202:
        month_n_date="0721"
    elif jday == 203:
        month_n_date="0722"
    elif jday == 204:
        month_n_date="0723"
    elif jday == 205:
        month_n_date="0724"
    elif jday == 206:
        month_n_date="0725"
    elif jday == 207:
        month_n_date="0726"
    elif jday == 208:
        month_n_date="0727"
    elif jday == 209:
        month_n_date="0728"
    elif jday == 210:
        month_n_date="0729"
    elif jday == 211:
        month_n_date="0730"
    elif jday == 212:
        month_n_date="0731"
        #--------------------------
    elif jday == 213:
        month_n_date="0801"
    elif jday == 214:
        month_n_date="0802"
    elif jday == 215:
        month_n_date="0803"
    elif jday == 216:
        month_n_date="0804"
    elif jday == 217:
        month_n_date="0805"
    elif jday == 218:
        month_n_date="0806"
    elif jday == 219:
        month_n_date="0807"
    elif jday == 220:
        month_n_date="0808"
    elif jday == 221:
        month_n_date="0809"
    elif jday == 222:
        month_n_date="0810"
    elif jday == 223:
        month_n_date="0811"
    elif jday == 224:
        month_n_date="0812"
    elif jday == 225:
        month_n_date="0813"
    elif jday == 226:
        month_n_date="0814"
    elif jday == 227:
        month_n_date="0815"
    elif jday == 228:
        month_n_date="0816"
    elif jday == 229:
        month_n_date="0817"
    elif jday == 230:
        month_n_date="0818"
    elif jday == 231:
        month_n_date="0819"
    elif jday == 232:
        month_n_date="0820"
    elif jday == 233:
        month_n_date="0821"
    elif jday == 234:
        month_n_date="0822"
    elif jday == 235:
        month_n_date="0823"
    elif jday == 236:
        month_n_date="0824"
    elif jday == 237:
        month_n_date="0825"
    elif jday == 238:
        month_n_date="0826"
    elif jday == 239:
        month_n_date="0827"
    elif jday == 240:
        month_n_date="0828"
    elif jday == 241:
        month_n_date="0829"
    elif jday == 242:
        month_n_date="0830"
    elif jday == 243:
        month_n_date="0831"
        #--------------------------
    elif jday == 244:
        month_n_date="0901"
    elif jday == 245:
        month_n_date="0902"
    elif jday == 246:
        month_n_date="0903"
    elif jday == 247:
        month_n_date="0904"
    elif jday == 248:
        month_n_date="0905"
    elif jday == 249:
        month_n_date="0906"
    elif jday == 250:
        month_n_date="0907"
    elif jday == 251:
        month_n_date="0908"
    elif jday == 252:
        month_n_date="0909"
    elif jday == 253:
        month_n_date="0910"
    elif jday == 254:
        month_n_date="0911"
    elif jday == 255:
        month_n_date="0912"
    elif jday == 256:
        month_n_date="0913"
    elif jday == 257:
        month_n_date="0914"
    elif jday == 258:
        month_n_date="0915"
    elif jday == 259:
        month_n_date="0916"
    elif jday == 260:
        month_n_date="0917"
    elif jday == 261:
        month_n_date="0918"
    elif jday == 262:
        month_n_date="0919"
    elif jday == 263:
        month_n_date="0920"
    elif jday == 264:
        month_n_date="0921"
    elif jday == 265:
        month_n_date="0922"
    elif jday == 266:
        month_n_date="0923"
    elif jday == 267:
        month_n_date="0924"
    elif jday == 268:
        month_n_date="0925"
    elif jday == 269:
        month_n_date="0926"
    elif jday == 270:
        month_n_date="0927"
    elif jday == 271:
        month_n_date="0928"
    elif jday == 272:
        month_n_date="0929"
    elif jday == 273:
        month_n_date="0930"
        #--------------------------
    elif jday == 274:
        month_n_date="1001"
    elif jday == 275:
        month_n_date="1002"
    elif jday == 276:
        month_n_date="1003"
    elif jday == 277:
        month_n_date="1004"
    elif jday == 278:
        month_n_date="1005"
    elif jday == 279:
        month_n_date="1006"
    elif jday == 280:
        month_n_date="1007"
    elif jday == 281:
        month_n_date="1008"
    elif jday == 282:
        month_n_date="1009"
    elif jday == 283:
        month_n_date="1010"
    elif jday == 284:
        month_n_date="1011"
    elif jday == 285:
        month_n_date="1012"
    elif jday == 286:
        month_n_date="1013"
    elif jday == 287:
        month_n_date="1014"
    elif jday == 288:
        month_n_date="1015"
    elif jday == 289:
        month_n_date="1016"
    elif jday == 290:
        month_n_date="1017"
    elif jday == 291:
        month_n_date="1018"
    elif jday == 292:
        month_n_date="1019"
    elif jday == 293:
        month_n_date="1020"
    elif jday == 294:
        month_n_date="1021"
    elif jday == 295:
        month_n_date="1022"
    elif jday == 296:
        month_n_date="1023"
    elif jday == 297:
        month_n_date="1024"
    elif jday == 298:
        month_n_date="1025"
    elif jday == 299:
        month_n_date="1026"
    elif jday == 300:
        month_n_date="1027"
    elif jday == 301:
        month_n_date="1028"
    elif jday == 302:
        month_n_date="1029"
    elif jday == 303:
        month_n_date="1030"
    elif jday == 304:
        month_n_date="1031"
        #--------------------------
    elif jday == 305:
        month_n_date="1101"
    elif jday == 306:
        month_n_date="1102"
    elif jday == 307:
        month_n_date="1103"
    elif jday == 308:
        month_n_date="1104"
    elif jday == 309:
        month_n_date="1105"
    elif jday == 310:
        month_n_date="1106"
    elif jday == 311:
        month_n_date="1107"
    elif jday == 312:
        month_n_date="1108"
    elif jday == 313:
        month_n_date="1109"
    elif jday == 314:
        month_n_date="1110"
    elif jday == 315:
        month_n_date="1111"
    elif jday == 316:
        month_n_date="1112"
    elif jday == 317:
        month_n_date="1113"
    elif jday == 318:
        month_n_date="1114"
    elif jday == 319:
        month_n_date="1115"
    elif jday == 320:
        month_n_date="1116"
    elif jday == 321:
        month_n_date="1117"
    elif jday == 322:
        month_n_date="1118"
    elif jday == 323:
        month_n_date="1119"
    elif jday == 324:
        month_n_date="1120"
    elif jday == 325:
        month_n_date="1121"
    elif jday == 326:
        month_n_date="1122"
    elif jday == 327:
        month_n_date="1123"
    elif jday == 328:
        month_n_date="1124"
    elif jday == 329:
        month_n_date="1125"
    elif jday == 330:
        month_n_date="1126"
    elif jday == 331:
        month_n_date="1127"
    elif jday == 332:
        month_n_date="1128"
    elif jday == 333:
        month_n_date="1129"
    elif jday == 334:
        month_n_date="1130"
        #--------------------------
    elif jday == 335:
        month_n_date="1201"
    elif jday == 336:
        month_n_date="1202"
    elif jday == 337:
        month_n_date="1203"
    elif jday == 338:
        month_n_date="1204"
    elif jday == 339:
        month_n_date="1205"
    elif jday == 340:
        month_n_date="1206"
    elif jday == 341:
        month_n_date="1207"
    elif jday == 342:
        month_n_date="1208"
    elif jday == 343:
        month_n_date="1209"
    elif jday == 344:
        month_n_date="1210"
    elif jday == 345:
        month_n_date="1211"
    elif jday == 346:
        month_n_date="1212"
    elif jday == 347:
        month_n_date="1213"
    elif jday == 348:
        month_n_date="1214"
    elif jday == 349:
        month_n_date="1215"
    elif jday == 350:
        month_n_date="1216"
    elif jday == 351:
        month_n_date="1217"
    elif jday == 352:
        month_n_date="1218"
    elif jday == 353:
        month_n_date="1219"
    elif jday == 354:
        month_n_date="1220"
    elif jday == 355:
        month_n_date="1221"
    elif jday == 356:
        month_n_date="1222"
    elif jday == 357:
        month_n_date="1223"
    elif jday == 358:
        month_n_date="1224"
    elif jday == 359:
        month_n_date="1225"
    elif jday == 360:
        month_n_date="1226"
    elif jday == 361:
        month_n_date="1227"
    elif jday == 362:
        month_n_date="1228"
    elif jday == 363:
        month_n_date="1229"
    elif jday == 364:
        month_n_date="1230"
    elif jday == 365:
        month_n_date="1231"
        #--------------------------
        #--------------------------
    #-=-=-=-=-=-=-=-=-=-=-=-=-=
    else:
    #-=-=-=-=-=-=-=-=-=-=-=-=-=
        month_n_date="0000"
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
    #
    #
    return month_n_date
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Determine_mndate_from_jday
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Determine_Wind_SPEED
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Determine_Wind_SPEED(data_from_netcdf):
    #
    #-----#-----#-----#-----#-----
    #
    MINUS99='-99'
    DBLDASH='--'
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    #
    #
    STR_WSPEED_A=data_from_netcdf
    STR_WSPEED_B=str(data_from_netcdf)
    STR_WSPEED_X10=STR_WSPEED_A*10.0
    STR_WSPEED_X10C=str(STR_WSPEED_X10)
    STR_WSPEED=STR_WSPEED_X10C[0:3]
    STR_Wind_SPEED_Value=STR_WSPEED_X10C[0:3]
    #
    #
    #-----------------------------
    #
    #----------------------------------------------------------------
    # If the Wind Speed is less than 0, then use -99, otherwise,
    # take the first three characters.
    #----------------------------------------------------------------
    #
    if STR_WSPEED_A < 0.0:
	#
        STR_WSPEED=MINUS99
        #
    elif STR_WSPEED_B == DBLDASH:
        #
        STR_WSPEED=MINUS99
        #
    else:
        #
        STR_WSPEED=STR_WSPEED_X10C[0:3]
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
        #
    #
    if (STR_WSPEED_A >= 10.0) and (STR_WSPEED_A < 100.0):
        STR_WSPEED=STR_WSPEED_X10C[0:3]
        #
    #
    if (STR_WSPEED_A >= 1.0) and (STR_WSPEED_A < 10.0):
        STR_WSPEED='+'+STR_WSPEED_X10C[0:2]
        #
    #
    if (STR_WSPEED_A >= 0.1) and (STR_WSPEED_A < 1.0):
        STR_WSPEED='+0'+STR_WSPEED_X10C[0:1]
        #
    #
    if (STR_WSPEED_A >= 0.0) and (STR_WSPEED_A < 0.1):
        STR_WSPEED='000'
        #
    #=QWERTYUIOP.ASDFGHJKL.ZXCVBNM=
    #
    #
    if MATH.isnan(data_from_netcdf):
        STR_WSPEED=MINUS99
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    #-----
    STR_Wind_SPEED_Value=STR_WSPEED
    #
    return STR_Wind_SPEED_Value
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Determine_Wind_SPEED
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Determine_Wind_Direction
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Determine_Wind_Direction(data_from_file):
    #
    #-----#-----#-----#-----#-----
    #
    MINUS99="-99"
    DBLDASH="--"
    #
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    STR_WDIR_A=data_from_file
    STR_WDIR_B=str(data_from_file)
    STR_WDIR_X1=STR_WDIR_A*1.0
    STR_WDIR_X1C=str(STR_WDIR_X1)
    STR_WDIR=STR_WDIR_X1C[0:3]
    #
    if MATH.isnan(STR_WDIR_A):
        STR_WDIR=MINUS99
	#
	#-----------------------------------------------------------
	# End of if block
	#-----------------------------------------------------------
    #
    #
    #----------------------------------------------------------------
    # If the Wind direction is less than 0, then use -99, otherwise,
    # take the first three characters.
    #----------------------------------------------------------------
    if STR_WDIR_A < 0.0:
	#
        STR_WDIR=MINUS99
        #
	#
    elif MATH.isnan(STR_WDIR_A):
        #
        STR_WDIR=MINUS99
	#
    elif STR_WDIR_B == DBLDASH:
        #
        STR_WDIR=MINUS99
        #
    else:
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # NESTED IF BLOCK 
        # If the Wind direction is less than 100, then pad a zero up front, otherwise,
        # take the first three characters.
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        #
        if (STR_WDIR_A >= 10.0) and (STR_WDIR_A < 100.0):
            STR_WDIR='0'+STR_WDIR_X1C[0:2]
            #
	if (STR_WDIR_A >= 1.0) and (STR_WDIR_A < 10.0):
            STR_WDIR='00'+STR_WDIR_X1C[0:1]
            #
	if (STR_WDIR_A >= 0.1) and (STR_WDIR_A < 1.0):
            STR_WDIR='000'
            #
	if (STR_WDIR_A >= 0.0) and (STR_WDIR_A < 0.1):
            STR_WDIR='000'
            #
        #if datawdir[i,j] < 100.0:
            #    ###STR_WDR="0"+str(datawdir[i,j])
            #    STR_WDR="0"+STR_WDR_X1C[0:2]
        #
	#else:
	##
        #    STR_WDR=STR_WDR_X1C[0:3]
	#   #	        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	# End of NESTED IF block
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
        #
        #
    #
    if MATH.isnan(data_from_file):
        STR_WDIR=MINUS99
	#
	#-----------------------------------------------------------
	# End of if block
	#-----------------------------------------------------------
    #
    STR_Wind_Direction_Value=STR_WDIR
    #
    #-----
    #
    return STR_Wind_Direction_Value
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Determine_Wind_Direction FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#

#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Compute_MLE_STRNG
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Compute_MLE_STRNG(datafromfile, MAX_data_Value):
    #-----
    ###import math as MATH
    #-----
    #
    dadash="-------------------------------------"
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    Value_of_MLE = 0
    #
    STR_Value_of_MLE = str(Value_of_MLE)
    #
    #-----math.fabs(-2.0)
    #
    # Calculate prob value.
    #
    probability0=0
    probability0=(datafromfile-MAX_data_Value)/2.0
    Value_of_MLE0 = MATH.exp(probability0)
    #
    #Value_of_MLE0 = MATH.exp(datafromfile)
    #
    Value_of_MLE1 = MATH.fabs(Value_of_MLE0)
    Value_of_MLE_3K = Value_of_MLE1*30000.0
    #
    if MATH.isnan(Value_of_MLE_3K):
        #
        Value_of_MLE  = Value_of_MLE1
        #
    else:
        Value_of_MLE  = MATH.trunc(Value_of_MLE_3K)
        #
        #MATH.trunc(x)
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    STR_Value_of_MLE0 = str(Value_of_MLE)
    LEN_Value_of_MLE0 = len(STR_Value_of_MLE0)
    #
    #
    #----------------------------------------------------------------
    # Begin IF Block for LEN_FLAGS_B
    #----------------------------------------------------------------
    #
    if LEN_Value_of_MLE0 == 1:
	#
        STR_Value_of_MLE='0000'+STR_Value_of_MLE0
	#
    elif LEN_Value_of_MLE0 == 2:
        #
        STR_Value_of_MLE='000'+STR_Value_of_MLE0
        #
    elif LEN_Value_of_MLE0 == 3:
        #
        STR_Value_of_MLE='00'+STR_Value_of_MLE0
        #
    elif LEN_Value_of_MLE0 == 4:
        #
        STR_Value_of_MLE='0'+STR_Value_of_MLE0
        #
    elif LEN_Value_of_MLE0 == 5:
        #
        STR_Value_of_MLE=STR_Value_of_MLE0
        #
    else:
        #
        STR_Value_of_MLE=STR_Value_of_MLE0[0:5]
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    if MATH.isnan(datafromfile):
        #
	STR_Value_of_MLE='---99'
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    temp_STR=STR_Value_of_MLE
    LEN_temp_STR = len(temp_STR)
    #
    if LEN_temp_STR != 5:
        print(dadash)
        print "The MLE String was NOT 5 Characters long!"
        print(dadash)
        if LEN_temp_STR > 5:
            STR_Value_of_MLE=temp_STR[0:5]
            #
            #-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
            # End of if block
            #-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
        if LEN_temp_STR == 0:
            STR_Value_of_MLE='00000'
            #
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
            # End of if block
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
        if LEN_temp_STR == 1:
            STR_Value_of_MLE='0000'+temp_STR
            #
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
            # End of if block
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
        if LEN_temp_STR == 2:
            STR_Value_of_MLE='000'+temp_STR
            #
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
            # End of if block
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
        if LEN_temp_STR == 3:
            STR_Value_of_MLE='00'+temp_STR
            #
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
            # End of if block
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
        if LEN_temp_STR == 4:
            STR_Value_of_MLE='0'+temp_STR
            #
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
            # End of if block
            #-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y-y
        #
        #
        #-----------------------------------------------------------
        # End of if block [[[LEN_temp_STR != 5]]]
        #-----------------------------------------------------------
    #
    if MATH.isnan(datafromfile):
        #
	STR_Value_of_MLE='---99'
        #
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    #
    #-----
    #
    return STR_Value_of_MLE
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Compute_MLE_STRNG FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#

#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Print_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Print_Current_Time(now):
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print
    print "Current date and time using str method of datetime object:"
    print str(now)
    #-----
    print " \n"
    print "Current date and time using instance attributes:"
    print "Current year: %d" % now.year
    print "Current month: %d" % now.month
    print "Current day: %d" % now.day
    print "Current hour: %d" % now.hour
    print "Current minute: %d" % now.minute
    print "Current second: %d" % now.second
    print "Current microsecond: %d" % now.microsecond
    #-----
    print " \n"
    print "Current date and time using strftime:"
    #print now.strftime("%Y-%m-%d %H:%M")
    print now.strftime("%Y-%m-%d...%H:%M")
    #-----
    print " \n"
    print "Current date and time using isoformat:"
    print now.isoformat()
    return now.strftime("%Y-%m-%d...%H:%M")
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Print_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
###---0

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#

#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Access_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Access_Current_Time(now):
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print
    print "Current date and time using str method of datetime object:"
    print str(now)
    #-----
    print " \n"
    print "Current date and time using instance attributes:"
    print "Current year: %d" % now.year
    print "Current month: %d" % now.month
    print "Current day: %d" % now.day
    print "Current hour: %d" % now.hour
    print "Current minute: %d" % now.minute
    print "Current second: %d" % now.second
    print "Current microsecond: %d" % now.microsecond
    #-----
    print " \n"
    print "Current date and time using strftime:"
    #print now.strftime("%Y-%m-%d %H:%M")
    print now.strftime("%Y-%m-%d...%H:%M")
    #-----
    print " \n"
    print "Current date and time using isoformat:"
    print now.isoformat()
    return now.strftime("%Y-%m-%d.rapidscat.ncdf.%H-%M")
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Access_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----



###---
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



###---1
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Get_Converted_Time90
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Get_Converted_Time90(spacecrafttime):
    #
    # The input variable -spacecrafttime- must be provided in seconds 
    # since January 1st, 1990:Time 0000UTC
    # This is referred to as the basis time, 0 seconds.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  The input  spacecrafttime is expressed in seconds. 
    #  The input value must be a floating point number.
    #  A typical input value cojuld be -507502997.521-sec. 
    #  This would be for Jan 30th, 2015 at around 1525 UTC
    #  This routine will code this time as:
    #  20150130-1525.00.000-UTC-
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - processed- - - - -
    # We will eventually output the converted time as a string -str_converted_sctime-
    # This will be a string in the following format:
    # yyyyMMdd-HHmm.SS.sss-UTC-
    # Thus the Basis time would be expressed as:
    # 19900101-0000.00.000-UTC-
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Another example. February 5th, 2015, 1234[hours and min] 
    # and 56.789 seconds UTC is expressed as :
    # 20150205-1234.56.789-UTC-
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # =====================
    # NOTE CAREFULLY!!!!! 
    # =====================
    # THIS FUNCTION WORKS FOR NASA RAPIDSCAT (FROM KNMI) AND NASA RAPIDSCAT (KNMI) ONLY!!!!!
    # --------------------------------------------------------------------
    # The basis time for RapidScat is currently a one-of-a-kind -19900101-0000.00.000-UTC--. 
    # No other active satellites use this basis time as far as we know!
    # Unless you KNOW that your satellite uses the 1990 basis time shown above, 
    # THEN YOU MUST REWRITE THIS FUNCTION FOR YOUR OWN PURPOSES.
    # This function will not work otherwise. 
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   
    #-----
    ###import datetime
    #-----
    #
    #-----------------------------------------------------
    #
    dadots=".  .  .  .  .  .  .  .  .  .  .  .  ."
    dadash="-------------------------------------"
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    #
    #--#print(dadots+dadots)
    #--#print(dadots+dadots)
    #--#print(dadots+dadots)

    #
    #--#print("spacecrafttime is...."+str(spacecrafttime))	###---===---
    #
    #
    temp_str="00"
    #
    #
    waterfalltime=spacecrafttime*1.0
    #
    rightnow = datetime.datetime.now()
    str_converted_sctime = str(rightnow)
    #
    #
    #--#print(dadots+dadots)
    #--#print(str_converted_sctime)TEST_20150901_AB.TXT
    #--#print(dadots+dadots)
    #
    # Values for observation time. I will eventually concatenate these together 
    # in the variable -str_converted_sctime- and return to the main program.
    #
    #
    ob_s_year = rightnow.year
    ob_s_mnth = rightnow.month
    ob_s_date = rightnow.day
    ob_s_hour = rightnow.hour
    ob_s__min = rightnow.minute
    ob_s__sec = rightnow.second
    ob_s_msec = rightnow.microsecond
    #
    #
    obs_year = str(rightnow.year)
    obs_mnth = str(rightnow.month)
    obs_date = str(rightnow.day)
    obs_hour = str(rightnow.hour)
    obs__min = str(rightnow.minute)
    obs__sec = str(rightnow.second)
    obs_msec = str(rightnow.microsecond)
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -
    #
    if ob_s_mnth < 10:
        temp_str='0'+obs_mnth
        obs_mnth=temp_str
        # - - - - - - - - - - - - - - - - - #
    if ob_s_date < 10:
        temp_str='0'+obs_date
        obs_date=temp_str
        # - - - - - - - - - - - - - - - - - #
    if ob_s_hour < 10:
        temp_str='0'+obs_hour
        obs_hour=temp_str
        # - - - - - - - - - - - - - - - - - #
    if ob_s__min < 10:
        temp_str='0'+obs__min
        obs__min=temp_str
        # - - - - - - - - - - - - - - - - - #
    if ob_s__sec < 10:
        temp_str='0'+obs__sec
        obs__sec=temp_str
        # - - - - - - - - - - - - - - - - - #
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -
    #
    str_converted_sctime_a=obs_year+obs_mnth+obs_date+'-'
    str_converted_sctime_b=obs_hour+obs__min+'.'+obs__sec+'.'+obs_msec
    str_converted_sctime=str_converted_sctime_a+str_converted_sctime_b+'-UTC-'
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -
    #
    # Constants for time conversions.
    #
    sec_pr_min=60.0	# The # of seconds per minute
    min_per_hr=60.0	# The # of minutes per hour
    hr_per_day=24.0	# The # of hours per day
    day_per_yr=365.0	# The # of days per year (non-leapyear)
    day_pr_lyr=366.0	# The # of days per leapyear
    #
    sec_per_hr = sec_pr_min*min_per_hr	           # The # of seconds per hour
    #						   #
    sec_pr_day = sec_pr_min*min_per_hr*hr_per_day  # The # of seconds per day
    #						   #
    sec_per_yr = sec_pr_day*day_per_yr		   # The # of seconds per year(non-leapyear) 
    #						   #
    sec_pr_lyr = sec_pr_day*day_pr_lyr		   # The # of seconds per leapyear
    #
    #-------------------------------------------------------------------------------
    #
    # No Rapidscat data IS known to exist prior to Jan 1st, 2013, 0000UTC.
    # I will refer to this date and time as the FNMOC_RapidScat Start time,
    # or simply -FR_start_13-.
    # Therefore, to simplify the converesion process, I will calculate the 
    # number of seconds from the basis time to FR_start. I will make comparisons
    # to -FR_Start- to figure out years dates etc. 
    #
    #-------------------------------------------------------------------------------
    #
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -
    # From 1990 to 1999, there have been 2 leap years [1992, 1996]
    # [That is Jan 90 to Jan 1999] 
    # From 1990 to 1999, there have been 7 non-leap years [1990, 1991, 1993, 1994, 1995, 1997, 1998]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    FR_start_9099 = (7.0*sec_per_yr) + (2.0 * sec_pr_lyr)
    #
    # answer should be 283996800.0
    # This represents the number of seconds from Jan 1 1990 at 0000UTC
    # UNTIL Jan 1, 1999 at 0000UTC
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -
    # From 1999 to 2013, there have been 4 leap years [2000, 04, 08, 12]
    # [Thats Jan 99 to Jan 2013] 
    # Since 1999, there have been 10 non-leap years [1999, 2001,02,03,05,06,07,09,10,11]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    FR_start_13 = FR_start_9099 + (10.0*sec_per_yr) + (4 * sec_pr_lyr)
    #
    # answer should be 725846400.0   (283996800.0 sec + 441849600.0 sec)
    # This represents the number of seconds from Jan 1 1999 at 0000UTC
    # UNTIL Jan 1, 2013 at 0000UTC
    #
    #-----------------------------------------------------
    # I will now calculate the start times out to 2030 
    # That means Jan 1st, 0000UTC each year.
    #-----------------------------------------------------
    #     
    FR_start_14 = FR_start_13 + (1.0*sec_per_yr)
    #
    FR_start_15 = FR_start_14 + (1.0*sec_per_yr)
    #
    FR_start_16 = FR_start_15 + (1.0*sec_per_yr)
    #
    FR_start_17 = FR_start_16 + (1.0*sec_pr_lyr)  ### 2016 is a leap year, you add the extra to 2017.
    #
    FR_start_18 = FR_start_17 + (1.0*sec_per_yr)
    #
    FR_start_19 = FR_start_18 + (1.0*sec_per_yr)
    #
    FR_start_20 = FR_start_19 + (1.0*sec_per_yr)
    #
    FR_start_21 = FR_start_20 + (1.0*sec_pr_lyr)  ### 2020 is a leap year, you add the extra to 2021.
    #
    FR_start_22 = FR_start_21 + (1.0*sec_per_yr)
    #
    FR_start_23 = FR_start_22 + (1.0*sec_per_yr)
    #
    FR_start_24 = FR_start_23 + (1.0*sec_per_yr)
    #
    FR_start_25 = FR_start_24 + (1.0*sec_pr_lyr)  ### 2024 is a leap year, you add the extra to 2025.
    #
    FR_start_26 = FR_start_25 + (1.0*sec_per_yr)
    #
    FR_start_27 = FR_start_26 + (1.0*sec_per_yr)
    #
    FR_start_28 = FR_start_27 + (1.0*sec_per_yr)
    #
    FR_start_29 = FR_start_28 + (1.0*sec_pr_lyr)  ### 2028 is a leap year, you add the extra to 2029.
    #
    FR_start_30 = FR_start_29 + (1.0*sec_per_yr)
    #
    # NEXT, WE DO A CASE TYPE STATEMENT WHERE WE ASSIGN THE VALUE OF THE YEAR BASED ON THE # OF SECONDS.
    #
    #~~~~~~~~~~~~~~~~~~~~~
    #----------------------------------------------------------------
    # If the wind direction is less than 100, pad a zero up front.
    #----------------------------------------------------------------
    #
    decrement4years = FR_start_13
    basis_year=1999
    my_year=0
    year__count=10.0
    Lyear_count=4.0
    yesnoleapyear = 0

    #
    if spacecrafttime > FR_start_13:
        obs_year = "2013"
        decrement4years = FR_start_13
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_14:
        obs_year = "2014"
        decrement4years = FR_start_14
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_15:
        obs_year = "2015"
        decrement4years = FR_start_15
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_16:
        obs_year = "2016"
        decrement4years = FR_start_16
        year__count=year__count+1.0
	yesnoleapyear = 1
        #
    if spacecrafttime > FR_start_17:
        obs_year = "2017"
        decrement4years = FR_start_17
        Lyear_count=Lyear_count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_18:
        obs_year = "2018"
        decrement4years = FR_start_18
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_19:
        obs_year = "2019"
        decrement4years = FR_start_19
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_20:
        obs_year = "2020"
        decrement4years = FR_start_20
        Lyear_count=Lyear_count+1.0
	yesnoleapyear = 1
        #
    if spacecrafttime > FR_start_21:
        obs_year = "2021"
        decrement4years = FR_start_21
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_22:
        obs_year = "2022"
        decrement4years = FR_start_22
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_23:
        obs_year = "2023"
        decrement4years = FR_start_23
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_24:
        obs_year = "2024"
        decrement4years = FR_start_24
        Lyear_count=Lyear_count+1.0
	yesnoleapyear = 1
        #
    if spacecrafttime > FR_start_25:
        obs_year = "2025"
        decrement4years = FR_start_25
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_26:
        obs_year = "2026"
        decrement4years = FR_start_26
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_27:
        obs_year = "2027"
        decrement4years = FR_start_27
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_28:
        obs_year = "2028"
        decrement4years = FR_start_28
        Lyear_count=Lyear_count+1.0
	yesnoleapyear = 1
        #
    if spacecrafttime > FR_start_29:
        obs_year = "2029"
        decrement4years = FR_start_29
        year__count=year__count+1.0
	yesnoleapyear = 0
        #
    if spacecrafttime > FR_start_30:
	my_year=basis_year +int(spacecrafttime/sec_per_yr)
        decrement4years = FR_start_30
      	decrement4years = (sec_pr_lyr * Lyear_count)+(sec_per_yr * year__count)
        obs_year =str(my_year)
	yesnoleapyear = 0
	#-----------------------------------------------------------
	# End of if block
	#-----------------------------------------------------------
    #
    #--#print("obs_year is...."+str(obs_year))	###---===---
    #

    #
    ynly = yesnoleapyear
    #
    ###decrement4years = (sec_pr_lyr * Lyear_count)+(sec_per_yr * year__count)
    #
    #--#print("decrement4years is...."+str(decrement4years))	###---===---
    #
    #
    if decrement4years < FR_start_14:
	print("ERROR==>decrement4years cannot be such a small number.")
	return str_converted_sctime
        #
	#----------------------------------------------------
	# End of if block
	#----------------------------------------------------
    #-----------------------------------------------------------0128
    if spacecrafttime > decrement4years:
        waterfalltime = spacecrafttime - decrement4years
        #--#print("waterfalltime-decrm- is...."+str(waterfalltime))	###---===---
	#
	#
	#----------------------------------------------------

	# End of if block
	#----------------------------------------------------
    #-----------------------------------------------------------
    if waterfalltime < 0:
	print(dadots+dadots)
	print("ERROR==>waterfalltime cannot be negative.")
	print(dadots+dadots)
	#----------------------------------------------------
	# End of if block
	#----------------------------------------------------
    #
    month_flag=1.0
    first_day_of_month=1.0
    #
    #-----------------------------------------------------------
    # Now get the number of days. 
    #-----------------------------------------------------------
    #
    num_days =  int(waterfalltime/sec_pr_day)
    #
    print("num_days is...."+str(num_days))	###---===---
    #
    #
    this_month_n_date="0000"                                       ###---===---
    #                                                               ##---===---
    this_month_n_date=Determine_mndate_from_jday(num_days-1)       ###---===---
    #                                                               ##---===---
    if yesnoleapyear == 1:                                         ###---===---
        print(dadots+dadots)                                       ###---===---
        print("This is a leap year.")                              ###---===---
        print(dadots+dadots)                                       ###---===---
        this_month_n_date=Determine_mndate_from_leapjday(num_days-1) #---===---
    else:                                                          ###---===---
        print("---This is [NOT] a leap year. ---")                 ###---===---
        #----------------------------------------------------      ###---===---
        # End of if block                                          ###---===---
        #----------------------------------------------------      ###---===---
        #----------------------------------------------------      ###---===---
    #
    #
    if num_days > 366:
	print(dadots+dadots)
	print("ERROR==>number of days cannot be greater than 366.")
	print(dadots+dadots)
	#----------------------------------------------------
	# End of if block
	#----------------------------------------------------
        #----------------------------------------------------
    if obs_mnth == "0":
        obs_mnth = "01"
        #
        #----------------------------------------------------
        #
    if ((num_days > 0) and (num_days <= 31)):
	obs_mnth = "01"
	month_flag=1.0
	first_day_of_month=1.0
	#----------------------------------------------------
    if ((num_days >= 32) and (num_days <= 59+ynly)):
	obs_mnth = "02"
	month_flag=2.0
	first_day_of_month=32.0
	#----------------------------------------------------
    if ((num_days >= 60+ynly) and (num_days <= 90+ynly)):
	obs_mnth = "03"
	month_flag=3.0
	first_day_of_month=60.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 91+ynly) and (num_days <= 120+ynly)):
	obs_mnth = "04"
	month_flag=4.0
	first_day_of_month=91.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 121+ynly) and (num_days <= 151+ynly)):
	obs_mnth = "05"
	month_flag=5.0
	first_day_of_month=121.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 152+ynly) and (num_days <= 181+ynly)):
	obs_mnth = "06"
	month_flag=6.0
	first_day_of_month=152.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 181+ynly) and (num_days <= 212+ynly)):
	obs_mnth = "07"
	month_flag=7.0
	first_day_of_month=181.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 213+ynly) and (num_days <= 243+ynly)):
	obs_mnth = "08"
	month_flag=8.0
	first_day_of_month=213.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 244+ynly) and (num_days <= 274+ynly)):
	obs_mnth = "09"
	month_flag=9.0
	first_day_of_month=244.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 274+ynly) and (num_days <= 304+ynly)):
	obs_mnth = "10"    #  20150130-1525.00.000-UTC-
	month_flag=10.0
	first_day_of_month=274.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 305+ynly) and (num_days <= 334+ynly)):
	obs_mnth = "11"
	month_flag=11.0
	first_day_of_month=305.0+(ynly*1.0)
    	#----------------------------------------------------
    if ((num_days >= 335+ynly) and (num_days <= 365+ynly)):
	obs_mnth = "12"
	month_flag=12.0
	first_day_of_month=335.0+(ynly*1.0)
    	#----------------------------------------------------
    #-----------------------------------------------
    obs_mnth = this_month_n_date[0:2]                                   #---===---

    #-----------------------------------------------
        #----------------------------------------------------
    if obs_mnth == "0":
        obs_mnth = "00"
        print("ERROR!!ERROR!! obs_mnth is...."+str(obs_mnth))                    ###---===---
        print("ERROR!!ERROR!! obs_mnth is not being calculated correctly.")      ###---===---
        #
    #-----------------------------------------------------
    #
    #-----------------------------------------------------
    #
    #--#print("obs_mnth is...."+str(obs_mnth))	###---===---
    #
    #--#print("first_day_of_month is...."+str(first_day_of_month))	###---===---
    #
    datewaterfalltime=waterfalltime-(1.0*first_day_of_month*sec_pr_day)
    #
    #--#print("datewaterfalltime is...."+str(datewaterfalltime))	###---===---
    #
    the_date_of_the_month =int(datewaterfalltime / sec_pr_day)
    #
    #--#print("the_date_of_the_month is...."+str(the_date_of_the_month))	###---===---
    #
    obs_date = str(the_date_of_the_month)
    #
    obs_date = this_month_n_date[2:4]                                    #---===---

    #
    #
    if obs_date == "1":
        obs_date = "01"
        #
    if obs_date == "2":
        obs_date = "02"
        #
    if obs_date == "3":
        obs_date = "03"
	#
    if obs_date == "4":
        obs_date = "04"
        #        #    #
    if obs_date == "5":
        obs_date = "05"
        #
    if obs_date == "6":
        obs_date = "06"
        #0128
    if obs_date == "7":
        obs_date = "07"
        #
    if obs_date == "8":
        obs_date = "08"
        #
    if obs_date == "9":
        obs_date = "09"
        #
    if obs_date == "0":
        obs_date = "00"
        #
    #
    #--#print("obs_date is...."+str(obs_date))	###---===---
    #
    #-----------------------------------------------------
    #
    hourwaterfalltime=waterfalltime-(1.0*num_days*sec_pr_day)

    num_hours = int(hourwaterfalltime/sec_per_hr) # sec_per_hr


    obs_hour = str(num_hours)
    #
    if obs_hour == "0":
        obs_hour = "00"
        #
    if obs_hour == "1":
        obs_hour = "01"
        #
    if obs_hour == "2":
        obs_hour = "02"
        #
    if obs_hour == "3":
        obs_hour = "03"
        #
    if obs_hour == "4":
        obs_hour = "04"
        #
    if obs_hour == "5":
        obs_hour = "05"
        #
    if obs_hour == "6":
        obs_hour = "06"
        #
    if obs_hour == "7":
        obs_hour = "07"
        #
    if obs_hour == "8":
        obs_hour = "08"
        #
    if obs_hour == "9":
        obs_hour = "09"
        #
    #
    #-----------------------------------------------------
    ###
    mintwaterfalltime=hourwaterfalltime-(1.0*num_hours*sec_per_hr)
    
    num_mint=int(mintwaterfalltime/sec_pr_min)

    obs__min = str(num_mint)
    #
    if obs__min == "0":
        obs__min = "00"
        #
    if obs__min == "1":
        obs__min = "01"
        #    #
    if obs__min == "2":
        obs__min = "02"
        #
    if obs__min == "3":
        obs__min = "03"
        #
    if obs__min == "4":
        obs__min = "04"
        #
    if obs__min == "5":
        obs__min = "05"
        #
    if obs__min == "6":
        obs__min = "06"
        #    #
    if obs__min == "7":
        obs__min = "07"
        #
    if obs__min == "8":
        obs__min = "08"
        #
    if obs__min == "9":
        obs__min = "09"
        #
    #-----------------------------------------------------
    ###
    sec_waterfalltime=mintwaterfalltime-(1.0*num_mint*sec_pr_min)

    num_sec=int(sec_waterfalltime/1.0)


    obs__sec = str(num_sec)
    #
    if obs__sec == "0":
        obs__sec = "00"
        #
    if obs__sec == "1":
        obs__sec = "01"
        #
    if obs__sec == "2":
        obs__sec = "02"
        #
    if obs__sec == "3":
        obs__sec = "03"
        #
    if obs__sec == "4":
        obs__sec = "04"
        #
    if obs__sec == "5":
        obs__sec = "05"
        #
    if obs__sec == "6":
        obs__sec = "06"
        #
    if obs__sec == "7":
        obs__sec = "07"
        #
    if obs__sec == "8":
        obs__sec = "08"
        #
    if obs__sec == "9":
        obs__sec = "09"
        #
    #
    #-----------------------------------------------------
    ###
    msec_waterfalltime=sec_waterfalltime-(1.0*num_sec)

    num_msec=int(msec_waterfalltime*1000.0)

    obs_msec = str(num_msec)
    #-----------------------------------------------------
    #    #  20150130-1525.00.000-UTC-
    #-----------------------------------------------------

    str_converted_sctime_a=obs_year+obs_mnth+obs_date+'-'

    str_converted_sctime_b=obs_hour+obs__min+'.'+obs__sec+'.'+obs_msec

    str_converted_sctime=str_converted_sctime_a+str_converted_sctime_b+'-UTC-'

    #
    #-----------------------------------------------------
    #
    return str_converted_sctime
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Get_Converted_Time90 FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
########################################################################################################
########################################################################################################
#### BEGINNING OF MAIN FUNCTION ########################################################################
########################################################################################################
########################################################################################################
#######-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
#######  Begin MAIN Function for processing NETCDF file of RAPIDSCAT DATA
#######-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
#######
#######

def main():

    dadots='.  .  .  .  .  .  .  .  .  .  .  .  .'
    dadash='-------------------------------------'
    dddots='.....................................'
    dastar='*************************************'
    dahash='#####################################'
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    #
    ONE_SPACE=' '
    STR_1_SPACE_CHAR=ONE_SPACE
    STR_2_SPACE_CHAR=ONE_SPACE+STR_1_SPACE_CHAR
    STR_3_SPACE_CHAR=ONE_SPACE+STR_2_SPACE_CHAR
    STR_4_SPACE_CHAR=ONE_SPACE+STR_3_SPACE_CHAR
    STR_5_SPACE_CHAR=ONE_SPACE+STR_4_SPACE_CHAR
    STR_6_SPACE_CHAR=ONE_SPACE+STR_5_SPACE_CHAR
    #
    this_execution=1
    #
    right_now=' '
    print(" \n")
    print(dadash+dadash)
    print(dadash+dadash)
    print(dadash+dadash)
    #
    the_start_time = Print_Current_Time(right_now)
    print(" \n")
    print(dadash+dadash)
    print(dadash+dadash)
    print(dadash+dadash)
    #
    print(dadots)
    print('---BEGIN rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py  -----')
    print('---BEGINNING THE --MAIN[]-- FUNCTION  -----')
    print(dadots)
    #
    print(dadash)
    #
    #----------------------------------------------------------------------------
    # Determine the paths of data:
    #   datapath:     	This is where the NETCDF from NASA files are stored.
    #   graphicpath:	This is the location where graphics are saved.
    #   ascii_path:   	This is where the ASCII version of the data is stored.
    #   binpath:	This is the location of this python source code.
    #   utilpath:       This is a utility subdirectory under the binpath.
    #   procpath:       This is a subdirectory that logs the NETCDF files already processed.
    #----------------------------------------------------------------------------
    #
    myhostname=socket.gethostname()
    thehost=myhostname[0:4]
    #
    #
    infromlinux = commands.getoutput('echo ${OPSBIN}')		### /satdat/bin
    #                                                           ### /u/ops/bin
    #
    my_OPSBIN=infromlinux
    #
    #-----------------
    if my_OPSBIN== '':
        my_OPSBIN='/satdat/bin'
        #----------------------
        if thehost == "a4bu":
            my_OPSBIN='/u/ops/bin'
            #
        #----------------------
        if thehost == "a4ou":
            my_OPSBIN='/u/ops/bin'
            #
        #----------------------

        #
    #----------------------------------------------------------------
        
    #
    infromlinux = commands.getoutput('echo ${XFER_BASEPATH}')   ### XFER_BASEPATH=/satdat/curr/rscat_knmi 
    #
    my_XFER_BASEPATH=infromlinux
    #
    #-----------------
    if my_XFER_BASEPATH== '':
        my_XFER_BASEPATH='/satdat/curr/rscat_knmi'
        #
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #
    #----------------------------------------------------------------
    #
    myinfromlinux = commands.getoutput('echo ${XFER_BASEPATH}')   ### XFER_BASEPATH=/satdat/curr/rscat_knmi
    #
    my_SATFOCUS_BASEPATH=myinfromlinux+'/../rscat_satfocus'
    #
    #-----------------
    if my_SATFOCUS_BASEPATH== '':
        my_SATFOCUS_BASEPATH='/satdat/curr/rscat_satfocus'
        #
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #
    infromlinux = commands.getoutput('echo ${RSCAT_BASEPATH}')  ### RSCAT_BASEPATH=$XFER_BASEPATH/../RapidScat
    #                                                           ### RSCAT_BASEPATH=/satdat/curr/RapidScat 
    #
    my_RSCAT_BASEPATH=infromlinux
    #
    #-----------------
    if my_RSCAT_BASEPATH== '':
        my_RSCAT_BASEPATH='/satdat/curr/RapidScat'
        #
    #----------------------------------------------------------------
    #
    infromlinux = commands.getoutput('echo ${KNMI_BASEPATH}')    ### KNMI_BASEPATH=$RSCAT_BASEPATH/KNMI
    #                                                            ### KNMI_BASEPATH=/satdat/curr/RapidScat/KNMI
    #
    my_KNMI_BASEPATH=infromlinux
    #
    #-----------------
    if my_KNMI_BASEPATH== '':
        my_KNMI_BASEPATH='/satdat/curr/RapidScat/KNMI'
        #
    #----------------------------------------------------------------
    #
    system_design8r='alpha'
    system_design8r='curr'
    #system_design8r='mccronep'
    #
    graphicpath='/satdat/'+system_design8r+'/RapidScat/KNMI/graphic/'
    graphicpath=my_KNMI_BASEPATH+'/graphic/'
    #
    ascii_path='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii/'
    ascii_path=my_KNMI_BASEPATH+'/ascii/'
    #
    ascii_path_orig='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii/'
    ascii_path_orig=my_KNMI_BASEPATH+'/ascii/'
    #
    ascii_path_temp='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_temp/'
    ascii_path_temp=my_KNMI_BASEPATH+'/ascii_temp/'
    #
    ascii_path_aa='/u/alpha/etc/dynamic/obs_data/met/cqc/rscat/'
    ascii_path_aa='/satdat/curr/RapidScat/KNMI/ascii_aa'
    #ascii_path_aa='/gpfs/alpha/alpha/NRL/transfer/outgoing/'
    #
    ascii_path_bb='/u/beta/etc/dynamic/obs_data/met/cqc/rscat/'
    #
    ascii_path_oo='/u/ops/etc/dynamic/obs_data/met/cqc/rscat/'
    #
    #----------------------------------------------------------------
    if thehost == "a4bu":
        ascii_path_aa='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_aa/'
        ascii_path_bb='/u/beta/etc/dynamic/obs_data/met/cqc/rscat/'
        ascii_path_oo='/u/ops/etc/dynamic/obs_data/met/cqc/rscat/'
        #
    #----------------------------------------------------------------
    if thehost == "a4ou":
        ascii_path_aa='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_aa/'
        ascii_path_bb='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_bb/'
        ascii_path_oo='/u/ops/etc/dynamic/obs_data/met/cqc/rscat/'
        #
    #----------------------------------------------------------------
    #
    ascii_path_isis='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_2_isis/'
    ascii_path_isis=my_KNMI_BASEPATH+'/ascii_2_isis/'
    #
    ascii_path=ascii_path_temp
    #
    #.....................................................................--------------------
    # NOTE regarding the -ascii_path- variables: 
    # DPS will pick up the ascii file from -ascii_path_orig-.
    # But if we originate the file there [...write the data to the file there...], 
    # it is possible that DPS will pick up the file BEFORE we are done writing to it.
    # To avoid this, we will write the original data file to -ascii_path_temp-.
    # We start writing the file to the ascii_temp location then 
    # move the file to the -orig- location. 
    #  
    # We will use the variable -ascii_path- as a value that can change depending on our needs.
    # Regarding -ascii_path_aa bb and oo: These are locations where FNMOC modellers want the
    # data files copied to...
    #......................................................................--------------------
    #
    ###datapath='/satdat/'+system_design8r+'/RapidScat/nrt/NETCDF/'
    ###datapath='/satdat/'+system_design8r+'/rscat_wind/'
    datapath='/satdat/'+system_design8r+'/rscat_knmi/'
    datapath=my_XFER_BASEPATH+'/'
    #
    # aaa
    #
    ##binpath='/home/satops/mccrone/python/src/RapidScat/'
    ##binpath='/home/satops/mccrone/python/src/RapidScat/KNMI/'
    binpath='/satdat/bin/'
    binpath=my_OPSBIN+'/'
    #
    #utilpath=binpath+'util/'
    utilpath='/satdat/'+system_design8r+'/RapidScat/KNMI/Nutil/'
    utilpath=my_KNMI_BASEPATH+'/Nutil/'
    #
    #
    #procpath=binpath+'processed/'
    procpath='/satdat/'+system_design8r+'/RapidScat/KNMI/Nprocessed/'
    procpath=my_KNMI_BASEPATH+'/Nprocessed/'
    #
    #----------------------------------------------------------------------------
    # Determine the file that will be processed:
    #     The most recent NETCDF file from NASA will be processed.
    #     This section just assigns inital values to the variables.
    #     Later on we will auto-detect the most recent file.
    #----------------------------------------------------------------------------
    #
    file_name='ORIG.72274.KTUS.Tucson.Observations.at.12Z.03.Jan.2015.txt'
    file_name='rs_l2b_v1_02009_201501301356.nc'
    file_name='rs_l2b_v1_02010_201501301525.nc'
    file_name='rapid_20150814_172503_iss____05058_2hr_o_250_1903_ovw_l2.nc'
    file_name='rapid_20150814_172506_iss____05058_2hr_o_500_1903_ovw_l2.nc'
    #
    #
    nc_filename=datapath+file_name
    #---------------------------------
    #
    #
    print(dadots)
    #
    #
    ###Remember the newline character in Python is the string ’\n’.
    #
    newline_character="\n"
    #
    #----------------------------------------------------
    #....................................................
    #----------------------------------------------------
    #
    #----------------------------------------------------------------
    # Let me know if each of the paths are valid.
    #----------------------------------------------------------------
    #
    # Check procpath
    #
    valid_proc_path=OS.path.exists(procpath)
    #
    if valid_proc_path:
        print(dadash)
        print("The procpath is: "+procpath)
        print("The procpath is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The procpath is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    # Check utilpath
    #
    valid_util_path=OS.path.exists(utilpath)
    #
    if valid_util_path:
        print(dadash)
        print("The datapath is: "+utilpath)
        print("The datapath is VALID and EXISTS")
        print(dadash)
        #
    else:

        #
        this_execution=90
        print("-------The utilpath is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    # Check binpath
    #
    valid_bin_path=OS.path.exists(binpath)
    #
    if valid_bin_path:
        print(dadash)
        print("The datapath is: "+binpath)
        print("The datapath is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The binpath is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    # Check datapath
    #
    valid_data_path=OS.path.exists(datapath)

    if valid_data_path:
        print(dadash)
        print("The datapath is: "+datapath)
        print("The datapath is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The datapath is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    # Check graphicpath
    #
    valid_graphic_path=OS.path.exists(graphicpath)

    if valid_graphic_path:
        print(dadash)
        print("The graphicpath is: "+graphicpath)
        print("The graphicpath is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The graphicpath is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #
    # Check ascii_path
    #
    valid_ascii_path=OS.path.exists(ascii_path)

    if valid_ascii_path:
        print(dadash)
        print("The ascii_path is: "+ascii_path)
        print("The ascii_path is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------

    #=============================================================================================
    #
    # Check ascii_path_isis
    #python ./rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py >> TEST_20150902_A
    valid_ascii_path_isis=OS.path.exists(ascii_path_isis)

    if valid_ascii_path_isis:
        print(dadash)
        print("The ascii_path_isis is: "+ascii_path_isis)
        print("The ascii_path_isis is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path_isis is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    # Check ascii_path_orig
    #
    valid_ascii_path_orig=OS.path.exists(ascii_path_orig)

    if valid_ascii_path_orig:
        print(dadash)
        print("The ascii_path_orig is: "+ascii_path_orig)
        print("The ascii_path_orig is VALID and EXISTS")
        print(dadash)
        #
    else:
        #

        this_execution=90
        print("-------The ascii_path_orig is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    # Check ascii_path_temp
    #
    valid_ascii_path_temp=OS.path.exists(ascii_path_temp)

    if valid_ascii_path_temp:
        print(dadash)
        print("The ascii_path_temp is: "+ascii_path_temp)
        print("The ascii_path_temp is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path_temp is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    # Check ascii_path_aa
    #
    valid_ascii_path_aa=OS.path.exists(ascii_path_aa)
    #
    if valid_ascii_path_aa:
        print(dadash)
        print("The ascii_path_aa is: "+ascii_path_aa)
        print("The ascii_path_aa is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path_aa is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    # Check ascii_path_bb
    #
    valid_ascii_path_bb=OS.path.exists(ascii_path_bb)

    if valid_ascii_path_bb:
        print(dadash)
        print("The ascii_path_bb is: "+ascii_path_bb)
        print("The ascii_path_bb is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path_bb is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    # Check ascii_path_oo
    #
    valid_ascii_path_oo=OS.path.exists(ascii_path_oo)

    if valid_ascii_path_oo:
        print(dadash)
        print("The ascii_path_oo is: "+ascii_path_oo)
        print("The ascii_path_oo is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        this_execution=90
        print("-------The ascii_path_oo is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    #=============================================================================================
    #
    #
    # Added PJMC 20150331
    #
    #-------------------------------------------------------
    # This section determines:
    #	-1- Are there any NETCDF files in datadir?
    #       --- *.ncpython ./rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py >> TEST_20150902_A
    #	-2- Are there any Gziped NETCDF files in datadir?
    #       --- *.nc.gz
    #
    # If there are any *.nc.gz files, we will gunzip them.
    #
    # If there are any *.nc files, we will execute.
    # If there are no files at all, we will terminate.
    #-----------------------------------------------------
    ls_data_files=OS.listdir(datapath)
    #
    num_ls_data_files=len(ls_data_files)
    #
    if num_ls_data_files==0:
        #
        this_execution=55
        print("-------There are no NETCDF files to process-- End Execution! Disregard any other error msgs-----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------        
    #-------------------------------------------------------
    #	-1- Are there any NETCDF files in datadir?
    #	-2- Are there any Gziped NETCDF files in datadir?
    #
    # nc_file_find_flag -AND- ncgz_file_find_flag are to be used
    # to keep track of any detections of .nc and-or .nc.gz files.
    #--------------------------------------------------------------
    nc_file_find_flag=0
    #
    ncgz_file_find_flag=0
    #
    ncgz_file_find_flag=0
    #
    for i in ls_data_files:
        #
        #-print(i)
        #-----------------------------------------------------------
        analyze_File_STR=i
        nctest1=analyze_File_STR.find('.nc', 0,len(analyze_File_STR))
        if (nctest1 != -1) and (nctest1 > 0):
            nc_file_find_flag=1
            #
            #----------------------
            # End of if block----
            #----------------------
        nctest2=analyze_File_STR.find('.nc.gz', 0,len(analyze_File_STR))
        if (nctest2 != -1) and (nctest2 > 0):
            ncgz_file_find_flag=1
            #
            #----------------------
            # End of if block----
            #----------------------
        #-----------------------------------------------------------
        # End of for block [for i in ls_data_files]
        #-----------------------------------------------------        
    #-----------------------------------------------------------
    #
    if ncgz_file_find_flag == 1:
        the_gunzip_file=OS.system('gunzip '+datapath+'rapid_*.nc.gz')
        #the_gunzip_file=OS.system('gunzip '+datapath+'rs_l2b_*.nc.gz')
        #python ./rscat_knmi_convert_rscat_ncdf_2_qscat_ASCII.py >> TEST_20150902_A
        #----------------------
        # End of if block----
        #----------------------
    if (nc_file_find_flag == 0) and (ncgz_file_find_flag == 0):
        #

        #this_execution=0
        this_execution=55
        print("----There are no NETCDF files to process-- End Execution! ------")
        return this_execution
        #
        #----------------------
        # End of if block----
        #----------------------
    #
    # Added PJMC 20150331
    #
    #----------------------------------------------------------------

    #
    #----------------------------------------------------------------
    # Determine the NETCDF file that will be processed.
    #----------------------------------------------------------------
    # Determine the file that will be processed:
    #     The most recent NETCDF file from NASA will be processed.
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #
    list_of_ncdf_files=utilpath+"ncdf_file_list.txt"
    templist_of_ncdf_files=utilpath+"ncdf_file_list.txt.temp"
    the_ncdf_files=OS.system('rm -rf '+list_of_ncdf_files)
    the_ncdf_files=OS.system('rm -rf '+templist_of_ncdf_files)
    the_ncdf_files=OS.system('ls -1 '+datapath+'rapid_*.nc > '+templist_of_ncdf_files)
    the_ncdf_files=OS.system('tail -1 '+templist_of_ncdf_files+' > '+list_of_ncdf_files)
    the_ncdf_files=OS.system('chmod 776 '+templist_of_ncdf_files)
    the_ncdf_files=OS.system('chmod 776 '+list_of_ncdf_files)
    #
    #----------------------------------------------------------------
    # 
    #----------------------------------------------------------------
    #
    list_file_handle=open(list_of_ncdf_files,"r")
    dataline=list_file_handle.read()
    print("dataline is: "+dataline)
    list_file_handle.close()
    #
    # This line strips the -new-line- character from the end of dataline
    #
    nc_filename=dataline[:-1]

    #
    #----------------------------------------------------------------
    # The paths are valid if you make it to this point.
    # NOW Let me know if the NETCDF file exists.
    #----------------------------------------------------------------
    #
    # Check nc_filename
    #
    valid_NCF_file=OS.path.isfile(nc_filename)

    if valid_NCF_file:
        print(dadash)
        print("The nc_filename is: "+nc_filename)
        print("The nc_filename EXISTS")
        print(dadash)
        #
    else:
        #
        #this_execution=0
        this_execution=55
        print("The nc_filename is supposed to be: "+nc_filename)
        print("-------The nc_filename does not EXIST! NEED TO CHECK THIS!!!!!!!! -----------------")
        return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #  
    #----------------------------------------------------
    #....................................................
    #----------------------------------------------------
    #
    length_nc_filename=len(nc_filename)
    length_datapath=len(datapath)
    only_the_nc_filename=nc_filename[length_datapath:]
    #rev_number=only_the_nc_filename[10:15]
    #rev_number=only_the_nc_filename[12:17]
    rev_number=only_the_nc_filename[29:34]
    #
    #
    print(dadash)
    print("Rev-Number:--->"+str(rev_number))
    print(dadash)
    #
    #  
    #----------------------------------------------------
    #....................................................
    #----------------------------------------------------
    #
    print(dadash)
    print("-------Reading  File -----------------")
    print(dadash)
    #
    #
    #----------------------------------------------------
    #
    fileobj = NCF.Dataset(nc_filename, mode='r')
    print(dadots)
    print(dadots)
    print("Title")
    print(fileobj.title)
    print(dadots)
    print(dadots)
    print("Dimensions")
    print(fileobj.dimensions)
    print(dadots)
    print(dadots)
    #
    print(dadash+dadash+dadash+dadash)
    print(dadash+dadash+dadash+dadash)
    print("Variables")
    print(dadash+dadash+dadash+dadash)
    print(fileobj.variables)
    print(dadash+dadash+dadash+dadash)
    print(dadash+dadash+dadash+dadash)
    print(dadash+dadash+dadash+dadash)
    #
    ###data = fileobj.variables['u'][:]
    #
    datawspd = fileobj.variables['wind_speed'][:]
    print(dadots)
    print(dadots)
    print("Datawspd Shape")
    print(N.shape(datawspd))
    ###ascii
    #
    datawdir = fileobj.variables['wind_dir'][:]
    print(dadots)
    print(dadots)
    print("DataWdir Shape")
    print(N.shape(datawdir))
    #
    datalat= fileobj.variables['lat'][:]
    print(dadots)
    print(dadots)
    print("DataLat Shape")
    print(N.shape(datalat))
    #
    datalon = fileobj.variables['lon'][:]
    print(dadots)
    print(dadots)
    print("DataLon Shape")
    print(N.shape(datalon))
    #
    datatim = fileobj.variables['time'][:]
    print(dadots)
    print(dadots)
    print("DataTim Shape")
    print(N.shape(datatim))
    print(dadots)
    print(dadots)
    #
    datawvci = fileobj.variables['wvc_index'][:]
    print("Datawvci Shape")
    print(N.shape(datawvci))
    print(dadots)
    print(dadots)
    #
    datamdlspd = fileobj.variables['model_speed'][:]
    print("Datamdlspd Shape")
    print(N.shape(datamdlspd))
    print(dadots)
    print(dadots)
    #
    datamdldir = fileobj.variables['model_dir'][:]
    print("Datamdldir Shape")
    print(N.shape(datamdldir))
    print(dadots)
    print(dadots)
    #
    dataiceprb = fileobj.variables['ice_prob'][:]
    print("Dataiceprb Shape")
    print(N.shape(dataiceprb))
    print(dadots)
    print(dadots)
    #
    dataiceage = fileobj.variables['ice_age'][:]
    print("Dataiceage Shape")
    print(N.shape(dataiceage))
    print(dadots)
    print(dadots)
    #
    datawvcqfl = fileobj.variables['wvc_quality_flag'][:]
    print("Datawvcqfl Shape")
    print(N.shape(datawvcqfl))
    print(dadots)
    print(dadots)
    #
    databsdst = fileobj.variables['bs_distance'][:]
    print("Databsdst Shape")
    print(N.shape(databsdst))
    print(dadots)
    print(dadots)
    #
    #=====================================================================
    #
    #datarain_impact = fileobj.variables['rain_impact'][:]
    print(dadots)
    #dataflags = fileobj.variables['flags'][:]
    print(dadots)
    #dataeflags = fileobj.variables['eflags'][:]
    print(dadots)
    #data_ndg_wndspd = fileobj.variables['nudge_wind_speed'][:]
    print(dadots)
    #data_ndg_wnddir = fileobj.variables['nudge_wind_direction'][:]
    print(dadots)
    #data_rtr_wspd_uncor = fileobj.variables['retrieved_wind_speed_uncorrected'][:]
    print(dadots)
    #data_xtrk_wspd_bias = fileobj.variables['cross_track_wind_speed_bias'][:]
    print(dadots)
    #data_atm_spd_bias = fileobj.variables['atmospheric_speed_bias'][:]
    print(dadots)
    #data_num_ambig = fileobj.variables['num_ambiguities'][:]
    #data_wind_obj = fileobj.variables['wind_obj'][:]
    print(dadots)
    #
    #data_ambig_spd = fileobj.variables['ambiguity_speed'][:]
    print(dadots)
    #data_ambig_dir = fileobj.variables['ambiguity_direction'][:]
    print(dadots)
    #data_ambig_obj = fileobj.variables['ambiguity_obj'][:]
    print(dadots)
    #data_num_infore = fileobj.variables['number_in_fore'][:]
    print(dadots)
    #data_num_inaft = fileobj.variables['number_in_aft'][:]
    #print(dadots)
    #data_num_outfore = fileobj.variables['number_out_fore'][:]
    #print(dadots)
    #data_num_outaft = fileobj.variables['number_out_aft'][:]
    #print(dadots)
    #
    #=====================================================================
    #
    #3#print(dadots)
    #3#print(dadots)
    #3#print("The datatim [-time-] value -1- is:")
    #3#print("-----------------------")
    #3#print(str(datatim[1]))
    #3#print("-----------------------")
    #3#print("The datatim [-time-] value -300--10- is:")
    #3#print("-----------------------")
    #3#print(str(datatim[300,10]))
    #3#print("-----------------------")
    #3#print(dadots)
    #3##
    #3#print(dadots)
    #3#print("The datawspd [-time-] value -1- is:")
    #3#print("-----------------------")
    #3#print(str(datawspd[1]))
    #3#print("-----------------------")
    #3#print("The datawspd [-time-] value -300--10- is:")
    #3#print("-----------------------")
    #3#print(str(datawspd[300,10]))
    #3#print("-----------------------")
    #3#print(dadots)
    #3##
    #3#print(dadots)
    #3#print("The datawdir [-time-] value -1- is:")
    #3#print("-----------------------")
    #3#print(str(datawdir[1]))
    #3#print("-----------------------")
    #3#print("The datawdir [-time-] value -300- is:")
    #3#print("-----------------------")
    #3#print(str(datawdir[300]))
    #3#print("-----------------------")
    #3#print(dadots)
    #3##
    #3#print(dadots)
    #3#print("The datalat [-time-] value -1- is:")
    #3#print("-----------------------")
    #3#print(str(datalat[1]))
    #3#print("-----------------------")
    #3#print("The datalat [-time-] value -300- is:")
    #3#print("-----------------------")
    #3#print(str(datalat[300]))
    #3#print("-----------------------")
    #3#print(dadots)
    #3##
    #3#print(dadots)
    #3#print("The datalon [-time-] value -1- is:")
    #3#print("-----------------------")
    #3#print(str(datalon[1]))
    #3#print("-----------------------")
    #3#print("The datalon [-time-] value -300- is:")
    #3#print("-----------------------")
    #3#print(str(datalon[300]))
    #3#print("-----------------------")
    #3#print(dadots)
    #3##
    #
    #=====================================================================
    #
    # Typical values of datatim----
    # The datatim [-time-] value -1- is:
    #-----------------------
    #[-- -- -- -- 808421113 808421113 808421113 808421113 808421113 808421113
    # 808421113 808421113 808421113 808421113 808421113 808421113 -- -- -- -- --]
    #-----------------------
    #The datatim [-time-] value -300- is:
    #-----------------------
    #[808423157 808423157 808423157 808423157 808423157 808423157 808423157
    # 808423157 808423157 808423157 808423157 808423157 808423157 808423157
    # 808423157 808423157 808423157 808423157 808423157 808423157 --]
    #-----------------------
    #
    #=====================================================================
    #
    #
    #
    #
    #-------------------------------------------------------------
    #
    # Determine the size of the wind_Speed array
    #
    #------------------------------------------------------------
    #
    shape_wspd = N.shape(datawspd)
    print(" \n")
    print(dadash)
    print("Wind Speed i component dimension: "+str(shape_wspd[0]))
    print("Wind Speed j component dimension: "+str(shape_wspd[1]))
    print(dadash)
    #
    print(" \n")
    #
    #
    #----------------------------------------------------
    # Since we processed this file, lets note this in the 
    # -procdata- subdirectory.
    #----------------------------------------------------
    #
    ###asciifilenamea = Print_Current_Time(right_now)
    asciifilenamea = Access_Current_Time(right_now)
    ascii_file_name_a = asciifilenamea+".knmi.ascii.txt"
    ascii_file_name=ascii_path+ascii_file_name_a
    the_ascii_files=OS.system('touch '+ascii_file_name)
    the_ascii_files=OS.system('chmod 776 '+ascii_file_name)
    the_ascii_files=OS.system('echo --- > '+ascii_file_name)
    #
    print("The ASCII file name is:")
    print("-----------------------")
    print(ascii_file_name)
    print("-----------------------")
    #
    writefileobj = open(ascii_file_name, "w")
    #
    #-------------------------------------------------------------
    # Now print out the data elements one by one:
    #
    # TIME, LAT, LONG, Wind_Speed, Wind_direction, Rain_Impact
    #------------------------------------------------------------
    #
    print(dadash)
    print(dadash+dadash)
    print(dadash)
    print("RAPIDSCAT WIND DATA IN ASCII FORMAT")
    print(dadash)
    print("TIME-------------------------LAT-------LONG------Wind_Spd--Wind_dir--Rain_Impact")
    print(dadash+dadash)
    print(" \n")
    #
    wspc=" , "
    wspc="[]"
    wdot="!!"
    wblk=""
    MINUS99="-99"
    DBLDASH="--"
    DASH="-"
    ZZERO="0"
    STR_TIME_INPUT=0.0
    STR_ORIG_TIME='0.0'
    #
    FACTOR48=2.0*24.0*60.0*60.0
    #
    ###FACTOR48=1.0*24.0*60.0*60.0
    #
    #
    #--------------------------------------------------------
    #Begin nested loop for printing out the data elements
    #--------------------------------------------------------
    #
    for i in xrange(shape_wspd[0]):
        for j in xrange(shape_wspd[1]):
            #
            STR_TIME=str(datatim[i,j])
            STR_ORIG_TIME=str(datatim[i,j])
            ORIG_TIME=datatim[i,j]
            #
            STR_TIME_INPUT=FACTOR48+datatim[i,j]
            #
	    #STR_TIME=Get_Converted_Time(STR_TIME_INPUT)
	    STR_TIME=Get_Converted_Time90(STR_TIME_INPUT)
            #print('STR_TIME IS: --- > '+STR_TIME)
            #
            #STR_TIME="20150129-0008.28.530-UTC-"
            M2M=STR_TIME[4:6]
            D2D=STR_TIME[6:8]
            H2H=STR_TIME[9:11]
            N2N=STR_TIME[11:13]
            #
            NEW_STR_TIME=M2M+D2D+H2H+N2N
            #print('NEW_STR_TIME IS: --- > '+NEW_STR_TIME)
            #
            STR_LAT_A=datalat[i,j]
            STR_LAT_X100=STR_LAT_A*100.0
            STR_LAT_X100C=str(STR_LAT_X100)
            STR_LAT=str(datalat[i,j])
            #
            #----------------------------------------------------------------
	    # If the Latitude is less than 0, then just convert, otherwise,
	    # PAD A SPACE CHARACTER in front of the latitude.
	    #----------------------------------------------------------------
            #
	    if (STR_LAT_A >= 0.0) and (STR_LAT_A < 0.1):
		#
                STR_LAT=STR_2_SPACE_CHAR+"00"+STR_LAT_X100C[0:1]
	        #
            elif (STR_LAT_A > -0.1) and (STR_LAT_A < 0.0):
		#
                STR_LAT=DASH+STR_1_SPACE_CHAR+(ZZERO*2)+STR_LAT_X100C[1:2]
	        #
            elif (STR_LAT_A >= 0.1) and (STR_LAT_A < 1.0):
		#
                STR_LAT=STR_1_SPACE_CHAR+"0"+STR_LAT_X100C[0:2]
	        #
            elif (STR_LAT_A >= 1.0) and (STR_LAT_A < 10.0):
		#
                STR_LAT="  "+STR_LAT_X100C[0:3]
	        #
            elif (STR_LAT_A >= 10.0) and (STR_LAT_A < 89.9):
		#
                STR_LAT=STR_1_SPACE_CHAR+STR_LAT_X100C[0:4]
	        #
            elif (STR_LAT_A >= -89.9) and (STR_LAT_A < -10.0):
		#
                STR_LAT=DASH+STR_LAT_X100C[1:5]
	        #
            elif (STR_LAT_A > -10.0) and (STR_LAT_A <= -1.0):
		#
                STR_LAT=DASH+STR_1_SPACE_CHAR+STR_LAT_X100C[1:4]
	        #
            elif (STR_LAT_A > -1.0) and (STR_LAT_A <= -0.1):
		#
                STR_LAT=DASH+STR_1_SPACE_CHAR+ZZERO+STR_LAT_X100C[1:3]
	        #
            elif (STR_LAT_A >= -0.01) and (STR_LAT_A <= 0.01):
		#
                STR_LAT=STR_1_SPACE_CHAR+(ZZERO*4)
	        #
            elif STR_LAT_A <= -90.0:
		#
                STR_LAT=STR_2_SPACE_CHAR+MINUS99
	        #
            elif STR_LAT_A >= 90.0:
		#
                STR_LAT=STR_2_SPACE_CHAR+MINUS99
	        #
	    else:
	        #
                STR_LAT=STR_1_SPACE_CHAR+STR_LAT_X100C[0:4]
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
                #
	    if (STR_LAT_A >= 1.0) and (STR_LAT_A < 10.0):
		#
                STR_LAT='+ '+STR_LAT_X100C[0:3]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
                #
	    if (STR_LAT_A >= 0.1) and (STR_LAT_A < 1.0):
		#
                STR_LAT='+ 0'+STR_LAT_X100C[0:2]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
                #
	    if (STR_LAT_A >= 0.0) and (STR_LAT_A < 0.1):
		#
                STR_LAT='+ 00'+STR_LAT_X100C[0:1]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #
            #
            #----------------------------------------------------------------#
	    # This part determines the longitude of the WVC.                 #
            # This is an -easting- longitude                                 #
            # [That means it goes from 0 to 360 east]                        #
            # [ ---000 to 180 is as per the normal east longitude]           #
            # [ ---181 to 360 is the same as the intl date line to the       #
            #                 prime meridian going east thru the Americas]   #
            # [    In other words 175 West Longitude = 185 East]             #
            # You need to multiply the longitude by 100.0                    #
	    # The end result is only FIVE characters long.                   #
	    # So 185.34 degrees east longitude becomes "18534"               #
	    #-----------------------------------------Title

            #
            STR_LON_A=datalon[i,j]
            STR_LON_B=str(datalon[i,j])
            STR_LON_X100=STR_LON_A*100.0
            STR_LON_X100C=str(STR_LON_X100)
            STR_LON=STR_LON_X100C[0:5]
            #
            #----------------------------------------------------------------#
	    # Careful-- if the longitude is less than 100, you need to watch #
	    # for missing characters.                                        #
	    #----------------------------------------------------------------#
            #
	    if (STR_LON_A >= 100.0) and (STR_LON_A < 360.0):
		#
                STR_LON=STR_LON_X100C[0:5]
                #
	    if (STR_LON_A >= 10.0) and (STR_LON_A < 100.0):
		#
                STR_LON=STR_1_SPACE_CHAR+STR_LON_X100C[0:4]
	        #
            if (STR_LON_A >= 1.0) and (STR_LON_A < 10.0):
	        #
                STR_LON='+0'+STR_LON_X100C[0:3]
	        #
            if (STR_LON_A >= 0.1) and (STR_LON_A < 1.0):
	        #
                STR_LON='+00'+STR_LON_X100C[0:2]
	        #
            if (STR_LON_A >= 0.01) and (STR_LON_A < 0.1):
	        #
                STR_LON='+000'+STR_LON_X100C[0:1]
	        #
            if STR_LON_A < 0.0:
	        #
                STR_LON=STR_2_SPACE_CHAR+MINUS99
	        #
	        #
            if STR_LON_A == 0.0:
	        #
                STR_LON='00000'
	        #
            if STR_LON_A >= 360.0:
	        #
                STR_LON=STR_2_SPACE_CHAR+MINUS99
	        #
	    #else:
	        #
            #    STR_LON=STR_LON_X100C[0:6]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
	    #
	    #-----------------------------
	    #
            STR_WSP_A=datawspd[i,j]
            STR_WSP_B=str(datawspd[i,j])
            STR_WSP_X10=STR_WSP_A*10.0
            STR_WSP_X10C=str(STR_WSP_X10)
            STR_WSP=STR_WSP_X10C[0:3]
            #
            if MATH.isnan(STR_WSP_A):
                STR_WSP=MINUS99
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #
            #----------------------------------------------------------------
	    # If the Wind Speed is less than 0, then use -99, otherwise,
	    # take the first three characters.
	    #----------------------------------------------------------------
	    if STR_WSP_A < 0.0:
		#
                STR_WSP=MINUS99
	        #
            elif STR_WSP_B == DBLDASH:
	        #
                STR_WSP=MINUS99
	        #
	    else:
	        #
                STR_WSP=STR_WSP_X10C[0:3]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
	    if (STR_WSP_A >= 10.0) and (STR_WSP_A < 100.0):
                STR_WSP=STR_WSP_X10C[0:3]
                #
            #
	    if (STR_WSP_A >= 1.0) and (STR_WSP_A < 10.0):
                STR_WSP='+'+STR_WSP_X10C[0:2]
                #
            #
	    if (STR_WSP_A >= 0.1) and (STR_WSP_A < 1.0):
                STR_WSP='+0'+STR_WSP_X10C[0:1]
                #
            #
	    if (STR_WSP_A >= 0.0) and (STR_WSP_A < 0.1):
                STR_WSP='000'
                #
            #
            #QWERTYUIOP.ASDFGHJKL.ZXCVBNM=
            #
            #
	    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==
            # IMPORTANT CHANGE: PJMC Sept 24 2015.
            # - - - - - - - - - - - - - - - - - - -
	    # Dr. Randy Pauley discovered that KNMI WINDS are stated in 
            # OCEANOGRAPHIC DIRECTIONS, NOT METEOROLOGICAL DIRECTIONS.
            # This means the directions are exactly 180 degrees out from
            # the value that is needed for NWP processing. 
            # So, for example, a SouthWest wind -225 degrees- in meteorological
            # data is stated as -045 degrees- in the KNMI file. 
            #
            # So, our approach will be to ADD 180 to our wind directions UNLESS
            # the Wind direction is 180 or more, in which we will SUBTRACT 180
            # from our wind directions.
            #
	    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==
            #
            #
	    #
            STR_WDR_A=datawdir[i,j]
            #
            STR_WDR_TEMP=STR_WDR_A+180.0
            #
	    if STR_WDR_A >= 180.0:
		#
                STR_WDR_TEMP=STR_WDR_A-180.0
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            STR_WDR_A=STR_WDR_TEMP
            #
            STR_WDR_B=str(datawdir[i,j])
            STR_WDR_X1=STR_WDR_A*1.0
            STR_WDR_X1C=str(STR_WDR_X1)
            STR_WDR=STR_WDR_X1C[0:3]
            #
            if MATH.isnan(STR_WDR_A):
                STR_WDR=MINUS99
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #----------------------------------------------------------------
	    # If the Wind direction is less than 0, then use -99, otherwise,
	    # take the first three characters.
	    #----------------------------------------------------------------
	    if STR_WDR_A < 0.0:
		#
                STR_WDR=MINUS99
	        #
            elif MATH.isnan(STR_WDR_A):
	        #
                STR_WDR=MINUS99
	        #
            elif STR_WDR_B == DBLDASH:
	        #
                STR_WDR=MINUS99
	        #
	    else:
                #
	        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                # NESTED IF BLOCK 
	        # If the Wind direction is less than 100, then pad a zero up front, otherwise,
	        # take the first three characters.
	        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                #
	        if (STR_WDR_A >= 10.0) and (STR_WDR_A < 100.0):
                    STR_WDR='0'+STR_WDR_X1C[0:2]
                    #
	        if (STR_WDR_A >= 1.0) and (STR_WDR_A < 10.0):
                    STR_WDR='00'+STR_WDR_X1C[0:1]
                    #
	        if (STR_WDR_A >= 0.1) and (STR_WDR_A < 1.0):
                    STR_WDR='000'
                    #
	        if (STR_WDR_A >= 0.0) and (STR_WDR_A < 0.1):
                    STR_WDR='000'
                    #
	        #if datawdir[i,j] < 100.0:
                #    ###STR_WDR="0"+str(datawdir[i,j])
                #    STR_WDR="0"+STR_WDR_X1C[0:2]
	        #
	        #else:
	        ##
                #    STR_WDR=STR_WDR_X1C[0:3]
	        #   #	        
                    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	            # End of NESTED IF block
	            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #
            #STR_RAIN=str(datarain_impact[i,j])
            #------------------------------------
            #
            #------------------------------------
            #STR_FLAGS=str(dataflags[i,j])
            #STR_EFLAGS=str(dataeflags[i,j])
            #------------------------------------
            # datamdlspd replaces data_ndg_wndspd
            # - - - - - - - - - - - - - - - - - -
            #STR_ND_WSPD=str(data_ndg_wndspd[i,j])
            #STR_NCEP_WSPD_A=data_ndg_wndspd[i,j]
            #STR_NCEP_WSPD_B=str(data_ndg_wndspd[i,j])
            STR_ND_WSPD=str(datamdlspd[i,j])
            STR_NCEP_WSPD_A=datamdlspd[i,j]
            STR_NCEP_WSPD_B=str(datamdlspd[i,j])
            STR_NCEP_WSPD_X10=STR_NCEP_WSPD_A*10.0
            STR_NCEP_WSPD_X10C=str(STR_NCEP_WSPD_X10)
            STR_NCEP_WSPD=STR_NCEP_WSPD_X10C[0:3]
            #
            #----------------------------------------------------------------
	    # If the Wind Speed is less than 0, then use -99, otherwise,
	    # take the first three characters.
	    #----------------------------------------------------------------
            #
            data_NCEP_netcdf=STR_NCEP_WSPD_A
	    STR_NCEP_WSPD=Determine_Wind_SPEED(data_NCEP_netcdf)
            #

	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #------------------------------------
            #------------------------------------
            # datamdldir replaces data_ndg_wnddir
            # - - - - - - - - - - - - - - - - - -
            STR_ND_WDIR=str(datamdldir[i,j])
            STR_NCEP_WDIR_A=datamdldir[i,j]
            STR_NCEP_WDIR_B=str(datamdldir[i,j])
            STR_NCEP_WDIR_X1=STR_NCEP_WDIR_A*1.0
            STR_NCEP_WDIR_X1C=str(STR_NCEP_WDIR_X1)
            STR_NCEP_WDIR=STR_NCEP_WDIR_X1C[0:3]
            #
            #----------------------------------------------------------------
	    # If the Wind direction is less than 0, then use -99, otherwise,
	    # take the first three characters.
	    #----------------------------------------------------------------
            data_NCEP_wdir=STR_NCEP_WDIR_A
            STR_NCEP_WDIR=Determine_Wind_Direction(data_NCEP_wdir)
            #
                #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #
            #MINUS99
            #
            STR_FNMOC2_WSPD=MINUS99
            STR_FNMOC2_WDIR=MINUS99
	    #
            #------------------------------------#------------------------------------#------------------------------------
	    # The Rev_Number was determined previously. Now we get Row and cell (I and J)
            #------------------------------------#------------------------------------#------------------------------------
	    #
            STR_REV_NUMBER=rev_number
            LEN_REV_NUMBER=len(rev_number)
            #
            #----------------------------------------------------------------
            # Begin IF Block for LEN_REV_NUMBER
	    #----------------------------------------------------------------
            #
	    if LEN_REV_NUMBER == 5:
		#
                STR_REV_NUMBER='0'+rev_number
	        #
            elif LEN_REV_NUMBER == 4:
	        #
                STR_REV_NUMBER='00'+rev_number
	        #
	    else:
	        #
                STR_REV_NUMBER=rev_number
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
	    #----------------------------------------------------------------
	    #
            #------------------------------------#------------------------------------#------------------------------------
	    # The Rev_Number was determined previously. Now we get Row and cell (I and J)
            #------------------------------------#------------------------------------#------------------------------------
	    #
            STR_ROW_A=i
            STR_CEL_A=j
            STR_ROW_B=str(i)
            STR_CEL_B=str(j)
            LEN_ROW_B=len(STR_ROW_B)
            LEN_CEL_B=len(STR_CEL_B)
            STR_ROW=str(i)
            STR_CEL=str(j)
            #
            #----------------------------------------------------------------
            # Begin IF Block for LEN_ROW_B - NO LARGER THAN 4 CHARACTERS
	    #----------------------------------------------------------------
            #
	    if LEN_ROW_B == 1:
		#
                #STR_ROW=STR_3_SPACE_CHAR+str(i)
                STR_ROW='000'+str(i)
	        #
            elif LEN_ROW_B == 2:
	        #
                #STR_ROW=STR_2_SPACE_CHAR+str(i)
                STR_ROW='00'+str(i)
	        #
            elif LEN_ROW_B == 3:
	        #
                STR_ROW='0'+str(i)
	        #
            elif LEN_ROW_B == 4:
	        #
                STR_ROW=str(i)
	        #
	    else:
	        #
                STR_ROW='9999'
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
	    #----------------------------------------------------------------
            #
            #----------------------------------------------------------------
            # Begin IF Block for LEN_CEL_B - NO LARGER THAN 3 CHARACTERS
	    #----------------------------------------------------------------
            #
	    if LEN_CEL_B == 1:
		#
                #STR_CEL=STR_3_SPACE_CHAR+str(j)
                STR_CEL='00'+str(j)
	        #
            elif LEN_CEL_B == 2:
	        #
                #STR_CEL=STR_2_SPACE_CHAR+str(j)
                STR_CEL='0'+str(j)
	        #
            elif LEN_CEL_B == 3:
	        #
                #STR_CEL=STR_1_SPACE_CHAR+str(j)
                STR_CEL=str(j)
	        #
	    else:
	        #
                STR_CEL='999'
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
	    #----------------------------------------------------------------
            TIME_TO_EDGE='-99-99'
	    #----------------------------------------------------------------
            #
            #STR_RAIN=str(datarain_impact[i,j])
            STR_RAIN=MINUS99

            #------------------------------------
            #
            #------------------------------------
            #STR_EFLAGS=str(dataeflags[i,j])
            STR_EFLAGS=MINUS99
            #------------------------------------datawvcqfl   dataflags
            #STR_FLAGS_A=dataflags[i,j]
            STR_FLAGS_A=datawvcqfl[i,j]
            STR_FLAGS_B=str(STR_FLAGS_A)
            LEN_FLAGS_B=len(STR_FLAGS_B)
            STR_WVC_FLAGS=str(STR_FLAGS_A)
            #
            #----------------------------------------------------------------
            # Begin IF Block for STR_FLAGS_A 
	    # NOTE:
	    # STR_WVC_FLAGS- must be NO LARGER THAN 6 CHARACTERS
	    #----------------------------------------------------------------
            #            
	    if MATH.isnan(STR_FLAGS_A):
		#
                #STR_CEL=STR_3_SPACE_CHAR+str(i)
                #STR_CEL='00'+str(i)
		STR_WVC_FLAGS='-99-99'
	        #
	    else:
	        #
                #STR_CEL='999'
                STR_FLAGS_INT=int(STR_FLAGS_A)
                #STR_FLAGS_B=str(STR_FLAGS_A)
                STR_FLAGS_B=str(STR_FLAGS_INT)
                LEN_FLAGS_B=len(STR_FLAGS_B)
                STR_WVC_FLAGS=str(STR_FLAGS_A)
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
	    #
            #------------------------------------
            #
            #----------------------------------------------------------------
            # Begin IF Block for LEN_FLAGS_B - NO LARGER THAN 6 CHARACTERS
	    #----------------------------------------------------------------
            #
	    if LEN_FLAGS_B == 1:
		#
                #STR_WVC_FLAGS=STR_5_SPACE_CHAR+STR_FLAGS_B
                STR_WVC_FLAGS='00000'+STR_FLAGS_B
	        #
            elif LEN_FLAGS_B == 2:
	        #
                #STR_WVC_FLAGS=STR_4_SPACE_CHAR+STR_FLAGS_B
                STR_WVC_FLAGS='0000'+STR_FLAGS_B
	        #
            elif LEN_FLAGS_B == 3:
	        #
                #STR_WVC_FLAGS=STR_3_SPACE_CHAR+STR_FLAGS_B
                STR_WVC_FLAGS='000'+STR_FLAGS_B
	        #
            elif LEN_FLAGS_B == 4:
	        #
                #STR_WVC_FLAGS=STR_2_SPACE_CHAR+STR_FLAGS_B
                STR_WVC_FLAGS='00'+STR_FLAGS_B
	        #
            elif LEN_FLAGS_B == 5:
	        #
                #STR_WVC_FLAGS=STR_1_SPACE_CHAR+STR_FLAGS_B
                STR_WVC_FLAGS='0'+STR_FLAGS_B
	        #
	    else:
	        #
                STR_WVC_FLAGS=STR_FLAGS_B[0:6]
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
	    #----------------------------------------------------------------
	    #
	    if MATH.isnan(STR_FLAGS_A):
		STR_WVC_FLAGS='-99-99'
	        #
	        #-----------------------------------------------------------
	        # End of if block
	        #-----------------------------------------------------------
            #------------------------------------#------------------------------------#------------------------------------
	    #
            #------------------------------------#------------------------------------#------------------------------------
	    #

            #------------------------------------
            #STR_R_WSPD_UC=str(data_rtr_wspd_uncor[i,j])
            #STR_XT_WSP_BI=str(data_xtrk_wspd_bias[i,j])
            #STR_A_SPD_BI=str(data_atm_spd_bias[i,j])
            STR_R_WSPD_UC=str(MINUS99)
            STR_XT_WSP_BI=str(MINUS99)
            STR_A_SPD_BI=str(MINUS99)

            #
            #STR_N_AMBIG=str(data_num_ambig[i,j])
            #STR_W_OBJ=str(data_wind_obj[i,j])
            STR_N_AMBIG=str(MINUS99)
            STR_W_OBJ=str(MINUS99)


            #########  8<     8<     8<  #########  8<     8<     8< #########  8<     8<     8<

            #--#<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<--------------------------
	    #--#	STR_AMBIG_SPD, STR_AMBIG_DIR, STR_AMBIG_OBJ
	    #--#   These parameters are actually arrays.	
            #--#<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<--------------------------
            #--#
	    #--# The wind_obj data field that is supposed to contain the likelihood value of the 
            #--# DIRTH wind vector is also not properly set. For now this field is filled with 
            #--# -Inf values. This will be corrected in a future release. Until that time, users 
            #--# interested in the likelihood values for the solution are encouraged to use the 
            #--# values for the 4 peaks of the likelihood function contained in the ambiguity_obj 
            #--# data field.
            #--#------------------------------------#------------------------------------#--------
            #--#
            #--#
            #--##STR_AMBIG_SPD=str(data_ambig_spd[i,j])
            #--##STR_AMBIG_DIR=str(data_ambig_dir[i,j])
            #--##STR_AMBIG_OBJ=str(data_ambig_obj[i,j])
            #--#-----------------------------------
            #--STR_AMBIG_SPD=data_ambig_spd[i,j]
            #--STR_AMBIG_DIR=data_ambig_dir[i,j]
            #--STR_AMBIG_OBJ=data_ambig_obj[i,j]
            #--#-----------------------------------
            #--#
            #--MAX_STR_AMBIG_OBJ=0
	    #--MAX_STR_AMBIG_OBJ=max(STR_AMBIG_OBJ)
            #--#
            #--#-----------------------------------
            #--#
            #--STR_AMBIG_SPD0=str(STR_AMBIG_SPD[0])
            #--STR_AMBIG_SPD1=str(STR_AMBIG_SPD[1])
            #--STR_AMBIG_SPD2=str(STR_AMBIG_SPD[2])
            #--STR_AMBIG_SPD3=str(STR_AMBIG_SPD[3])
            #--# - - - - - - - - - - - - - - - - - 
            #--STR_AMBIG_DIR0=str(STR_AMBIG_DIR[0])
            #--STR_AMBIG_DIR1=str(STR_AMBIG_DIR[1])
            #--STR_AMBIG_DIR2=str(STR_AMBIG_DIR[2])
            #--STR_AMBIG_DIR3=str(STR_AMBIG_DIR[3])
            #--# - - - - - - - - - - - - - - - - - 
            #--STR_AMBIG_OBJ0=str(STR_AMBIG_OBJ[0])
            #--STR_AMBIG_OBJ1=str(STR_AMBIG_OBJ[1])
            #--STR_AMBIG_OBJ2=str(STR_AMBIG_OBJ[2])
            #--STR_AMBIG_OBJ3=str(STR_AMBIG_OBJ[3])
            #--# - - - - - - - - - - - - - - - - - 
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--#
            #--STR_AMBIG_SPD0_A=STR_AMBIG_SPD[0]
            #--STR_AMBIG_DIR0_A=STR_AMBIG_DIR[0]
            #--STR_AMBIG_OBJ0_A=STR_AMBIG_OBJ[0]
            #--STR_AMBIG_SPD0_B=str(STR_AMBIG_SPD[0])
            #--STR_AMBIG_DIR0_B=str(STR_AMBIG_DIR[0])
            #--STR_AMBIG_OBJ0_B=str(STR_AMBIG_OBJ[0])
            #--#
            #--#
            #--data_from_netcdf=STR_AMBIG_SPD0_A
	    #--STR_AMBIG_SPD0_B=Determine_Wind_SPEED(data_from_netcdf)
            #--#
            #--data_from_file=STR_AMBIG_DIR0_A
            #--STR_AMBIG_DIR0_B=Determine_Wind_Direction(data_from_file)
            #--#
            #--datafromfile=STR_AMBIG_OBJ0_A
	    #--STR_AMBIG_OBJ0_B=Compute_MLE_STRNG(datafromfile,MAX_STR_AMBIG_OBJ)
	    #--#STR_AMBIG_OBJ0_B=Compute_MLE_STRNG(datafromfile)
            #--#
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--#
            #--STR_AMBIG_SPD1_A=STR_AMBIG_SPD[1]
            #--STR_AMBIG_DIR1_A=STR_AMBIG_DIR[1]
            #--STR_AMBIG_OBJ1_A=STR_AMBIG_OBJ[1]
            #--STR_AMBIG_SPD1_B=str(STR_AMBIG_SPD[1])
            #--STR_AMBIG_DIR1_B=str(STR_AMBIG_DIR[1])
            #--STR_AMBIG_OBJ1_B=str(STR_AMBIG_OBJ[1])
            #--#
            #--data_from_netcdf=STR_AMBIG_SPD1_A
	    #--STR_AMBIG_SPD1_B=Determine_Wind_SPEED(data_from_netcdf)
            #--#
            #--data_from_file=STR_AMBIG_DIR1_A
            #--STR_AMBIG_DIR1_B=Determine_Wind_Direction(data_from_file)
            #--#
            #--datafromfile=STR_AMBIG_OBJ1_A
	    #--STR_AMBIG_OBJ1_B=Compute_MLE_STRNG(datafromfile,MAX_STR_AMBIG_OBJ)
	    #--#STR_AMBIG_OBJ1_B=Compute_MLE_STRNG(datafromfile)
            #--#
            #--#
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--#
            #--STR_AMBIG_SPD2_A=STR_AMBIG_SPD[2]
            #--STR_AMBIG_DIR2_A=STR_AMBIG_DIR[2]
            #--STR_AMBIG_OBJ2_A=STR_AMBIG_OBJ[2]
            #--STR_AMBIG_SPD2_B=str(STR_AMBIG_SPD[2])
            #--STR_AMBIG_DIR2_B=str(STR_AMBIG_DIR[2])
            #--STR_AMBIG_OBJ2_B=str(STR_AMBIG_OBJ[2])
            #--#
            #--data_from_netcdf=STR_AMBIG_SPD2_A
	    #--STR_AMBIG_SPD2_B=Determine_Wind_SPEED(data_from_netcdf)
            #--#
            #--data_from_file=STR_AMBIG_DIR2_A
            #--STR_AMBIG_DIR2_B=Determine_Wind_Direction(data_from_file)
            #--#
            #--datafromfile=STR_AMBIG_OBJ2_A
	    #--STR_AMBIG_OBJ2_B=Compute_MLE_STRNG(datafromfile,MAX_STR_AMBIG_OBJ)
	    #--#STR_AMBIG_OBJ2_B=Compute_MLE_STRNG(datafromfile)
            #--#
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--# Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #--#
            #--STR_AMBIG_SPD3_A=STR_AMBIG_SPD[3]
            #--STR_AMBIG_DIR3_A=STR_AMBIG_DIR[3]
            #--STR_AMBIG_OBJ3_A=STR_AMBIG_OBJ[3]
            #--STR_AMBIG_SPD3_B=str(STR_AMBIG_SPD[3])
            #--STR_AMBIG_DIR3_B=str(STR_AMBIG_DIR[3])
            #--STR_AMBIG_OBJ3_B=str(STR_AMBIG_OBJ[3])
            #--#
            #--data_from_netcdf=STR_AMBIG_SPD3_A
	    #--STR_AMBIG_SPD3_B=Determine_Wind_SPEED(data_from_netcdf)
            #--#
            #--data_from_file=STR_AMBIG_DIR3_A
            #--STR_AMBIG_DIR3_B=Determine_Wind_Direction(data_from_file)
            #--#
            #--datafromfile=STR_AMBIG_OBJ3_A
	    #--STR_AMBIG_OBJ3_B=Compute_MLE_STRNG(datafromfile,MAX_STR_AMBIG_OBJ)
	    #--STR_AMBIG_OBJ3_B=Compute_MLE_STRNG(datafromfile)
            #
            # Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #
	    STR_AMBIG_SPD0_B=str(MINUS99)
	    STR_AMBIG_DIR0_B=str(MINUS99)
	    STR_AMBIG_OBJ0_B=str('---99')
            #
	    STR_AMBIG_SPD1_B=str(MINUS99)
	    STR_AMBIG_DIR1_B=str(MINUS99)
	    STR_AMBIG_OBJ1_B=str('---99')
            #
	    STR_AMBIG_SPD2_B=str(MINUS99)
	    STR_AMBIG_DIR2_B=str(MINUS99)
	    STR_AMBIG_OBJ2_B=str('---99')
            #
	    STR_AMBIG_SPD3_B=str(MINUS99)
	    STR_AMBIG_DIR3_B=str(MINUS99)
	    STR_AMBIG_OBJ3_B=str('  -99')
            #
            # Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z  
            #
            #

            #########  8<     8<     8<  #########  8<     8<     8< #########  8<     8<     8<

            #
            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            # AS OF 13 March 2015:
            # [Refer to http://opendap.jpl.nasa.gov/opendap/hyrax/allData/rapidscat/L2B12/v1/README.txt ]
            #
            # 2) The data fields containing the number of measurements of each type for each wind vector cell 
            #    are currently zero filled. These fields include: 
            #        ---> number_in_aft
            #        ---> number_in_fore
            #        ---> number_out_aft
            #        ---> number_out_fore. 
            #    In the next release [from NASA JPL] the correct number of measurements will be included 
            #    but for now these fields are zeroed out. Until the next data release, 
            #    please ignore these data fields.
            # - - - - - - - - - - - - - - - - - 
            # Note: I am leaving these next four lines in for future use. PJMC/FNMOC/13MAR2015
            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            #
            #STR_N_INFORE=str(data_num_infore[i,j])
            #STR_N_INAFT=str(data_num_inaft[i,j])
            #STR_N_OUTFORE=str(data_num_outfore[i,j])
            #STR_N_OUTAFT=str(data_num_outaft[i,j])
            STR_N_INFORE=str(MINUS99)
            STR_N_INAFT=str(MINUS99)
            STR_N_OUTFORE=str(MINUS99)
            STR_N_OUTAFT=str(MINUS99)
            #
            #------------------------------------#------------------------------------
            # Now put everything together as a line of data!
            #------------------------------------#------------------------------------
            #
            #
	    STR_THIS_LINE1=NEW_STR_TIME+STR_LAT+STR_LON+STR_WSP+STR_WDR
            #
            #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
	    #STR_TEST_LINE=NEW_STR_TIME+STR_LAT+'[]'+STR_LON+'[---[RAW-LONG]---]'+str(STR_LON_A)+'[]'+STR_WSP+'[---[RAW-WSPD]---]'+str(STR_WSP_A)
            #--#
	    #--#STR_TEST_LINE1='[]'+STR_AMBIG_OBJ0_B+'[-[AMBG_OBJ0]-]'+'[]'+STR_AMBIG_OBJ1_B+'[-[AMBG_OBJ1]-]'
            #--##STR_TEST_LINE1=NEW_STR_TIME+STR_LAT+STR_LON+STR_WSP+STR_WDR+STR_NCEP_WSPD+STR_NCEP_WDIR
            #--##
	    #--##STR_TEST_LINE2='[]'+STR_ROW+'[-[Row]-]'+str(i)+'[]'+STR_CEL+'[-[STR_CEL]-]'+str(j)
            #--#STR_TEST_LINE2='[]'+STR_AMBIG_OBJ2_B+'[-[AMBG_OBJ2]-]'+'[]'+STR_AMBIG_OBJ3_B+'[-[AMBG_OBJ3]-]'
            #--## 
	    #--#STR_TEST_LINE=STR_TEST_LINE1+STR_TEST_LINE2
            #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
	    #STRTESTLINE1='MMDDhhmmLLLLLgggggSSSdddSSSdddSSSdddRRRRRRrrrrCCCttttttFFFFFFsssDDDeeeeeSSSdddEEEEEsssDDDeeeeeSSSdddEEEEE'
	    #STRTESTLINE2='DTG-----Lat--Long-SpdDirNCPNCPxxxxxxRev---row-CelTime2EFlag--Ambig0-----Ambig1-----Ambig2-----Ambig3-----'
            #STRTESTLINE3='STR_CEL:--->'+STR_CEL
            # STR_AMBIG_OBJ0_A
	    #
            #
            #4#STRTESTLINE1='[]'+str(STR_AMBIG_OBJ0_A)+'[-[RwABG_OJ0]-]'+'[]'+str(STR_AMBIG_OBJ1_A)+'[-[RwABG_OJ1]-]'
            #4#STRTESTLINE2='[]'+str(STR_AMBIG_OBJ2_A)+'[-[RwABG_OJ2]-]'+'[]'+str(STR_AMBIG_OBJ3_A)+'[-[RwABG_OJ3]-]'
            #4#STRTESTLINE3=STRTESTLINE1+STRTESTLINE2
            #
            #
            #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
            #
            #--#
            #
	    STR_THIS_LINE2=STR_NCEP_WSPD+STR_NCEP_WDIR+STR_FNMOC2_WSPD+STR_FNMOC2_WDIR+STR_REV_NUMBER
            #
	    STR_THIS_LINE3=STR_ROW+STR_CEL+TIME_TO_EDGE+STR_WVC_FLAGS
            #
	    STR_THIS_LINE4=STR_AMBIG_SPD0_B+STR_AMBIG_DIR0_B+STR_AMBIG_OBJ0_B
            #
	    STR_THIS_LINE5=STR_AMBIG_SPD1_B+STR_AMBIG_DIR1_B+STR_AMBIG_OBJ1_B
            #
	    STR_THIS_LINE6=STR_AMBIG_SPD2_B+STR_AMBIG_DIR2_B+STR_AMBIG_OBJ2_B
            #
	    STR_THIS_LINE7=STR_AMBIG_SPD3_B+STR_AMBIG_DIR3_B+STR_AMBIG_OBJ3_B
            #
	    #STR_THIS_LINE1=NEW_STR_TIME+wblk+STR_LAT+wblk+STR_LON+wblk+STR_WSP+wblk+STR_WDR+wblk
	    #STR_THIS_LINE2=STR_NCEP_WSPD+wblk+STR_NCEP_WDIR+wblk+STR_FNMOC2_WSPD+wblk+STR_FNMOC2_WDIR+wblk+STR_REV_NUMBER+wblk
	    #STR_THIS_LINE3=STR_ROW+wblk+STR_CEL+wblk+TIME_TO_EDGE+wblk+STR_WVC_FLAGS+wblk
            #
	    #STR_THIS_LINE4=STR_AMBIG_SPD0_B+wblk+STR_AMBIG_DIR0_B+wblk+STR_AMBIG_OBJ0_B+wblk
	    #STR_THIS_LINE5=STR_AMBIG_SPD1_B+wblk+STR_AMBIG_DIR1_B+wblk+STR_AMBIG_OBJ1_B+wblk
            #
	    #STR_THIS_LINE6=STR_AMBIG_SPD2_B+wblk+STR_AMBIG_DIR2_B+wblk+STR_AMBIG_OBJ2_B+wblk
	    #STR_THIS_LINE7=STR_AMBIG_SPD3_B+wblk+STR_AMBIG_DIR3_B+wblk+STR_AMBIG_OBJ3_B+wblk
            #
            STR_THIS_LINE=STR_THIS_LINE1+STR_THIS_LINE2+STR_THIS_LINE3+STR_THIS_LINE4+STR_THIS_LINE5+STR_THIS_LINE6+STR_THIS_LINE7+newline_character
            #
            #print("Rev-Number:--->"+str(rev_number))
            #
	    if STR_WDR_B == "--":
	        zxc=0
	        #print(dadash)
	    else:
                writefileobj.write(STR_THIS_LINE)
                ####writefileobj.write(STR_ORIG_TIME)
                ####the_ascii_files=OS.system('echo '+STR_THIS_LINE+' >> '+ascii_file_name)
	        #print(STR_THIS_LINE)
                ##### END OF if block
            #-----------------------------
            # END OF j loop
            #-----------------------------
        # End of i loop
    #---END OF LOOPS----------------------------------------
    #
    #-------------------------------------------------------
    #END OF nested loop for printing out the data elements
    #-------------------------------------------------------
    #
    print(dadash)
    print(dadash+dadash)
    print(dadash)
    print("RAPIDSCAT WIND DATA IN ASCII FORMAT")
    print(dadash)
    print("TIME-----------------------LAT-------LONG------Wind_Spd--Wind_dir--Rain_Impact")
    print(dadash+dadash)
    print(dadash)
    print(" \n")
    #
    #
    print(dadash)
    print(dadash)
    #
    fileobj.close()
    #
    writefileobj.close()
    #
    #-----------------------------------------------------------------------
    # Perform ascii data modifications required for FNMOC modeling group    
    # using -timer_adjust_rscat_data.pl- a PERL script.                     
    #-----------------------------------------------------------------------
    #
    print(dadash)
    print("Now we perform ascii data modifications required for FNMOC modeling group.")
    print(dadash)                                                                      
    the_ascii_modification=binpath+'rscat_wind_adjust_rscat_data.pl'
    #
    the_ascii_files=OS.system(the_ascii_modification+' '+ascii_file_name)              
    #
    #-----------------------------------------------------------------------
    # Copy the --ascii_file_name-- file to alpha-beta and ops
    #-----------------------------------------------------------------------
    #
    #
    print(dadots)
    print("---Changing  permissions on ascii file to 775 -----"+ascii_file_name)
    print(dadots)
    #
    copy_the_ascii_files=OS.system('chmod 775 '+ascii_file_name)
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL CHMOD to 775 of file....."+ascii_file_name)
        #
    else:
        print("---FAILURE! Could not change permission of ascii file....."+ascii_file_name)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    print(dadots)
    print(dadots)
    print("---Copying  -----"+ascii_file_name+"to the following locations.....")
    print(dadots)
    print(dadots)

    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_orig)
    print("---Copying  to the location....."+ascii_path_orig)
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_orig)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_orig)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_aa)
    print("---Copying  to the location....."+ascii_path_aa)
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_aa)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_aa)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_bb)
    print("---Copying  to the location....."+ascii_path_bb)
    #
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_bb)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_bb)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_oo)
    print("---Copying  to the location....."+ascii_path_oo)
    #---===---===---
    #
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_oo)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_oo)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_isis)
    print("---Copying  to the location....."+ascii_path_isis)
    #
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_isis)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_isis)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    print(dadots)
    #
    #-------------------------=====================-------------------------------
    #-------------------------=====================-------------------------------
    # This section added July 21, 2016 in version 2.5.0 to support
    # Yiping Wangs effort to write the data to ISIS.
    # She needs the data in a file with a special filename type.
    #
    #-------------------------=====================-------------------------------
    #-------------------------=====================-------------------------------
    #
    ascii_path_bbp='/satdat/'+system_design8r+'/RapidScat/KNMI/ascii_bb/'
    #
    #.....................
    #
    # Check ascii_path_bbp
    #
    valid_ascii_path_bbp=OS.path.exists(ascii_path_bbp)

    if valid_ascii_path_bbp:
        print(dadash)
        print("The ascii_path_bbp is: "+ascii_path_bbp)
        print("The ascii_path_bbp is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        #this_execution=90
        print("-------The ascii_path_bbp is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        #return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    #
    #only_nc_filename=nc_filename[s_len:n_len]
    only_nc_filename=only_the_nc_filename
    alt_nc_filename=only_the_nc_filename
    #
    #-------------------------------------
    #
    if ('____' in alt_nc_filename):
        alt_nc_filename=only_the_nc_filename.replace('____','_')
        #
    #
    alt_ascii_file_name=alt_nc_filename+'_ovw_tc_fnmoc_ascii_2_isis.txt'
    #
    print(dadots)
    #
    print("The Alternate ASCII file name is:")
    print("-----------------------")
    print(alt_ascii_file_name)
    print("-----------------------")
    #
    print(dadots)
    #
    print('cp '+ascii_file_name+' '+ascii_path_bbp+alt_ascii_file_name)
    #
    print(dadots+dadots)
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_bbp+alt_ascii_file_name)
    print("---Copying  to the location....."+ascii_path_bbp)                                      
    #                                                                                            
    #---===---===---                                                                             
    #                                                                                            
    if copy_the_ascii_files==0:                                                                  
        #                                                                                        
        print("---SUCCESSFUL Copy to the location....."+ascii_path_bbp)                           
        #                                                                                        
    else:                                                                                        
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_bbp) 
        this_execution=97                                                                        
        #                                                                                        
        #----------------------------------------------------------------                        
        #END IF                                                                                  
        #----------------------------------------------------------------                        
    #---===---===---                                                                        
    #---===---===---                                                                        
    #
    ascii_path_datain='/satdat/curr/data_in/'
    #
    #.....................
    #
    # Check ascii_path_datain
    #
    valid_ascii_path_datain=OS.path.exists(ascii_path_datain)

    if valid_ascii_path_datain:
        print(dadash)
        print("The ascii_path_datain is: "+ascii_path_datain)
        print("The ascii_path_datain is VALID and EXISTS")
        print(dadash)
        #
    else:
        #
        #this_execution=90
        print("-------The ascii_path_datain is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        #return this_execution
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................

    #
    print(dadots)
    #
    print('cp '+ascii_file_name+' '+ascii_path_datain+alt_ascii_file_name)
    #
    print(dadots+dadots)
    #
    copy_the_ascii_files=OS.system('cp '+ascii_file_name+' '+ascii_path_datain+alt_ascii_file_name)
    print("---Copying  to the location....."+ascii_path_datain)
    #
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFUL Copy to the location....."+ascii_path_datain)
        #
    else:
        print("---FAILURE! Copy of ascii file did not occur to the location....."+ascii_path_datain)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #---===---===---                                                                        
    #---===---===---                                                                        
    #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # End of change from July 21, 2016
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #


    #
    #-------------------------=====================-------------------------------
    #-------------------------=====================-------------------------------
    #
    #-------------------------=====================-------------------------------
    #-------------------------=====================-------------------------------
    #

    #
    print("---Removing the ascii file from the temp directory.....")
    #
    copy_the_ascii_files=OS.system('rm -rf '+ascii_file_name)
    #
    #---===---===---
    #
    if copy_the_ascii_files==0:
        #
        print("---SUCCESSFULLY deleted the file....."+ascii_file_name)
        #
    else:
        print("---FAILURE! DELETION of ascii file did not occur at the location....."+ascii_path_isis)
        this_execution=97
        #
        #----------------------------------------------------------------
        #END IF
        #----------------------------------------------------------------
    #---===---===---
    #
    print(dadots)
    print(dadots)
    print(dadots)
    #
    #
    #----------------------------------------------------
    # Since we processed this file, lets note this in the 
    # -procdata- subdirectory.
    #----------------------------------------------------
    #

    procfilenamep = Print_Current_Time(right_now)
    proc_file_name_p = procfilenamep+".p"
    proc_file_name=procpath+proc_file_name_p
    the_ncdf_files=OS.system('touch '+proc_file_name)
    the_ncdf_files=OS.system('chmod 776 '+proc_file_name)
    the_ncdf_files=OS.system('cat '+list_of_ncdf_files+" > "+proc_file_name)

    #
    #----------------------------------------------------
    #
    #----------------------------------------------------
    #
    print(dadots)
    print("---END convert_Rapidscat_NETCDF_2_QSCAT_ASCII.py -----")
    print(dadots)
    print(" \n")
    print(dadash+dadash)
    print(dadash+dadash)
    print(dadash+dadash)
    #
    the_end_time = Print_Current_Time(right_now)
    #
    print(dadash+dadash)
    print(dadash+dadash)
    print(dadash+dadash)
    #
    print("Starting Time:"+str(the_start_time))
    print("\n")
    print("Ending   Time:"+str(the_end_time))
    #
    print(dadash+dadash)
    print(dadash+dadash)
    print(dadash+dadash)
    #
    #----------------------------------------------------

    proc_nc_filename=nc_filename+'.p'

    the_proc_files=OS.system('touch '+proc_nc_filename)

    the_proc_files=OS.system('cp '+proc_nc_filename+' '+procpath)

    the_proc_files=OS.system('rm -rf '+proc_nc_filename)

    #the_dataproc_files=OS.system('rm -rf '+nc_filename)

    #----------------------------------------------------
    #----------------------------------------------------
    #----------------------------------------------------
    #
    print("Copying the netCDF file: "+str(nc_filename)+'..to..'+my_SATFOCUS_BASEPATH)
    #
    the_dataproc_files=OS.system('cp '+nc_filename+' '+my_SATFOCUS_BASEPATH)
    #
    #----------------------------------------------------
    #----------------------------------------------------
    #----------------------------------------------------


    #----------------------------------------------------

    print('---ENDING THE --MAIN[]-- FUNCTION  -----')

    this_execution=1
    return this_execution
    ########################################################################################################
    ########################################################################################################
    #### END OF MAIN FUNCTION ##############################################################################
    ########################################################################################################
    ########################################################################################################

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#
#----------------------------------------------------------------------
# This is the so-called primary part of the program where
# everything starts. It starts with invoking the -main- function below.
# The intent is to have virtually everything be done in the -main- function
# and call other functions as needed from within the -main- function.
# The reason for doing this is to enable error trapping more easily
# in the -main- routine. If the -main- code were not in a function, 
# then more effort would need to be expended in trapping runtime errors.
#
# For a simple demo of this idea , See: 
# http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
#    
#----------------------------------------------------------------------
#
my_execution=main()
#
#
#----------------------------------------------------------------
# Let me know if the program executed successfully.
# Otherwise, give me a --helpful-- error message!
#----------------------------------------------------------------
#
if my_execution == 1:
    print("--------------------------------------------------------------------------------")
    print("-------Program Executed SUCCESSFULLY, No Errors were detected! -----------------")
    print("--------------------------------------------------------------------------------")
    #
elif my_execution == 55:
    #
    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    print("------Program Execution Code....."+str(my_execution))
    print("_________________________________________________________________________________")
    print("------There were or was no NETCDF file(s) available to be processed! ------------")
    print("------If there are no valid NETCDF files- the process just ends!  ---------------")
    print("------PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!!!!! -----")
    print("------POSSILBE DPS or BFT problem! POSSIBLE SYSTEM OPERATING SYSTEM PROBLEM!-----")
    print("------POSSIBLE GPFS FILE SYSTEM PROBLEM!-----------------------------------------")
    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    #
elif my_execution == 90:
    #
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    print("-------Program Execution Code....."+str(my_execution))
    print("_________________________________________________________________________________")
    print("-----There were or was a problem with PYTHON getting access to a PATH! ----------")
    print("-----In other words--- the software could not access a subdirectory it needs!  --")
    print("-----The software cant get to a data path either to read or write etc!  ---------")
    print("-----PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!!!!! ------")
    print("-----POSSIBLE LINUX OPERATING SYSTEM PROBLEM! POSSIBLE GPFS FILE SYSTEM PROBLEM!-")
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    #
    #
elif my_execution == 97:
    #
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print("-------Program Execution Code....."+str(my_execution))
    print("________________________________________________________________________________")
    print("-------Data conversion executed successfully (an ASCII file was made)....-------")
    print("-------but ....there were issues interfacing with the operating system! --------")
    print("-------Issues with the operating system could include......... -----------------")
    print("-------file copy- file move- file rename--- file permissions- etc.  ------------")
    print("-------PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!! ------")
    print("-------POSSILBE DPS or BFT problem! POSSIBLE SYSTEM OS PROBLEM!          -------")
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    #
else:
    #
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("-------Program Execution Code....."+str(my_execution))
    print("________________________________________________________________________________")
    print("-------It appears that the program did not execute properly!!!!!!!! ------------")
    print("-------The software exited with an unexpected error code!!!!!!!!!!! ------------")
    print("-------PLEASE CHECK PREVIOUS log entries for ERROR MESSAGES!!!!!!!! ------------")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    #-----------------------------------------------------------
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#
#
#
print(dadash)
print("-------Program END EXECUTION-----------------")
print(dadash)

#-------------------------------------------------------------------------------
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--## END OF PYTHON CODE
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
#
#
#
######################################################################################################
###-------------------------------------
###-------Reading  File -----------------
###-------------------------------------
###The datapath is: /home/mccronep/data/RapidScat/nrt/NETCDF/
###.  .  .  .  .  .  .  .  .  .  .  .  .
###The graphicpath is: /home/mccronep/data/RapidScat/graphic/
###.  .  .  .  .  .  .  .  .  .  .  .  .
###The ASCII path is: /home/mccronep/data/RapidScat/ascii/
###.  .  .  .  .  .  .  .  .  .  .  .  .
###.  .  .  .  .  .  .  .  .  .  .  .  .
####------------------------------------------------------------------------------
#### Title
#### ISS RapidScat Level 2 50.0 km Ocean Surface Wind Vector Product
#### .  .  .  .  .  .  .  .  .  .  .  .  .
#### Dimensions
#### OrderedDict([(u'NUMROWS', <netCDF4.Dimension object at 0x10f44d0>), 
####              (u'NUMCELLS', <netCDF4.Dimension object at 0x10f4758>)])
####------------------------------------------------------------------------------
####------------------------------------------------------------------------------
####------------------------------------------------------------------------------
#### Variables
####------------------------------------------------------------------------------
#### 
#### OrderedDict([(u'time', <netCDF4.Variable object at 0x10ed1d0>), 
#### 		  (u'lat', <netCDF4.Variable object at 0x10ed250>), 
#### 		  (u'lon', <netCDF4.Variable object at 0x10ed2d0>), 
#### 		  (u'wvc_index', <netCDF4.Variable object at 0x10ed350>), 
#### 		  (u'model_speed', <netCDF4.Variable object at 0x10ed3d0>), 
#### 		  (u'model_dir', <netCDF4.Variable object at 0x10ed450>), 
#### 		  (u'ice_prob', <netCDF4.Variable object at 0x10ed4d0>), 
#### 		  (u'ice_age', <netCDF4.Variable object at 0x10ed550>), 
#### 		  (u'wvc_quality_flag', <netCDF4.Variable object at 0x10ed5d0>), 
#### 		  (u'wind_speed', <netCDF4.Variable object at 0x10ed650>), 
#### 		  (u'wind_dir', <netCDF4.Variable object at 0x10ed6d0>), 
#### 		  (u'bs_distance', <netCDF4.Variable object at 0x10ed750>)])
####------------------------------------------------------------------------------
#### 
######################################################################################################
######################################################################################################
#### 
#### PARAMETERS NOT INCLUDED OR CHANGED WITH KNMI VERSION:
#### ------------------------------------------------------------------------------
#### 
#### CHANGE:
####     datawspd = fileobj.variables['retrieved_wind_speed'][:]
####     ---BECAME---
####     datawspd = fileobj.variables['wind_speed'][:]
####     -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
####     datawdir = fileobj.variables['retrieved_wind_direction'][:]
####     ---BECAME---
####     datawdir = fileobj.variables['wind_dir'][:]
####     -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#### 
####     -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#### 
#### ------------------------------------------------------------------------------
#### NOT INCLUDED (These were in the JPL version, not the KNMI version):
####-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
####     datarain_impact = fileobj.variables['rain_impact'][:]
####     dataflags = fileobj.variables['flags'][:]
####     dataeflags = fileobj.variables['eflags'][:]
####     data_ndg_wndspd = fileobj.variables['nudge_wind_speed'][:]
####     data_ndg_wnddir = fileobj.variables['nudge_wind_direction'][:]
####     data_rtr_wspd_uncor = fileobj.variables['retrieved_wind_speed_uncorrected'][:]
####     data_xtrk_wspd_bias = fileobj.variables['cross_track_wind_speed_bias'][:]
####     data_atm_spd_bias = fileobj.variables['atmospheric_speed_bias'][:]
####     data_num_ambig = fileobj.variables['num_ambiguities'][:]
####     data_wind_obj = fileobj.variables['wind_obj'][:]
####     data_ambig_spd = fileobj.variables['ambiguity_speed'][:]
####     data_ambig_dir = fileobj.variables['ambiguity_direction'][:]
####     data_ambig_obj = fileobj.variables['ambiguity_obj'][:]
####     data_num_infore = fileobj.variables['number_in_fore'][:]
####     data_num_inaft = fileobj.variables['number_in_aft'][:]
####     data_num_outfore = fileobj.variables['number_out_fore'][:]
####     data_num_outaft = fileobj.variables['number_out_aft'][:]
#### 
####------------------------------------------------------------------------------
###
###
###  00000000001111111111222222
###  01234567890123456789012345
###  20150129-0008.28.530-UTC-
###		 
###  STR_TIME="20150129-0008.28.530-UTC-"
###  
###  M2M=STR_TIME[4:6]
###  D2D=STR_TIME[6:8]
###  H2H=STR_TIME[9:11]
###  N2N=STR_TIME[11:13]
###
###  NEW_STR_TIME=M2M+D2D+H2H+N2N
###
###
###---------------------------------------------------------------------------------------
###  0000000000111111111122222222223333333333444444444455555555556
###  0123456789012345678901234567890123456789012345678901234567890
###  rapid_20150814_172503_iss____05058_2hr_o_250_1903_ovw_l2.nc
###---------------------------------------------------------------------------------------
###
###
############################################################################################################
############################################################################################################
###													####
### 	This is the documentation for the format of the output FGGE (ASCII) 				####
### 	file that this program produces:								####
###													####
###				This comes from:							####
###				http://a4au-a002/fgge_format/scatq_2.html				####
###.....................................................................................................####
###				QuikSCAT Scattermeter reports - record 2				####
###.....................................................................................................####
###													####
###  Parameter 			Width 	Column Posit.	Units 		Remarks				####
###  ---------                  -----   -------------   -----           ----------------------------	####
###  month 			2 	01-02 		--		01-12 for Jan - Dec		####
###  day 			2 	03-04 		--		01-31				####
###  hour 			2 	05-06 		--		00-23 UT			####
###  minute 			2 	07-08 		--		00-59				####
###  latitude 			5      	09-13 		1/100 degree	north(+), south(-)		####
###  longitude 			5	14-18		1/100 degree	east  0-359.99			####
###  WMO wind speed 		3 	19-21 		1/10 m/s	wind speed at 10m		####
###  WMO wnd direction 		3 	22-24 		degrees 	wind direction at 10m, 0-359   	####
###  FNMOC wind speed 1 	3 	25-27 		1/10 m/s	wind speed at 10m		####
###  FNMOC wind direction 1 	3 	28-30 		degrees 	wind direction at 10m, 0-359	####
###  FNMOC wind speed 2 	3	31-33		1/10 m/s	wind speed at 10m		####
###  FNMOC wind direction 2 	3	34-36		degrees		wind direction at 10m, 0-359	####
###  rev number 		6	37-42		number		orbit number			####
###  row 			4	43-46		number		track row number		####
###  cell 			3	47-49		number		track cell number		####
###  time to edge 		6	50-55		seconds		time to edge			####
###  wvc flag 			6	56-61		code		SeaWinds wind quality flag 	####
###				-      	-		-		(Note: see BUFR 21 109)		####
###  rank 1 wind speed 		3 	62-64 		1/10 m/s	wind speed at 10m		####
###  rank 1 direction 		3 	65-67 		degrees 	wind direction at 10m, 0-359	####
###  rank 1 mle 		5	68-72		code		likelihood (BUFR 21 104)	####
###  rank 1 wind speed 		3	73-75		1/10 m/s	wind speed at 10m		####
###  rank 1 direction 		3	76-78		degrees		wind direction at 10m, 0-359	####
###  rank 1 mle 		5	79-83		code		likelihood (BUFR 21 104)	####
###  rank 1 wind speed 		3	84-86		1/10 m/s	wind speed at 10m		####
###  rank 1 direction 		3	87-89		degrees		wind direction at 10m, 0-359	####
###  rank 1 mle 		5	90-94		code		likelihood (BUFR 21 104)	####
###  rank 1 wind speed 		3	95-97		1/10 m/s	wind speed at 10m		####
###  rank 1 direction 		3	98-100		degrees		wind direction at 10m, 0-359	####
###  rank 1 mle 		5	101-105		code		likelihood (BUFR 21 104)	####
###													####
############################################################################################################
############################################################################################################
#
#
#
############################################################################################################
############################################################################################################
###													####
### 	This is the documentation for the format of the output FGGE (ASCII) 				####
### 	file that this program produces:								####
###													####
###				This comes from:							####
###				http://a4au-a002/fgge_format/scat_2.html				####
###.....................................................................................................####
###				QuikSCAT Scattermeter reports - record 2				####
###.....................................................................................................####
###													####
###  Parameter 			Width 	Column Posit.	Units 		Remarks				####
###  ---------                  -----   -------------   -----           ----------------------------	####
###  month 			2 	01-02 		--		01-12 for Jan - Dec		####
###  month 			2 	01-02 		--		01-12 for Jan - Dec		####
###  day 			2 	03-04 		--		01-31				####
###  hour 			2 	05-06 		--		00-23 UT			####
###  minute 			2 	07-08 		--		00-59				####
###  latitude 			5      	09-13 		1/100 degree	north(+), south(-)		####
###  longitude 			5	14-18		1/100 degree	east  0-359.99			####
###  Wind speed 1		3 	19-21 		1/10 m/s	wind speed at 10m		####
###  Wind direction 2 [1]	3 	22-24 		degrees 	wind direction at 10m, 0-359   	####
###  Wind speed 2		3 	25-27 		1/10 m/s	wind speed at 10m		####
###  Wind direction 2 		3 	28-30 		degrees 	wind direction at 10m, 0-359   	####
###  Wind speed (fdp)		3 	31-33 		1/10 m/s	wind speed at 10m		####
###  Wind direction (fdp)	3 	34-36 		degrees 	wind direction at 10m, 0-359   	####
###													####
############################################################################################################
############################################################################################################
#
###--###
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### The datatim [-time-] value -1- is:
###--### -----------------------
###--### [-- -- -- -- 808421113 808421113 808421113 808421113 808421113 808421113
###--###  808421113 808421113 808421113 808421113 808421113 808421113 -- -- -- -- --]
###--### -----------------------
###--### The datatim [-time-] value -300- is:
###--### -----------------------
###--### [808423157 808423157 808423157 808423157 808423157 808423157 808423157
###--###  808423157 808423157 808423157 808423157 808423157 808423157 808423157
###--###  808423157 808423157 808423157 808423157 808423157 808423157 --]
###--### -----------------------
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### The datawspd [-time-] value -1- is:
###--### -----------------------
###--### [-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --]
###--### -----------------------
###--### The datawspd [-time-] value -300- is:
###--### -----------------------
###--### [5.2700000000000005 5.4400000000000004 5.7599999999999998
###--###  6.5300000000000002 6.9400000000000004 7.3600000000000003 8.120000000000001
###--###  7.2199999999999998 5.2599999999999998 5.9299999999999997
###--###  6.7000000000000002 7.0099999999999998 7.4900000000000002
###--###  7.9699999999999998 8.6099999999999994 8.5800000000000001
###--###  8.2200000000000006 8.8200000000000003 -- 8.9199999999999999 --]
###--### -----------------------
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### The datawdir [-time-] value -1- is:
###--### -----------------------
###--### [-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --]
###--### -----------------------
###--### The datawdir [-time-] value -300- is:
###--### -----------------------
###--### [310.0 297.5 287.5 287.5 285.0 282.5 280.0 282.5 285.0 280.0 272.5 270.0
###--###  267.5 267.5 265.0 265.0 262.5 260.0 -- 257.5 --]
###--### -----------------------
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### The datalat [-time-] value -1- is:
###--### -----------------------
###--### [-- -- -- -- -49.060000000000002 -49.470000000000006 -49.910000000000004
###--###  -50.370000000000005 -50.830000000000005 -51.260000000000005
###--###  -51.710000000000001 -52.150000000000006 -52.590000000000003
###--###  -53.040000000000006 -53.470000000000006 -53.850000000000001 -- -- -- -- --]
###--### -----------------------
###--### The datalat [-time-] value -300- is:
###--### -----------------------
###--### [39.100000000000001 38.770000000000003 38.440000000000005
###--###  38.100000000000001 37.790000000000006 37.43 37.080000000000005
###--###  36.740000000000002 36.410000000000004 36.07 35.740000000000002
###--###  35.370000000000005 35.030000000000001 34.670000000000002
###--###  34.330000000000005 33.980000000000004 33.630000000000003 33.25
###--###  32.910000000000004 32.560000000000002 --]
###--### -----------------------
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### The datalon [-time-] value -1- is:
###--### -----------------------
###--### [-- -- -- -- 206.28999000000002 206.20000000000002 206.23000000000002
###--###  206.31000000000003 206.27000000000001 206.48000000000002
###--###  206.39999000000003 206.60001000000003 206.75000000000003
###--###  206.88000000000002 206.91000000000003 207.20000000000002 -- -- -- -- --]
###--### -----------------------
###--### The datalon [-time-] value -300- is:
###--### -----------------------
###--### [310.14001000000002 310.53000000000003 310.92999000000003
###--###  311.28000000000003 311.67999000000003 312.03000000000003
###--###  312.41000000000003 312.78000000000003 313.14999 313.48999000000003 313.87
###--###  314.19 314.57001000000002 314.91998000000001 315.26001000000002
###--###  315.60999000000004 315.94 316.29001000000005 316.62 316.95999 --]
###--### -----------------------
###--### .  .  .  .  .  .  .  .  .  .  .  .  .
###--### ###--### ###--### ###--### ###--### ###--### ###--### ###--### ###--### 
###--### ###--### ###--### ###--### ###--### ###--### ###--### ###--### ###--### 













