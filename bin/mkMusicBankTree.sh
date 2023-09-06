#!/usr/bin/bash

#set -x

MUSIC_ROOT=${MUSIC_ROOT}
ARTIST="Example"

if [[ -e $MUSIC_ROOT ]]; then
  echo "${MUSIC_ROOT} FOUND"
else
  echo "${MUSIC_ROOT} NOT FOUND. Creating"
  mkdir -p ${MUSIC_ROOT}
fi

mkdir -p ${MUSIC_ROOT}/{Alpha,Archive,Attic}/{A..Z}
mkdir -p ${MUSIC_ROOT}/{Alpha,Archive,Attic}/0-9
mkdir -p ${MUSIC_ROOT}/bin
mkdir -p ${MUSIC_ROOT}/Rip/{AlphaStage,Stage}
mkdir -p ${MUSIC_ROOT}/Other/{Classical,Clips,Comedy,Compilations}
mkdir -p ${MUSIC_ROOT}/Other/{Covers,List,Mixes,Sountracks,Various}
