#20190620pmc


#region ################################ DESCRIPTION ################################

"""
This script is used to make the plots and movies for the prediction of the signal diffusion model. 

Run this file and use the command line arguments to specify the chromosome specifications. 

To learn about the arguments, run the script from the command line with the -h argument. 

In bried, the arguments are as follows:
    -d: The main directory to use.
    -f: The file from which the prediction is based upon.
        (This is only used to save the file with the same name as the original file, but with the _copos.pdf extension.)
    -l: The chromosome length.
    -p: The positions of the crossovers.
    -y: The y limit of the plot.

An example of the command line will be as follows:
    python model_prediction.py -d /home/user/ -f original_file_name.tif -l 300 -p 20 280 -y 1000

"""

#endregion ############################# END DESCRIPTION ############################


from matplotlib import pyplot as pl
from matplotlib import cm
import argparse


import sys
import os

pl.rcParams['figure.dpi'] = 150
plotymax=800
def copos_timing(xsl=100,pos=[25,74],starttimes=[0.0,0.0],endtimes=[0.5,0.5]):
    
    #run_coefficient=int(200/len(pos)) # factor to multiply `xsl` to give number of steps
    run_coefficient=100
    #add_coefficient=0.5 # phosphoprotein added for this proportion of total runs
    dp=0.5   # diffusion proportion, how much stays at same location
    ip=1     # how much enters at each CO each step
    runs=run_coefficient*xsl # how many iterations to do
    xs=[0.0]*xsl
    xs_plot=[]
    #set up left and right boundaries:
    lb=[0];
    for i in pos:
        lb.append(i+1)
    rb=[xsl-1]
    for i in pos:
        rb.append(i-1)

    #iterate the simulation    
    for i in range(runs):
        for count,j in enumerate(pos):
            if(i>(runs*starttimes[count]) and i<(runs*endtimes[count])): # only add if within a set proportion of the total run
                xs[j]+=ip
        xs2=[0.0]*xsl #placeholder for the next iteration
        for count,val in enumerate(xs):
            r=val*dp;s=(val-r)/2;
            xs2[count]+=r
            a=100
            if(count in lb): #left boundary treatment
                xs2[count]+=s
                xs2[count+1]+=s
            if(count in rb): #right boundary treatment
                xs2[count]+=s
                xs2[count-1]+=s
            if((not (count in lb)) and (not (count in rb))): #non-boundary treatment, including @CO itself
                xs2[count-1]+=s
                xs2[count+1]+=s
        xs=xs2.copy()
        if(0==(i%xsl)):
          xs_plot.append(xs)
    return xs_plot

def copos(xsl=100,pos=[25,74]):    
    
    #run_coefficient=int(200/len(pos)) # factor to multiply `xsl` to give number of steps
    run_coefficient=100
    add_coefficient=0.5 # phosphoprotein added for this proportion of total runs
    dp=0.4   # diffusion proportion, how much stays at same location
    ip=1     # how much enters at each CO each step
    runs=run_coefficient*xsl # how many iterations to do
    xs=[0.0]*xsl
    xs_plot=[]
    #set up left and right boundaries:
    lb=[0];
    for i in pos:
        lb.append(i+1)
    rb=[xsl-1]
    for i in pos:
        rb.append(i-1)

    #iterate the simulation    
    for i in range(runs):
        for j in pos:
            if(i<(runs*add_coefficient)): # only add if below a set proportion of the total run
                xs[j]+=ip
        xs2=[0.0]*xsl #placeholder for the next iteration
        for count,val in enumerate(xs):
            r=val*dp;s=(val-r)/2;
            xs2[count]+=r
            a=100
            if(count in lb): #left boundary treatment
                xs2[count]+=s
                xs2[count+1]+=s
            if(count in rb): #right boundary treatment
                xs2[count]+=s
                xs2[count-1]+=s
            if((not (count in lb)) and (not (count in rb))): #non-boundary treatment, including @CO itself
                xs2[count-1]+=s
                xs2[count+1]+=s
        xs=xs2.copy()
        if(0==(i%xsl)):
            xs_plot.append(xs)
    return xs_plot

#TODO: implement post-accumulation wave of redistribution in a "rich get richer" manner 
# where signal flows uphill across boundaries 02019-06-28

def copos_plot_all(xsl=100,pos=[24,75],starttimes=[0,0],endtimes=[0.5,0.5]):
    xs_plot=copos(xsl,pos)
    #xs_plot=copos_timing(xsl,pos,starttimes,endtimes)
    numlines=len(xs_plot)
    cm_subsection=[]
    for i in range(numlines):
        cm_subsection.append(i/(numlines-1))
    colors = [ cm.coolwarm(x) for x in cm_subsection ]

    myplot=pl.plot()
    for count,i in enumerate(xs_plot):
        myplot.append(pl.plot(range(len(i)),i,color=colors[count]))
    return(myplot)

def copos_plot_anim(xsl=100,pos=[24,75], saving_directory = os.getcwd(), y_limit_set=None):
    xs_plot=copos(xsl,pos)
    numlines=len(xs_plot)
    cm_subsection=[]
    for i in range(numlines):
        cm_subsection.append(i/(numlines-1))
    colors = [ cm.turbo(x) for x in cm_subsection ]
    
    #start the plot
    myplot = pl.plot()

    #if the y limit is set
    if y_limit_set:

        #set the y limit
        pl.ylim(ymax=2000)

    #iterate through the pos variable
    for position in pos:

        #plot the axvline
        pl.axvline(x=position, color="green", linestyle="--")

    #start a plotted counter
    plotted_counter = 0

    #start a bruto counter
    bruto_counter = 0

    #print the length of the xs_plot
    print(f"The length of the xs_plot is {len(xs_plot)}")

    #iterate through the xs_plot (where the actual time points are) and plot them, saving them as you go
    for count,i in enumerate(xs_plot):

        #print the count
        print(f"The count is {count}")

        #print the bruto counter
        print(f"The bruto counter is {bruto_counter}")

        #if the brute counter is 0
        if bruto_counter == 0:
            
            #print that you're plotting
            print("Plotting...")

            #print a space
            print("")

            pdf_filename=saving_directory + 'img'+str(plotted_counter).zfill(4)+'.pdf'
            myplot.append(pl.plot(range(len(i)),i,color=colors[count]))
            pl.savefig(pdf_filename, dpi=300)
            png_filename=saving_directory + 'img'+str(plotted_counter).zfill(4)+'.png'
            pl.savefig(png_filename, dpi=300)

            #add one to the bruto counter
            bruto_counter += 1

            #add one to the plotted counter
            plotted_counter += 1

            #continue
            continue

        #print you're not plotting
        print("Not plotting...")

        #print a space
        print("")

        #add one to the bruto counter
        bruto_counter += 1


        #if the bruto counter is 5
        if bruto_counter >= 1:

            #reset the bruto counter
            bruto_counter = 0

    #make the movie using ffmpeg
    os.system("ffmpeg -framerate 10 -i " + saving_directory + "img%04d.png -c:v libx264 -pix_fmt yuv420p " + saving_directory + "out.mp4")

    return(pl.plot)


def copos_plot_all_gaps(xsl=100,pos=[24,75]):
    xs_plot=copos(xsl,pos)
    numlines=len(xs_plot)
    cm_subsection=[]
    for i in range(numlines):
        cm_subsection.append(i/(numlines-1))
    colors = [ cm.coolwarm(x) for x in cm_subsection ]

    myplot=pl.plot()
    pos.append(xsl+1)
    for count,i in enumerate(xs_plot):
        xaxis=[];yaxis=[]
        j=0
        for i in pos:
            xaxis.append([x for x in range(j,i-1)])
            yaxis.append([xs_plot[x] for x in range(j,i-1)])
            j=i
        for i in range(len(xaxis)):
            print(i)
            myplot.append(pl.plot(xaxis[i],yaxis[i],color=colors[count]))
    return(myplot)

def copos_plot_anim_gaps(xsl=100,pos=[24,75], saving_directory = os.getcwd()):
    xs_plot=copos(xsl,pos)
    numlines=len(xs_plot)
    for count,i in enumerate(xs_plot):
        xaxis=list(range(xsl))
        gapoffset=0
        for gap in pos:
            xaxis.pop(gap-gapoffset)
            i.pop(gap-gapoffset)
            gapoffset+=1
        pl.cla()
        pl.plot(figsize=(8,4))
        fn=saving_directory + 'img'+str(count).zfill(4)+'.pdf'
        pl.plot(xaxis,i)
        pl.ylim(ymax=plotymax,ymin=0)
        pl.savefig(fn)
    return(pl.plot)

def copos_plot_anim_gaps_timing(xsl=100,pos=[24,75],starttimes=[0.0,0.0],endtimes=[0.5,0.5]):
    xs_plot=copos_timing(xsl,pos,starttimes,endtimes)
    numlines=len(xs_plot)
    for count,i in enumerate(xs_plot):
        xaxis=list(range(xsl))
        gapoffset=0
        for gap in pos:
            xaxis.pop(gap-gapoffset)
            i.pop(gap-gapoffset)
            gapoffset+=1
        pl.cla()
        pl.ylim(ymax=plotymax)
        fn='img'+str(count).zfill(4)+'.png'
        pl.plot(xaxis,i)
        pl.savefig(fn)
    return(pl.plot)

#set up the main directory
main_dir = None

#set up the xsl 
xsl = None

#set up the positions
pos = None

#set up the file name
original_filename = None

#set up the y limitm
y_limit = None

#add the argument parser options]
parser = argparse.ArgumentParser(description='Plot the average differences from the combined dataframes.')

#add the argument for the main directory
parser.add_argument('-d', type=str, help='The main directory to use.')

#add the argument for the file name
parser.add_argument('-f', type=str, help='The file from which the prediction is based upon.')

#add the argument for the xsl
parser.add_argument('-l', type=int, help='The chromosome length.')

#add the argument for the positions
parser.add_argument('-p', type=int, nargs='+', help='The positions of the crossovers.')

#add the argument for the y limit
parser.add_argument('-y', type=int, help='The y limit of the plot.')

#parse the arguments
arguments = parser.parse_args()

#if the main directory is not none
if arguments.d is not None:
    #set the main directory
    main_dir = arguments.d

    #if the main directory does not end with a /
    if not main_dir.endswith("/"):
        #add the /
        main_dir += "/"

    #if the main directory does not exist
    if not os.path.isdir(main_dir):
        #print the error
        print("The main directory does not exist.")

        #exit
        sys.exit()

    #if the main directory is ./
    if main_dir == "./":

        #get the current directory
        main_dir = os.getcwd()

        #if the main directory does not end with a /
        if not main_dir.endswith("/"):
            #add the /
            main_dir += "/"

#if the main directory is none
if arguments.d is None:
    #set the main directory to the current directory
    main_dir = os.getcwd()

    #if the main directory does not end with a /
    if not main_dir.endswith("/"):
        #add the /
        main_dir += "/" 

#if the file name is not none
if arguments.f is not None:
    #set the file name
    original_filename = arguments.f

#if the file name is none
if arguments.f is None:

    #print the error
    print("The original file name is missing.")

    #exit
    sys.exit()

#if the xsl is not none
if arguments.l is not None:

    #set the xsl
    xsl = arguments.l

#if the xsl is none
if arguments.l is None:

    #print the error
    print("The chromosome length is missing.")

    #exit
    sys.exit()

#if the positions are not none
if arguments.p is not None:

    #set the positions
    pos = arguments.p

#if the positions are none
if arguments.p is None:
    
    #print the error
    print("The positions are missing.")

    #exit
    sys.exit()

#if the y limit is not none
if arguments.y is not None:

    #set the y limit
    y_limit = arguments.y

#print a blank line
print("")

#print that you're running the prediction
print("Running the prediction...")

#print the main directory
print(f"The main directory is {main_dir}")

#print the file name
print(f"The original file name is {original_filename}")

#print the xsl
print(f"The chromosome length is {xsl}")

#print the positions
print(f"The positions are {pos}")

#pos=[int(x) for x in sys.argv[2:4]]
#starttimes=[float(x) for x in sys.argv[4:6]]
#endtimes=[float(x) for x in sys.argv[6:8]]
#copos_plot_anim_gaps(xsl=xsl,pos=pos)


#run coppos plot all to plot the entire thing
#copos_plot_all(xsl=xsl,pos=pos)

#run copos plot anim to plot the animation
copos_plot_anim(xsl=xsl,pos=pos, saving_directory = main_dir, y_limit_set=y_limit)
original_filename = original_filename.split(".")[0]
pl.savefig(original_filename+"_copos.pdf",dpi=150)

#print that the file was saved
print(f"The file was saved as {original_filename}_copos.pdf")
