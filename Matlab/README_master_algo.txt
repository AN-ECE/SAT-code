{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Arial-BoldMT;\f1\fswiss\fcharset0 ArialMT;\f2\fswiss\fcharset0 Arial-ItalicMT;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{hyphen\}}{\leveltext\leveltemplateid2\'01\uc0\u8259 ;}{\levelnumbers;}\fi-360\li1440\lin1440 }{\listname ;}\listid1}
{\list\listtemplateid2\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{square\}}{\leveltext\leveltemplateid101\'01\uc0\u9642 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid2}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}{\listoverride\listid2\listoverridecount0\ls2}}
\margl1440\margr1440\vieww18220\viewh9760\viewkind0
\deftab720
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs28 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Overview
\fs36 \
\pard\pardeftab720\sa240\partightenfactor0

\fs26 \cf0 master_algo.m
\f1\b0\fs24  is the main script for solving k-SAT problems using a reduction to 3-SAT and applying a Solver Algorithm. It processes CNF/DIMACS files and provides the final SAT state and TTS calculation.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs28 \cf0 Input Parameters
\fs36 \
\pard\pardeftab720\sa240\partightenfactor0

\f1\b0\fs24 \cf0 The function takes the following inputs:\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\f0\b \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 cnffile
\f1\b0  
\f2\i (string)
\f1\i0 : Path to the k-SAT CNF/DIMACS file (Line 16).\
\ls1\ilvl0
\f0\b \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 cnffile_new
\f1\b0  
\f2\i (string, optional)
\f1\i0 : Path to save the 3-SAT reduced CNF file if needed. Default is an empty string (
\fs26 ''
\fs24 ) \outl0\strokewidth0 (Line 17)\outl0\strokewidth0 \strokec2 .\
\ls1\ilvl0
\f0\b \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 digital_backup
\f1\b0  
\f2\i (integer, optional)
\f1\i0 : \outl0\strokewidth0 (Line 20)\outl0\strokewidth0 \strokec2 \
\pard\tx940\tx1440\pardeftab720\li1440\fi-1440\sl192\slmult1\partightenfactor0
\ls1\ilvl1\cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8259 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Set to 
\fs26 1
\fs24  to run the Solver Algorithm on the k-SAT problem after a certain number of iterations .\
\ls1\ilvl1\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8259 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Usually set to 
\fs26 1
\fs24  when the 3-SAT reduced problem has more than 4000 variables.\
\ls1\ilvl1\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8259 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Default value: 
\fs26 0
\fs24 .\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs28 \cf0 Output
\fs36 \
\pard\pardeftab720\sa240\partightenfactor0

\f1\b0\fs24 \cf0 The function displays the following outputs:\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls2\ilvl0
\f0\b \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u9642 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 X
\f1\b0 : Final SAT state for all the variables.\
\ls2\ilvl0
\f0\b \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u9642 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 TTS
\f1\b0 : TTS calculated for the current run.\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\fs28 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 \
\
}