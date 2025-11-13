MODIFIED FILES

backend:
i: soil_analysis.py [check]
i: soil_moisture.py [check]
i: npk_router.py [check]
i: soilph_router.py [check]
i: temhum_router.py [check]
i: waterlevel_router.py 

frontend: 
i; SoilAnalysis.vue [check]
i: LandingPage.vue [check]
i: SoilMoisture.vue [check]
i: SoilPH.vue [check]
i: TemperatureHumidity.vue [check]
i: WaterLevel.vue [check]
i: npkData.vue [check]


can you make in this page is the fetching of the data that will be displayed in the table will be per page? like for example the limit of the number of data that will be displayed in the table is only 20 records, how can i implement this kind of logic because if i singly fetch all the data from mongodb and display in the table timeout occurs because the number of data saved in database is more than 3000 records, that's why when it is fetch timeout error occurs


is it possible to put a range of data on the print function, for example when the user click the print button the user will select or input a range of date for the data he wants to print can you possibly make it only for the date range


UPLOAD 

Frontend: ReCalibration.vue

Backend: esp32_ip.py