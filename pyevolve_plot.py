import pylab
from matplotlib.font_manager import FontProperties
import matplotlib.cm

def graph_pop_heatmap_raw(pop, identify, minimize=False, colormap="jet", filesave=None):
   pylab.imshow(pop, aspect="auto", interpolation="gaussian", cmap=matplotlib.cm.__dict__[colormap])
   pylab.title("Plot of pop. raw scores along the generations")
   pylab.xlabel('Population')
   pylab.ylabel('Generations')
   pylab.grid(True)
   pylab.colorbar()

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_diff_raw(pop, identify, minimize=False, filesave=None):
   x = []

   diff_raw_y = []
   diff_fit_y = []

   for it in pop:
      x.append(it["generation"])
      diff_raw_y.append(it["rawMax"] - it["rawMin"])
      diff_fit_y.append(it["fitMax"] - it["fitMin"])

   pylab.figure()
   pylab.subplot(211)
   
   pylab.plot(x, diff_raw_y, "g", label="Raw difference", linewidth=1.2)
   pylab.fill_between(x, diff_raw_y, color="g", alpha=0.1)

   diff_raw_max= max(diff_raw_y)
   gen_max_raw = x[diff_raw_y.index(diff_raw_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_raw_max,), xy=(gen_max_raw, diff_raw_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Raw difference")
   pylab.title("Plot of evolution identified by '%s'" % (identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"), loc=0)

   pylab.subplot(212) 

   pylab.plot(x, diff_fit_y, "b", label="Fitness difference", linewidth=1.2)
   pylab.fill_between(x, diff_fit_y, color="b", alpha=0.1)


   diff_fit_max= max(diff_fit_y)
   gen_max_fit = x[diff_fit_y.index(diff_fit_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_fit_max,), xy=(gen_max_fit, diff_fit_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Fitness difference")

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"), loc=0)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_errorbars_raw(pop, identify, minimize=False, filesave=None):
    x = []
    y = []
    yerr_max = []
    yerr_min = []

    for it in pop:
        x.append(it["generation"])
        y.append(it["rawAve"])
        ymax = it["rawMax"] - it["rawAve"]
        ymin = it["rawAve"] - it["rawMin"]

        yerr_max.append(ymax)
        yerr_min.append(ymin)

    pylab.figure()
    pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
    pylab.xlabel('Generation (#)')
    pylab.ylabel('Raw score Min/Avg/Max')
    pylab.title("Plot of evolution identified by '%s' (raw scores)" % (identify))
    pylab.grid(True)

    if filesave:
        pylab.savefig(filesave)
        print "Graph saved to %s file !" % (filesave,)
    else:
        pylab.show()
        
def graph_errorbars_fitness(pop, identify, minimize=False, filesave=None):
   x = []
   y = []
   yerr_max = []
   yerr_min = []

   for it in pop:
      x.append(it["generation"])
      y.append(it["fitAve"])
      ymax = it["fitMax"] - it["fitAve"]
      ymin = it["fitAve"] - it["fitMin"]
      
      yerr_max.append(ymax)
      yerr_min.append(ymin)

   pylab.figure()
   pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
   pylab.xlabel('Generation (#)')
   pylab.ylabel('Fitness score Min/Avg/Max')
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (identify))

   pylab.grid(True)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_maxmin_raw(pop, identify, minimize=False, filesave=None):
   x = []
   max_y = []
   min_y = []
   std_dev_y = []
   avg_y = []

   for it in pop:
      x.append(it["generation"])
      max_y.append(it["rawMax"])
      min_y.append(it["rawMin"])
      std_dev_y.append(it["rawDev"])
      avg_y.append(it["rawAve"])

   pylab.figure()

   pylab.plot(x, max_y, "g", label="Max raw", linewidth=1.2)
   pylab.plot(x, min_y, "r", label="Min raw", linewidth=1.2)
   pylab.plot(x, avg_y, "b", label="Avg raw", linewidth=1.2)
   pylab.plot(x, std_dev_y, "k", label="Std Dev raw", linewidth=1.2)

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if minimize: raw_max = min(min_y)
   else: raw_max= max(max_y)

   if minimize: gen_max = x[min_y.index(raw_max)]
   else: gen_max = x[max_y.index(raw_max)]

   min_std = min(std_dev_y)
   gen_min_std = x[std_dev_y.index(min_std)]

   max_std = max(std_dev_y)
   gen_max_std = x[std_dev_y.index(max_std)]

   if minimize: annot_label = "Minimum (%.2f)" % (raw_max,)
   else: annot_label = "Maximum (%.2f)" % (raw_max,)


   pylab.annotate(annot_label, xy=(gen_max, raw_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Min StdDev (%.2f)" % (min_std,), xy=(gen_min_std, min_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Max StdDev (%.2f)" % (max_std,), xy=(gen_max_std, max_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Raw score")
   pylab.title("Plot of evolution identified by '%s' (raw scores)" % (identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"),loc=0)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


def graph_maxmin_fitness(pop, identify, minimize=False, filesave=None):
   x = []
   max_y = []
   min_y = []
   avg_y = []

   for it in pop:
      x.append(it["generation"])
      max_y.append(it["fitMax"])
      min_y.append(it["fitMin"])
      avg_y.append(it["fitAve"])

   pylab.figure()
   pylab.plot(x, max_y, "g", label="Max fitness")
   pylab.plot(x, min_y, "r", label="Min fitness")
   pylab.plot(x, avg_y, "b", label="Avg fitness")

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if minimize: raw_max = min(min_y)
   else: raw_max = max(max_y)

   if minimize: gen_max = x[min_y.index(raw_max)]
   else: gen_max = x[max_y.index(raw_max)]

   if minimize: annot_label = "Minimum (%.2f)" % (raw_max,)
   else: annot_label = "Maximum (%.2f)" % (raw_max,)

   pylab.annotate(annot_label, xy=(gen_max, raw_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Fitness score")
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (identify))
   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"),loc=0)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def load_population(dbfile, identify):
    pop = None

    import os.path
    if not os.path.exists(dbfile):
        print "Database file '%s' not found !" % (dbfile, )
        return pop

    import sqlite3
    print "Loading database..."

    conn = sqlite3.connect(dbfile)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    ret = c.execute("select * from statistics where identify = ?", (identify,))
    pop = ret.fetchall()
    ret.close()
    conn.close()

    if len(pop) <= 0:
        print "No statistic data found for the identify '%s' !" % (identify,)
        return pop

    print "%d generations found !" % (len(pop),)
    return pop

def load_population_hm(dbfile, identify):
    pop = None

    import os.path
    if not os.path.exists(dbfile):
        print "Database file '%s' not found !" % (dbfile, )
        return pop

    import sqlite3
    print "Loading database..."
    
    conn = sqlite3.connect(dbfile)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    ret = c.execute("select distinct generation from population where identify = ?", (identify,))
    generations = ret.fetchall()
    if len(generations) <= 0:
        print "No generation data found for the identify '%s' !" % (identify,)
        return pop
    
    pop = []
    for gen in generations:
        pop_tmp = []

        ret = c.execute("""
                         select *  from population
                         where identify = ?
                         and generation = ?
                         """, (identify, gen[0]))

        ret_fetch = ret.fetchall()
        for it in ret_fetch:
            pop_tmp.append(it["raw"])
        pop.append(pop_tmp)
    ret.close()
    conn.close()

    if len(pop) <= 0:
        print "No statistic data found for the identify '%s' !" % (identify,)
        return pop

    print "%d generations found !" % (len(pop),)
    return pop
    
def plot_errorbars_raw(dbfile, identify):
    pop = load_population(dbfile, identify)
    if len(pop) > 0:
        graph_errorbars_raw(pop, identify)
        
def plot_errorbars_fitness(dbfile, identify):
    pop = load_population(dbfile, identify)
    if len(pop) > 0:
        graph_errorbars_fitness(pop, identify)
        
def plot_maxmin_raw(dbfile, identify):
    pop = load_population(dbfile, identify)
    if len(pop) > 0:
        graph_maxmin_raw(pop, identify)

def plot_maxmin_fitness(dbfile, identify):
    pop = load_population(dbfile, identify)
    if len(pop) > 0:
        graph_maxmin_fitness(pop, identify)
        
def plot_diff_raw(dbfile, identify):
    pop = load_population(dbfile, identify)
    if len(pop) > 0:
        graph_diff_raw(pop, identify)
        
def plot_pop_heatmap_raw(dbfile, identify):
    pop = load_population_hm(dbfile, identify)
    if len(pop) > 0:
        graph_pop_heatmap_raw(pop, identify)
       