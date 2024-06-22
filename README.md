# Metro
Analyze subway stations

Algorithm: Statistical analysis of the OD of bus stations around subway stations Data from OD reverse Detect OD on a bus line Observe the changes in passenger flow before and after subway construction i Amplitude ii Direction

Issues to note: i Process in different time periods Morning and evening peaks Flat peaks ii The degree of public response after the subway is open for one week iii Pay attention to the changes in OD direction iv Compare subway stations with and without subway transfers Their changes

The final table should be: Subway station name Latitude and longitude Number of surrounding bus stations Passenger flow before station construction The top three main values ​​of the direction before station construction Passenger flow after station construction The top three main values ​​of the direction after station construction Is there a subway transfer station

Field Description BUS_LINE Bus line METRO_LINE Subway line METRO_STATION_ID Subway station METRO_STATION_NAME Subway station Chinese METRO_GATE_ID Subway gate METRO_GATE_NAME Subway gate Chinese BUS_STATION_ID Bus station BUS_STATION_NAME Bus station Chinese INS_TIME: time to check in (get on or get off) PASS: flow rate SURROUNDING_STATION: surrounding bus stops (multiple) SURROUNDING_LINE: surrounding bus lines (multiple)


![地铁站点周围公交站的OD数量的统计](https://user-images.githubusercontent.com/18719360/131454246-82f11820-e33b-4156-9e3f-a80758d1350b.png)
