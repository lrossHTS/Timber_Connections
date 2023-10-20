# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:01:22 2023

@author: PSCOTT
"""

# Functions to produce plots
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------- # 
def vectorField(cxn, el):        
    scale = 0.01

    if el.type == 'Column':
            xForce = np.array(cxn.v_2)
            yForce = np.array(cxn.v_1) *-1
            
            x = np.array(cxn.xCoord)
            y = np.array(cxn.yCoord)
            
            # key points
            a = -el.h/2
            b = el.h/2
            c = max(cxn.yCoord) + cxn.a_3_group
            d = -1000           
            
            # line coords
            left    = [a,a],[d,c]
            right   = [b,b],[d,c]
            top     = [a,b],[c,c]
            
            # plate points
            e       = min(cxn.xCoord) - cxn.plate_edge
            f       = el.h/2
            g       = min(cxn.yCoord) - cxn.plate_edge
            h       = max(cxn.yCoord) + cxn.plate_edge

            end_pl = [e,e], [g,h]
            top_pl  = [e,f], [h,h]
            bot_pl  = [e,f], [g,g]
    
            # Plot limits
            ylim = c + 50
            xlim = el.h
    
    elif el.type == 'Beam':
            xForce = np.array(cxn.v_1) 
            yForce = np.array(cxn.v_2)    
    
            x = np.array(cxn.yCoord) *-1
            y = np.array(cxn.xCoord)
            
            # key points
            a = (max(cxn.yCoord) + cxn.a_3_group) * -1     
            b = 1000    
            c = el.h/2            
            d = -el.h/2
            
            # line coords
            left    = [b,a],[d,d]
            right   = [b,a],[c,c]
            top     = [a,a],[d,c]
            
            # plate points
            e       = max(cxn.yCoord) + cxn.plate_edge
            f       = (max(cxn.yCoord) + cxn.a_3_group) * -1 
            g       = min(cxn.xCoord) - cxn.plate_edge
            h       = max(cxn.xCoord) + cxn.plate_edge

            end_pl  = [e,e], [g,h]
            top_pl  = [f,e], [h,h]
            bot_pl  = [e,f], [g,g]
            
            # Plot limits
            xlim = (a - 50)*-1
            ylim = el.h
    
    # print(xlim)
    
    forceX_scaled = xForce / scale
    forceY_scaled = yForce / scale
    
    # resultant    
    u = x + forceX_scaled
    v = y + forceY_scaled
    
    # x Component:
    u1 = u
    v1 = y
    
    # y Component:
    u2 = x
    v2 = v
    
    vecPlot = plt.subplots(subplot_kw = {'aspect':'equal'})             # creates tuple of figure and subplot
    
    vecPlot[1].plot(left[0],left[1],'k')                                # plot timber edges
    vecPlot[1].plot(right[0],right[1],'k')                              
    vecPlot[1].plot(top[0],top[1],'k')                                  
    
    vecPlot[1].plot(end_pl[0],end_pl[1],'k', linestyle = '--')                       # plot plate edges
    vecPlot[1].plot(top_pl[0],top_pl[1],'k', linestyle = '--')                       
    vecPlot[1].plot(bot_pl[0],bot_pl[1],'k', linestyle = '--')                      
    
    patch = [a,d], [a,c], [b,c], [b,d]                                  # plots patch
    vecPlot[1].add_patch(plt.Polygon(patch,facecolor = '#f3eddd'))      # sets patch to timber colour
    
    vecPlot[1].plot(x,y,'.',markersize = cxn.d/2, color = 'k')          # plots markers
    vecPlot[1].quiver(x,y,u,v)                                          # plots quivers
    vecPlot[1].quiver(x,y,u1,v1, linestyle ='dashed', facecolor = 'none',linewidth = 0.5, edgecolor = 'b')
    vecPlot[1].quiver(x,y,u2,v2, linestyle = 'dashed', facecolor = 'none',linewidth = 0.5, edgecolor = 'r')

    vecPlot[1].text(0, -350,'Bolt Load Vectors', horizontalalignment = 'center')

    vecPlot[1].axis('off')

    vecPlot[1].set_xlim([-xlim, xlim])
    vecPlot[1].set_ylim([-ylim, ylim])
    
    cxn.vec_plot = vecPlot
    
# --------------------------------------------------------------------------- #
def plotBolts(cxn, el):        
    
    boltPlot = plt.subplots(subplot_kw = {'aspect':'equal'})  

    if el.type == 'Column':           
            # key points
            a = -el.h/2
            b = el.h/2
            c = max(cxn.yCoord) + cxn.a_3_group
            d = -1000           
            
            # line coords
            left    = [a,a],[d,c]
            right   = [b,b],[d,c]
            top     = [a,b],[c,c]
            
            # plate points
            e       = min(cxn.xCoord) - cxn.plate_edge
            f       = el.h/2
            g       = min(cxn.yCoord) - cxn.plate_edge
            h       = max(cxn.yCoord) + cxn.plate_edge

            end_pl = [e,e], [g,h]
            top_pl  = [e,f], [h,h]
            bot_pl  = [e,f], [g,g]

            # Other element
            j = f + cxn.end_clear
            k = j + 300
            l = j + 500
            m = -c

            otherElLeft     = [j,j],[c,m]
            otherElRight    = [k,k],[c,m]
            otherElTop      = [j,l],[c,c]
            otherElBot      = [j,l],[m,m]
            extPlateBot     = [f,j],[g,g]
            extPlateTop     = [f,j],[h,h]

            otherElPatch = [l,m], [l,c], [j,c], [j,m]                                        # fill other element
            boltPlot[1].add_patch(plt.Polygon(otherElPatch,facecolor = '#f3eddd'))
            
            # Plot limits
            ylim = c + 50
            xlim = el.h
            
            x  = cxn.xCoord
            y  = cxn.yCoord 

            boltPlot[1].plot(otherElTop[0],otherElTop[1],'#B2B2B2')                         
            boltPlot[1].plot(otherElBot[0],otherElBot[1],'#B2B2B2')
    
    elif el.type == 'Beam':
            # key points
            a = (max(cxn.yCoord) + cxn.a_3_group) * -1     
            b = 1000    
            c = el.h/2            
            d = -el.h/2
            
            # line coords
            left    = [b,a],[d,d]
            right   = [b,a],[c,c]
            top     = [a,a],[d,c]
            
            # plate points
            e       = max(cxn.yCoord) + cxn.plate_edge
            f       = (max(cxn.yCoord) + cxn.a_3_group) * -1 
            g       = min(cxn.xCoord) - cxn.plate_edge
            h       = max(cxn.xCoord) + cxn.plate_edge

            # Other element
            j = f - cxn.end_clear
            k = j - 300
            l = d - 50
            m = c + 50


            end_pl  = [e,e], [g,h]
            top_pl  = [f,e], [h,h]
            bot_pl  = [e,f], [g,g]

            otherElRight = [j,j], [m,l]
            otherElLeft = [k,k], [m,l]
            extPlateBot = [f,j], [g,g]
            extPlateTop = [f,j], [h,h]

            otherElPatch = [j,l], [j,m], [k,m], [k,l]                                        # fill other element
            boltPlot[1].add_patch(plt.Polygon(otherElPatch,facecolor = '#f3eddd'))

            # Plot limits
            xlim = (a - 450)*-1
            ylim = el.h
            
            x = np.array(cxn.yCoord) *-1
            y = np.array(cxn.xCoord)
    
    boltPlot[1].plot(left[0],left[1],'k')                                           # plot left
    boltPlot[1].plot(right[0],right[1],'k')                                         # plot right
    boltPlot[1].plot(top[0],top[1],'k')                                             # plot top
    
    boltPlot[1].plot(end_pl[0],end_pl[1],'k', linestyle = '--')                     # plot plate edges
    boltPlot[1].plot(top_pl[0],top_pl[1],'k', linestyle = '--')                       
    boltPlot[1].plot(bot_pl[0],bot_pl[1],'k', linestyle = '--')  

    boltPlot[1].plot(otherElRight[0],otherElRight[1],'#B2B2B2')
    boltPlot[1].plot(otherElLeft[0],otherElLeft[1],'#B2B2B2')
    boltPlot[1].plot(extPlateBot[0],extPlateBot[1],'#B2B2B2', linestyle = '--')    
    boltPlot[1].plot(extPlateTop[0],extPlateTop[1],'#B2B2B2', linestyle = '--')         
    
    patch = [a,d], [a,c], [b,c], [b,d]
    boltPlot[1].add_patch(plt.Polygon(patch,facecolor = '#f3eddd'))
    boltPlot[1].plot(x,y,'.',markersize = cxn.d/2)
    
    boltPlot[1].text(0, -350,'Elevation', horizontalalignment = 'center')

    boltPlot[1].axis('off')
    
    boltPlot[1].set_xlim([-xlim, xlim])
    boltPlot[1].set_ylim([-ylim, ylim])

    count = 0
    boltref = 1
    
    for x, y in zip(x, y):
                        
            label = str(boltref)
        
            boltPlot[1].annotate(label,(x,y), textcoords="offset points", xytext=(0,5), ha = 'center')
            count = count + 1
            boltref = boltref + 1
            
    cxn.bolt_plot = boltPlot
# --------------------------------------------------------------------------- #
def plotSection(cxn, el):        

    a = -el.t/2
    b = el.t/2
    c = el.h/2
    d = -el.h/2          
    
    # line coords
    sec_L   = [a,a],[d,c]
    sec_R   = [b,b],[d,c]
    sec_T   = [a,b],[c,c]
    sec_B   = [a,b],[d,d]
    
    # plate points / lines
    e       = -cxn.pl_thk / 2 
    f       =  cxn.pl_thk / 2 
    g       =  el.h/2
    h       = -el.h/2
    
    plate_L  = [e, e] , [h, g]
    plate_R = [f, f] , [h, g]
    plate_T   = [e, f] , [g, g]
    plate_B   = [e, f] , [h, h]
    
    # bolt points
    i       = -el.t/2
    j       =  el.t/2
    k       =  cxn.d/2
    l       = -cxn.d/2
    
    # char extent
    if el.fire_time > 0:
        m       = a + el.d_char_ef
        n       = b - el.d_char_ef
        o       = c - el.d_char_ef
        p       = d + el.d_char_ef
        
        char_L  = [m,m], [p,o]
        char_R  = [n,n], [p,o]
        char_T  = [m,n], [o,o]
        char_B  = [m,n], [p,p]

        i   = m
        j   = n 
    
    bolt_L  = [i, i], [l, k]
    bolt_R = [j, j], [l, k]
    bolt_T   = [i, j], [k, k]
    bolt_B   = [i, j], [l, l]

    if cxn.type == 'Bolted':
        if cxn.recessed == 'Y' and cxn.concealed == 'Y':

            q = -el.t/2 + cxn.H_p
            r = -el.t/2 + cxn.H_p + cxn.H_r
            s = cxn.D_r/2
            t = -cxn.D_r/2

            recess_L = [q,q],[s,t]
            recess_R = [r,r],[s,t]
            recess_T = [q,r],[s,s]
            recess_B = [q,r],[t,t]

            recess2_R = [-q,-q],[-s,-t]
            recess2_L = [-r,-r],[-s,-t]
            recess2_B = [-q,-r],[-s,-s]
            recess2_T = [-q,-r],[-t,-t]

            u = -el.t/2
            v = -el.t/2 + cxn.H_p
            w = cxn.D_r/2
            x = -cxn.D_r/2

            plug_L = [u,u],[w,x]
            plug_R = [v,v],[w,x]
            plug_T = [u,v],[w,w]
            plug_B = [u,v],[x,x]

            plug2_R = [-u,-u],[-w,-x]
            plug2_L = [-v,-v],[-w,-x]
            plug2_B = [-u,-v],[-w,-w]
            plug2_T = [-u,-v],[-x,-x]            

    # plot limits
    xlim    = el.t/2 + 50
    ylim    = el.h/2 + 100

    sec_plot = plt.subplots(subplot_kw = {'aspect':'equal'})  
    
    sec_plot[1].plot(sec_L[0],  sec_R[1],'k')       # plot left
    sec_plot[1].plot(sec_R[0],  sec_R[1],'k')       # plot right
    sec_plot[1].plot(sec_T[0],  sec_T[1],'k')       # plot top
    sec_plot[1].plot(sec_B[0],  sec_B[1],'k')       # plot top
    
    sec_plot[1].plot(plate_L[0],  plate_L[1],'k')   # plot left
    sec_plot[1].plot(plate_R[0],  plate_R[1],'k')   # plot right
    sec_plot[1].plot(plate_T[0],  plate_T[1],'k')   # plot top
    sec_plot[1].plot(plate_B[0],  plate_B[1],'k')   # plot top
    
    sec_plot[1].plot(bolt_L[0],  bolt_L[1],'k')     # plot left
    sec_plot[1].plot(bolt_R[0],  bolt_R[1],'k')     # plot right
    sec_plot[1].plot(bolt_T[0],  bolt_T[1],'k')     # plot top
    sec_plot[1].plot(bolt_B[0],  bolt_B[1],'k')     # plot top
    
    if el.fire_time > 0:
        sec_plot[1].plot(char_L[0],  char_L[1],'r', linestyle = '--')     # plot left
        sec_plot[1].plot(char_R[0],  char_R[1],'r', linestyle = '--')     # plot right
        sec_plot[1].plot(char_T[0],  char_T[1],'r', linestyle = '--')     # plot top
        sec_plot[1].plot(char_B[0],  char_B[1],'r', linestyle = '--')     # plot top

    # boltPlot[1].plot(end_pl[0],end_pl[1],'k', linestyle = '--')                       # plot plate edges
    # boltPlot[1].plot(top_pl[0],top_pl[1],'k', linestyle = '--')                       
    # boltPlot[1].plot(bot_pl[0],bot_pl[1],'k', linestyle = '--')                      
    
    patch = [a,d], [a,c], [b,c], [b,d]
    sec_plot[1].add_patch(plt.Polygon(patch,facecolor = '#f3eddd'))

    platePatch = [e,h], [f,h], [f,g], [e,g]
    sec_plot[1].add_patch(plt.Polygon(platePatch, fill = False,hatch = '//'))

    if cxn.type == 'Bolted':
        if cxn.recessed == 'Y' and cxn.concealed == 'Y':
            
            sec_plot[1].plot(recess_L[0],  recess_R[1],'k')       # plot recess
            sec_plot[1].plot(recess_R[0],  recess_R[1],'k')       
            sec_plot[1].plot(recess_T[0],  recess_T[1],'k')      
            sec_plot[1].plot(recess_B[0],  recess_B[1],'k')   

            sec_plot[1].plot(recess2_L[0],  recess2_R[1],'k')       # plot recess
            sec_plot[1].plot(recess2_R[0],  recess2_R[1],'k')       
            sec_plot[1].plot(recess2_T[0],  recess2_T[1],'k')      
            sec_plot[1].plot(recess2_B[0],  recess2_B[1],'k') 

            recessPatch = [q,s], [r,s], [r,t], [q,t]
            sec_plot[1].add_patch(plt.Polygon(recessPatch,facecolor = 'w'))

            recessPatch = [-q,-s], [-r,-s], [-r,-t], [-q,-t]
            sec_plot[1].add_patch(plt.Polygon(recessPatch,facecolor = 'w'))

            sec_plot[1].plot(plug_L[0],  plug_R[1],'k')       # plot plug
            sec_plot[1].plot(plug_R[0],  plug_R[1],'k')       
            sec_plot[1].plot(plug_T[0],  plug_T[1],'k')      
            sec_plot[1].plot(plug_B[0],  plug_B[1],'k')   

            sec_plot[1].plot(plug2_L[0],  plug2_R[1],'k')       # plot plug
            sec_plot[1].plot(plug2_R[0],  plug2_R[1],'k')       
            sec_plot[1].plot(plug2_T[0],  plug2_T[1],'k')      
            sec_plot[1].plot(plug2_B[0],  plug2_B[1],'k')              
            
            plugPatch = [u,w], [v,w], [v,x], [u,x]
            sec_plot[1].add_patch(plt.Polygon(plugPatch,facecolor = '#f3eddd', hatch ='xx'))

            plugPatch = [-u,-w], [-v,-w], [-v,-x], [-u,-x]
            sec_plot[1].add_patch(plt.Polygon(plugPatch,facecolor = '#f3eddd', hatch ='xx'))
        
    boltPatch = [i,k], [j,k], [j,l], [i,l]
    sec_plot[1].add_patch(plt.Polygon(boltPatch,facecolor = '#0066CC'))
    
    sec_plot[1].text(0, d-50,'Indicative Section', horizontalalignment = 'center')

    sec_plot[1].axis('off')
    
    sec_plot[1].set_xlim([-xlim, xlim])
    sec_plot[1].set_ylim([-ylim, ylim])
            
    cxn.sec_plot = sec_plot
# --------------------------------------------------------------------------- #