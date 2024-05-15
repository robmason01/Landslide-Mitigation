# Intialise

# Import modules 
import hyrcan as hy  
import numpy as np
import xlsxwriter

#------------------------------------------------------------------------------
# Inputs

# Slope height (m)
h_set = [5,10,15,20,25,30]
# Slope angle (degrees)
a_set = [10,20,30,40,50]
# Depth of top of stratum at top of slope (m)
st_set = [3,6,9,12]
# Thickness of stratum
ss_set = [3,6,9,12]
# Soil 1 friction (degrees)
f1_set = [25,30,35]
# Soil 2 friction (degrees)
f2_set = [15,20,25]
# Cohesion (kPa)
c_set = [0.1,10,20]

# Constants

# Soil 1 dry unit weight (kN/m^3)
wdry1 = 18
# Soil 1 saturated unit weight (kN/m^3)
wsat1 = 20
# Soil 2 dry unit weight (kN/m^3)
wdry2 = 18
# Soil 2 saturated unit weight (kN/m^3)
wsat2 = 20
# Desired factor of safety
dfos = 1.0

#------------------------------------------------------------------------------
# Excel
workbook = xlsxwriter.Workbook('data.xlsx', {"nan_inf_to_errors": True})
worksheet = workbook.add_worksheet()
worksheet.set_column(0, 20, 20)
bold = workbook.add_format({'bold': 1})
bold.set_align('vjustify')
standard = workbook.add_format({'num_format': '#,##0.00'})
row0 = ['Slope height (m)', 'Slope angle (degrees)', 'Depth of layer 1 (m)', 'Depth of layer 2 (m)', 'Soil 1 friction (degrees)', 'Soil 2 friction (degrees)', 'Cohesion (kPa)', 'Original factor of safety', 'Regrading EC (kgCO2e/m)', 'Soil nailing EC (kgCO2e/m)', 'Gabion wall EC (kgCO2e/m)', 'Anchored wall EC (kgCO2e/m)']
worksheet.write_row(0, 0, row0, bold)

#------------------------------------------------------------------------------
#Setup

mega = []

pi = np.pi


for h in h_set:
    for a in a_set:
        for st in st_set:
            for ss in ss_set:
                for f1 in f1_set:
                    for f2 in f2_set:
                        for c in c_set:
                            
                            sb = st + ss
                            sd = a
                            c1 = c
                            c2 = c
                            
                            #------------------------------------------------------------------------------
                            # Original slope
                            
                            # Create model
                            hy.command(""" 
                            newmodel() 
                            set("unit","metric","failureDir","r2l","numSlice",20,"tolerance",0.01,"numSample",300,"searchMethod","slopeSearch","maxIter",20)
                            extboundary(0,0,550,0,550,100,500,100,"""+str(500-(h/np.tan(a*pi/180)))+""","""+str(100-h)+""",0,"""+str(100-h)+""",0,0) 
                            matboundary(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""") 
                            matboundary(0,"""+str(100-sb-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-sb)+""",550,"""+str(100-sb+(50*np.tan(sd*pi/180)))+""") 
                            definemat('ground','matID',1,'matName','Soil 1','satUW','on','uw',"""+str(wdry1)+""",'suw',"""+str(wsat1)+""",'cohesion',"""+str(c1)+""",'friction',"""+str(f1)+""") 
                            definemat('ground','matID',2,'matName','Soil 2','satUW','on','uw',"""+str(wdry2)+""",'suw',"""+str(wsat2)+""",'cohesion',"""+str(c2)+""",'friction',"""+str(f2)+""") 
                            assignsoilmat('matid',2,'atpoint',500,"""+str(100-st-0.01)+""")
                            assignsoilmat('matid',2,'atpoint',0,"""+str(100-st-(500*np.tan(sd*pi/180))-0.01)+""")
                            addwatertable(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""")
                            definelimits('limit',"""+str(460-(h/np.tan(a*pi/180)))+""","""+str(500-(h/(2*np.tan(a*pi/180))))+""",'limit2',"""+str(500-(h/(2*np.tan(a*pi/180))))+""",540) 
                            set('Method','BishopSim','on') 
                            """)
                            
                            # Calculate original factor of safety
                            hy.command("compute('silence')")
                            ogfos = hy.min_fos('BishopSim')
                            if ogfos >= dfos:
                                sample = [h, a, st, ss, f1, f2, c, ogfos, 0, 0, 0, 0]
                            else:    
                                sample = [h, a, st, ss, f1, f2, c, ogfos]
                            
                                #------------------------------------------------------------------------------
                                # Regrading
                                
                                # Iterate slopes
                                list6 = []
                                regradeangles = np.arange(5, a, 5)
                                for ra in regradeangles:
                                    hy.command(""" 
                                    newmodel() 
                                    set("unit","metric","failureDir","r2l","numSlice",20,"tolerance",0.01,"numSample",300,"searchMethod","slopeSearch","maxIter",20)
                                    extboundary(0,0,550,0,550,100,500,100,"""+str(500-(h/np.tan(ra*pi/180)))+""","""+str(100-h)+""",0,"""+str(100-h)+""",0,0) 
                                    matboundary(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""") 
                                    matboundary(0,"""+str(100-sb-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-sb)+""",550,"""+str(100-sb+(50*np.tan(sd*pi/180)))+""") 
                                    definemat('ground','matID',1,'matName','Soil 1','satUW','on','uw',"""+str(wdry1)+""",'suw',"""+str(wsat1)+""",'cohesion',"""+str(c1)+""",'friction',"""+str(f1)+""") 
                                    definemat('ground','matID',2,'matName','Soil 2','satUW','on','uw',"""+str(wdry2)+""",'suw',"""+str(wsat2)+""",'cohesion',"""+str(c2)+""",'friction',"""+str(f2)+""") 
                                    assignsoilmat('matid',2,'atpoint',500,"""+str(100-st-0.01)+""")
                                    assignsoilmat('matid',2,'atpoint',0,"""+str(100-st-(500*np.tan(sd*pi/180))-0.01)+""")
                                    addwatertable(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""")
                                    definelimits('limit',"""+str(460-(h/np.tan(ra*pi/180)))+""","""+str(500-(h/(2*np.tan(ra*pi/180))))+""",'limit2',"""+str(500-(h/(2*np.tan(ra*pi/180))))+""",540)
                                    set('Method','BishopSim','on') 
                                    """)
                                    hy.command("compute('silence')")
                                    ec = 2 * h**2 * np.sin((a-ra)*pi/180) / (4 * np.sin(ra*pi/180) * np.sin(a*pi/180))
                                    list6a = [ec, hy.min_fos('BishopSim'), ra]
                                    list6.append(list6a)
                                
                                # Find optimal value
                                opt = min((x for x in list6 if x[1] > dfos), key=lambda k:k[0], default=["n/a","n/a","n/a"])
                                ec = opt[0]
                                sample.append(ec)
                                print(ec)
                                
                                #------------------------------------------------------------------------------
                                # Soil nails
                                
                                bond_strength = pi*0.1*c1 + 2 * 0.1 * (0.5*wdry1*h) * np.tan(f1*pi/180)
                                
                                # Create model
                                hy.command(""" 
                                newmodel() 
                                set("unit","metric","failureDir","r2l","numSlice",20,"tolerance",0.01,"numSample",300,"searchMethod","slopeSearch","maxIter",20)
                                extboundary(0,0,550,0,550,100,500,100,"""+str(500-(h/np.tan(a*pi/180)))+""","""+str(100-h)+""",0,"""+str(100-h)+""",0,0) 
                                matboundary(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""") 
                                matboundary(0,"""+str(100-sb-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-sb)+""",550,"""+str(100-sb+(50*np.tan(sd*pi/180)))+""")
                                definemat('ground','matID',1,'matName','Soil 1','satUW','on','uw',"""+str(wdry1)+""",'suw',"""+str(wsat1)+""",'cohesion',"""+str(c1)+""",'friction',"""+str(f1)+""") 
                                definemat('ground','matID',2,'matName','Soil 2','satUW','on','uw',"""+str(wdry2)+""",'suw',"""+str(wsat2)+""",'cohesion',"""+str(c2)+""",'friction',"""+str(f2)+""") 
                                definemat('support','matID',3,'matName','Soil Nail','supportType','SoilNail','forceApp','Active','spacing',2,'tensCapacity',340,'plateCapacity',340,'bondStrength',"""+str(bond_strength)+""")
                                assignsoilmat('matid',2,'atpoint',500,"""+str(100-st-0.01)+""")
                                assignsoilmat('matid',2,'atpoint',0,"""+str(100-st-(500*np.tan(sd*pi/180))-0.01)+""")
                                addwatertable(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""",500,"""+str(100-st)+""",550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""")
                                definelimits('limit',"""+str(460-(h/np.tan(a*pi/180)))+""","""+str(500-(h/(2*np.tan(a*pi/180))))+""",'limit2',"""+str(500-(h/(2*np.tan(a*pi/180))))+""",540)
                                set('Method','BishopSim','on') 
                                """)
                                
                                # Iterate
                                list1 = []
                                cmd1 = "definemat('support','matID',3,'matName','Soil Nail','supportType','SoilNail','forceApp','Active','spacing',{0},'tensCapacity',340,'plateCapacity',340,'bondStrength',"+str(bond_strength)+")"
                                cmd2 = "addsupport('pattern','id',1,'matid',3,'orientation','anglefromhoriz','angle',{0},'length',{1},'spaced','along','dist',{2},'frompoint',500,100,'topoint',"+str(500-(h/np.tan(a*pi/180)))+","+str(100-h)+")"
                                for spacing in [1, 2]:
                                    for angle in [-20]:
                                        for length in [5, 10, 15, 20, 25, 30]:
                                            hy.command(cmd1.format(spacing))
                                            hy.command('delsupport("patternid",1)')
                                            hy.command(cmd2.format(angle, length, spacing))
                                            hy.command("compute('silence')")
                                            noofnails = (h / np.sin(a*pi/180)) / spacing / spacing
                                            ec = noofnails * length * (16.7 + 2.6)
                                            list2 = [ec, hy.min_fos('BishopSim'), angle, length, spacing]
                                            list1.append(list2)
                                
                                # Find optimal value
                                opt = min((x for x in list1 if x[1] > dfos), key=lambda k:k[0], default=["n/a","n/a","n/a","n/a","n/a"])
                                ec = opt[0]
                                sample.append(ec)
                                print(ec)
                                
                                #------------------------------------------------------------------------------
                                # Wall height
                                
                                if f1 > a+2:
                                    
                                    temporary = []
                                    for h1 in np.arange(3,h,1):
                                        hy.command(""" 
                                        newmodel() 
                                        set("unit","metric","failureDir","r2l","numSlice",20,"tolerance",0.01,"numSample",300,"searchMethod","slopeSearch","maxIter",20)
                                        extboundary(0,0,550,0,550,100,500,100,"""+str(500-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-h+h1)+""","""+str(499-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-h+h1)+""","""+str(499-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-h)+""",0,"""+str(100-h)+""",0,0) 
                                        matboundary("""+str(500-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-h+h1)+""","""+str(500-((h-h1)/np.tan(a*pi/180)))+""","""+str(99-h)+""","""+str(499-((h-h1)/np.tan(a*pi/180)))+""","""+str(99-h)+""","""+str(499-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-h)+""")
                                        matboundary(550,"""+str(100-st+(50*np.tan(sd*pi/180)))+""","""+str(500.1-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-st-(((h-h1)/np.tan(a*pi/180))-0.1)*np.tan(sd*pi/180))+""","""+str(500.1-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-sb-(((h-h1)/np.tan(a*pi/180))-0.1)*np.tan(sd*pi/180))+""",550,"""+str(100-sb+(50*np.tan(sd*pi/180)))+""") 
                                        matboundary(0,"""+str(100-st-(500*np.tan(sd*pi/180)))+""","""+str(498.9-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-st-(((h-h1)/np.tan(a*pi/180))+1.1)*np.tan(sd*pi/180))+""","""+str(498.9-((h-h1)/np.tan(a*pi/180)))+""","""+str(100-sb-(((h-h1)/np.tan(a*pi/180))+1.1)*np.tan(sd*pi/180))+""", 0, """+str(100-sb-(500*np.tan(sd*pi/180)))+""")
                                        definemat('ground','matID',1,'matName','Soil 1','satUW','on','uw',"""+str(wdry1)+""",'suw',"""+str(wsat1)+""",'cohesion',"""+str(c1)+""",'friction',"""+str(f1)+""") 
                                        definemat('ground','matID',2,'matName','Soil 2','satUW','on','uw',"""+str(wdry2)+""",'suw',"""+str(wsat2)+""",'cohesion',"""+str(c2)+""",'friction',"""+str(f2)+""") 
                                        definemat('ground','matID',3,'matName','Wall','satUW','off','uw',24,'cohesion',1e+50,'friction',90)
                                        assignsoilmat('matid',2,'atpoint',500,"""+str(100-st-0.01)+""")
                                        assignsoilmat('matid',2,'atpoint',0,"""+str(100-st-(500*np.tan(sd*pi/180))-0.01)+""")
                                        assignsoilmat('matid',2,'atpoint',"""+str(500-(h/np.tan(a*pi/180)))+""","""+str(99.9-h-st)+""")
                                        assignsoilmat('matid',3,'atpoint',"""+str(499.5-((h-h1)/np.tan(a*pi/180)))+""","""+str(99.9-h+h1)+""")
                                        definelimits('limit',"""+str(460-(h/np.tan(a*pi/180)))+""","""+str(499-((h-h1)/np.tan(a*pi/180)))+""",'limit2',"""+str(500-((h-h1)/np.tan(a*pi/180)))+""",540) 
                                        set('Method','BishopSim','on') 
                                        """)
                                        hy.command("compute('silence')")
                                        temporary.append([hy.min_fos('BishopSim'),h1])
                                    opt = min((x for x in temporary if x[0] > dfos), key=lambda k:k[1], default=[1,h])
                                    h1 = opt[1]
                                    
                                    # Earth pressure coefficients
                                    if h1 == h:
                                        Ka = (1-np.sin(f1*pi/180)) / (1+np.sin(f1*pi/180))
                                        Kp = (1+np.sin(f1*pi/180)) / (1-np.sin(f1*pi/180))
                                    else:
                                        Ka = (np.cos(a*pi/180)-((np.cos(a*pi/180))**2-(np.cos(f1*pi/180))**2)**0.5) / (np.cos(a*pi/180)+((np.cos(a*pi/180))**2-(np.cos(f1*pi/180))**2)**0.5) * np.cos(a*pi/180)
                                        Kp = (np.cos(a*pi/180)+((np.cos(a*pi/180))**2-(np.cos(f1*pi/180))**2)**0.5) / (np.cos(a*pi/180)-((np.cos(a*pi/180))**2-(np.cos(f1*pi/180))**2)**0.5) * np.cos(a*pi/180)
                                    
                                else:
                                    
                                    h1 = h
                                    
                                    # Earth pressure coefficients
                                    Ka = (1-np.sin(f1*pi/180)) / (1+np.sin(f1*pi/180))
                                    Kp = (1+np.sin(f1*pi/180)) / (1-np.sin(f1*pi/180))
                                    
                                #------------------------------------------------------------------------------
                                # Gabion wall
                                
                                # Pressure equations
                                sigv = wdry1*h1
                                sigh = Ka*sigv
                                P = 1/2 * sigh * h1
                                
                                # Wall design
                                if 100-sb-((h-h1)/np.tan(a*pi/180))*np.tan(sd*pi/180)-1 < 100-h < 100-st-((h-h1)/np.tan(a*pi/180))*np.tan(sd*pi/180)+1:
                                    B = max( 2*P/27/h/np.tan(f2*pi/180), (abs(4/45*P))**0.5 )
                                else:
                                    B = max( 2*P/27/h/np.tan(f1*pi/180), (abs(4/45*P))**0.5 )
                                
                                T = B/2
                                
                                # Embodied carbon (gabions + excavation)
                                ec = 15.7 * h1 * (T+B) + h1 * h1 / np.tan(a*pi/180)
                                sample.append(ec)
                                print(ec)
                                
                                #------------------------------------------------------------------------------
                                # Anchored retaining wall
                                    
                                # Cubic equation in terms of d
                                cubic_a = 2*Ka - 2*Kp
                                cubic_b = 6*Ka*h1 - 6*Ka - 3*Kp*h1 + 6*Kp
                                cubic_c = 6*Ka*h1**2 - 12*Ka*h1
                                cubic_d = 2*Ka*h1**3 - 6*Ka*h1**2
                                
                                # Calculate d
                                roots = np.roots([cubic_a, cubic_b, cubic_c, cubic_d])
                                d = min([i for i in roots if i > 0], default=1)
                                d = max(1,d)
                                
                                # Design tendon
                                active_pressure = Ka*wdry1*(h1+d)
                                passive_pressure = Kp*wdry1*d
                                active_force = 0.5 * active_pressure * (h1+d)
                                passive_force = 0.5 * passive_pressure * d
                                tendon_force = active_force - passive_force
                                tendon_area = tendon_force / 275000 # m^2
                                
                                # Wall bending moment
                                moments = list()
                                positions = np.arange(2,h1+d,0.5)
                                positions = np.append(positions, [round(h1+d, 2)] )
                                for x in positions:
                                    if x > h1:
                                        A = (x/(h1+d)) * active_pressure
                                        P = (x-h1)/d * passive_pressure
                                        M = round(tendon_force * (x-2) - (1/2*A*x*x/3) + 1/2*P*(x-h1)*(x-h1)/3, 2)
                                        moments.append(M)
                                    else:
                                        A = (x/(h1+d)) * active_pressure
                                        M = round(tendon_force * (x-2) - (1/2*A*x*x/3), 2)
                                        moments.append(M)    
                                        
                                # Wall thickness
                                moment = max(moments) # kNm/m
                                moment = abs(moment)
                                structural_depth = (moment/5376)**0.5 # m
                                wall_thickness = structural_depth + 0.061
                                
                                # Anchor size
                                d2 = ((2*tendon_force + 4*Kp*wdry1 + 4*Ka*wdry1) / (Kp*wdry1 + Ka*wdry1))**0.5
                                anchor_height = d2 - 2
                                
                                # Embodied carbon
                                wall_volume = wall_thickness * (h1+d+anchor_height)
                                steel_volume = tendon_area * 5
                                soil_volume = 0.5 * h1 * h1 / np.tan(a*pi/180) # m^3/m
                                ec = wall_volume * 619 + steel_volume * 13260 + soil_volume * 2
                                sample.append(ec)
                                print(ec)
                            
                            print(sample)
                            mega.append(sample)
    
#------------------------------------------------------------------------------
# Finalise

for row_num, data in enumerate(mega):
    worksheet.write_row(row_num+1, 0, data, standard)

workbook.close()