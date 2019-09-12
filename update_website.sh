#!/bin/bash

TARGET=/Volumes/userfiles/public_html/acp/forum-resources/

echo
echo "** Remember to update downloaded data if needed..."
echo

./graphit_fendon_road.py

cp journey_time_fendon_road_area_BUS.pdf ${TARGET}

chmod go+r ${TARGET}/*.pdf
