from ui .components import AQICard ,InfoSection ,PollutantCard ,StationCard 

print ('Creating AQICard and sections...')
card =AQICard ()

p =InfoSection ('Pollutant Analysis',None )
p .add_item (PollutantCard ('PM2.5',153.0 ,is_dominant =True ))

s =InfoSection ('Monitoring Stations',None )
s .add_item (StationCard ('Golden Temple',325 ))

r =InfoSection ('Health Recommendations',None )
r .add_item ('Wear a mask')

print ('Calling set_details...')
card .set_details ([p ,s ,r ])
print ('Done')
